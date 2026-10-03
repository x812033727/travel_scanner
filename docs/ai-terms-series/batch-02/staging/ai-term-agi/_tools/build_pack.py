# helper: builds pack.json from the content below (deleted before delivery)
import json, re, sys
from pathlib import Path

SLUG = "ai-term-agi"
OUT = Path(__file__).resolve().parent.parent / "pack.json"
CHECKED = "2026-10-03"


def P(text):
    return {"type": "paragraph", "text": text}


def H(text):
    return {"type": "heading", "level": 2, "text": text}


def T(text):
    return {"type": "text", "text": text}


def A(text, slug):
    return {"type": "article", "text": text, "kind": "life", "slug": slug}


def RP(*inlines):
    return {"type": "rich_paragraph", "inlines": list(inlines)}


def body_parts(blocks):
    parts = []
    for b in blocks:
        t = b["type"]
        if t == "paragraph":
            parts.append(b["text"])
        elif t == "rich_paragraph":
            parts.append("".join(n["text"] for n in b["inlines"]))
        elif t == "list":
            parts.extend(b["items"])
        elif t == "table":
            parts.extend(b["header"])
            for r in b["rows"]:
                parts.extend(r)
        elif t == "callout":
            parts.extend((b["title"], b["text"]))
    return parts


def body_len(blocks):
    return sum(len(re.sub(r"\s+", "", p)) for p in body_parts(blocks))


def body_len_no_links(blocks):
    n = 0
    for b in blocks:
        if b["type"] == "rich_paragraph":
            n += sum(len(re.sub(r"\s+", "", x["text"])) for x in b["inlines"] if x["type"] != "article")
        elif b["type"] in ("paragraph", "list", "table", "callout"):
            n += body_len([b])
    return n


blocks = []
exec(Path(__file__).with_name("content.py").read_text(encoding="utf-8"))

TITLE = "通用人工智慧（AGI）是什麼：各家定義為什麼不一樣"
DESCRIPTION = Path(__file__).with_name("description.txt").read_text(encoding="utf-8").strip()

SOURCES = [
    ("OpenAI：OpenAI Charter（官方章程頁）", "https://openai.com/charter/"),
    ("OpenAI：Planning for AGI and beyond（官方文章）", "https://openai.com/index/planning-for-agi-and-beyond/"),
    ("Morris 等：Levels of AGI for Operationalizing Progress on the Path to AGI（arXiv:2311.02462，ICML 2024）", "https://arxiv.org/abs/2311.02462"),
    ("Legg、Hutter：Universal Intelligence: A Definition of Machine Intelligence（arXiv:0712.3329）", "https://arxiv.org/abs/0712.3329"),
    ("Chollet：On the Measure of Intelligence（arXiv:1911.01547）", "https://arxiv.org/abs/1911.01547"),
    ("ARC Prize：What is ARC-AGI?（官方說明頁）", "https://arcprize.org/arc-agi"),
    ("Shah 等：An Approach to Technical AGI Safety and Security（arXiv:2504.01849）", "https://arxiv.org/abs/2504.01849"),
    ("Microsoft：The next chapter of the Microsoft–OpenAI partnership（官方部落格公告）", "https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/"),
    ("OpenAI：The next chapter of the Microsoft–OpenAI partnership（官方公告）", "https://openai.com/index/next-chapter-of-microsoft-openai-partnership/"),
]

pack = {
    "slug": SLUG,
    "kind": "life",
    "destination_id": None,
    "topics": ["ai", "tutorial"],
    "valid_until": None,
    "featured": False,
    "display_order": 100,
    "locales": {
        "zh-TW": {
            "title": TITLE,
            "description": DESCRIPTION,
            "hero": {
                "src": f"/guides/{SLUG}/hero.jpg",
                "alt": "三種形狀不同的量尺，各自指向同一個虛線圈起的目標",
                "width": 1600,
                "height": 900,
            },
            "blocks": blocks,
            "sources": [{"title": t, "url": u, "checked_on": CHECKED} for t, u in SOURCES],
        }
    },
}
OUT.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("title chars", len(TITLE), "description chars", len(DESCRIPTION))
print("body chars (tool algorithm):", body_len(blocks))
print("body chars (excluding article-inline text):", body_len_no_links(blocks))
for b in blocks:
    if b["type"] in ("paragraph", "rich_paragraph", "list", "table", "callout"):
        print(f'  {b["type"][:6]:6} {body_len([b]):4}')
    elif b["type"] == "heading":
        print("  H2", b["text"])
