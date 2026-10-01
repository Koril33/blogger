"""Validated, side-effect-free configuration shared by CLI and builder."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from platformdirs import user_config_path

CONFIG_FILE_PATH = user_config_path("djhx-blogger", "djhx") / "config.toml"


class BloggerError(ValueError):
    """An actionable input/build error that the CLI reports without a traceback."""


def web_url(value: str, *, relative: bool = False) -> str:
    if not isinstance(value, str) or any(c in value for c in "\r\n\x00\\"):
        raise BloggerError("URL 必须是合法的字符串")
    parsed = urlsplit(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc and not parsed.username:
        return value
    if relative and not parsed.scheme and not parsed.netloc and value:
        return value
    raise BloggerError(f"不支持的 URL: {value!r}")


@dataclass(frozen=True)
class SiteConfig:
    title: str = "DJHX BLOG"
    description: str = "记录技术、实践与生活。"
    search_url: str = "https://search.djhx.site/"
    about_url: str = "/about/index.html"
    footer: str = "浙ICP备19051268号"
    footer_url: str = "https://beian.miit.gov.cn/"
    base_path: str = "/"

    def __post_init__(self):
        for field in self.__dataclass_fields__:
            if not isinstance(getattr(self, field), str):
                raise BloggerError(f"site.{field} 必须是字符串")
        for value in (self.search_url, self.footer_url):
            if value:
                web_url(value)
        if self.about_url:
            web_url(self.about_url, relative=True)
        if not self.base_path.startswith("/") or self.base_path.startswith("//"):
            raise BloggerError("site.base_path 必须是以 / 开头的站点路径")
        if any(c in self.base_path for c in "?#\\\r\n\x00") or ".." in self.base_path.split("/"):
            raise BloggerError("site.base_path 包含非法路径")


@dataclass(frozen=True)
class BuildOptions:
    workers: int = 4
    cache: bool = True
    compress_images: bool = True
    image_quality: int = 85
    max_width: int = 1920
    max_height: int = 1920

    def __post_init__(self):
        for field, low, high in (
            ("workers", 1, 32),
            ("image_quality", 1, 95),
            ("max_width", 1, 32768),
            ("max_height", 1, 32768),
        ):
            value = getattr(self, field)
            if type(value) is not int or not low <= value <= high:
                raise BloggerError(f"build.{field} 必须是 {low}–{high} 的整数")
        for field in ("cache", "compress_images"):
            if type(getattr(self, field)) is not bool:
                raise BloggerError(f"build.{field} 必须是布尔值")


_SECTIONS = {
    "local": {"origin": str, "target": str},
    "site": {name: str for name in SiteConfig.__dataclass_fields__},
    "build": {
        "workers": int,
        "cache": bool,
        "compress_images": bool,
        "image_quality": int,
        "max_width": int,
        "max_height": int,
    },
    "deploy": {
        "server": str,
        "target": str,
        "user": str,
        "port": int,
        "identity_file": str,
        "known_hosts": str,
        "sudo": bool,
        "timeout": int,
        "compression_level": int,
    },
    "search": {"refresh_url": str, "timeout": int, "enabled": bool},
}


def read_config(path: Path | None = None) -> dict:
    path = path or CONFIG_FILE_PATH
    if not path.exists():
        return {}
    try:
        with path.open("rb") as stream:
            data = tomllib.load(stream)
    except (OSError, ValueError) as exc:
        raise BloggerError(f"读取配置失败 {path}: {exc}") from exc
    for section, values in data.items():
        if section not in _SECTIONS or not isinstance(values, dict):
            raise BloggerError(f"未知配置节或格式错误: {section}")
        for key, value in values.items():
            expected = _SECTIONS[section].get(key)
            if expected is None or type(value) is not expected:
                raise BloggerError(f"未知配置项或类型错误: {section}.{key}")
    SiteConfig(**data.get("site", {}))
    BuildOptions(**data.get("build", {}))
    for section, key, low, high in (
        ("deploy", "port", 1, 65535),
        ("deploy", "timeout", 1, 3600),
        ("deploy", "compression_level", 0, 9),
        ("search", "timeout", 1, 3600),
    ):
        value = data.get(section, {}).get(key)
        if value is not None and not low <= value <= high:
            raise BloggerError(f"{section}.{key} 必须在 {low}–{high} 之间")
    if data.get("search", {}).get("refresh_url"):
        web_url(data["search"]["refresh_url"])
    return data
