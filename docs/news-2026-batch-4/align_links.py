"""Make every closing link of the batch's three verticals carry its target's title in that locale.

usage: align_links.py [--apply] [--only=<part of a slug>,...]
A link's text is frozen into the pack, so a title that changed in fact-checking or a
translation that landed after the link was written leaves stale text behind. Handles both the
plain ``link`` block and the relinked ``rich_paragraph`` holding one ``article`` inline.
Without --apply it only prints what it would change. ``--only`` limits which packs are
rewritten -- for the days when other packs of the batch are still open in someone's editor --
while every pack's title is still read as a target.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "apps/api/app/guides/content"
APPLY = "--apply" in sys.argv
ONLY = [part for a in sys.argv[1:] if a.startswith("--only=") for part in a.split("=", 1)[1].split(",") if part]
# The three verticals of the batch; the AI index keeps its frozen slug, so it is matched by prefix too.
PACKS = sorted(p for prefix in ("crypto-news-", "tech-news-", "ai-news-") for p in CONTENT.glob(prefix + "*.json"))

titles = {}
for path in PACKS:
    pack = json.loads(path.read_text(encoding="utf-8"))
    titles[pack["slug"]] = {loc: doc.get("title") for loc, doc in pack["locales"].items()}


def target_of(url: str, locale: str):
    prefix = f"https://mokaair.com/{locale}/life/"
    return url[len(prefix):] if url.startswith(prefix) else None


changed = 0
for path in PACKS:
    pack = json.loads(path.read_text(encoding="utf-8"))
    if "_stub" in pack:
        continue
    if ONLY and not any(part in pack["slug"] for part in ONLY):
        continue
    dirty = False
    for locale, doc in pack["locales"].items():
        for block in doc.get("blocks", []):
            if block["type"] == "link":
                slug = target_of(block["url"], locale)
                holder, key = block, "text"
            elif block["type"] == "rich_paragraph" and len(block["inlines"]) == 1 and block["inlines"][0]["type"] == "article":
                slug = block["inlines"][0]["slug"]
                holder, key = block["inlines"][0], "text"
            else:
                continue
            if slug not in titles:
                continue
            want = titles[slug].get(locale)
            if want is None:
                print(f"MISSING {pack['slug']} {locale}: target {slug} has no {locale} title yet")
                continue
            if holder[key] != want:
                print(f"{pack['slug']} {locale}: '{holder[key][:40]}' -> '{want[:40]}'")
                holder[key] = want
                dirty = True
                changed += 1
    if dirty and APPLY:
        path.write_bytes((json.dumps(pack, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print("links to change:" if not APPLY else "links changed:", changed)
