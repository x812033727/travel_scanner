"""Merge one translated locale into its pack without touching the other locales.

``merge_locale.py <slug> <locale> <document.json>`` -- the file holds one GuideDocument
(title, description, hero, blocks, sources). The document is validated, its structure compared
with zh-TW, and the pack rewritten with locales in the order zh-TW, en, ja, ko, zh-CN.
Run from ``apps/api`` with the API virtualenv.

Batch 4 adds three refusals to batch 3's: the summary sentence count and the FAQ question count
must match zh-TW (BRIEF.md "翻譯"), the hero and diagram must point at this locale's own files,
and a finance/crypto article's disclaimer callout must carry this locale's own marker rather
than a translation of the zh-TW sentence -- the one thing ``lint_document`` cannot catch,
because it is never told which locale it is reading.

Every way in is a ``REFUSED:`` line, never a traceback: a translator hands over a file that is
truncated or hand-edited, and a slug is mistyped or its pack is not written yet, often enough
that a stack trace here is a review note nobody can act on.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verticals import CONTENT, LOCALES, block_kind, locale_markers, suffix  # noqa: E402

from app.guides.pack_ingest import FINANCE_TOPICS  # noqa: E402
from app.guides.schemas import GuideDocument  # noqa: E402

ORDER = LOCALES


class Refused(ValueError):
    """One refusal, raised where a file is read and printed by ``main`` as its one line."""


def load_json(path: Path, what: str) -> dict:
    """The JSON in one file, or a ``Refused``. Batch 3 read both files with a bare
    ``json.loads(path.read_text())``, so a truncated translation and a slug whose pack is not
    written yet -- the mid-batch state, since the index article and the four translations are
    written over days -- ended in a JSONDecodeError or a FileNotFoundError instead."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise Refused(f"there is no {what} at {path}") from None
    except OSError as error:
        raise Refused(f"cannot read the {what} {path}: {error.strerror}") from None
    try:
        return json.loads(text)
    except ValueError as error:
        raise Refused(f"the {what} {path.name} is not valid JSON: {error}") from None


def counted(blocks: list[dict], type_name: str) -> list[int]:
    """How many items each ``summary``/``faq`` block carries, in order."""
    return [len(b["items"]) for b in blocks if b["type"] == type_name]


def sources_of(document: dict) -> list[dict]:
    """``GuideDocument.sources`` carries a ``default_factory`` (schemas.py), so a translation
    with no ``sources`` key validates cleanly -- and ``sources`` is the one array identical to
    zh-TW and therefore the easiest to leave out. Read with a default here so that omission is
    refused by the comparison below, the way a reordered one is, rather than by a KeyError."""
    return document.get("sources") or []


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[2] not in ORDER[1:]:
        print("usage: merge_locale.py <slug> <en|ja|ko|zh-CN> <document.json>")
        return 2
    slug, locale, source = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    path = CONTENT / f"{slug}.json"
    try:
        pack = load_json(path, f"pack for {slug}")
        document = load_json(source, "translation")
    except Refused as problem:
        print("REFUSED:", problem)
        return 1
    # A translation that does not load is refused the same way a misaligned one is: batch 4's
    # schema pins the summary at 2-5 sentences and the faq at 2-10 pairs, so a translator who
    # drops a FAQ pair lands here, and a stack trace is not a review note. Reported on its own
    # because the comparisons below read blocks and sources this document may not have.
    try:
        GuideDocument.model_validate(document)
    except ValueError as error:
        # Indented whole, the way check_article.py and update_index.py report the same model:
        # "1 validation error for GuideDocument" alone does not tell a translator which block.
        print("REFUSED:", str(error).replace("\n", "\n   "))
        return 1
    if "zh-TW" not in pack.get("locales", {}):
        # Everything below compares this document with the original. A pack without one is not
        # a translation this script can place.
        print(f"REFUSED: {path.name} has no zh-TW document to compare with")
        return 1
    zh = pack["locales"]["zh-TW"]
    before = hashlib.sha256(json.dumps(zh, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    problems = []
    # Compared by role, not by stored type: `pack_cli relink` rewrites a paragraph that gained
    # an article inline into a rich_paragraph, and it does that per locale, so zh-TW and this
    # document can hold different raw types for the same block and still correspond.
    if [block_kind(b) for b in document["blocks"]] != [block_kind(b) for b in zh["blocks"]]:
        problems.append("block types or order differ from zh-TW")
    else:
        # Only once the roles line up: pairing block 6 of a document that gained a paragraph
        # with block 6 of zh-TW compares a table with a heading, which is how batch 3's loop
        # died on `theirs["header"]` in the one case this script exists to refuse. Equal roles
        # make a table the peer of a table and a heading the peer of a heading.
        for mine, theirs in zip(document["blocks"], zh["blocks"]):
            if mine["type"] == "table" and (len(mine["header"]), len(mine["rows"])) != (len(theirs["header"]), len(theirs["rows"])):
                problems.append("table shape differs from zh-TW")
            if mine["type"] == "heading" and mine.get("level") != theirs.get("level"):
                problems.append("heading level differs from zh-TW")
    for block_type, what in (("summary", "summary sentences"), ("faq", "faq questions")):
        if counted(document["blocks"], block_type) != counted(zh["blocks"], block_type):
            problems.append(f"{what} differ from zh-TW")
    translated, original = sources_of(document), sources_of(zh)
    if [s.get("url") for s in translated] != [s.get("url") for s in original]:
        problems.append("source urls differ from zh-TW")
    if [s.get("checked_on") for s in translated] != [s.get("checked_on") for s in original]:
        problems.append("source checked_on differs from zh-TW")
    s = suffix(locale)
    hero = (document.get("hero") or {}).get("src")
    if hero != f"/guides/{slug}/hero{s}.jpg":
        problems.append(f"hero src is {hero}, want /guides/{slug}/hero{s}.jpg")
    for block in document["blocks"]:
        if block["type"] == "image" and block["src"] != f"/guides/{slug}/diagram-1{s}.svg":
            problems.append(f"diagram src is {block['src']}, want /guides/{slug}/diagram-1{s}.svg")
    if FINANCE_TOPICS.intersection(topic.casefold() for topic in pack.get("topics", [])):
        marker = locale_markers()[locale]
        callouts = [b for b in document["blocks"] if b["type"] == "callout"]
        if not any(marker.casefold() in b["text"].casefold() for b in callouts):
            problems.append(f"the disclaimer callout must contain this locale's own marker {marker!r}")
    if problems:
        print("REFUSED:", "; ".join(problems))
        return 1
    pack["locales"][locale] = document
    pack["locales"] = {name: pack["locales"][name] for name in ORDER if name in pack["locales"]}
    after = hashlib.sha256(json.dumps(pack["locales"]["zh-TW"], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    assert before == after
    path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("merged", slug, locale, "locales now", list(pack["locales"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
