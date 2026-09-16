"""Apply translation-review corrections: ``apply_corrections.py <corrections.json>...``.

Each file is a list of ``{"slug", "locale", "file": "pack"|"research", "old", "new", "reason"}``.
``old`` must occur exactly once inside that locale's document (pack) or that locale's
``translations`` entry (research); zh-TW is never edited here. Applied entries are appended to
``translation-corrections.json`` in this directory.

Run from ``apps/api`` with the API virtualenv: a corrected pack document is validated before it
is written, so a correction cannot push a summary sentence past 300 characters or a FAQ answer
past 1,000 and leave the pack unloadable. The research record of a slug is looked up in that
vertical's workspace, which the slug prefix decides.

A corrections file is written by hand by a reviewer, so its own shape is checked the same way
its entries are: a file that is not JSON, or is not a list, and an entry missing a key or
naming zh-TW, are each a ``SKIPPED`` line and a non-zero exit -- never a traceback that also
drops every entry after it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verticals import CONTENT, locale_markers, workspace_of  # noqa: E402

from app.guides.pack_ingest import FINANCE_TOPICS  # noqa: E402
from app.guides.schemas import GuideDocument  # noqa: E402

LOG = HERE / "translation-corrections.json"
# Keys whose value is machinery, not prose: replacing inside them turns a correction into a
# broken link or a mislabelled block. ``slug`` and ``kind`` are new in batch 4 -- after
# `pack_cli relink` the closing links are ``article`` inlines carrying both, and a correction
# to a title that happens to read like a slug would otherwise repoint the link.
KEEP = ("url", "src", "checked_on", "type", "level", "tone", "width", "height", "slug", "kind",
        "language", "partner", "event_date", "news_date")


def replace_in(node, old: str, new: str) -> tuple[object, int]:
    if isinstance(node, str):
        return node.replace(old, new), node.count(old)
    if isinstance(node, list):
        total = 0
        out = []
        for item in node:
            value, count = replace_in(item, old, new)
            out.append(value)
            total += count
        return out, total
    if isinstance(node, dict):
        total = 0
        out = {}
        for key, item in node.items():
            if key in KEEP:
                out[key] = item
                continue
            value, count = replace_in(item, old, new)
            out[key] = value
            total += count
        return out, total
    return node, 0


def refusal(document: dict, topics: list[str], locale: str) -> str | None:
    """Why this corrected document may not be written. The disclaimer check is here because a
    reviewer rewording the crypto callout is exactly how the marker gets paraphrased away, and
    an error at import is a worse place to find that out than a skipped correction."""
    try:
        GuideDocument.model_validate(document)
    except ValueError as error:
        # The first line of a pydantic error is only the count; the field and the reason are
        # the two under it, and a SKIPPED line that does not say which block is not a review
        # note. Joined, because this one has to stay on one line.
        return " ".join(part.strip() for part in str(error).splitlines()[:3])
    if FINANCE_TOPICS.intersection(topic.casefold() for topic in topics):
        marker = locale_markers()[locale]
        if not any(b["type"] == "callout" and marker.casefold() in b["text"].casefold()
                   for b in document["blocks"]):
            return f"the correction removes the disclaimer marker {marker!r}"
    return None


LOCALES_HERE = ("en", "ja", "ko", "zh-CN")


def entry_problem(entry: object) -> str | None:
    """Why this entry cannot be applied, before anything is read from disk -- or None.

    A reviewer hands in a hand-written list, so a missing key and a typo in ``locale`` are
    the ordinary mistakes. Both used to end the run: ``entry["old"]`` as a KeyError and the
    zh-TW guard as a bare ``assert``, which ``python -O`` removes altogether, leaving the
    original silently editable. Reported like every other refusal instead."""
    if not isinstance(entry, dict):
        return f"entry is a {type(entry).__name__}, not an object"
    missing = [key for key in ("slug", "locale", "old", "new") if not isinstance(entry.get(key), str)]
    if missing:
        return "entry has no " + ", ".join(missing)
    if entry["locale"] not in LOCALES_HERE:
        return f"{entry['locale']} is not a translated locale; zh-TW is never edited here"
    if entry.get("file", "pack") not in ("pack", "research"):
        return f"file is {entry['file']!r}, want 'pack' or 'research'"
    return None


def locate(slug: str, locale: str, is_pack: bool) -> tuple[Path, dict, dict] | str:
    """The file this correction edits and the document inside it -- or, as a string, why it
    cannot be edited. A pack that is not written yet and a locale ``merge_locale.py`` has not
    merged yet are both the ordinary mid-batch state: the four translations of an article are
    reviewed and merged one at a time, so a corrections file naturally names a locale that is
    not in the pack this morning. That is a skipped entry with a reason, the way a correction
    whose ``old`` no longer matches is, and not a traceback that drops every entry after it."""
    path = CONTENT / f"{slug}.json" if is_pack else workspace_of(slug) / "research" / f"{slug}.json"
    inner = "locales" if is_pack else "translations"
    if not path.is_file():
        return f"no {path.name} in {path.parent.name} yet"
    data = json.loads(path.read_text(encoding="utf-8"))
    if locale not in data.get(inner, {}):
        return f"{path.name} has no {locale} in {inner} yet"
    return path, data, data[inner][locale]


def main() -> int:
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else []
    failed = 0
    for name in sys.argv[1:]:
        try:
            entries = json.loads(Path(name).read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            print(f"SKIPPED ({error}): the corrections file {name}")
            failed += 1
            continue
        if not isinstance(entries, list):
            print(f"SKIPPED (a corrections file is a list of entries, not a "
                  f"{type(entries).__name__}): {name}")
            failed += 1
            continue
        for position, entry in enumerate(entries):
            problem = entry_problem(entry)
            if problem is not None:
                print(f"SKIPPED ({problem}): {Path(name).name} entry {position}")
                failed += 1
                continue
            slug, locale = entry["slug"], entry["locale"]
            is_pack = entry.get("file", "pack") == "pack"
            found = locate(slug, locale, is_pack)
            if isinstance(found, str):
                print(f"SKIPPED ({found}): {slug} {locale} {entry['old'][:50]!r}")
                failed += 1
                continue
            path, data, target = found
            value, count = replace_in(target, entry["old"], entry["new"])
            if count != 1:
                print(f"SKIPPED ({count} matches): {slug} {locale} {entry['old'][:50]!r}")
                failed += 1
                continue
            if is_pack:
                problem = refusal(value, data.get("topics", []), locale)
                if problem is not None:
                    print(f"SKIPPED ({problem}): {slug} {locale} {entry['old'][:50]!r}")
                    failed += 1
                    continue
                data["locales"][locale] = value
            else:
                data["translations"][locale] = value
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            log.append(entry)
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"applied {len(log)} corrections in total; {failed} skipped")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
