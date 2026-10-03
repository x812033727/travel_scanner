"""Link the AI-term batches from ai-terms-index and ai-glossary-50-terms.

Reads each batch's catalogue for where a term goes and the ingested pack for its title,
so it runs after `pack_cli ingest`. A term whose pack is not ingested yet is skipped.
Idempotent: a link, sentence or table row already present is not added twice.

The index labels every entry with the head of its title -- 「檢索增強生成（RAG）」, not the
whole 「檢索增強生成（RAG）是什麼：讓回答附上可查的依據」 -- because the definition card
the page shows on a term link already carries the full title and description, and the
full titles made the index alone run past the 6,000-character guideline for life pages.

Run from the repo root: python3 docs/ai-terms-series/integrate.py
"""

import json
import re
from pathlib import Path

CONTENT = Path("apps/api/app/guides/content")
SERIES = Path("docs/ai-terms-series")
BATCHES = ("batch-02", "batch-03")

GROUP_HEADINGS = {
    "foundation": "模型與 AI 基礎",
    "context": "提示、token 與上下文",
    "agents": "代理、工具與互通協定",
    "engineering": "AI 工程方法與維運",
    "retrieval": "搜尋、文件與知識",
    "training": "訓練、調整與推論資源",
    "evaluation": "評測、安全與人工介入",
    "multimodal": "影像、語音、開放模型與來源",
}

# One sentence per batch and group, appended to the group's lead paragraph once every
# term the sentence names is ingested.
GROUP_SENTENCES: dict[str, list[tuple[tuple[str, ...], str]]] = {
    "模型與 AI 基礎": [
        (("ai-term-neural-network", "ai-term-attention-mechanism", "ai-term-inference",
          "ai-term-scaling-laws", "ai-term-agi"),
         "神經網路與注意力機制說明模型怎麼計算，推論是每次回答都在做的那一段；"
         "縮放定律談規模與表現的經驗關係，AGI 則各家定義不同。"),
        (("ai-term-overfitting", "ai-term-world-model"),
         "過擬合說明模型為什麼在沒看過的資料上失準，世界模型則是一個各家用法不同的詞。"),
    ],
    "提示、token 與上下文": [
        (("ai-term-temperature", "ai-term-knowledge-cutoff", "ai-term-structured-outputs"),
         "溫度影響回答的變化程度，知識截止日說明模型知道到哪裡，結構化輸出讓回答照固定欄位交出。"),
    ],
    "代理、工具與互通協定": [
        (("ai-term-computer-use",),
         "電腦操作則讓代理看畫面、動滑鼠鍵盤，而不是呼叫定義好的工具。"),
    ],
    "搜尋、文件與知識": [
        (("ai-term-grounding",),
         "接地把回答連回可查的來源，但有引用仍要逐句核對。"),
    ],
    "訓練、調整與推論資源": [
        (("ai-term-chain-of-thought", "ai-term-synthetic-data"),
         "思維鏈談寫出的步驟能信多少，合成資料談用模型產生的資料再訓練模型。"),
        (("ai-term-reinforcement-learning", "ai-term-kv-cache", "ai-term-local-inference",
          "ai-term-rate-limit"),
         "強化學習是用獎勵訓練的方法；KV 快取、本機推論與速率限制則談回答時的記憶體、裝置與用量上限。"),
    ],
    "評測、安全與人工介入": [
        (("ai-term-ai-alignment", "ai-term-sycophancy"),
         "對齊是讓行為符合人的意圖，迎合是常見的失敗：順著使用者說，而不是照事實說。"),
        (("ai-term-interpretability", "ai-term-data-poisoning", "ai-term-reward-hacking"),
         "可解釋性想看懂模型為什麼這樣答；資料投毒與獎勵駭客則是訓練資料與評分被鑽漏洞的兩種風險。"),
    ],
    "影像、語音、開放模型與來源": [
        (("ai-term-vision-language-model",),
         "視覺語言模型讀圖後用文字回答，方向和文字生圖相反。"),
    ],
}

INDEX_ROWS = [
    (("ai-term-sycophancy", "ai-term-temperature", "ai-term-chain-of-thought"),
     ["AI 一直附和我，或同一題每次答得不同", "迎合、溫度、思維鏈"]),
    (("ai-term-local-inference", "ai-term-kv-cache", "ai-term-rate-limit"),
     ["想在自己電腦跑模型，或 API 一直回 429", "本機推論、KV 快取、速率限制"]),
]
DATE_ANCHOR = "首輪資料整理截止日"
INDEX_DATE_SENTENCES = [
    ("batch-02", "2026 年 10 月起補進第二批 14 個詞。"),
    ("batch-03", "同月再補第三批 10 個詞。"),
]

