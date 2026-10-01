"""Parse Markdown once; normalize dates independently of host timezone."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

import markdown
import yaml

from .config import BloggerError
from .log_config import app_logger as logger


@dataclass
class Document:
    metadata: dict
    body: str
    source_hash: str = ""


def parse_metadata(text: str) -> dict:
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise BloggerError(f"YAML 元数据格式错误: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict) or not all(isinstance(key, str) for key in data):
        raise BloggerError("YAML 元数据必须是字符串键的映射")
    for key in ("title", "summary"):
        if key in data and not isinstance(data[key], str):
            raise BloggerError(f'元数据 {key} 必须是字符串（空摘要请写 summary: ""）')
    if "draft" in data and type(data["draft"]) is not bool:
        raise BloggerError("元数据 draft 必须是 true 或 false，不能加引号")
    value = data.get("date")
    if isinstance(value, (date, datetime)):
        data["date"] = value.isoformat()
    elif value is not None and not isinstance(value, str):
        raise BloggerError("元数据 date 必须是 ISO 8601 日期")
    if value is None:
        data["date"] = ""
    return data


def parse_document(path: Path) -> Document:
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise BloggerError(f"无法读取 Markdown {path}: {exc}") from exc
    lines = text.splitlines(keepends=True)
    metadata = {}
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() in {"---", "..."}), None)
        looks_like_yaml = any(re.match(r"^[A-Za-z_][\w-]*\s*:", line) for line in lines[1:end])
        if looks_like_yaml:
            if end is None:
                raise BloggerError(f"未闭合的 YAML 元数据: {path}")
            try:
                metadata = parse_metadata("".join(lines[1:end]))
            except BloggerError as exc:
                raise BloggerError(f"{path}: {exc}") from exc
            text = "".join(lines[end + 1 :])
    metadata.setdefault("title", path.parent.name if path.name.lower() == "index.md" else path.stem)
    metadata.setdefault("summary", "")
    metadata.setdefault("date", "")
    metadata.setdefault("draft", False)
    if metadata["date"] and date_rank(metadata["date"]) is None:
        logger.warning("%s 的日期无效，归入‘未注明日期’: %s", path, metadata["date"])
        metadata["date"] = ""
    return Document(metadata, text, hashlib.sha256(raw).hexdigest())


def date_rank(value: str) -> float | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return (parsed - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()
    except (ValueError, TypeError, OverflowError):
        return None


def render_markdown(body: str) -> tuple[str, str]:
    converter = markdown.Markdown(
        extensions=["toc", "tables", "sane_lists", "fenced_code", "codehilite"],
        extension_configs={"codehilite": {"guess_lang": False, "css_class": "highlight"}},
    )
    html = converter.convert(body)
    return html, converter.toc


def read_metadata(path: Path) -> dict:
    return parse_document(Path(path)).metadata


def md_to_html(path: Path) -> str:
    return render_markdown(parse_document(Path(path)).body)[0]
