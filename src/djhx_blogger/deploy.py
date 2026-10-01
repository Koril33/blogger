"""Reproducible archives, verified SSH uploads and atomic release switching."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import shlex
import tarfile
import tempfile
from getpass import getpass
from importlib import resources
from pathlib import Path, PurePosixPath
from urllib import request

from fabric import Config, Connection
from paramiko import RejectPolicy

from .config import BloggerError, web_url
from .gen import _linked
from .log_config import app_logger as logger


def compress_dir(blog_path: Path, *, compression_level=1) -> Path:
    blog_path = Path(blog_path)
    if _linked(blog_path) or not blog_path.is_dir() or not (blog_path / "index.html").is_file():
        raise BloggerError("只能打包完整的博客输出目录")
    if type(compression_level) is not int or not 0 <= compression_level <= 9:
        raise BloggerError("gzip 压缩等级必须是 0–9")
    output = blog_path.parent / "public.tar.gz"
    if _linked(output):
        raise BloggerError("压缩包输出不能是符号链接")
    descriptor, temporary = tempfile.mkstemp(prefix=".blogger-archive-", dir=output.parent)
    os.close(descriptor)
    try:
        with (
            open(temporary, "wb") as stream,
            gzip.GzipFile(
                fileobj=stream, filename="", mode="wb", mtime=0, compresslevel=compression_level
            ) as compressed,
            tarfile.open(fileobj=compressed, mode="w|") as archive,
        ):
            for path in [blog_path, *sorted(blog_path.rglob("*"))]:
                if _linked(path) or not (path.is_file() or path.is_dir()):
                    raise BloggerError(f"压缩目录包含不安全的文件: {path}")
                relative = path.relative_to(blog_path)
                if any(part.startswith(".") for part in relative.parts):
                    continue
                info = archive.gettarinfo(
                    str(path),
                    arcname=(
                        PurePosixPath("public") / PurePosixPath(relative.as_posix())
                    ).as_posix(),
                )
                info.uid = info.gid = info.mtime = 0
                info.uname = info.gname = ""
                info.mode = 0o755 if path.is_dir() else 0o644
                if path.is_file():
                    with path.open("rb") as file:
                        archive.addfile(info, file)
                else:
                    archive.addfile(info)
        Path(temporary).replace(output)
    finally:
        Path(temporary).unlink(missing_ok=True)
    logger.info("压缩完成: %s", output)
    return output


def validate_remote_root(value: str) -> str:
    if not value or any(c in value for c in "\r\n\x00\\"):
        raise BloggerError("远程路径不能为空或包含控制字符")
    path = PurePosixPath(value)
    if not path.is_absolute() or ".." in path.parts or len(path.parts) < 3:
        raise BloggerError("远程路径必须是至少两级的绝对目录，例如 /var/www/example.com")
    return str(path)


def _validate_archive(path: Path):
    total, names = 0, set()
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            parts = PurePosixPath(member.name).parts
            if (
                not parts
                or parts[0] != "public"
                or ".." in parts
                or not (member.isfile() or member.isdir())
            ):
                raise BloggerError(f"压缩包包含非法成员: {member.name}")
            if member.name in names:
                raise BloggerError(f"压缩包包含重复成员: {member.name}")
            names.add(member.name)
            total += member.size
            if total > 20 * 1024**3:
                raise BloggerError("压缩包展开后超过 20 GiB")
    if not {"public/index.html", "public/archive.html"} <= names:
        raise BloggerError("压缩包缺少首页或归档页")


def deploy_blog(
    server_name: str,
    local_tar_path: Path,
    remote_web_root: str,
    *,
    user="koril",
    port=22,
    identity_file=None,
    known_hosts=None,
    sudo=True,
    timeout=120,
    ssh_password=None,
    sudo_password=None,
):
    remote_web_root = validate_remote_root(remote_web_root)
    if not server_name or any(c in server_name for c in "\r\n\x00"):
        raise BloggerError("必须指定合法的 SSH 服务器")
    if type(port) is not int or not 1 <= port <= 65535 or timeout <= 0:
        raise BloggerError("SSH 端口或超时无效")
    archive = Path(local_tar_path)
    _validate_archive(archive)
    digest = _sha256(archive)
    ssh_password = ssh_password or os.getenv("DJHX_BLOGGER_SSH_PASSWORD")
    sudo_password = sudo_password or os.getenv("DJHX_BLOGGER_SUDO_PASSWORD")
    if sudo and not sudo_password:
        sudo_password = getpass("[sudo password]: ")
    connect_kwargs = {"banner_timeout": timeout, "auth_timeout": timeout}
    if ssh_password:
        connect_kwargs["password"] = ssh_password
    if identity_file:
        connect_kwargs["key_filename"] = str(identity_file)
    config = Config(overrides={"sudo": {"password": sudo_password}})
    with Connection(
        host=server_name,
        user=user,
        port=port,
        config=config,
        connect_timeout=timeout,
        connect_kwargs=connect_kwargs,
    ) as connection:
        connection.client.load_system_host_keys()
        hosts = (
            Path(known_hosts).expanduser() if known_hosts else Path.home() / ".ssh" / "known_hosts"
        )
        if known_hosts and not hosts.is_file():
            raise BloggerError(f"known_hosts 文件不存在: {hosts}")
        if hosts.is_file():
            connection.client.load_host_keys(str(hosts))
        connection.client.set_missing_host_key_policy(RejectPolicy())
        temporary = connection.run(
            "mktemp -d /tmp/djhx-blogger.XXXXXXXXXX", hide=True, timeout=timeout
        ).stdout.strip()
        # The server chooses this path; constrain it before using it in cleanup.
        if not temporary.startswith("/tmp/djhx-blogger.") or "/" in temporary[len("/tmp/") :]:
            raise BloggerError("远程临时目录返回值无效")
        try:
            remote_archive = temporary + "/public.tar.gz"
            remote_script = temporary + "/deploy.py"
            connection.put(str(archive), remote=remote_archive)
            script = resources.files("djhx_blogger").joinpath("remote_deploy.py").read_bytes()
            import io

            connection.put(io.BytesIO(script), remote=remote_script)
            command = " ".join(
                shlex.quote(part)
                for part in ("python3", remote_script, remote_archive, remote_web_root, digest)
            )
            runner = connection.sudo if sudo else connection.run
            runner(command, hide=True, timeout=timeout)
            logger.info("部署完成: %s:%s/blog", server_name, remote_web_root)
        finally:
            connection.run(
                "rm -rf -- " + shlex.quote(temporary), hide=True, warn=True, timeout=timeout
            )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def refresh_site_search_db(url="https://search.djhx.site/refresh-db", *, timeout=30):
    web_url(url)
    if timeout <= 0:
        raise BloggerError("搜索接口超时必须为正数")
    with request.urlopen(url, timeout=timeout) as response:
        raw = response.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise BloggerError("搜索接口响应超过 1 MiB")
    result = json.loads(raw.decode("utf-8"))
    if not isinstance(result, dict) or result.get("success") is not True:
        raise BloggerError("博客已部署，但搜索接口报告索引刷新失败")
    logger.info("搜索索引刷新完成")
    return result
