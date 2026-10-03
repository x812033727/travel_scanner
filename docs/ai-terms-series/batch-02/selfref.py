"""Apply the reader-first self-reference fixes (本文/這篇 at most once per article).

Each entry is an exact substring and its replacement; the script refuses to run if a
substring is missing, so a later edit to the draft cannot be silently skipped.
"""

import json
import sys
from pathlib import Path

STAGING = Path("docs/ai-terms-series/batch-02/staging")

FIXES: dict[str, list[tuple[str, str]]] = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

for slug, pairs in FIXES.items():
    path = STAGING / slug / "pack.json"
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if text.count(old) != 1:
            sys.exit(f"{slug}: expected exactly one {old!r}, found {text.count(old)}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    left = sum(text.count(w) for w in ("本文", "這篇"))
    print(f"{slug}: 本文/這篇 left {left}")
