"""Merge one translated locale into its pack without touching the other locales.

``merge_locale.py <slug> <locale> <document.json>`` -- the file holds one GuideDocument
(title, description, hero, blocks, sources). The document is validated, its block structure
compared with zh-TW, and the pack rewritten with locales in the order zh-TW, en, ja, ko, zh-CN.
Run from ``apps/api`` with the API virtualenv.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "apps/api"))

from app.guides.schemas import GuideDocument  # noqa: E402

CONTENT = ROOT / "apps/api/app/guides/content"
ORDER = ["zh-TW", "en", "ja", "ko", "zh-CN"]


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[2] not in ORDER[1:]:
        print("usage: merge_locale.py <slug> <en|ja|ko|zh-CN> <document.json>")
        return 2
    slug, locale, source = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    path = CONTENT / f"{slug}.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    document = json.loads(source.read_text(encoding="utf-8"))
    GuideDocument.model_validate(document)
    zh = pack["locales"]["zh-TW"]
    before = hashlib.sha256(json.dumps(zh, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    problems = []
    if [b["type"] for b in document["blocks"]] != [b["type"] for b in zh["blocks"]]:
        problems.append("block types or order differ from zh-TW")
    for mine, theirs in zip(document["blocks"], zh["blocks"]):
        if mine["type"] == "table" and (len(mine["header"]), len(mine["rows"])) != (len(theirs["header"]), len(theirs["rows"])):
            problems.append("table shape differs from zh-TW")
        if mine["type"] == "heading" and mine.get("level") != theirs.get("level"):
            problems.append("heading level differs from zh-TW")
    if [s["url"] for s in document["sources"]] != [s["url"] for s in zh["sources"]]:
        problems.append("source urls differ from zh-TW")
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
