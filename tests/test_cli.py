import pytest
from typer.testing import CliRunner

from djhx_blogger import cli
from djhx_blogger.config import BloggerError, BuildOptions, SiteConfig, read_config

runner = CliRunner()


@pytest.fixture(autouse=True)
def no_user_config(monkeypatch):
    monkeypatch.setattr(cli, "read_config", lambda _: {})


def test_version_help_and_config_path_are_side_effect_free(tmp_path, monkeypatch):
    missing = tmp_path / "missing/config.toml"
    monkeypatch.setattr(cli, "CONFIG_FILE_PATH", missing)
    assert runner.invoke(cli.app, ["--help"]).exit_code == 0
    assert "0.3.1" in runner.invoke(cli.app, ["--version"]).output
    assert str(missing) in runner.invoke(cli.app, ["-c"]).output
    assert not missing.parent.exists()


def test_missing_origin_and_missing_deploy_config_fail_before_build(tmp_path, monkeypatch):
    assert runner.invoke(cli.app, []).exit_code == 1
    called = []
    monkeypatch.setattr(cli, "generate_blog", lambda *a, **k: called.append(True))
    result = runner.invoke(cli.app, ["-o", str(tmp_path), "-d"])
    assert result.exit_code == 1
    assert "server" in result.output
    assert not called


def test_legacy_cli_build_and_new_post(blog, tmp_path):
    assert runner.invoke(cli.app, ["-o", str(blog), "-p", "post"]).exit_code == 0
    result = runner.invoke(cli.app, ["-o", str(blog), "-t", str(tmp_path / "out"), "--archive"])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "out/public.tar.gz").is_file()


def test_deployment_failure_never_refreshes(blog, post, tmp_path, monkeypatch):
    post(blog)
    refreshed = []
    monkeypatch.setattr(
        cli, "deploy_blog", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("upload failed"))
    )
    monkeypatch.setattr(cli, "refresh_site_search_db", lambda *a, **k: refreshed.append(True))
    result = runner.invoke(
        cli.app,
        [
            "-o",
            str(blog),
            "-t",
            str(tmp_path / "out"),
            "-d",
            "-s",
            "example",
            "-T",
            "/var/www/example",
        ],
    )
    assert result.exit_code == 1
    assert not refreshed


def test_refresh_failure_has_distinct_exit_code(blog, post, tmp_path, monkeypatch):
    post(blog)
    monkeypatch.setattr(cli, "deploy_blog", lambda *a, **k: None)
    monkeypatch.setattr(
        cli,
        "refresh_site_search_db",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("search unavailable")),
    )
    result = runner.invoke(
        cli.app,
        [
            "-o",
            str(blog),
            "-t",
            str(tmp_path / "out"),
            "-d",
            "-s",
            "example",
            "-T",
            "/var/www/example",
        ],
    )
    assert result.exit_code == 3
    assert "博客部署成功" in result.output


def test_cli_overrides_config_paths_and_workers(blog, post, tmp_path, monkeypatch):
    post(blog)
    monkeypatch.setattr(
        cli,
        "read_config",
        lambda _: {"local": {"origin": "wrong", "target": "wrong"}, "build": {"workers": 1}},
    )
    result = runner.invoke(
        cli.app, ["-o", str(blog), "-t", str(tmp_path / "out"), "--workers", "2", "--no-cache"]
    )
    assert result.exit_code == 0, result.output
    assert (tmp_path / "out/public/index.html").exists()


def test_bad_config_is_reported_and_not_ignored(tmp_path):
    missing = tmp_path / "config.toml"
    assert read_config(missing) == {}
    missing.write_text("[local]\norigin = 123", "utf-8")
    with pytest.raises(BloggerError, match="类型错误"):
        read_config(missing)
    missing.write_text("[local", "utf-8")
    with pytest.raises(BloggerError, match="读取配置失败"):
        read_config(missing)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"search_url": "javascript:alert(1)"},
        {"about_url": "//evil.test"},
        {"base_path": "/../"},
        {"title": 123},
    ],
)
def test_unsafe_site_config(kwargs):
    with pytest.raises(BloggerError):
        SiteConfig(**kwargs)


@pytest.mark.parametrize(
    "kwargs", [{"workers": 0}, {"workers": True}, {"cache": "false"}, {"image_quality": 100}]
)
def test_invalid_build_config(kwargs):
    with pytest.raises(BloggerError):
        BuildOptions(**kwargs)
