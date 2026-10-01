import json
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from djhx_blogger import gen
from djhx_blogger.config import BloggerError, SiteConfig


def test_drafts_escape_metadata_and_encode_paths(blog, post, tmp_path):
    post(
        blog,
        metadata='title: "<script>alert(1)</script>"\nsummary: "<b>intro</b>"\ndraft: true\ndate: 2025-01-01',
    )
    root = gen.generate_blog(str(blog), str(tmp_path / "output"))
    article = root.destination_path / "分类/中文 & space/index.html"
    soup = BeautifulSoup(article.read_text("utf-8"), "html.parser")
    assert soup.select_one("article h1").get_text() == "<script>alert(1)</script>"
    assert not soup.select_one("article h1 script")
    assert soup.select_one(".draft-badge").get_text() == "未完成"
    assert soup.select_one('meta[property="article:published_time"]')["content"] == "2025-01-01"
    assert soup.select_one(".article-content h2")
    category = BeautifulSoup(
        (root.destination_path / "分类/index.html").read_text("utf-8"), "html.parser"
    )
    assert (
        category.select_one(".entry-card")["href"] == "%E4%B8%AD%E6%96%87%20%26%20space/index.html"
    )
    archive = BeautifulSoup(
        (root.destination_path / "archive.html").read_text("utf-8"), "html.parser"
    )
    assert archive.select_one(".draft-badge")
    assert "\\" not in archive.select_one(".archive-title").parent["href"]


def test_assets_hidden_files_loose_markdown_and_link_conversion(blog, post, tmp_path):
    article = post(blog, body="[另一个页面](extra.md#test)\n\n## Test")
    (article.parent / "extra.md").write_text("extra", "utf-8")
    (article.parent / "attachment.pdf").write_bytes(b"PDF bytes")
    (blog / ".env").write_text("secret", "utf-8")
    root = gen.generate_blog(str(blog), str(tmp_path / "out"))
    output = root.destination_path / article.parent.relative_to(blog)
    assert (output / "attachment.pdf").read_bytes() == b"PDF bytes"
    assert (output / "extra.html").is_file()
    assert 'href="extra.html#test"' in (output / "index.html").read_text("utf-8")
    assert not (root.destination_path / ".env").exists()
    assert root.stats["articles"] == 2


def test_repeated_build_cache_corruption_changes_and_deletions(blog, post, tmp_path):
    article = post(blog)
    attachment = article.parent / "note.txt"
    attachment.write_text("one", "utf-8")
    target = tmp_path / "out"
    first = gen.generate_blog(str(blog), str(target))
    assert first.stats["processed"] == 2
    second = gen.generate_blog(str(blog), str(target))
    assert second.stats["cached"] == 2
    page = second.destination_path / article.relative_to(blog).with_suffix(".html")
    page.write_text("corrupt output", "utf-8")
    third = gen.generate_blog(str(blog), str(target))
    assert third.stats["processed"] == 1
    assert "corrupt output" not in page.read_text("utf-8")
    attachment.unlink()
    article.write_text("updated body", "utf-8")
    fourth = gen.generate_blog(str(blog), str(target))
    assert fourth.stats["processed"] == 1
    assert not page.with_name("note.txt").exists()
    assert "updated body" in page.read_text("utf-8")


def test_render_config_invalidates_html(blog, post, tmp_path):
    post(blog)
    target = tmp_path / "out"
    gen.generate_blog(str(blog), str(target))
    root = gen.generate_blog(
        str(blog), str(target), site=SiteConfig(title="New Site", base_path="/notes/")
    )
    assert root.stats["processed"] == 1
    assert 'href="/notes/css/site.css"' in (root.destination_path / "index.html").read_text("utf-8")


def test_image_failure_keeps_live_build_and_removes_stage(blog, post, tmp_path):
    article = post(blog)
    target = tmp_path / "out"
    root = gen.generate_blog(str(blog), str(target))
    before = (root.destination_path / gen.MANIFEST).read_bytes()
    (article.parent / "broken.png").write_bytes(b"invalid image")
    with pytest.raises(BloggerError, match="无法处理图片"):
        gen.generate_blog(str(blog), str(target))
    assert (root.destination_path / gen.MANIFEST).read_bytes() == before
    assert not list(target.glob(".blogger-*"))


