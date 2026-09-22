"""Coordinator intake checks for one article pack: the things ``pack_cli`` does not check.

Run from ``<ROOT>/apps/api`` with that worktree's virtualenv; ``<SCRIPTS>`` below stands for
``<ROOT>/.agents/skills/content-pipeline/scripts``. The checks import the site's own rules from
``app.guides``, so a rule that changes there changes here too::

    <PY> <SCRIPTS>/intake_check.py --slug <SLUG> --workdir <WORKDIR>
    <PY> <SCRIPTS>/intake_check.py --slug <SLUG> --from-content
    ... [--manifest <BATCH_DOCS>/batch.json] [--locale zh-TW] [--no-reader-first] [--api-dir DIR]

``--workdir`` reads ``<WORKDIR>/<slug>/pack.json`` (plus ``images.json`` and ``diagram-*.svg``)
as the writer left them; ``--from-content`` reads the ingested pack from the repository. One line
per finding: ``FAIL`` (exit 1), ``WARN`` (read it) or ``ok``.

Beyond what ``pack_cli ingest`` validates, this checks: body length against the batch's band;
the structure minimums; offer count, position and adjacency; article-inline targets (slug and
kind exist, or belong to this batch); site links (no ``?city=``, the null-destination rules);
summary numbers verbatim in the body; the reader-first counts; sources with ``checked_on`` and
no forbidden host; hero uniqueness across the site and the other workdirs; credits after
ingest; the site's ``lint_document`` errors; ``check_svg`` and ``missing_diagram_numbers`` on
every diagram.

The manifest is optional JSON kept with the batch. Every key is optional::

    {
      "articles": {
        "<slug>": {"kind": "howto", "destination_id": "okinawa",
                   "band": [2400, 3200], "diagrams": 1}
      },
      "bands": {"howto": [1800, 4200], "intel": [0, 2200]},
      "forbidden_hosts": ["example.invalid"],
      "max_table_columns": 4,
      "structure": {"min_h2": 3, "photos": [1, 2], "diagrams": 1},
      "reader_first": {"self_ref_limit": 1, "attrib_para_limit": 1}
    }

Without ``articles`` the pack's own kind and destination_id are trusted (with a WARN); without
``bands`` the repository's ``TEXT_RANGE`` and ``INTEL_TEXT_RANGE`` apply.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[4]

SELF_REF = re.compile(r"本文|這篇")
ATTRIB = re.compile(
    r"官方頁(?:寫|說|的|上)|官網(?:寫|說|上寫|標|載明)|依[^，。；]{0,14}(?:公告|公布)"
    r"|公告(?:寫|說|載明)|頁面(?:寫|說)"
)
NARRATION = re.compile(
    r"查證時|查證當天|查證日|我們查不到|查不到所以|本文不提供|官方頁沒寫|官網沒寫|沒有寫所以"
    r"|我們(?:就)?不標|不是我們加的|本批|規格|撰稿"
)
COUNT_IN_META = re.compile(
    r"(?:[0-9０-９]+|[一二兩三四五六七八九十]+)\s*(?:篇|條|個|家|項|種|處|間|站|款|類|座|段)"
)
NUMBER = re.compile(r"\d[\d,.:]*\d|\d")
DEFAULT_PHOTOS = {"howto": (1, 2), "intel": (1, 2), "life": (0, 2)}
DEFAULT_MIN_H2 = 3
DEFAULT_DIAGRAMS = 1
DEFAULT_MAX_TABLE_COLUMNS = 4
DEFAULT_SELF_REF_LIMIT = 1
DEFAULT_ATTRIB_PARA_LIMIT = 1

FAILS: list[str] = []


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    FAILS.append(msg)


def warn(msg: str) -> None:
    print(f"WARN {msg}")


def ok(msg: str) -> None:
    print(f"ok   {msg}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def block_texts(block: dict[str, Any]) -> list[str]:
    kind = block.get("type")
    if kind in ("paragraph", "heading"):
        return [block.get("text", "")]
    if kind == "rich_paragraph":
        return ["".join(node.get("text", "") for node in block.get("inlines", []))]
    if kind == "list":
        return list(block.get("items", []))
    if kind == "table":
        cells = list(block.get("header", []))
        for row in block.get("rows", []):
            cells.extend(row)
        if block.get("caption"):
            cells.append(block["caption"])
        return cells
    if kind == "callout":
        return [block.get("title", ""), block.get("text", "")]
    if kind == "image":
        return [block.get("caption", ""), block.get("alt", "")]
    if kind == "faq":
        out = []
        for item in block.get("items", []):
            out.extend([item.get("question", ""), item.get("answer", "")])
        return out
    if kind == "link":
        return [block.get("text", "")]
    if kind == "offer":
        return [block.get("heading", "")]
    if kind == "summary":
        return list(block.get("items", []))
    return []


def paragraphs(blocks: list[dict[str, Any]]) -> list[str]:
    out = []
    for block in blocks:
        if block.get("type") == "paragraph":
            out.append(block.get("text", ""))
        elif block.get("type") == "rich_paragraph":
            out.append("".join(node.get("text", "") for node in block.get("inlines", [])))
        elif block.get("type") == "callout":
            out.append(block.get("text", ""))
        elif block.get("type") == "faq":
            out.extend(item.get("answer", "") for item in block.get("items", []))
    return out


def commons_key(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^https?://commons\.wikimedia\.org/wiki/", "", value)
    value = re.sub(r"^https?://commons\.wikimedia\.org/w/index\.php\?title=", "", value)
    value = value.split("#")[0]
    if value.lower().startswith("file:"):
        value = value[5:]
    return value.replace("_", " ").casefold()


def resolve_api_dir(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    root = os.environ.get("MOKAAIR_ROOT")
    base = Path(root) if root else SKILL_ROOT
    return (base / "apps" / "api").resolve()


def pair(value: Any, fallback: tuple[int, int]) -> tuple[int, int]:
    if isinstance(value, list | tuple) and len(value) == 2:
        return int(value[0]), int(value[1])
    return fallback


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--slug", required=True)
    parser.add_argument("--workdir", type=Path, help="Batch working directory holding <slug>/")
    parser.add_argument("--from-content", action="store_true", help="Read the ingested pack")
    parser.add_argument("--manifest", type=Path, help="The batch's batch.json (optional)")
    parser.add_argument("--locale", default="zh-TW")
    parser.add_argument("--api-dir", type=Path, help="apps/api of the worktree (auto-detected)")
    parser.add_argument(
        "--no-reader-first", action="store_true", help="Skip the reader-first counts"
    )
    args = parser.parse_args()
    if not args.from_content and args.workdir is None:
        parser.error("--workdir is required unless --from-content")

    api_dir = resolve_api_dir(args.api_dir)
    if not (api_dir / "app" / "guides").is_dir():
        parser.error(f"{api_dir} is not apps/api; pass --api-dir or set MOKAAIR_ROOT")
    sys.path.insert(0, str(api_dir))
    os.chdir(api_dir)
    from app.guides.admin_service import MAX_OFFER_BLOCKS  # noqa: E402
    from app.guides.content_pack import ArticlePack, default_directory  # noqa: E402
    from app.guides.pack_cli import default_public_dir  # noqa: E402
    from app.guides.pack_ingest import (  # noqa: E402
        HERO_MAX_BYTES,
        INTEL_TEXT_RANGE,
        TEXT_RANGE,
        _body_length,
        check_svg,
        errors,
        lint_document,
        missing_diagram_numbers,
    )

    manifest: dict[str, Any] = load_json(args.manifest) if args.manifest else {}
    articles: dict[str, dict[str, Any]] = manifest.get("articles", {})
    structure: dict[str, Any] = manifest.get("structure", {})
    reader_first: dict[str, Any] = manifest.get("reader_first", {})
    forbidden_hosts = tuple(manifest.get("forbidden_hosts", []))
    max_table_columns = int(manifest.get("max_table_columns", DEFAULT_MAX_TABLE_COLUMNS))

    content_dir = default_directory()
    public_dir = default_public_dir()
    slug = args.slug
    locale = args.locale
    pack_path = (
        content_dir / f"{slug}.json" if args.from_content else args.workdir / slug / "pack.json"
    )
    if not pack_path.exists():
        fail(f"pack not found: {pack_path}")
        return 1
    raw = load_json(pack_path)
    try:
        pack = ArticlePack.model_validate(raw)
    except Exception as exc:  # noqa: BLE001
        fail(f"ArticlePack validation: {str(exc)[:400]}")
        return 1

    kind = raw.get("kind")
    destination = raw.get("destination_id")
    entry = articles.get(slug)
    if entry is None:
        warn("slug not in the manifest: kind and destination_id taken from the pack, not checked")
    else:
        if "kind" in entry and entry["kind"] != kind:
            fail(f"kind {kind} != manifest {entry['kind']}")
        if "destination_id" in entry and entry["destination_id"] != destination:
            fail(f"destination_id {destination} != manifest {entry['destination_id']}")
    doc_raw = raw["locales"].get(locale)
    if doc_raw is None:
        fail(f"no {locale} locale")
        return 1
    document = pack.locales[locale]
    blocks: list[dict[str, Any]] = doc_raw["blocks"]

    # 1. body length and band
    repo_band = INTEL_TEXT_RANGE if kind == "intel" else TEXT_RANGE
    band = pair(manifest.get("bands", {}).get(kind), repo_band)
    if entry is not None and "band" in entry:
        band = pair(entry["band"], band)
    length = _body_length(document)
    low, high = band
    in_band = low <= length <= high
    (ok if in_band else fail)(
        f"body_length={length} band={low}-{high}{'' if in_band else ' OUT OF BAND'}"
    )

    # 2. structure
    types = [b.get("type") for b in blocks]
    if not types or types[0] != "summary":
        fail("first block is not summary")
    h2 = sum(1 for b in blocks if b.get("type") == "heading" and b.get("level") == 2)
    tables = [b for b in blocks if b.get("type") == "table"]
    callouts = sum(1 for t in types if t == "callout")
    images = [b for b in blocks if b.get("type") == "image"]
    diagrams = [b for b in images if re.search(r"/diagram-\d+\.svg$", b.get("src", ""))]
    photos = [b for b in images if b not in diagrams]
    faq = sum(1 for t in types if t == "faq")
    offers = [(i, b) for i, b in enumerate(blocks) if b.get("type") == "offer"]
    print(
        f"info H2={h2} tables={len(tables)} callouts={callouts} diagrams={len(diagrams)}"
        f" photos={len(photos)} offers={len(offers)} faq={faq}"
    )
    min_h2 = int(structure.get("min_h2", DEFAULT_MIN_H2))
    if h2 < min_h2:
        fail(f"fewer than {min_h2} H2")
    if not tables:
        fail("no table")
    if not callouts:
        fail("no callout")
    expected_diagrams = int(structure.get("diagrams", DEFAULT_DIAGRAMS))
    if entry is not None and "diagrams" in entry:
        expected_diagrams = int(entry["diagrams"])
    if len(diagrams) != expected_diagrams:
        warn(f"diagram count {len(diagrams)} (expected {expected_diagrams})")
    photo_setting = structure.get("photos")
    photo_band = pair(photo_setting, DEFAULT_PHOTOS.get(kind, (1, 2)))
    if not photo_band[0] <= len(photos) <= photo_band[1]:
        fail(f"photo count {len(photos)} (expected {photo_band[0]}-{photo_band[1]})")
    for t in tables:
        if len(t.get("header", [])) > max_table_columns:
            fail(f"table with {len(t['header'])} columns (max {max_table_columns}): {t['header']}")

    # 3. offers
    first_h2 = next(
        (i for i, b in enumerate(blocks) if b.get("type") == "heading" and b.get("level") == 2),
        len(blocks),
    )
    if len(offers) > MAX_OFFER_BLOCKS:
        fail(f"{len(offers)} offers (max {MAX_OFFER_BLOCKS})")
    if destination is None and offers:
        fail("destination_id is null but the article carries offers")
    for i, b in offers:
        if i < first_h2:
            fail(f"offer at block {i} before the first H2")
        if i + 1 < len(blocks) and blocks[i + 1].get("type") == "offer":
            fail(f"offers adjacent at blocks {i} and {i + 1}")
        if b.get("destination_id") not in (None, destination):
            warn(f"offer at block {i} points at destination {b.get('destination_id')}")
        if not b.get("heading"):
            warn(f"offer at block {i} has no heading")

    # 4. article inlines and links
    for i, b in enumerate(blocks):
        if b.get("type") == "rich_paragraph":
            for node in b.get("inlines", []):
                if node.get("type") == "article":
                    target = node.get("slug", "")
                    target_kind = node.get("kind")
                    sibling = articles.get(target)
                    if sibling is not None and "kind" in sibling:
                        if sibling["kind"] != target_kind:
                            fail(
                                f"block {i}: inline {target} kind {target_kind}"
                                f" != batch kind {sibling['kind']}"
                            )
                        else:
                            ok(f"block {i}: inline -> batch {target} ({target_kind})")
                        continue
                    tpath = content_dir / f"{target}.json"
                    if not tpath.exists():
                        fail(f"block {i}: inline target {target} does not exist")
                        continue
                    tp = load_json(tpath)
                    if locale not in tp.get("locales", {}):
                        fail(f"block {i}: inline target {target} has no {locale}")
                    if tp.get("kind") != target_kind:
                        fail(f"block {i}: inline {target} kind {target_kind} != {tp.get('kind')}")
                    else:
                        ok(f"block {i}: inline -> {target} ({target_kind})")
                elif node.get("type") == "link":
                    url = node.get("url", "")
                    if "?city=" in url:
                        fail(f"block {i}: link uses ?city= ({url})")
                    if "mokaair.com" not in url:
                        warn(f"block {i}: external link inline {url}")
        elif b.get("type") == "link":
            url = b.get("url", "")
            if "?city=" in url:
                fail(f"block {i}: link block uses ?city= ({url})")
            if "mokaair.com" not in url:
                fail(f"block {i}: link block must be a site URL ({url})")
            if destination is None and "foods?" in url:
                fail(f"block {i}: null-destination article links the food catalogue")

    # 5. summary numbers verbatim in body
    summary = blocks[0].get("items", []) if types and types[0] == "summary" else []
    body = "\n".join(t for b in blocks[1:] for t in block_texts(b))
    for item in summary:
        for num in NUMBER.findall(item):
            if len(num) >= 2 and num not in body:
                fail(f"summary number {num!r} not found verbatim in the body: {item[:60]}")

    # 6. reader-first counts
    if not args.no_reader_first:
        all_text = "\n".join(
            [doc_raw["title"], doc_raw["description"]] + [t for b in blocks for t in block_texts(b)]
        )
        self_ref_limit = int(reader_first.get("self_ref_limit", DEFAULT_SELF_REF_LIMIT))
        attrib_limit = int(reader_first.get("attrib_para_limit", DEFAULT_ATTRIB_PARA_LIMIT))
        self_refs = len(SELF_REF.findall(all_text))
        (ok if self_refs <= self_ref_limit else fail)(
            f"self-reference count (本文/這篇) = {self_refs} (limit {self_ref_limit})"
        )
        for idx, para in enumerate(paragraphs(blocks)):
            n = len(ATTRIB.findall(para))
            if n > attrib_limit:
                fail(f"paragraph {idx} has {n} attribution phrases: {para[:70]}")
        for m in NARRATION.finditer(all_text):
            context = all_text[max(0, m.start() - 25) : m.end() + 25]
            warn(f"verification narration {m.group(0)!r}: ...{context!r}")
        for field, text in (("title", doc_raw["title"]), ("description", doc_raw["description"])):
            for m in COUNT_IN_META.finditer(text):
                warn(f"{field} carries a count {m.group(0)!r}")
        for item in summary:
            for m in COUNT_IN_META.finditer(item):
                warn(f"summary carries a count {m.group(0)!r}: {item[:60]}")
        if len(doc_raw["description"]) < 60:
            warn(f"description is short ({len(doc_raw['description'])} chars)")

    # 7. sources
    sources = doc_raw.get("sources", [])
    if not sources:
        fail("no sources")
    for s in sources:
        if not s.get("checked_on"):
            fail(f"source without checked_on: {s.get('title')}")
        host = re.sub(r"^https?://", "", s.get("url", "")).split("/")[0]
        if any(host.endswith(h) for h in forbidden_hosts):
            fail(f"forbidden source host {host}")
    dates = sorted({s.get("checked_on") for s in sources if s.get("checked_on")})
    print(f"info sources={len(sources)} checked_on={dates}")

    # 8. hero uniqueness (workdir images.json vs every content pack and every other workdir)
    hero_key = None
    if not args.from_content:
        images_path = args.workdir / slug / "images.json"
        if images_path.exists():
            hero_key = commons_key(load_json(images_path).get("hero", {}).get("title", ""))
    elif doc_raw.get("hero") and (doc_raw["hero"].get("credit") or {}).get("source_url"):
        hero_key = commons_key(doc_raw["hero"]["credit"]["source_url"])
    if hero_key:
        clashes = []
        for other in content_dir.glob("*.json"):
            if other.stem == slug:
                continue
            op = load_json(other)
            for loc, d in op.get("locales", {}).items():
                credit = (d.get("hero") or {}).get("credit") or {}
                source_url = credit.get("source_url")
                if source_url and commons_key(source_url) == hero_key:
                    clashes.append(f"{other.stem}:{loc}")
        if not args.from_content:
            for other_dir in args.workdir.iterdir():
                if other_dir.name == slug or not (other_dir / "images.json").exists():
                    continue
                other_title = load_json(other_dir / "images.json").get("hero", {}).get("title", "")
                if commons_key(other_title) == hero_key:
                    clashes.append(f"workdir:{other_dir.name}")
        (fail if clashes else ok)(f"hero uniqueness ({hero_key}) clashes={clashes}")
    else:
        warn("no hero title found to check uniqueness")

    # 9. credits after ingest
    if args.from_content:
        labelled = [("hero", doc_raw.get("hero"))] + [
            (f"block {i}", b)
            for i, b in enumerate(blocks)
            if b.get("type") == "image" and not re.search(r"/diagram-", b.get("src", ""))
        ]
        for label, image in labelled:
            credit = (image or {}).get("credit") or {}
            author = credit.get("author", "")
            if not author:
                fail(f"{label}: no credit author")
            elif author.startswith("http") or "licen" in author.lower() or "CC " in author:
                fail(f"{label}: credit author looks wrong: {author!r}")
        hero_file = public_dir / "guides" / slug / "hero.jpg"
        if hero_file.exists():
            size = hero_file.stat().st_size
            (ok if size <= HERO_MAX_BYTES else warn)(
                f"hero.jpg {size} bytes (guideline {HERO_MAX_BYTES})"
            )

    # 10. the site's own editorial rules, with the pack's topics so topic-bound rules fire
    for problem in errors(lint_document(document, kind, topics=pack.topics)):
        fail(f"lint {locale}: {problem}")

    # 11. every diagram: the SVG contract, and every number drawn on it present in the text
    svg_dir = public_dir / "guides" / slug if args.from_content else args.workdir / slug
    svgs = sorted(svg_dir.glob("diagram-*.svg"))
    if not svgs:
        warn(f"no diagram-*.svg under {svg_dir}")
    for svg in svgs:
        text = svg.read_text(encoding="utf-8")
        for problem in errors(check_svg(text)):
            fail(f"{svg.name}: {problem}")
        missing = missing_diagram_numbers(text, document)
        if missing:
            fail(f"{svg.name}: numbers drawn but absent from the {locale} text: {missing}")
        else:
            ok(f"{svg.name}: every number on the diagram is in the text")

    print(f"RESULT {'FAIL' if FAILS else 'PASS'} ({len(FAILS)} failures)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
