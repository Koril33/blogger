"""Deterministic directory discovery and transactional, incremental site builds."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tempfile
import time
import uuid
from collections import defaultdict, deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime
from functools import lru_cache
from importlib import resources
from importlib.metadata import version
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

import yaml
from bs4 import BeautifulSoup
from jinja2 import DictLoader, Environment, select_autoescape
from markupsafe import Markup
from pygments.formatters import HtmlFormatter

from .config import BloggerError, BuildOptions, SiteConfig
from .content import Document, date_rank, parse_document, render_markdown
from .content import md_to_html as md_to_html
from .content import parse_metadata as parse_metadata
from .content import read_metadata as read_metadata
from .images import IMAGE_SUFFIXES, compress_image
from .log_config import app_logger as logger

MANIFEST = ".blogger-build.json"
SCHEMA = 1
IGNORED = {"LICENSE", "node_modules", "__pycache__"}
RESERVED = {"css", "js", "archive.html", MANIFEST}


@dataclass
class Node:
    source_path: Path
    destination_path: Path
    node_type: str
    children: list[Node] = field(default_factory=list)
    metadata: dict | None = None
    document: Document | None = None
    asset: bool = False
    stats: dict = field(default_factory=dict)


def _linked(path: Path) -> bool:
    if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _rename(source: Path, destination: Path):
    # Windows scanners may briefly retain a file handle after the writer closes it.
    for attempt in range(6):
        try:
            return source.rename(destination)
        except PermissionError:
            if os.name != "nt" or attempt == 5:
                raise
            time.sleep(0.05 * (attempt + 1))


def _safe_paths(source: Path, target: Path, name: str) -> tuple[Path, Path]:
    if name in {"", ".", ".."} or Path(name).name != name or "/" in name or "\\" in name:
        raise BloggerError("输出目录名必须是单个目录名")
    if _linked(source) or _linked(target) or _linked(target / name):
        raise BloggerError("源目录和输出目录不能是符号链接或 junction")
    source, target = source.resolve(), target.resolve()
    destination = target / name
    if not source.is_dir():
        raise BloggerError(f"源目录不存在或不是目录: {source}")
    if _within(target, source) or _within(source, destination):
        raise BloggerError("源目录与输出目录不能重叠；请用 -t 指定博客目录之外的位置")
    if target.exists() and not target.is_dir():
        raise BloggerError(f"输出父路径不是目录: {target}")
    return source, destination


def walk_dir(dir_path_str: str, destination_blog_dir_path_str: str, target_name="public") -> Node:
    source, destination = _safe_paths(
        Path(dir_path_str), Path(destination_blog_dir_path_str), target_name
    )
    root = Node(source, destination, "category")
    queue = deque([root])
    while queue:
        node = queue.popleft()
        with os.scandir(node.source_path) as entries:
            children = sorted(entries, key=lambda entry: (entry.name.casefold(), entry.name))
        mapped = set()
        for entry in children:
            if entry.name.startswith(".") or entry.name in IGNORED:
                continue
            source_path = Path(entry.path)
            if _linked(source_path):
                raise BloggerError(f"拒绝跟随符号链接或 junction: {source_path}")
            is_directory = entry.is_dir(follow_symlinks=False)
            if not is_directory and not entry.is_file(follow_symlinks=False):
                raise BloggerError(f"源文件不是普通文件: {source_path}")
            asset = node.asset or (is_directory and entry.name == "images")
            is_markdown = not asset and source_path.suffix.lower() == ".md" and not is_directory
            output_name = source_path.with_suffix(".html").name if is_markdown else entry.name
            if is_markdown and source_path.name.lower() == "index.md":
                output_name = "index.html"
            if node is root and output_name in RESERVED:
                raise BloggerError(f"源目录包含保留的输出名称: {entry.name}")
            # Every content directory owns index.html, except an explicit index.md.
            if not node.asset and output_name.lower() == "index.html" and not is_markdown:
                raise BloggerError(f"源文件与生成页面冲突: {source_path}")
            if output_name.casefold() in mapped:
                raise BloggerError(f"多个源文件对应同一输出路径: {source_path}")
            mapped.add(output_name.casefold())
            child = Node(
                source_path,
                node.destination_path / output_name,
                "category" if is_directory else "leaf",
                asset=asset,
            )
            if is_markdown:
                child.document = parse_document(source_path)
                child.metadata = child.document.metadata
                if source_path.name.lower() == "index.md":
                    node.node_type = "article"
                    node.metadata = child.metadata
            node.children.append(child)
            if is_directory:
                queue.append(child)
    return root


def _nodes(root: Node):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        yield node
        queue.extend(node.children)


def load_template(name: str) -> str:
    return resources.files("djhx_blogger").joinpath("static", "template", name).read_text("utf-8")


def load_image(name: str) -> Path:
    return Path(str(resources.files("djhx_blogger").joinpath("static", "images", name)))


@lru_cache(maxsize=1)
def _environment() -> Environment:
    templates = {
        name: load_template(name)
        for name in ("base.html", "article.html", "category.html", "archive.html")
    }
    return Environment(loader=DictLoader(templates), autoescape=select_autoescape(["html"]))


def _context(site: SiteConfig) -> dict:
    base = site.base_path.rstrip("/") + "/"
    about = site.about_url
    if about and not urlsplit(about).scheme:
        about = base + about.lstrip("/")
    return {"site": site, "base": base, "about_url": about, "year": datetime.now().year}


def _url(path: Path) -> str:
    return quote(path.as_posix(), safe="/")


def _article_html(document: Document, site: SiteConfig, breadcrumbs=()) -> str:
    content, toc = render_markdown(document.body)
    soup = BeautifulSoup(content, "html.parser")
    for image in soup.find_all("img"):
        image.attrs.setdefault("loading", "lazy")
        image.attrs.setdefault("decoding", "async")
    for link in soup.find_all("a", href=True):
        parsed = urlsplit(link["href"])
        if not parsed.scheme and not parsed.netloc and parsed.path.lower().endswith(".md"):
            converted = unquote(parsed.path)[:-3] + ".html"
            link["href"] = urlunsplit(
                ("", "", quote(converted, safe="/"), parsed.query, parsed.fragment)
            )
    return (
        _environment()
        .get_template("article.html")
        .render(
            **_context(site),
            metadata=document.metadata,
            content=Markup(str(soup)),
            toc=Markup(toc) if "<li>" in toc else "",
            breadcrumbs=breadcrumbs,
            page_kind="article",
        )
    )


def gen_article_index(md_file_path: Path, article_name=None) -> str:
    return _article_html(parse_document(Path(md_file_path)), SiteConfig())


def sort_categories(item):
    if item["type"] == "category":
        return 0, item["name"].casefold(), item["href"]
    rank = date_rank(item["metadata"].get("date", ""))
    return 1, rank is None, -(rank or 0), item["name"].casefold(), item["href"]


def gen_category_index(categories: list, category_name: str, site=None, breadcrumbs=()) -> str:
    return (
        _environment()
        .get_template("category.html")
        .render(
            **_context(site or SiteConfig()),
            categories=categories,
            category_name=category_name,
            breadcrumbs=breadcrumbs,
            page_kind="category",
        )
    )


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fingerprint(data) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _old_manifest(destination: Path) -> dict:
    try:
        data = json.loads((destination / MANIFEST).read_text("utf-8"))
        if (
            isinstance(data, dict)
            and data.get("generator") == "djhx-blogger"
            and data.get("schema") == SCHEMA
            and isinstance(data.get("files"), dict)
        ):
            return data
    except (OSError, ValueError):
        pass
    return {}


def _breadcrumbs(path: Path, root: Node, site: SiteConfig) -> list:
    relative = path.relative_to(root.source_path)
    base = site.base_path.rstrip("/") + "/"
    result = [{"title": "首页", "href": base + "index.html"}]
    for i, part in enumerate(relative.parts):
        result.append(
            {"title": part, "href": base + _url(Path(*relative.parts[: i + 1]) / "index.html")}
        )
    return result


def _copy_resource(destination: Path):
    for name in ("css", "js", "images"):
        source = resources.files("djhx_blogger").joinpath("static", name)
        for item in source.iterdir():
            if item.is_file():
                if name == "images" and item.name == "mountain.jpg":
                    continue  # The demo copies this image into its own article directory.
                target = destination / name / item.name
                if target.exists():
                    raise BloggerError(f"内容与内置资源重名: {target.name}")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(item.read_bytes())
    (destination / "css" / "highlight.css").write_text(
        HtmlFormatter(style="friendly").get_style_defs(".highlight"), "utf-8"
    )


def _build(root: Node, old: Path, site: SiteConfig, options: BuildOptions) -> dict:
    nodes = list(_nodes(root))
    old_files = _old_manifest(old).get("files", {}) if options.cache else {}
    template_hash = _fingerprint(
        {
            name: load_template(name)
            for name in ("base.html", "article.html", "category.html", "archive.html")
        }
    )
    render_key = _fingerprint(
        [
            SCHEMA,
            template_hash,
            asdict(site),
            datetime.now().year,
            {
                package: version(package)
                for package in ("djhx-blogger", "markdown", "pygments", "jinja2", "beautifulsoup4")
            },
        ]
    )
    image_key = _fingerprint(
        [
            SCHEMA,
            options.compress_images,
            options.image_quality,
            options.max_width,
            options.max_height,
            version("pillow"),
        ]
    )
    manifest_files, tasks, articles = {}, [], []
    stats = {"cached": 0, "processed": 0, "articles": 0, "images": 0, "input_bytes": 0}
    for node in nodes:
        if node.node_type != "leaf":
            node.destination_path.mkdir(parents=True, exist_ok=True)
            if node.node_type == "category" and not node.asset:
                categories = []
                for child in node.children:
                    if child.asset or (child.node_type == "leaf" and child.document is None):
                        continue
                    kind = (
                        "article" if child.document or child.node_type == "article" else "category"
                    )
                    href = (
                        child.destination_path.name
                        if child.document
                        else child.destination_path.name + "/index.html"
                    )
                    categories.append(
                        {
                            "type": kind,
                            "name": (child.metadata or {}).get("title", child.source_path.name),
                            "href": quote(href, safe="/"),
                            "metadata": child.metadata or {"summary": "", "date": ""},
                        }
                    )
                categories.sort(key=sort_categories)
                title = site.title if node is root else node.source_path.name
                html = gen_category_index(
                    categories,
                    title,
                    site,
                    _breadcrumbs(node.source_path.parent, root, site) if node is not root else [],
                )
                (node.destination_path / "index.html").write_text(html, "utf-8")
            continue
        relative = node.source_path.relative_to(root.source_path).as_posix()
        output = node.destination_path.relative_to(root.destination_path).as_posix()
        source_hash = node.document.source_hash if node.document else _hash(node.source_path)
        key = (
            render_key
            if node.document
            else image_key
            if node.source_path.suffix.lower() in IMAGE_SUFFIXES
            else "copy-v1"
        )
        record = {"source_hash": source_hash, "key": key, "output": output}
        stats["input_bytes"] += node.source_path.stat().st_size
        stats["images"] += node.source_path.suffix.lower() in IMAGE_SUFFIXES
        if node.document:
            articles.append({"metadata": node.metadata, "url": _url(Path(output))})
        cached = old_files.get(relative, {})
        old_path = old / output
        node.destination_path.parent.mkdir(parents=True, exist_ok=True)
        if (
            isinstance(cached, dict)
            and all(cached.get(k) == v for k, v in record.items())
            and old_path.is_file()
            and not _linked(old_path)
            and _hash(old_path) == cached.get("output_hash")
        ):
            shutil.copy2(old_path, node.destination_path)
            stats["cached"] += 1
        else:
            tasks.append(node)
        manifest_files[relative] = record

    def process(node):
        if node.document:
            node.destination_path.write_text(
                _article_html(
                    node.document, site, _breadcrumbs(node.source_path.parent, root, site)
                ),
                "utf-8",
            )
        elif options.compress_images and node.source_path.suffix.lower() in IMAGE_SUFFIXES:
            compress_image(
                node.source_path,
                node.destination_path,
                options.image_quality,
                (options.max_width, options.max_height),
            )
        else:
            shutil.copy2(node.source_path, node.destination_path)

    # Bounded futures keep memory and concurrent image decoders under control.
    with ThreadPoolExecutor(max_workers=options.workers) as executor:
        pending = set()
        for node in tasks:
            pending.add(executor.submit(process, node))
            if len(pending) >= options.workers * 2:
                done, pending = wait(pending, return_when=FIRST_COMPLETED)
                for future in done:
                    future.result()
        for future in pending:
            future.result()
    for node in nodes:
        if node.node_type == "leaf":
            relative = node.source_path.relative_to(root.source_path).as_posix()
            # Abort if a source was edited during this build; never cache mismatched bytes.
            if _hash(node.source_path) != manifest_files[relative]["source_hash"]:
                raise BloggerError(f"构建期间源文件发生变化，请重试: {node.source_path}")
            manifest_files[relative]["output_hash"] = _hash(node.destination_path)
    stats["processed"] = len(tasks)
    stats["articles"] = len(articles)
    archives = {}
    for article in sorted(
        articles,
        key=lambda a: (
            date_rank(a["metadata"]["date"]) is None,
            -(date_rank(a["metadata"]["date"]) or 0),
            a["url"],
        ),
    ):
        metadata = article["metadata"]
        year = metadata["date"][:4] or "未注明日期"
        group = archives.setdefault(year, {"articles": [], "total": 0})
        group["articles"].append(
            {
                "title": metadata["title"],
                "date": metadata["date"][:10],
                "draft": metadata["draft"],
                "url": article["url"],
            }
        )
        group["total"] += 1
    html = (
        _environment()
        .get_template("archive.html")
        .render(**_context(site), archives=archives, total=len(articles), page_kind="archive")
    )
    (root.destination_path / "archive.html").write_text(html, "utf-8")
    _copy_resource(root.destination_path)
    (root.destination_path / MANIFEST).write_text(
        json.dumps(
            {"generator": "djhx-blogger", "schema": SCHEMA, "files": manifest_files},
            ensure_ascii=False,
            sort_keys=True,
        ),
        "utf-8",
    )
    return stats


def generate_blog(
    blog_dir: str, blog_target: str, *, site=None, options=None, target_name="public"
) -> Node:
    start = time.perf_counter()
    site, options = site or SiteConfig(), options or BuildOptions()
    source, destination = _safe_paths(Path(blog_dir), Path(blog_target), target_name)
    if site.about_url == "/about/index.html" and not (source / "about" / "index.md").is_file():
        site = replace(site, about_url="")
    target = destination.parent
    if destination.exists() and not _old_manifest(destination):
        # Recognize an output from <=0.2.3 for migration, otherwise protect user data.
        legacy = all(
            (destination / name).exists()
            for name in ("index.html", "archive.html", "css", "images")
        )
        if not destination.is_dir() or not legacy:
            raise BloggerError(f"拒绝覆盖非 blogger 输出目录: {destination}")
    target.mkdir(parents=True, exist_ok=True)
    lock = target / f".blogger-{target_name}.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise BloggerError(f"输出目录正被另一构建占用；确认进程已退出后再移除 {lock}") from exc
    os.close(descriptor)
    stage = None
    backup = target / f".blogger-backup-{uuid.uuid4().hex}"
    try:
        stage = Path(tempfile.mkdtemp(prefix=".blogger-stage-", dir=target))
        root = walk_dir(str(source), str(target), target_name)
        for node in _nodes(root):
            node.destination_path = stage / node.destination_path.relative_to(destination)
        stats = _build(root, destination, site, options)
        if destination.exists():
            _rename(destination, backup)
        try:
            _rename(stage, destination)
        except BaseException:
            if backup.exists():
                _rename(backup, destination)
            raise
        for node in _nodes(root):
            node.destination_path = destination / node.destination_path.relative_to(stage)
        stats["elapsed_seconds"] = round(time.perf_counter() - start, 3)
        stats["output_bytes"] = sum(p.stat().st_size for p in destination.rglob("*") if p.is_file())
        root.stats = stats
        if backup.exists():
            try:
                shutil.rmtree(backup)
            except OSError:
                logger.warning("构建成功，旧输出备份未能清理: %s", backup)
        logger.info(
            "生成 %s 篇文章；处理 %s、复用 %s 个文件；%ss；输出 %s",
            stats["articles"],
            stats["processed"],
            stats["cached"],
            stats["elapsed_seconds"],
            format_size(stats["output_bytes"]),
        )
        return root
    finally:
        if stage is not None and stage.exists():
            shutil.rmtree(stage)
        lock.unlink(missing_ok=True)


def init_new_post(blog_dir: str, post_name: str):
    source = Path(blog_dir)
    if _linked(source):
        raise BloggerError("博客根目录不能是符号链接或 junction")
    source = source.resolve()
    relative = Path(post_name)
    if (
        not source.is_dir()
        or relative.is_absolute()
        or ".." in relative.parts
        or any(c in post_name for c in "\r\n\x00")
    ):
        raise BloggerError("文章路径必须是博客根目录内的相对路径")
    target = source / relative
    if not _within(target.resolve(), source) or target.resolve() == source:
        raise BloggerError("文章路径必须位于博客根目录内")
    for parent in (target, *target.parents):
        if parent == source:
            break
        if _linked(parent):
            raise BloggerError("文章路径不能包含符号链接")
    target.mkdir(parents=True, exist_ok=True)
    metadata = {
        "title": target.name,
        "date": datetime.now().astimezone().isoformat(timespec="seconds"),
        "summary": "",
        "draft": True,
    }
    try:
        with (target / "index.md").open("x", encoding="utf-8") as stream:
            stream.write(
                "---\n"
                + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
                + "---\n\n正文内容。\n"
            )
    except FileExistsError as exc:
        raise BloggerError(f"文章已存在: {target / 'index.md'}") from exc
    (target / "images").mkdir(exist_ok=True)
    return target


def init_new_blog(blog_dir: str):
    target = Path(blog_dir) / "simple-blog"
    if target.exists():
        raise BloggerError(f"示例博客已存在: {target}")
    target.mkdir(parents=True)
    post = init_new_post(str(target), "demo-article")
    (post / "index.md").write_text(
        '---\ntitle: "第一篇博客"\ndate: "2026-01-01T08:00:00+08:00"\nsummary: "从一篇 Markdown 开始。"\n---\n\n## Hello, world\n\n![山景](images/mountain.jpg)\n\n```python\nprint("Hello, blogger!")\n```\n',
        "utf-8",
    )
    shutil.copy2(load_image("mountain.jpg"), post / "images" / "mountain.jpg")
    return target


def analyze_directory_size(directory_path):
    stats = defaultdict(lambda: {"count": 0, "size_bytes": 0})
    for path in Path(directory_path).rglob("*"):
        if path.is_file() and not _linked(path):
            suffix = path.suffix.lstrip(".").lower() or "无扩展名"
            stats[suffix]["count"] += 1
            stats[suffix]["size_bytes"] += path.stat().st_size
    return dict(stats)


def format_size(size_bytes):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size_bytes < 1024 or unit == "TB":
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024


def print_directory_stats(directory_path):
    for suffix, stats in sorted(analyze_directory_size(directory_path).items()):
        print(f"{suffix}: {stats['count']} files, {format_size(stats['size_bytes'])}")
