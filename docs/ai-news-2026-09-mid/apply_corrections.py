"""Apply translation-review corrections: ``apply_corrections.py <corrections.json>...``.

Each file is a list of ``{"slug", "locale", "file": "pack"|"research", "old", "new", "reason"}``.
``old`` must occur exactly once inside that locale's document (pack) or that locale's
``translations`` entry (research); zh-TW is never edited here. Applied entries are appended to
``translation-corrections.json`` in this directory.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTENT = ROOT / "apps/api/app/guides/content"
LOG = HERE / "translation-corrections.json"


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
            if key in ("url", "src", "checked_on", "type", "level", "tone", "width", "height"):
                out[key] = item
                continue
            value, count = replace_in(item, old, new)
            out[key] = value
            total += count
        return out, total
    return node, 0


def main() -> int:
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else []
    failed = 0
    for name in sys.argv[1:]:
        for entry in json.loads(Path(name).read_text(encoding="utf-8")):
            slug, locale = entry["slug"], entry["locale"]
            assert locale in ("en", "ja", "ko", "zh-CN"), entry
            if entry.get("file", "pack") == "pack":
                path = CONTENT / f"{slug}.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                target = data["locales"][locale]
            else:
                path = HERE / "research" / f"{slug}.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                target = data["translations"][locale]
            value, count = replace_in(target, entry["old"], entry["new"])
            if count != 1:
                print(f"SKIPPED ({count} matches): {slug} {locale} {entry['old'][:50]!r}")
                failed += 1
                continue
            if entry.get("file", "pack") == "pack":
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
