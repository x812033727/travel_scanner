"""Shared-number cross-checks between sibling packs of one batch.

Articles that describe the same fare, tax or timetable must agree character for character, and
an article that must NOT carry a number (a cap that only applies to one village, a price that
belongs to another route) must not have it. The rules live with the batch, not here; ``<RULES>``
is the batch's ``shared-numbers.json``::

    <PY> shared_check.py --rules <RULES> --group okinawa --workdir <WORKDIR>
    <PY> shared_check.py --rules <RULES> --from-content [--content-dir DIR]

``shared-numbers.json``::

    {
      "okinawa": [
        {"pattern": "每人每晚上限 2,000 日圓",
         "must": ["okinawa-lodging-tax-2027"], "must_not": ["okinawa-without-a-car"]},
        {"pattern": "2027 年 2 月 1 日",
         "must": ["okinawa-lodging-tax-2027", "kerama-islands-ferry-from-naha"]}
      ]
    }

``pattern`` is a regular expression matched against the title, description and every block of the
chosen locale. ``--group`` limits the run to one group; without it every group runs. A pack is
read from ``<WORKDIR>/<slug>/pack.json`` unless ``--from-content``, which reads the ingested pack
from the repository's content directory. A pack that does not exist yet is reported as MISSING
and skipped, so the check can run while a batch is still being written. Exit 1 on any FAIL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONTENT_DIR = SKILL_ROOT / "apps" / "api" / "app" / "guides" / "content"


def text_of(pack: dict[str, Any], locale: str) -> str | None:
    doc = pack.get("locales", {}).get(locale)
    if doc is None:
        return None
    parts = [doc.get("title", ""), doc.get("description", "")]
    for block in doc.get("blocks", []):
        parts.append(json.dumps(block, ensure_ascii=False))
    return "\n".join(parts)


def load_rules(path: Path) -> dict[str, list[dict[str, Any]]]:
    rules = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rules, dict):
        raise SystemExit(f"{path}: expected an object of groups")
    for group, entries in rules.items():
        if not isinstance(entries, list):
            raise SystemExit(f"{path}: group {group!r} must be a list of rules")
        for entry in entries:
            if "pattern" not in entry:
                raise SystemExit(f"{path}: a rule in group {group!r} has no pattern")
    return rules


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--rules", type=Path, required=True, help="The batch's shared-numbers.json")
    parser.add_argument("--group", help="Only this group (default: every group)")
    parser.add_argument(
        "--workdir", type=Path, help="Batch working directory holding <slug>/pack.json"
    )
    parser.add_argument("--from-content", action="store_true", help="Read ingested packs instead")
    parser.add_argument("--content-dir", type=Path, default=DEFAULT_CONTENT_DIR)
    parser.add_argument("--locale", default="zh-TW")
    args = parser.parse_args()

    if not args.from_content and args.workdir is None:
        parser.error("--workdir is required unless --from-content")
    rules = load_rules(args.rules)
    groups = [args.group] if args.group else sorted(rules)
    unknown = [group for group in groups if group not in rules]
    if unknown:
        parser.error(f"unknown group(s): {', '.join(unknown)}; known: {', '.join(sorted(rules))}")

    bad = 0
    for group in groups:
        entries = rules[group]
        slugs = sorted({s for e in entries for s in e.get("must", []) + e.get("must_not", [])})
        texts: dict[str, str] = {}
        for slug in slugs:
            path = (
                args.content_dir / f"{slug}.json"
                if args.from_content
                else args.workdir / slug / "pack.json"
            )
            if not path.exists():
                print(f"MISSING {group}: {slug}")
                continue
            text = text_of(json.loads(path.read_text(encoding="utf-8")), args.locale)
            if text is None:
                print(f"MISSING {group}: {slug} has no {args.locale} locale")
                continue
            texts[slug] = text
        for entry in entries:
            pattern = entry["pattern"]
            rx = re.compile(pattern)
            for slug in entry.get("must", []):
                if slug in texts and not rx.search(texts[slug]):
                    print(f"FAIL {group}: {slug} should contain /{pattern}/")
                    bad += 1
            for slug in entry.get("must_not", []):
                if slug in texts and rx.search(texts[slug]):
                    hits = len(rx.findall(texts[slug]))
                    print(f"FAIL {group}: {slug} must not contain /{pattern}/ ({hits} hits)")
                    bad += 1
            hits = {slug: len(rx.findall(text)) for slug, text in texts.items() if rx.search(text)}
            print(f"info {group}: /{pattern}/ -> {hits}")
    print(f"RESULT {'FAIL' if bad else 'PASS'} ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
