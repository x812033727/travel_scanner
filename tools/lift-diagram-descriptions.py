#!/usr/bin/env python3
"""Lift each diagram's ``<desc>`` into the content pack that references it.

Every localized guide document draws one SVG diagram, and the diagram's ``<desc>`` states
facts -- fares, journey times, station names -- that appear nowhere else in the article. The
web renderer references the file as ``<img>``, so a crawler and every AI answer engine get the
``alt`` and the caption and nothing else. This one-off copies the ``<desc>`` text into the
image block's optional ``description`` field, which ``ImageBlock`` validates and
``ContentBlocks`` draws folded under the caption. The SVG markup itself is never copied:
``contentImageSrc`` vets a path, not a file's contents, so inlining would make any future SVG
a script-injection surface.

    python3 tools/lift-diagram-descriptions.py --dry-run       # counts per pack, writes nothing
    python3 tools/lift-diagram-descriptions.py --slug korea-ktx-srt-ticket-guide
    python3 tools/lift-diagram-descriptions.py                 # every pack

The rules, in the order they apply to an image block:

- Only ``/guides/<slug>/diagram-*.svg`` sources are read (``diagram-1.svg`` shared by every
  locale, or ``diagram-1-en.svg`` drawn for one); photographs are left alone.
- A ``<desc>`` that, once whitespace is normalised, equals the block's ``alt`` or its
  ``caption`` is already on the page and is skipped.
- Otherwise the block's ``description`` becomes the normalised ``<desc>`` text. Nothing else
  in the pack is touched, and a pack is written only when a block changed, in the formatting
  the pack tooling uses (``json.dumps(..., ensure_ascii=False, indent=2) + "\\n"``). A pack
  that would not round-trip byte-for-byte through that formatting is skipped and reported
  rather than reformatted.

The run is idempotent: a second pass reports every lifted block as unchanged and writes
nothing. The ``<title>`` is not lifted: it is the diagram's accessible name, which the block's
``alt`` already carries.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "apps" / "api" / "app" / "guides" / "content"
PUBLIC_DIR = ROOT / "apps" / "web" / "public"

# The block's src grammar (``IMAGE_SRC_PATTERN`` in ``app/guides/schemas.py``) narrowed to
# the diagram family.
DIAGRAM_SRC = re.compile(
    r"^/guides/(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)/(?P<name>diagram-[a-z0-9]+(?:-[a-z0-9]+)*)\.svg$"
)
DESC = re.compile(r"<desc\b[^>]*>(.*?)</desc>", re.DOTALL)
# What ``plain_text`` in ``app/site_pages/schemas.py`` refuses, mirrored so this script never
# writes a description the API would then reject on import.
CONTROL = re.compile(r"[\x00-\x09\x0b-\x1f\x7f-\x9f]")
MARKUP = re.compile(r"<[!/?A-Za-z]")
MAX_DESCRIPTION = 4000  # ``ImageBlock.description``'s ceiling

OUTCOMES = (
    ("lifted", "description set"),
    ("unchanged", "already carried it"),
    ("restates_alt", "desc equals alt"),
    ("restates_caption", "desc equals caption"),
    ("no_desc", "SVG has no desc"),
    ("unusable", "SVG missing or desc refused"),
)


def normalise(text: str) -> str:
    """One space between words and none around them: how the API strips text, and how two
    strings that differ only in whitespace are told apart from two that say different things."""
    return " ".join(text.split())


def svg_description(svg_text: str) -> str | None:
    """The first ``<desc>``'s text with XML entities resolved, or None when there is none.

    A regular expression is enough here: the diagrams are the repository's own, well-formed,
    with one ``<desc>`` each and no markup inside it.
    """
    match = DESC.search(svg_text)
    if match is None:
        return None
    return normalise(html.unescape(match.group(1))) or None


def place_description(block: dict, description: str) -> None:
    """Set ``description`` after ``caption``, the order ``ImageBlock`` declares its fields, or
    after ``alt`` in a block written without a caption, leaving every other key where it is."""
    if "description" in block:
        block["description"] = description
        return
    anchor = "caption" if "caption" in block else "alt"
    entries = list(block.items())
    block.clear()
    for key, value in entries:
        block[key] = value
        if key == anchor:
            block["description"] = description
    block.setdefault("description", description)


def lift_block(block: dict, public_dir: Path) -> str:
    """Apply the rules to one diagram block in place; returns the outcome's name."""
    try:
        svg_text = (public_dir / block["src"].lstrip("/")).read_text(encoding="utf-8")
    except OSError:
        return "unusable"
    description = svg_description(svg_text)
    if description is None:
        return "no_desc"
    if description == normalise(block.get("alt", "")):
        return "restates_alt"
    if description == normalise(block.get("caption", "")):
        return "restates_caption"
    if len(description) > MAX_DESCRIPTION or CONTROL.search(description):
        return "unusable"
    if MARKUP.search(description):
        return "unusable"
    if block.get("description") == description:
        return "unchanged"
    place_description(block, description)
    return "lifted"


def lift_pack(path: Path, public_dir: Path, *, dry_run: bool) -> Counter[str] | None:
    """Lift every diagram block of one pack. Returns the outcome counts, or None when the pack
    is not in the tooling's formatting and so must not be rewritten by this script."""
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if json.dumps(data, ensure_ascii=False, indent=2) + "\n" != raw:
        return None
    counts: Counter[str] = Counter()
    for document in data.get("locales", {}).values():
        for block in document.get("blocks", []):
            if block.get("type") == "image" and DIAGRAM_SRC.match(block.get("src", "")):
                counts[lift_block(block, public_dir)] += 1
    if counts["lifted"] and not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return counts


def describe(counts: Counter[str]) -> str:
    return ", ".join(f"{name} {counts[name]}" for name, _ in OUTCOMES if counts[name])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Copy each diagram's <desc> into the image block's description field."
    )
    parser.add_argument("--dry-run", action="store_true", help="report per pack; write nothing")
    parser.add_argument(
        "--slug", action="append", default=[], metavar="SLUG", help="only this pack (repeatable)"
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=CONTENT_DIR,
        help="the packs (default: the repository's)",
    )
    parser.add_argument(
        "--public-dir",
        type=Path,
        default=PUBLIC_DIR,
        help="the SVGs' web root (default: the repository's)",
    )
    args = parser.parse_args(argv)

    paths = sorted(args.content_dir.glob("*.json"))
    if args.slug:
        wanted = set(args.slug)
        paths = [path for path in paths if path.stem in wanted]
        missing = wanted - {path.stem for path in paths}
        if missing:
            print(f"no pack named: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2

    totals: Counter[str] = Counter()
    with_diagram = changed = 0
    unformatted: list[str] = []
    for path in paths:
        counts = lift_pack(path, args.public_dir, dry_run=args.dry_run)
        if counts is None:
            unformatted.append(path.stem)
            continue
        if not counts:
            continue
        with_diagram += 1
        totals.update(counts)
        if counts["lifted"]:
            changed += 1
        if args.dry_run or counts["lifted"]:
            prefix = "" if args.dry_run else "wrote "
            print(f"{prefix}{path.stem}: {describe(counts)}")
    verb = "would change" if args.dry_run else "changed"
    print(
        f"{with_diagram} pack(s) with a diagram, {changed} {verb}; "
        f"blocks: {describe(totals) or 'none'}"
    )
    for slug in unformatted:
        print(f"skipped {slug}: not in the pack tooling's JSON formatting", file=sys.stderr)
    return 1 if unformatted or totals["unusable"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
