import pytest

from djhx_blogger.config import BloggerError
from djhx_blogger.content import date_rank, parse_document, parse_metadata, render_markdown


def test_bom_crlf_yaml_and_multiline_summary(tmp_path):
    path = tmp_path / "index.md"
    path.write_bytes(
        b'\xef\xbb\xbf---\r\n# comment\r\ntitle: "A: B"\r\nsummary: |\r\n  first\r\n  second\r\ndate: 2026-10-01T09:30:00+08:00\r\ndraft: true\r\n---\r\n\r\n## Body\r\n'
    )
    doc = parse_document(path)
    assert doc.metadata["title"] == "A: B"
    assert doc.metadata["summary"] == "first\nsecond\n"
    assert doc.metadata["draft"] is True
    assert doc.metadata["date"] == "2026-10-01T09:30:00+08:00"
    assert "<h2" in render_markdown(doc.body)[0]
    assert "first" not in doc.body


@pytest.mark.parametrize(
    "text",
    [
        'draft: "true"',
        "title: 123",
        "summary:",
        "date: []",
        '!!python/object/apply:os.system ["echo bad"]',
    ],
)
def test_bad_metadata_is_rejected(text):
    with pytest.raises(BloggerError):
        parse_metadata(text)


def test_unterminated_metadata_reports_file(tmp_path):
    path = tmp_path / "index.md"
    path.write_text("---\ntitle: test\nbody", "utf-8")
    with pytest.raises(BloggerError, match="未闭合"):
        parse_document(path)


def test_horizontal_rule_is_not_eaten(tmp_path):
    path = tmp_path / "index.md"
    path.write_text("---\n\nParagraph\n\n---\n\nSecond", "utf-8")
    assert parse_document(path).body.startswith("---")


@pytest.mark.parametrize("value", ["", "not-date", "2026-99-01", None])
def test_invalid_dates_are_sortable(value):
    assert date_rank(value) is None


def test_dates_are_timezone_independent():
    assert date_rank("2026-01-01T08:00:00+08:00") == date_rank("2026-01-01T00:00:00Z")
    assert date_rank("2026-01-01") == date_rank("2026-01-01T00:00:00Z")
    assert date_rank("1900-01-01") < 0


def test_missing_and_null_dates_have_safe_defaults(tmp_path):
    path = tmp_path / "note.md"
    path.write_text("---\ndate:\n---\nhello", "utf-8")
    metadata = parse_document(path).metadata
    assert metadata == {"date": "", "title": "note", "summary": "", "draft": False}


def test_fences_tables_toc_and_highlighting():
    html, toc = render_markdown(
        "## Test\n\n[TOC]\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n```python\nprint('hi')\n```"
    )
    assert "<table>" in html
    assert "highlight" in html
    assert 'href="#test"' in toc
