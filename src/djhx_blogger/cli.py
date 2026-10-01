"""The legacy single-command blg interface, with explicit failure statuses."""

from __future__ import annotations

from dataclasses import replace
from getpass import getpass
from importlib.metadata import version
from pathlib import Path

import typer

from .config import CONFIG_FILE_PATH, BloggerError, BuildOptions, SiteConfig, read_config
from .deploy import compress_dir, deploy_blog, refresh_site_search_db, validate_remote_root
from .gen import generate_blog, init_new_blog, init_new_post
from .log_config import app_logger as logger
from .log_config import log_init

app = typer.Typer(
    add_completion=False,
    pretty_exceptions_enable=False,
    help="把 Markdown 博客构建为静态站点，并安全部署到 SSH 服务器。",
)


@app.command()
def run(
    origin: Path | None = typer.Option(None, "--origin", "-o", help="Markdown 博客根目录。"),
    target: Path | None = typer.Option(
        None, "--target", "-t", help="输出父目录，站点生成到 public/。"
    ),
    server: str | None = typer.Option(None, "--server", "-s", help="SSH 主机或配置别名。"),
    server_target: str | None = typer.Option(
        None, "--server-target", "-T", help="远程父目录，站点入口为 blog/。"
    ),
    deploy: bool = typer.Option(False, "--deploy", "-d", help="构建、打包、上传并切换远程站点。"),
    archive: bool = typer.Option(False, "--archive", help="构建后生成 public.tar.gz。"),
    new_blog: Path | None = typer.Option(
        None, "--new-blog", "-n", help="在指定目录创建 simple-blog 示例。"
    ),
    new_post: str | None = typer.Option(
        None, "--new-post", "-p", help="创建文章，可包含分类路径。"
    ),
    show_config_path: bool = typer.Option(
        False, "--config-path", "-c", help="输出默认配置文件路径。"
    ),
    config_path: Path | None = typer.Option(None, "--config", help="读取指定 TOML 配置。"),
    workers: int | None = typer.Option(
        None, "--workers", min=1, max=32, help="并行工作数，默认 4。"
    ),
    no_cache: bool = typer.Option(False, "--no-cache", help="重新处理全部文件。"),
    no_compress: bool = typer.Option(False, "--no-compress", help="原样复制图片。"),
    no_refresh: bool = typer.Option(False, "--no-refresh", help="部署后跳过搜索索引刷新。"),
    ssh_user: str | None = typer.Option(
        None, "--ssh-user", help="SSH 用户，默认 koril（兼容旧版）。"
    ),
    port: int | None = typer.Option(None, "--port", min=1, max=65535, help="SSH 端口。"),
    identity_file: Path | None = typer.Option(None, "--identity-file", help="SSH 私钥路径。"),
    no_sudo: bool = typer.Option(False, "--no-sudo", help="远程部署使用 SSH 用户权限。"),
    password: bool = typer.Option(
        False, "--password", help="交互输入 SSH 密码，默认使用密钥/agent。"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="显示错误堆栈。"),
    show_version: bool = typer.Option(False, "--version", help="输出版本号。"),
):
    log_init(verbose)
    if show_version:
        typer.echo(f"djhx-blogger {version('djhx-blogger')}")
        return
    if show_config_path:
        typer.echo(config_path or CONFIG_FILE_PATH)
        return
    try:
        if sum((bool(new_blog), bool(new_post))) > 1 or (
            (new_blog or new_post) and (deploy or archive)
        ):
            raise BloggerError("新建博客/文章与构建部署选项不能同时使用")
        if config_path is not None and not config_path.is_file():
            raise BloggerError(f"配置文件不存在: {config_path}")
        config = read_config(config_path)
        if new_blog:
            typer.echo(f"示例博客: {init_new_blog(str(new_blog))}")
            return
        local, remote, search = (
            config.get(section, {}) for section in ("local", "deploy", "search")
        )
        origin = origin or (Path(local["origin"]) if local.get("origin") else None)
        target = target or Path(local.get("target", Path.cwd()))
        if origin is None:
            raise BloggerError("需要 --origin/-o 或配置 local.origin")
        if new_post:
            typer.echo(f"新文章: {init_new_post(str(origin), new_post)}")
            return
        site = SiteConfig(**config.get("site", {}))
        options = BuildOptions(**config.get("build", {}))
        options = replace(
            options,
            workers=workers if workers is not None else options.workers,
            cache=options.cache and not no_cache,
            compress_images=options.compress_images and not no_compress,
        )
        server = server or remote.get("server")
        server_target = server_target or remote.get("target")
        if deploy:
            if not server or not server_target:
                raise BloggerError(
                    "部署需要 server 和 server-target（或 deploy.server/target 配置）"
                )
            validate_remote_root(server_target)
        root = generate_blog(str(origin), str(target), site=site, options=options)
        typer.echo(f"站点: {root.destination_path}")
        if deploy or archive:
            tar_path = compress_dir(
                root.destination_path, compression_level=remote.get("compression_level", 1)
            )
            typer.echo(f"压缩包: {tar_path}")
        if deploy:
            deploy_blog(
                server,
                tar_path,
                server_target,
                user=ssh_user or remote.get("user", "koril"),
                port=port or remote.get("port", 22),
                identity_file=identity_file or remote.get("identity_file"),
                known_hosts=remote.get("known_hosts"),
                sudo=remote.get("sudo", True) and not no_sudo,
                timeout=remote.get("timeout", 120),
                ssh_password=getpass("[SSH password]: ") if password else None,
            )
            if search.get("enabled", True) and not no_refresh:
                try:
                    refresh_site_search_db(
                        search.get("refresh_url", "https://search.djhx.site/refresh-db"),
                        timeout=search.get("timeout", 30),
                    )
                except Exception as exc:
                    typer.echo(f"博客部署成功，但搜索索引刷新失败: {exc}", err=True)
                    raise typer.Exit(3) from exc
    except typer.Exit:
        raise
    except Exception as exc:
        if verbose:
            logger.exception("操作失败")
        else:
            typer.echo(f"错误: {exc}", err=True)
        raise typer.Exit(1) from exc
