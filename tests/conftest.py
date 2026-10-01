from pathlib import Path

import pytest


@pytest.fixture
def blog(tmp_path):
    source = tmp_path / "blog"
    source.mkdir()
    return source


@pytest.fixture
def post():
    def write(
        source: Path,
        slug="分类/中文 & space",
        *,
        metadata='title: "自定义标题"\ndate: 2025-01-01\nsummary: "一段摘要"',
        body="## 小节\n\n正文。",
    ):
        path = source / slug / "index.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        text = f"---\n{metadata}\n---\n\n{body}" if metadata is not None else body
        path.write_text(text, "utf-8")
        return path

    return write
