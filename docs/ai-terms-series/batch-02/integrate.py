"""Link the batch-02 articles from ai-terms-index and ai-glossary-50-terms.

Reads each article's title from the ingested pack, so it runs after `pack_cli ingest`.
Idempotent: an article already linked from a section is not added twice.
Run from the repo root: python3 docs/ai-terms-series/batch-02/integrate.py
"""

import json
from pathlib import Path

CONTENT = Path("apps/api/app/guides/content")

INDEX_GROUPS = {
    "模型與 AI 基礎": (
        ["ai-term-neural-network", "ai-term-attention-mechanism", "ai-term-inference",
         "ai-term-scaling-laws", "ai-term-agi"],
        "神經網路與注意力機制說明模型怎麼計算，推論是每次回答都在做的那一段；"
        "縮放定律談規模與表現的經驗關係，AGI 則各家定義不同。",
    ),
    "提示、token 與上下文": (
        ["ai-term-temperature", "ai-term-knowledge-cutoff", "ai-term-structured-outputs"],
        "溫度影響回答的變化程度，知識截止日說明模型知道到哪裡，結構化輸出讓回答照固定欄位交出。",
    ),
    "代理、工具與互通協定": (
        ["ai-term-computer-use"],
        "電腦操作則讓代理看畫面、動滑鼠鍵盤，而不是呼叫定義好的工具。",
    ),
    "搜尋、文件與知識": (
        ["ai-term-grounding"],
        "接地把回答連回可查的來源，但有引用仍要逐句核對。",
    ),
    "訓練、調整與推論資源": (
        ["ai-term-chain-of-thought", "ai-term-synthetic-data"],
        "思維鏈談寫出的步驟能信多少，合成資料談用模型產生的資料再訓練模型。",
    ),
    "評測、安全與人工介入": (
        ["ai-term-ai-alignment", "ai-term-sycophancy"],
        "對齊是讓行為符合人的意圖，迎合是常見的失敗：順著使用者說，而不是照事實說。",
    ),
}

INDEX_ROW = ["AI 一直附和我，或同一題每次答得不同", "迎合、溫度、思維鏈"]
INDEX_DATE_SENTENCE = "2026 年 10 月起補進第二批 14 個詞。"

GLOSSARY_LINKS = {
    "模型與訓練：它是怎麼被做出來的": ["ai-term-temperature", "ai-term-knowledge-cutoff"],
    "推理與代理：它開始自己動手之後": ["ai-term-computer-use"],
}


def title_of(slug: str) -> str:
    pack = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))
    return pack["locales"]["zh-TW"]["title"]


def link_block(slug: str) -> dict:
    return {"type": "rich_paragraph",
            "inlines": [{"type": "article", "text": title_of(slug), "kind": "life", "slug": slug}]}


def linked(block: dict) -> set[str]:
    return {i["slug"] for i in block.get("inlines", []) if i.get("type") == "article"}


def sections(blocks: list[dict]) -> dict[str, tuple[int, int]]:
    """heading text -> (index of heading, index of next level-2 heading or end)."""
    heads = [(i, b["text"]) for i, b in enumerate(blocks)
             if b["type"] == "heading" and b.get("level") == 2]
    out = {}
    for n, (i, text) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(blocks)
        out[text] = (i, end)
    return out


def write(path: Path, pack: dict) -> None:
    path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def integrate_index() -> None:
    path = CONTENT / "ai-terms-index.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    blocks = pack["locales"]["zh-TW"]["blocks"]
    if INDEX_DATE_SENTENCE not in blocks[1]["text"]:
        blocks[1]["text"] += INDEX_DATE_SENTENCE
    for b in blocks:
        if b["type"] == "table" and INDEX_ROW not in b["rows"]:
            b["rows"].append(INDEX_ROW)
            break
    for heading, (slugs, sentence) in INDEX_GROUPS.items():
        start, end = sections(blocks)[heading]
        para = next(b for b in blocks[start:end] if b["type"] == "paragraph")
        if sentence not in para["text"]:
            para["text"] += sentence
        present = set().union(*(linked(b) for b in blocks[start:end]))
        last_link = max(i for i in range(start, end) if blocks[i]["type"] == "rich_paragraph")
        new = [link_block(s) for s in slugs if s not in present]
        blocks[last_link + 1:last_link + 1] = new
    write(path, pack)


def integrate_glossary() -> None:
    path = CONTENT / "ai-glossary-50-terms.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    blocks = pack["locales"]["zh-TW"]["blocks"]
    for heading, slugs in GLOSSARY_LINKS.items():
        start, end = sections(blocks)[heading]
        present = set().union(*(linked(b) for b in blocks[start:end]))
        last_link = max(i for i in range(start, end) if blocks[i]["type"] == "rich_paragraph")
        blocks[last_link + 1:last_link + 1] = [link_block(s) for s in slugs if s not in present]
    write(path, pack)


if __name__ == "__main__":
    integrate_index()
    integrate_glossary()
