"""Self-check for one article of this batch: ``check_article.py <slug> [--full] [--assets]``.

Run from ``apps/api`` with the API virtualenv. Without ``--full`` only the zh-TW original and
its research record are checked; ``--full`` adds the four translations, ``--assets`` the
published images. Prints OK or the list of failures; writes nothing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "apps/api"))

from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import _document_text, errors, lint_document  # noqa: E402

CONTENT = ROOT / "apps/api/app/guides/content"
PUBLIC = ROOT / "apps/web/public"
CHECKED = "2026-09-15"
LOCALES = ["zh-TW", "en", "ja", "ko", "zh-CN"]
INDEX = "ai-news-2026-january-september-index"
RELATED = {
    "ai-news-gpt-live-voice-20260708": "ai-news-gemini-live-20260826",
    "ai-news-google-assistant-gemini-20260904": "ai-news-gemini-spark-20260519",
    "ai-news-anthropic-threat-report-20260910": "ai-news-project-glasswing-20260407",
    "ai-news-openai-agents-api-20260910": "ai-news-gpt-6-astra-20260903",
    "ai-news-deepseek-v41-flash-20260910": "ai-news-qwen-35-20260216",
    "ai-news-pace-the-frontier-20260912": "ai-news-claude-fable-51-20260901",
    "ai-news-siri-ai-ios-27-20260914": "ai-news-gemini-personal-intelligence-20260114",
}
ORDER = {slug: 142 + i for i, slug in enumerate(RELATED)}
SIMPLIFIED = re.compile("[价单适发应实来体结条轮对构补现这们说时让为么过还开关语问题网页务处设备]")
TOPICS = {"ai", "daily", "finance", "gadgets", "misc", "productivity", "software", "tutorial"}


def suffix(locale: str) -> str:
    return "" if locale == "zh-TW" else "-" + locale.lower()


def paragraphs(doc) -> str:
    return "".join(b.text for b in doc.blocks if b.type == "paragraph")


def cjk_units(text: str) -> float:
    return sum(1 if ord(c) > 255 else 0.55 for c in text)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    full, assets = "--full" in sys.argv, "--assets" in sys.argv
    if len(args) != 1 or args[0] not in RELATED:
        print("usage: check_article.py <slug> [--full] [--assets]; slug one of", *RELATED)
        return 2
    slug = args[0]
    fails: list[str] = []

    def need(ok: bool, message: str) -> None:
        if not ok:
            fails.append(message)

    raw = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))
    pack = ArticlePack.model_validate(raw)
    research = json.loads((HERE / "research" / f"{slug}.json").read_text(encoding="utf-8"))
    event = slug[-8:]
    event_date = f"{event[:4]}-{event[4:6]}-{event[6:]}"

    need(pack.slug == slug and pack.kind == "life" and pack.destination_id is None, "slug/kind/destination")
    need(pack.topics[:1] == ["ai"] and set(pack.topics) <= TOPICS, f"topics {pack.topics}")
    need(pack.display_order == ORDER[slug], f"display_order should be {ORDER[slug]}")
    wanted = LOCALES if full else ["zh-TW"]
    need(list(raw["locales"]) == wanted, f"locales {list(raw['locales'])} != {wanted}")

    zh = pack.locales["zh-TW"]
    text = paragraphs(zh)
    need(1800 <= len(text) <= 3000, f"zh-TW paragraph characters {len(text)} not in 1800–3000")
    need(len(zh.title) <= 60, f"title {len(zh.title)} > 60")
    need(100 <= len(zh.description) <= 220, f"description length {len(zh.description)}")
    found = SIMPLIFIED.findall(_document_text(zh))
    need(not found, f"simplified characters in zh-TW: {''.join(sorted(set(found)))}")
    first_two = " ".join(b.text for b in zh.blocks[:2] if b.type == "paragraph")
    y, m, d = (int(v) for v in event_date.split("-"))
    need(f"{y} 年 {m} 月 {d} 日" in first_two or event_date in first_two, "event date not in the opening paragraphs")
    need("2026 年 9 月 15 日" in first_two or CHECKED in first_two, "checked date not in the opening paragraphs")
    need(research["event_date"] == event_date and research["slug"] == slug, "research slug/event_date")
    need(research.get("title") == zh.title, "research title differs from zh-TW title")

    for problem in errors(lint_document(zh, "life")):
        fails.append(f"lint zh-TW: {problem}")

    types = [b.type for b in zh.blocks]
    headings = [i for i, b in enumerate(zh.blocks) if b.type == "heading" and b.level == 2]
    need(len(headings) == 5, f"{len(headings)} level-2 headings, want 5")
    need(types.count("table") == 1 and types.count("image") == 1 and types.count("callout") == 1, "one table, one image, one callout")
    need(types[-3:] == ["callout", "link", "link"], "blocks must end callout, link, link")
    need(types[:2] == ["paragraph", "paragraph"], "two opening paragraphs")
    if len(headings) == 5 and "table" in types and "image" in types:
        need(headings[1] < types.index("table") < headings[2], "table belongs at the end of section 2")
        need(headings[2] < types.index("image") < headings[3], "diagram belongs at the end of section 3")

    for locale in wanted:
        doc = pack.locales[locale]
        s = suffix(locale)
        need(doc.hero is not None and doc.hero.src == f"/guides/{slug}/hero{s}.jpg", f"{locale} hero src")
        need(doc.hero is not None and (doc.hero.width, doc.hero.height) == (1600, 900), f"{locale} hero size")
        images = [b for b in doc.blocks if b.type == "image"]
        need(len(images) == 1 and images[0].src == f"/guides/{slug}/diagram-1{s}.svg", f"{locale} diagram src")
        need(all(str(src.checked_on) == CHECKED for src in doc.sources), f"{locale} sources checked_on")
        need(2 <= len(doc.sources) <= 4, f"{locale} {len(doc.sources)} sources, want 2–4")
        for table in (b for b in doc.blocks if b.type == "table"):
            need(len(table.header) <= 4, f"{locale} table has {len(table.header)} columns (max 4)")
            need(all(len(row) == len(table.header) for row in table.rows), f"{locale} table row width")
            need(3 <= len(table.rows) <= 6, f"{locale} table rows {len(table.rows)}")
        links = [b for b in doc.blocks if b.type == "link"]
        targets = [INDEX, RELATED[slug]]
        for link, target in zip(links, targets):
            need(link.url == f"https://mokaair.com/{locale}/life/{target}", f"{locale} link url {link.url}")
            other = json.loads((CONTENT / f"{target}.json").read_text(encoding="utf-8"))["locales"].get(locale)
            need(other is not None and link.text == other["title"], f"{locale} link text must be the title of {target}")
        if locale != "zh-TW":
            need([b.type for b in doc.blocks] == types, f"{locale} block types differ from zh-TW")
            need([src.url for src in doc.sources] == [src.url for src in zh.sources], f"{locale} source urls differ")
            for a, b in zip(doc.blocks, zh.blocks):
                if a.type == "table":
                    need((len(a.header), len(a.rows)) == (len(b.header), len(b.rows)), f"{locale} table shape")
                if a.type == "heading":
                    need(a.level == b.level, f"{locale} heading level")
            need(len(paragraphs(doc)) >= 0.45 * len(text) if locale != "en" else True, f"{locale} translation looks short")
            for problem in errors(lint_document(doc, "life")):
                fails.append(f"lint {locale}: {problem}")

    diagram = research.get("diagram") or {}
    nodes = diagram.get("nodes") or []
    need(len(nodes) == 4 and all(len(n) == 2 for n in nodes), "research diagram needs 4 [heading, detail] nodes")
    need(cjk_units(research.get("hero_label", "")) <= 13, "hero_label too long")
    need(cjk_units(diagram.get("title", "")) <= 21, "diagram title too long")
    for heading, detail in nodes:
        need(cjk_units(heading) <= 9, f"node heading too long: {heading}")
        need(cjk_units(detail) <= 15, f"node detail too long: {detail}")
    image = next((b for b in zh.blocks if b.type == "image"), None)
    need(image is not None and diagram.get("caption") == image.caption, "research diagram caption differs from pack")
    need([s["url"] for s in research.get("sources", [])] == [s.url for s in zh.sources], "research sources differ from pack")
    need(bool(research.get("verified_facts")), "research verified_facts empty")
    body = re.sub(r"[,，]", "", _document_text(zh))
    drawn = " ".join([diagram.get("title", ""), research.get("hero_label", "")] + [" ".join(n) for n in nodes])
    for number in re.findall(r"\d+(?:[.:]\d+)*", drawn):
        need(number in body, f"number {number} on the artwork is not in the zh-TW text")
    if full:
        for locale in LOCALES[1:]:
            tr = research.get("translations", {}).get(locale, {})
            tnodes = tr.get("diagram", {}).get("nodes") or []
            need(bool(tr.get("hero_label")) and len(tnodes) == 4, f"research translations.{locale} incomplete")
            limit = 1.9 if locale == "en" else 1.25
            need(cjk_units(tr.get("hero_label", "")) <= 13 * limit, f"{locale} hero_label too long")
            for heading, detail in tnodes:
                need(cjk_units(heading) <= 9 * limit + 2, f"{locale} node heading too long: {heading}")
                need(cjk_units(detail) <= 15 * limit + 3, f"{locale} node detail too long: {detail}")
            timage = next((b for b in pack.locales[locale].blocks if b.type == "image"), None)
            need(timage is not None and tr.get("diagram", {}).get("caption") == timage.caption, f"{locale} diagram caption differs")

    if assets:
        for locale in LOCALES:
            s = suffix(locale)
            for name in (f"hero{s}.jpg", f"hero{s}.svg", f"diagram-1{s}.svg"):
                path = PUBLIC / "guides" / slug / name
                need(path.is_file(), f"missing {path.relative_to(ROOT)}")
                need(not path.is_file() or path.stat().st_size <= 300_000, f"{name} over 300 KB")

    if fails:
        print("FAIL")
        for message in fails:
            print(" -", message)
        return 1
    print("OK", slug, f"zh-TW paragraphs {len(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
