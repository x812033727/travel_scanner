"""Series rules for 搜尋最佳化名詞系列 that `pack_cli` does not enforce.

`pack_cli lint` encodes the house minimum for every 生活分享 article: three level-2
headings, a hero, a table, a callout, sound SVGs, sources with a check date. This
series asks for more than that minimum, and it asks for things that are specific to
these eleven articles -- an exact topic vocabulary, a link allowlist per article, one
check date, prose inside a narrower band than the tool's warning range.

Rather than restate the tool's rules and drift from them, this delegates to
``lint_document``, ``check_svg`` and ``missing_diagram_numbers`` and only adds what
they leave out. Every rule here comes from ``docs/ai-search-series/brief.md`` or from
the assignment in ``catalogue.json``; nothing is invented at this layer.

It reads the writing workspace, not the shipped packs, so it can run before ingest::

    cd apps/api && uv run python ../../docs/ai-search-series/check.py
    cd apps/api && uv run python ../../docs/ai-search-series/check.py --slug ai-search-geo

Exit code is 1 when anything is reported, so CI or a coordinator can gate on it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SERIES_DIR = Path(__file__).resolve().parent
REPO = SERIES_DIR.parent.parent
API = REPO / "apps" / "api"
if str(API) not in sys.path:
    sys.path.insert(0, str(API))

from app.guides.pack_ingest import (  # noqa: E402
    _body_length,
    _document_text,
    check_svg,
    lint_document,
    missing_diagram_numbers,
)
from app.guides.schemas import GuideDocument  # noqa: E402

#: The brief asks for 1,800-3,000 characters of running prose. The tool only warns
#: outside 1,500-6,000, which lets a 1,600-character stub through.
PROSE_RANGE = (1_800, 3_000)
#: Five, not the tool's three. A term this contested needs room for the disagreement.
MIN_LEVEL_2_HEADINGS = 5
#: One comparison table per article: the series is a comparison, and two tables in one
#: article has always meant the second one is a list wearing a table's clothes.
TABLE_COUNT = 1
MIN_INTERNAL_LINKS = 3
MIN_SOURCES = 2
CHECK_DATE = "2026-09-14"
TITLE_MAX = 60
DESCRIPTION_RANGE = (120, 200)

TRACKING = re.compile(r"[?&](utm_[a-z]+|gclid|fbclid|ref|referrer|aff|affiliate)=", re.I)
#: Simplified forms whose traditional counterpart is the house spelling. A Taiwanese
#: reader notices these immediately and they survive every automated translation pass.
SIMPLIFIED = ("软件", "网络", "数据", "视频", "质量", "用户", "项目", "文件夹", "搜索引擎优化")

EXPECTED = {
    "kind": "life",
    "destination_id": None,
    "topics": ["ai", "tutorial"],
    "valid_until": None,
    "featured": False,
    "display_order": 100,
}

SITE = "https://mokaair.com/zh-TW/life/"


def catalogue() -> dict:
    return json.loads((SERIES_DIR / "catalogue.json").read_text(encoding="utf-8"))


def shipped_slugs() -> set[str]:
    return {p.stem for p in (API / "app" / "guides" / "content").glob("*.json")}


def internal_targets(document: GuideDocument) -> list[str]:
    """Slugs this article points at, however it points at them.

    Body cross-links are ``article`` inlines, which are locale-relative. The index
    article instead lists absolute URLs in ``link`` blocks, the way `ai-terms-index`
    does, because a list of links renders as a list and a paragraph does not.
    """
    targets: list[str] = []
    for block in document.blocks:
        kind = getattr(block, "type", None)
        if kind == "rich_paragraph":
            targets += [i.slug for i in block.inlines if getattr(i, "type", None) == "article"]
        elif kind == "link" and block.url.startswith(SITE):
            targets.append(block.url[len(SITE) :].strip("/"))
    return targets


def check_pack(slug: str, entry: dict, batch: set[str], shipped: set[str]) -> list[str]:
    workdir = SERIES_DIR / "staging" / slug
    pack_path = workdir / "pack.json"
    if not pack_path.is_file():
        return ["no pack.json in the workspace"]

    found: list[str] = []
    pack = json.loads(pack_path.read_text(encoding="utf-8"))

    if pack.get("slug") != slug:
        found.append(f"pack slug is {pack.get('slug')!r}, directory says {slug!r}")
    for field, want in EXPECTED.items():
        if pack.get(field) != want:
            found.append(f"{field} is {pack.get(field)!r}, the series uses {want!r}")
    if set(pack.get("locales", {})) != {"zh-TW"}:
        found.append(f"locales are {sorted(pack.get('locales', {}))}, the series is zh-TW only")

    raw = pack.get("locales", {}).get("zh-TW")
    if raw is None:
        return found + ["no zh-TW document"]
    document = GuideDocument.model_validate(raw)

    # Everything the tool already refuses, reported here so one run says it all.
    found += [f"{p.code}: {p.detail}" for p in lint_document(document, "life")]

    length = _body_length(document)
    low, high = PROSE_RANGE
    if not low <= length <= high:
        found.append(f"{length} characters of prose; the series asks for {low:,}-{high:,}")

    headings = [b for b in document.blocks if getattr(b, "type", None) == "heading" and b.level == 2]
    if len(headings) < MIN_LEVEL_2_HEADINGS:
        found.append(f"{len(headings)} level-2 headings; the series asks for {MIN_LEVEL_2_HEADINGS}")

    tables = [b for b in document.blocks if getattr(b, "type", None) == "table"]
    if len(tables) != TABLE_COUNT:
        found.append(f"{len(tables)} tables; the series asks for exactly {TABLE_COUNT}")

    if any(getattr(b, "type", None) == "partner_link" for b in document.blocks):
        found.append("a partner_link block; this series carries no affiliate links")

    title, description = document.title, document.description
    if len(title) > TITLE_MAX:
        found.append(f"title is {len(title)} characters, the series caps it at {TITLE_MAX}")
    lo, hi = DESCRIPTION_RANGE
    if not lo <= len(description) <= hi:
        found.append(f"description is {len(description)} characters, the series asks for {lo}-{hi}")

    if document.hero is None:
        found.append("no hero")
    elif document.hero.src != f"/guides/{slug}/hero.jpg":
        found.append(f"hero src is {document.hero.src}, expected /guides/{slug}/hero.jpg")

    diagrams = [
        b
        for b in document.blocks
        if getattr(b, "type", None) == "image" and b.src.startswith(f"/guides/{slug}/diagram-")
    ]
    if not diagrams:
        found.append("no diagram image block")

    allowed = set(entry["links"])
    targets = internal_targets(document)
    if len(targets) < MIN_INTERNAL_LINKS:
        found.append(f"{len(targets)} internal links; the series asks for {MIN_INTERNAL_LINKS}")
    for target in targets:
        if target not in allowed:
            found.append(f"links to {target}, which the assignment does not list")
        if target not in batch and target not in shipped:
            found.append(f"links to {target}, which is not a real article")

    if len(document.sources) < MIN_SOURCES:
        found.append(f"{len(document.sources)} sources; the series asks for {MIN_SOURCES}")
    for source in document.sources:
        if str(source.checked_on) != CHECK_DATE:
            found.append(f"{source.url} is checked_on {source.checked_on}, expected {CHECK_DATE}")
        if TRACKING.search(source.url):
            found.append(f"{source.url} carries a tracking parameter")

    body = _document_text(document)
    for form in SIMPLIFIED:
        if form in body:
            found.append(f"simplified form {form!r} in the body")

    # The tool checks the SVGs it has already staged. These have not been staged yet,
    # so check them where the writer left them.
    for name in ("hero.svg", "diagram-1.svg", "diagram-2.svg"):
        svg = workdir / name
        if not svg.is_file():
            if name != "diagram-2.svg":
                found.append(f"no {name}")
            continue
        text = svg.read_text(encoding="utf-8")
        found += [f"{name} {p.code}: {p.detail}" for p in check_svg(text)]
        missing = missing_diagram_numbers(text, document)
        if missing:
            found.append(f"{name} shows {', '.join(missing)}, which the body never says")

    for name in ("notes.md", "research.json"):
        if not (workdir / name).is_file():
            found.append(f"no {name}")

    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--slug", action="append", help="Only this slug (repeatable)")
    args = parser.parse_args(argv)

    data = catalogue()
    entries = {a["slug"]: a for a in data["articles"]}
    batch = set(entries)
    shipped = shipped_slugs()
    wanted = args.slug or list(entries)

    total = 0
    for slug in wanted:
        entry = entries.get(slug)
        if entry is None:
            print(f"{slug}\n  not in catalogue.json")
            total += 1
            continue
        found = check_pack(slug, entry, batch, shipped)
        if found:
            print(slug)
            for line in found:
                print(f"  {line}")
            total += len(found)

    print(f"{len(wanted)} article(s) checked, {total} finding(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