GLOSSARY_LINKS = {
    "模型與訓練：它是怎麼被做出來的": ["ai-term-temperature", "ai-term-knowledge-cutoff"],
    "推理與代理：它開始自己動手之後": ["ai-term-computer-use"],
    "基礎設施與費用：帳單和硬體上的字": ["ai-term-rate-limit", "ai-term-local-inference"],
}

LABEL_CUT = re.compile(r"是什麼|：|？")


def ingested(slug: str) -> bool:
    return (CONTENT / f"{slug}.json").is_file()


def title_of(slug: str) -> str:
    pack = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))
    return pack["locales"]["zh-TW"]["title"]


def short_label(title: str) -> str:
    """The term a title is about: everything before 「是什麼」, 「：」 or 「？」."""
    return LABEL_CUT.split(title, maxsplit=1)[0].strip()


def link_block(slug: str, text: str) -> dict:
    return {"type": "rich_paragraph",
            "inlines": [{"type": "article", "text": text, "kind": "life", "slug": slug}]}


def single_link(block: dict) -> str | None:
    """The slug of a paragraph that is one article link and nothing else."""
    inlines = block.get("inlines", []) if block.get("type") == "rich_paragraph" else []
    if len(inlines) == 1 and inlines[0].get("type") == "article":
        return inlines[0]["slug"]
    return None


def linked(blocks: list[dict]) -> set[str]:
    return {i["slug"] for b in blocks for i in b.get("inlines", []) if i.get("type") == "article"}


def sections(blocks: list[dict]) -> dict[str, tuple[int, int]]:
    """heading text -> (index of heading, index of next level-2 heading or end)."""
    heads = [(i, b["text"]) for i, b in enumerate(blocks)
             if b["type"] == "heading" and b.get("level") == 2]
    out = {}
    for n, (i, text) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(blocks)
        out[text] = (i, end)
    return out


def catalogue_terms() -> list[dict]:
    terms = []
    for batch in BATCHES:
        path = SERIES / batch / "catalogue.json"
        if path.is_file():
            terms.extend(json.loads(path.read_text(encoding="utf-8"))["terms"])
    return terms


def write(path: Path, pack: dict) -> None:
    path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def integrate_index() -> None:
    path = CONTENT / "ai-terms-index.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    blocks = pack["locales"]["zh-TW"]["blocks"]

    # The paragraph that dates the series; found by its words, not its position, because a
    # summary block now sits in front of it and anything else could be added later.
    paragraphs = [b for b in blocks if b["type"] == "paragraph"]
    dated = next(b for b in paragraphs if DATE_ANCHOR in b["text"])
    for batch, sentence in INDEX_DATE_SENTENCES:
        catalogue = SERIES / batch / "catalogue.json"
        if not catalogue.is_file() or any(sentence in b["text"] for b in paragraphs):
            continue
        terms = json.loads(catalogue.read_text(encoding="utf-8"))["terms"]
        if all(ingested(t["slug"]) for t in terms):
            dated["text"] += sentence
    table = next(b for b in blocks if b["type"] == "table")
    for needs, row in INDEX_ROWS:
        if all(ingested(s) for s in needs) and row not in table["rows"]:
            table["rows"].append(row)

    for term in catalogue_terms():
        slug = term["slug"]
        if not ingested(slug):
            continue
        heading = GROUP_HEADINGS[term["index_group"]]
        start, end = sections(blocks)[heading]
        if slug in linked(blocks[start:end]):
            continue
        last = max(i for i in range(start, end) if single_link(blocks[i]))
        blocks.insert(last + 1, link_block(slug, title_of(slug)))

    for heading, entries in GROUP_SENTENCES.items():
        start, end = sections(blocks)[heading]
        para = next(b for b in blocks[start:end] if b["type"] == "paragraph")
        for needs, sentence in entries:
            if all(ingested(s) for s in needs) and sentence not in para["text"]:
                para["text"] += sentence

    # Every entry of the series groups is labelled by its term, not its full title. The
    # last section's link to the 50-term glossary is a cross-reference and keeps its title.
    series_headings = set(GROUP_HEADINGS.values())
    current = None
    for block in blocks:
        if block["type"] == "heading" and block.get("level") == 2:
            current = block["text"]
        slug = single_link(block)
        if slug and current in series_headings:
            block["inlines"][0]["text"] = short_label(title_of(slug))
    write(path, pack)


def integrate_glossary() -> None:
    path = CONTENT / "ai-glossary-50-terms.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    blocks = pack["locales"]["zh-TW"]["blocks"]
    for heading, slugs in GLOSSARY_LINKS.items():
        start, end = sections(blocks)[heading]
        present = linked(blocks[start:end])
        last = max(i for i in range(start, end) if single_link(blocks[i]))
        new = [link_block(s, title_of(s)) for s in slugs if ingested(s) and s not in present]
        blocks[last + 1:last + 1] = new
    write(path, pack)


if __name__ == "__main__":
    integrate_index()
    integrate_glossary()
