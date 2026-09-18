"""sync_captions.py <prefix> [slug...] [--apply] -- make research diagram captions equal the pack's image caption (pack wins).

Named slugs limit the run (the AI prefix also matches batch 3's articles, whose records are elsewhere)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "docs/news-2026-batch-4"))
from verticals import workspace_of
prefix, apply = sys.argv[1], "--apply" in sys.argv
only = {a for a in sys.argv[2:] if not a.startswith("--")}
for path in sorted((ROOT / "apps/api/app/guides/content").glob(prefix + "*.json")):
    if only and path.stem not in only:
        continue
    pack = json.loads(path.read_text(encoding="utf-8"))
    rpath = workspace_of(pack["slug"]) / "research" / path.name
    rec = json.loads(rpath.read_text(encoding="utf-8"))
    dirty = False
    for locale, doc in pack["locales"].items():
        caption = next(b["caption"] for b in doc["blocks"] if b["type"] == "image")
        holder = rec if locale == "zh-TW" else rec.get("translations", {}).get(locale, {})
        diagram = holder.get("diagram")
        if diagram and diagram.get("caption") != caption:
            print(pack["slug"], locale, "|", diagram.get("caption", "")[:50], "->", caption[:50])
            diagram["caption"] = caption
            dirty = True
    if dirty and apply:
        rpath.write_bytes((json.dumps(rec, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
