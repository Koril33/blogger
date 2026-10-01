import io
import json
import shlex
import sys
import tarfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from paramiko import RejectPolicy

from djhx_blogger import deploy as module
from djhx_blogger.config import BloggerError
from djhx_blogger.gen import MANIFEST, generate_blog
from djhx_blogger.remote_deploy import deploy as remote_deploy


def make_archive(path, entries):
    with tarfile.open(path, "w:gz") as archive:
        for name, value in entries:
            info = tarfile.TarInfo(name)
            if value is None:
                info.type = tarfile.SYMTYPE
                info.linkname = "/etc/passwd"
                archive.addfile(info)
            else:
                info.size = len(value)
                archive.addfile(info, io.BytesIO(value))
    return path


def test_reproducible_archive_permissions_and_private_manifest(blog, post, tmp_path):
    post(blog)
    root = generate_blog(str(blog), str(tmp_path / "out"))
    path = module.compress_dir(root.destination_path)
    before = path.read_bytes()
    assert module.compress_dir(root.destination_path).read_bytes() == before
    with tarfile.open(path) as archive:
        members = archive.getmembers()
        assert "public/index.html" in [m.name for m in members]
        assert not any(MANIFEST in m.name for m in members)
        assert all(m.mtime == 0 and m.uid == 0 for m in members)
        assert all(m.mode == (0o755 if m.isdir() else 0o644) for m in members)


@pytest.mark.parametrize(
    "name,value",
    [("public/../../escape", b"bad"), ("/public/index.html", b"bad"), ("public/link", None)],
)
def test_unsafe_archives_fail_before_connect(tmp_path, name, value):
    path = make_archive(tmp_path / "unsafe.tar.gz", [(name, value)])
    with pytest.raises(BloggerError, match="非法成员"):
        module._validate_archive(path)


@pytest.mark.parametrize(
    "value", ["/", "/var", "relative/path", "/var/../etc", "/var/www\nrm -rf /"]
)
def test_unsafe_remote_roots(value):
    with pytest.raises(BloggerError):
        module.validate_remote_root(value)


def test_shell_arguments_host_keys_and_upload_cleanup(blog, post, tmp_path, monkeypatch):
    post(blog)
    archive = module.compress_dir(generate_blog(str(blog), str(tmp_path / "out")).destination_path)
    hosts = tmp_path / "known_hosts"
    hosts.write_text("", "utf-8")
    calls, policies = [], []

    class FakeConnection:
        client = SimpleNamespace(
            load_system_host_keys=lambda: None,
            load_host_keys=lambda _: None,
            set_missing_host_key_policy=lambda p: policies.append(p),
        )

        def __init__(self, **kwargs):
            calls.append(("connect", kwargs))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            calls.append(("closed", None))

        def run(self, command, **kwargs):
            calls.append((command, kwargs))
            return SimpleNamespace(stdout="/tmp/djhx-blogger.test123\n")

        def put(self, source, **kwargs):
            calls.append(("upload", kwargs))

    monkeypatch.setattr(module, "Connection", FakeConnection)
    root = "/var/www/site '; echo injection"
    module.deploy_blog("example", archive, root, sudo=False, known_hosts=hosts)
    command = next(c for c, _ in calls if c.startswith("python3 "))
    assert shlex.split(command)[3] == root
    assert isinstance(policies[0], RejectPolicy)
    assert any(c.startswith("rm -rf -- /tmp/djhx-blogger.") for c, _ in calls)
    assert calls[-1][0] == "closed"


def test_refresh_timeout_and_failed_json(monkeypatch):
    calls = []

    def response(url, **kwargs):
        calls.append((url, kwargs))
        return io.BytesIO(json.dumps({"success": True}).encode())

    monkeypatch.setattr(module.request, "urlopen", response)
    assert module.refresh_site_search_db(timeout=17)["success"]
    assert calls[0][1]["timeout"] == 17
    monkeypatch.setattr(module.request, "urlopen", lambda *a, **k: io.BytesIO(b'{"success":false}'))
    with pytest.raises(BloggerError, match="刷新失败"):
        module.refresh_site_search_db()


def test_remote_hash_and_extraction_failure_preserve_old_site(tmp_path):
    root = tmp_path / "www/example"
    live = root / "blog"
    live.mkdir(parents=True)
    (live / "index.html").write_text("old", "utf-8")
    (live / "archive.html").write_text("archive", "utf-8")
    archive = make_archive(
        tmp_path / "archive.tar.gz",
        [("public/index.html", b"new"), ("public/../../escape", b"bad")],
    )
    with pytest.raises(ValueError, match="SHA-256"):
        remote_deploy(str(archive), str(root), "wrong")
    with pytest.raises(ValueError, match="Unsafe archive"):
        remote_deploy(str(archive), str(root), module._sha256(archive))
    assert (live / "index.html").read_text("utf-8") == "old"
    assert not list((root / ".blogger/releases").iterdir())
    assert not (root / ".blogger/deploy.lock").exists()


