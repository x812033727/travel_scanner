"""space_cjk.py <slug>... [--apply] -- house style: a space between CJK and Latin letters/digits in zh-TW.

Text inside 「…」 and 『…』 is left exactly as it is (verbatim quotes and official names). The same
transformation is applied to the research record's title, hero_label and diagram so that the caption
stays identical to the pack's. Without --apply it only reports. Run from apps/api with the API venv.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
sys.path.insert(0, str(ROOT / "docs/news-2026-batch-4"))
from app.guides.schemas import GuideDocument  # noqa: E402
from verticals import workspace_of  # noqa: E402

CONTENT = ROOT / "apps/api/app/guides/content"
KEEP = ("url", "src", "checked_on", "type", "level", "tone", "width", "height", "slug", "kind",
        "language", "partner", "event_date", "news_date")
CJK = r"\u3400-\u4dbf\u4e00-\u9fff"
RULES = [
    (re.compile(rf"([{CJK}])([A-Za-z0-9])"), r"\1 \2"),
    (re.compile(rf"([A-Za-z0-9%])([{CJK}])"), r"\1 \2"),
]
QUOTED = re.compile(r"(「[^」]*」|『[^』]*』)")


def fix(text: str) -> str:
    parts = QUOTED.split(text)
    for i in range(0, len(parts), 2):  # even parts are outside quotes
        for pattern, repl in RULES:
            parts[i] = pattern.sub(repl, parts[i])
    out = "".join(parts)
    # the boundary between an unquoted part and a quote mark needs no space: 「 and 」 are full-width
    return out


def walk(node):
    if isinstance(node, str):
        return fix(node)
    if isinstance(node, list):
        return [walk(item) for item in node]
    if isinstance(node, dict):
        return {key: (item if key in KEEP else walk(item)) for key, item in node.items()}
    return node


apply = "--apply" in sys.argv
LOCALE = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--locale=")), "zh-TW")
for slug in [a for a in sys.argv[1:] if not a.startswith("--")]:
    path = CONTENT / f"{slug}.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    if LOCALE not in pack["locales"]:
        print(slug, "has no", LOCALE)
        continue
    before = pack["locales"][LOCALE]
    after = walk(before)
    GuideDocument.model_validate(after)
    count = lambda doc: sum(len(b["text"]) for b in doc["blocks"] if b["type"] == "paragraph")  # noqa: E731
    nospace = lambda doc: sum(len(b["text"].replace(" ", "")) for b in doc["blocks"] if b["type"] == "paragraph")  # noqa: E731
    changed = json.dumps(before, ensure_ascii=False) != json.dumps(after, ensure_ascii=False)
    print("CHANGED" if changed else "same   ", slug, "paragraph chars", count(before), "->", count(after), "| without spaces", nospace(after),
          "| title:", after["title"])
    record_path = ROOT / workspace_of(slug) / "research" / f"{slug}.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    holder = record if LOCALE == "zh-TW" else record.get("translations", {}).get(LOCALE, {})
    for key in (("title", "hero_label", "diagram") if LOCALE == "zh-TW" else ("hero_label", "diagram")):
        if key in holder:
            holder[key] = walk(holder[key])
    if apply:
        pack["locales"][LOCALE] = after
        path.write_bytes((json.dumps(pack, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        record_path.write_bytes((json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
