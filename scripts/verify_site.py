"""Read-only local output checks; authored broken links are reported separately."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup


def verify(root: Path) -> dict:
    articles, drafts, broken, errors = [], [], [], []
    for page in sorted(root.rglob("*.html")):
        soup = BeautifulSoup(page.read_text("utf-8"), "html.parser")
        marker = soup.select_one('meta[name="blogger:page"]')
        if marker is None:
            errors.append(f"Missing page marker: {page.relative_to(root)}")
        elif marker.get("content") == "article":
            articles.append(page.relative_to(root).as_posix())
            if soup.select_one('meta[name="blogger:draft"][content="true"]'):
                drafts.append(articles[-1])
            if not soup.select_one("article h1") or not soup.select_one(".article-content"):
                errors.append(f"Missing article structure: {articles[-1]}")
        for tag, attr in (("a", "href"), ("img", "src"), ("script", "src"), ("link", "href")):
            for element in soup.find_all(tag):
                value = element.get(attr, "")
                parsed = urlsplit(value)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                path = unquote(parsed.path)
                target = root / path.lstrip("/") if path.startswith("/") else page.parent / path
                if not target.exists():
                    broken.append(
                        {"page": page.relative_to(root).as_posix(), "url": value, "element": tag}
                    )
    return {
        "articles": len(articles),
        "drafts": len(drafts),
        "errors": errors,
        "broken_links": broken,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.root.resolve())
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result["errors"]))
