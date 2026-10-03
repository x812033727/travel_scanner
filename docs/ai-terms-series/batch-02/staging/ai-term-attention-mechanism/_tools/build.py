import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ai-term-attention-mechanism"
DAY = "2026-10-03"


def P(text):
    return {"type": "paragraph", "text": text}


def RP(*parts):
    inlines = []
    for part in parts:
        if isinstance(part, str):
            inlines.append({"type": "text", "text": part})
        else:
            text, slug = part
            inlines.append({"type": "article", "text": text, "kind": "life", "slug": slug})
    return {"type": "rich_paragraph", "inlines": inlines}


def H2(text):
    return {"type": "heading", "level": 2, "text": text}


def L(items, ordered=False):
    return {"type": "list", "items": items, "ordered": ordered}


blocks = []

# ---- intro -------------------------------------------------------------
blocks += [
    P("注意力機制（Attention）是一種計算：處理序列中的某個位置時，替其他每個位置打相關分數，轉成總和為 1 的權重，再把各位置的內容加權平均成新的表示。「注意力」是譯名，指數學上的加權，不是人類有意識的專注。它讓相隔很遠的兩個詞在同一層就能直接比對，代價是標準做法的計算量大約隨序列長度的平方成長。"),
    P("本文從翻譯對齊問題講到 Q、K、V、自注意力與多頭注意力，並說明權重為何不能直接讀成「模型的理由」，以及長度與成本的關係。查證日為 2026 年 10 月 3 日；標「示例」的內容是教學編的，未實測。"),
]

# ---- SECTIONS-GO-HERE ---------------------------------------------------
exec(Path(__file__).with_name("sections.py").read_text(encoding="utf-8")) if Path(__file__).with_name("sections.py").exists() else None

meta = json.loads(Path(__file__).with_name("meta.json").read_text(encoding="utf-8"))

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
            "title": meta["title"],
            "description": meta["description"],
            "hero": {
                "src": f"/guides/{SLUG}/hero.jpg",
                "alt": meta["hero_alt"],
                "width": 1600,
                "height": 900,
            },
            "blocks": blocks,
            "sources": [dict(s, checked_on=DAY) for s in meta["sources"]],
        }
    },
}
(ROOT / "pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---- counting (same as pack_ingest._body_length) -------------------------
def parts(blocks):
    out = []
    for b in blocks:
        t = b["type"]
        if t == "paragraph":
            out.append(b["text"])
        elif t == "rich_paragraph":
            out.append("".join(n["text"] for n in b["inlines"]))
        elif t == "list":
            out.extend(b["items"])
        elif t == "table":
            out.extend(b["header"])
            for r in b["rows"]:
                out.extend(r)
        elif t == "callout":
            out.extend((b["title"], b["text"]))
    return out


def ln(s):
    return len(re.sub(r"\s+", "", s))


total = sum(ln(p) for p in parts(blocks))
links = sum(
    ln(n["text"])
    for b in blocks
    if b["type"] == "rich_paragraph"
    for n in b["inlines"]
    if n["type"] == "article"
)
print("title", ln(meta["title"]), "description", ln(meta["description"]))
print("_body_length", total, "excluding link text", total - links)