@pytest.fixture
def symlink_support(tmp_path):
    link = tmp_path / "probe"
    try:
        link.symlink_to(tmp_path, target_is_directory=True)
        link.unlink()
    except OSError:
        pytest.skip("OS does not grant symlink creation; Linux CI exercises real release switching")


def test_remote_first_deploy_redeploy_migration_and_retention(tmp_path, symlink_support):
    root = tmp_path / "www/example"
    old = root / "blog"
    old.mkdir(parents=True)
    (old / "index.html").write_text("legacy", "utf-8")
    (old / "archive.html").write_text("archive", "utf-8")
    for i in range(3):
        archive = make_archive(
            tmp_path / "archive.tar.gz",
            [("public/index.html", str(i).encode()), ("public/archive.html", b"archive")],
        )
        remote_deploy(str(archive), str(root), module._sha256(archive))
        assert (root / "blog").is_symlink()
        assert (root / "blog/index.html").read_text("utf-8") == str(i)
    assert (root / "blog.bak/index.html").read_text("utf-8") == "1"
    assert len([p for p in (root / ".blogger/releases").iterdir() if len(p.name) == 32]) == 2


def test_remote_switch_failure_rolls_back_legacy(tmp_path, symlink_support, monkeypatch):
    root = tmp_path / "www/example"
    old = root / "blog"
    old.mkdir(parents=True)
    (old / "index.html").write_text("legacy", "utf-8")
    (old / "archive.html").write_text("archive", "utf-8")
    archive = make_archive(
        tmp_path / "archive.tar.gz",
        [("public/index.html", b"new"), ("public/archive.html", b"archive")],
    )
    original = module.os.replace

    def replace(source, target):
        if Path(source).name.startswith(".blogger-link-"):
            raise OSError("switch failure")
        return original(source, target)

    monkeypatch.setattr(module.os, "replace", replace)
    with pytest.raises(OSError, match="switch failure"):
        remote_deploy(str(archive), str(root), module._sha256(archive))
    assert (old / "index.html").read_text("utf-8") == "legacy"


@pytest.fixture
def linux_fs(fs, monkeypatch):
    from pyfakefs.fake_filesystem import OSType

    fs.os = OSType.LINUX
    # Windows' stdlib caches a reparse-point predicate at import time. Match the
    # simulated POSIX OS while leaving the deployment helper itself unchanged.
    if sys.platform == "win32":
        from pyfakefs.helpers import FakeStatResult

        monkeypatch.setattr(FakeStatResult, "st_file_attributes", property(lambda result: 0))
    return fs


def test_remote_release_switches_on_simulated_linux(linux_fs):
    fs = linux_fs
    fs.create_dir("/srv/site/example/blog")
    root = Path("/srv/site/example")
    (root / "blog/index.html").write_text("legacy", "utf-8")
    (root / "blog/archive.html").write_text("archive", "utf-8")
    for i in range(3):
        archive = make_archive(
            root / "upload.tar.gz",
            [("public/index.html", str(i).encode()), ("public/archive.html", b"archive")],
        )
        remote_deploy(str(archive), str(root), module._sha256(archive))
        assert (root / "blog").is_symlink()
        assert (root / "blog/index.html").read_text("utf-8") == str(i)
    assert (root / "blog.bak/index.html").read_text("utf-8") == "1"
    assert len([p for p in (root / ".blogger/releases").iterdir() if len(p.name) == 32]) == 2


def test_remote_failed_switch_restores_live_and_backup_on_simulated_linux(linux_fs, monkeypatch):
    fs = linux_fs
    fs.create_dir("/srv/site/example/blog")
    fs.create_dir("/srv/site/example/blog.bak")
    root = Path("/srv/site/example")
    for folder, text in (("blog", "legacy"), ("blog.bak", "older backup")):
        (root / folder / "index.html").write_text(text, "utf-8")
        (root / folder / "archive.html").write_text("archive", "utf-8")
    archive = make_archive(
        root / "upload.tar.gz", [("public/index.html", b"new"), ("public/archive.html", b"archive")]
    )
    original = module.os.replace

    def replace(source, target):
        if Path(source).name.startswith(".blogger-link-"):
            raise OSError("switch failed")
        return original(source, target)

    monkeypatch.setattr(module.os, "replace", replace)
    with pytest.raises(OSError, match="switch failed"):
        remote_deploy(str(archive), str(root), module._sha256(archive))
    assert (root / "blog/index.html").read_text("utf-8") == "legacy"
    assert (root / "blog.bak/index.html").read_text("utf-8") == "older backup"
    assert not (root / ".blogger/deploy.lock").exists()