def test_commit_failure_rolls_back(blog, post, tmp_path, monkeypatch):
    post(blog)
    target = tmp_path / "out"
    root = gen.generate_blog(str(blog), str(target))
    before = (root.destination_path / gen.MANIFEST).read_bytes()
    original = Path.rename

    def rename(path, destination):
        if path.name.startswith(".blogger-stage-"):
            raise OSError("simulated switch failure")
        return original(path, destination)

    monkeypatch.setattr(Path, "rename", rename)
    with pytest.raises(OSError, match="switch failure"):
        gen.generate_blog(str(blog), str(target))
    assert (root.destination_path / gen.MANIFEST).read_bytes() == before
    assert not list(target.glob(".blogger-*"))


def test_edit_during_build_aborts(blog, post, tmp_path, monkeypatch):
    article = post(blog)
    original = gen._article_html

    def changed(*args, **kwargs):
        article.write_text("changed during build", "utf-8")
        return original(*args, **kwargs)

    monkeypatch.setattr(gen, "_article_html", changed)
    with pytest.raises(BloggerError, match="构建期间"):
        gen.generate_blog(str(blog), str(tmp_path / "out"))
    assert not (tmp_path / "out/public").exists()


@pytest.mark.parametrize("target_name", ["..", "../other", "folder/name", "folder\\name"])
def test_unsafe_output_name(blog, tmp_path, target_name):
    with pytest.raises(BloggerError):
        gen.generate_blog(str(blog), str(tmp_path / "out"), target_name=target_name)


def test_overlap_and_unmanaged_output_protection(blog, post, tmp_path):
    source = post(blog)
    with pytest.raises(BloggerError, match="重叠"):
        gen.generate_blog(str(blog), str(blog / "out"))
    public = tmp_path / "out/public"
    public.mkdir(parents=True)
    (public / "keep.txt").write_text("user data", "utf-8")
    with pytest.raises(BloggerError, match="拒绝覆盖"):
        gen.generate_blog(str(blog), str(public.parent))
    assert source.is_file()
    assert (public / "keep.txt").read_text("utf-8") == "user data"


def test_reserved_output_collision(blog, tmp_path):
    (blog / "archive.md").write_text("collision", "utf-8")
    with pytest.raises(BloggerError, match="保留"):
        gen.generate_blog(str(blog), str(tmp_path / "out"))


def test_directory_links_are_rejected(blog, post, tmp_path, monkeypatch):
    article = post(blog)
    original = gen._linked
    monkeypatch.setattr(gen, "_linked", lambda path: path == article.parent or original(path))
    with pytest.raises(BloggerError, match="链接"):
        gen.generate_blog(str(blog), str(tmp_path / "out"))


def test_root_article_missing_dates_nested_and_custom_destination(blog, post, tmp_path):
    post(blog, slug=".", metadata=None, body="root article")
    post(blog, slug="nested", metadata="date: bad\ndraft: true")
    root = gen.generate_blog(str(blog), str(tmp_path / "out"), target_name="site")
    assert root.stats["articles"] == 2
    assert root.node_type == "article"
    assert (root.destination_path / "css/site.css").is_file()
    archive = (root.destination_path / "archive.html").read_text("utf-8")
    assert "未注明日期" in archive
    assert 'href="index.html"' in archive


def test_build_lock_does_not_remove_other_process_lock(blog, post, tmp_path):
    post(blog)
    target = tmp_path / "out"
    target.mkdir()
    lock = target / ".blogger-public.lock"
    lock.write_text("other process", "utf-8")
    with pytest.raises(BloggerError, match="另一构建"):
        gen.generate_blog(str(blog), str(target))
    assert lock.read_text("utf-8") == "other process"


def test_new_post_draft_and_path_safety(blog):
    target = gen.init_new_post(str(blog), "分类/标题带单引号'")
    assert gen.read_metadata(target / "index.md")["draft"] is True
    with pytest.raises(BloggerError, match="已存在"):
        gen.init_new_post(str(blog), "分类/标题带单引号'")
    with pytest.raises(BloggerError):
        gen.init_new_post(str(blog), "../escape")


def test_empty_blog_builds_offline_and_manifest_is_valid(blog, tmp_path):
    root = gen.generate_blog(str(blog), str(tmp_path / "out"))
    assert root.stats["articles"] == 0
    assert "cdn." not in (root.destination_path / "index.html").read_text("utf-8")
    assert 'href="/about/index.html"' not in (root.destination_path / "index.html").read_text(
        "utf-8"
    )
    assert json.loads((root.destination_path / gen.MANIFEST).read_text("utf-8"))["files"] == {}
