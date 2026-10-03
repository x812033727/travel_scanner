#!/usr/bin/env python3
"""Build pack.json for ai-term-knowledge-cutoff and count body characters like _body_length."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "pack.json"
SLUG = "ai-term-knowledge-cutoff"
CHECKED = "2026-10-03"


def p(text):
    return {"type": "paragraph", "text": text}


def h2(text):
    return {"type": "heading", "level": 2, "text": text}


def rich(*parts):
    inl = []
    for part in parts:
        if isinstance(part, str):
            inl.append({"type": "text", "text": part})
        else:
            text, slug = part
            inl.append({"type": "article", "text": text, "kind": "life", "slug": slug})
    return {"type": "rich_paragraph", "inlines": inl}


def lst(items, ordered=False):
    return {"type": "list", "items": items, "ordered": ordered}


SECTIONS = []

# ---------------------------------------------------------------- intro
SECTIONS.append([
    p("知識截止日（knowledge cutoff）是供應商用來說明模型訓練資料時間範圍的標示，意思是這個日期之後發生的事，模型多半沒有學到。它是粗略的參考線，不是保證：日期之前的事，模型不一定知道，知道的也不一定正確；日期之後的事，則要靠你或工具把資料交給它。"),
    rich("本文依 Anthropic、OpenAI、Google 的官方文件與三篇研究論文，說明各家怎麼標示、為什麼越靠近截止日越不牢靠，用虛構案例示範三種回答型態，再談附上資料、檢索與搜尋能補到哪裡、在哪裡失敗。訓練資料從哪裡來，見",
         ("預訓練（Pretraining）", "ai-term-pretraining"),
         "；文中不列模型的截止日期，那會過期，請看供應商當天的頁面。"),
])

# ---------------------------------------------------------------- section 1
SECTIONS.append([
    h2("供應商怎麼標示截止日"),
    p("三家文件的標法並不一致。Anthropic 的模型總覽頁把「可靠知識截止日」（reliable knowledge cutoff）與「訓練資料截止日」（training data cutoff）分成兩列；它的透明度頁面把前者解釋為模型知識「最廣泛也最可靠」所及的日期，並寫明有的模型訓練資料截止日比可靠知識截止日晚。也就是說，訓練資料到了某天，不代表之前最後幾個月都學得牢。"),
    p("OpenAI 的模型頁只有一個「Knowledge cutoff」欄位加一個日期，我讀到的頁面沒有另外定義它指訓練資料還是可靠知識。Google 把截止日放在部分模型頁的欄位和 Gemini 3 指南的表格裡，指南還補了一句：需要更新的資訊，請用搜尋接地工具；較新的幾個 Gemini 模型頁則沒有這個欄位。三家沒有共用的定義，同樣寫「截止日」，意思未必相同；比較兩個模型前，先確認標的是哪一種。"),
])

# ---------------------------------------------------------------- section 2
SECTIONS.append([
    h2("為什麼越接近截止日，越不牢靠"),
    p("把截止日想成一條銳利的邊界，是常見的誤解。Cheng 等人 2024 年的論文提出「有效截止日」（effective cutoff）：同一個模型對不同資料來源，表現出的截止時間可以不同，也可能和供應商報的不同。他們主要分析訓練資料公開的模型，用 Wikipedia 每月的版本量困惑度（perplexity），發現有些模型的有效截止日比標示早得多，其中一個甚至早了以年計。論文歸因於兩點：新的網頁爬取資料混著大量舊內容，去重複的流程擋不住字面略有差異的重複文件。也有模型和標示吻合，所以結論是「常常不一致」，不是「都不準」。"),
    p("Dai 等人（ICML 2025）的 Daily Oracle 每天用新聞出真假題與選擇題，在不提供資料的設定下測多個模型。在幾個模型上，截止日之前的幾個月答對率就開始緩慢下降，作者推測是訓練資料裡近期新聞的比重不足；截止日之後，有幾個模型在選擇題上下滑得更快。"),
    p("Pęzik 等人（2025 預印本）的 LLMLagBench 用 1,713 題新聞問答，另請一個模型當評審，替許多模型估計訓練邊界。有的模型不只一個「部分截止點」；在某些模型上，直接問模型得到的截止日比量到的邊界早了一年以上，作者並指出模型可能自述保守，卻對更晚的事作答。所以標示的日期比較像「大約到這附近」，不是「到這天為止樣樣都知道」。"),
    {"type": "image", "src": f"/guides/{SLUG}/diagram-1.svg",
     "alt": "時間軸分成三段：較早的事件資料較完整、接近截止日的資料稀薄且版本混雜、截止日之後模型沒有訓練到；下方三條補救路徑把資料送進上下文視窗，旁邊標出各自的失敗點",
     "width": 1600, "height": 900,
     "caption": "截止日不是一條銳利的線；補救只能把內容放進上下文視窗，來源本身也可能過期。"},
])

# ---------------------------------------------------------------- section 3
SECTIONS.append([
    h2("示範：問一件截止日之後才發生的事"),
    p("以下是虛構示例，未對任何模型實測。假設虛構的「濱海光影節」在某模型的訓練資料截止後，才公布今年的場次與票價。你問：「今年光影節哪天開始，票價多少？」常見的回答型態有三種。"),
    lst([
        "型態一，承認可能不知道：「我的資料可能沒涵蓋今年的公告，請以主辦單位網站為準。」這是最安全的訊號，但只是沒有答案，下一步要自己查或開搜尋。",
        "型態二，拿舊資料當現在：「光影節通常在夏天舉行，票價大約是……」內容可能曾經正確，只是已過期。線索是沒有年份、用「通常」帶過；追問「這是哪一年的資訊」就能攤開。",
        "型態三，流暢的新細節：「今年改在三個港區舉行，票價調漲。」具體又有細節，卻沒有來源支持，這才是幻覺。把場次與票價拆成可查的主張，逐項對主辦單位的頁面。",
    ]),
    p("最容易被忽略的是型態二：它讀起來既不像拒答，也不像編造。"),
])

# ---------------------------------------------------------------- section 4
SECTIONS.append([
    h2("它和過期資訊、幻覺差在哪"),
    rich("三個詞常被混用，問題卻不同。截止日描述模型「學到哪裡」；過期資訊是內容曾經正確、現在不再正確，成因可能是截止日後世界改變，也可能是舊版本在訓練資料裡佔多數；幻覺是產生缺乏事實支持的內容，不一定和時間有關。過期資訊要問日期並換新來源，幻覺要拆成主張核對，拆法見",
         ("AI 幻覺（Hallucination）是什麼", "ai-hallucination-fact-check"),
         "；三者可能同時出現在一個回答裡。"),
])

# ---------------------------------------------------------------- section 5
SECTIONS.append([
    h2("補救：附上資料、檢索與搜尋工具"),
    p("補上截止日之後的資訊只有一條路：讓內容進到上下文視窗，模型才讀得到。差別在誰找資料，失敗處也不同。"),
    {"type": "table",
     "header": ["做法", "誰找資料", "常見失敗點"],
     "rows": [
         ["自己附上資料", "你貼上文字或檔案", "貼的版本過期，或漏了關鍵段落"],
         ["檢索（RAG）", "系統從資料庫找", "資料庫沒更新，或找到不相關的段落"],
         ["搜尋工具", "模型決定搜不搜", "沒搜就直接答，或頁面過期、不支持引用"],
     ],
     "caption": "概念對照；來源查證於 2026 年 10 月。"},
    rich("搜尋工具的失敗點可以更具體。Anthropic、Google 與 OpenAI（Responses API）的文件，都寫明由模型依提示詞判斷搜不搜，所以看似常識的問題可能沒觸發搜尋，答案只來自記憶。Anthropic 說搜尋成功卻沒有結果時回傳空列表，不是錯誤；OpenAI 有只用快取結果的模式，也另有完整來源清單，數量常多於引用。連結存在不等於頁面支持那句話，要點開看日期和內容。原理見",
         ("檢索增強生成（RAG）", "ai-term-retrieval-augmented-generation"),
         "與",
         ("接地（Grounding）", "ai-term-grounding"),
         "。"),
    p("Daily Oracle 的受限檢索實驗（BM25 取前 5 篇新聞、每篇截至 512 個英文單字）也看得到：資料庫停在某天，成績就在那天之後掉下來；有個模型在檢索資料比自己的訓練截止日更舊時，表現可能不如不給資料。就算直接給含答案的原文，多數模型的成績仍隨時間下滑。"),
])

# ---------------------------------------------------------------- section 6
SECTIONS.append([
    h2("使用時怎麼檢查"),
    lst([
        "先看是哪一種日期：訓練資料截止日、可靠知識截止日，還是沒有定義的欄位。",
        "判斷問題有沒有時效：價格、規定、版本、活動日期屬於時效問題；穩定的概念通常不是。",
        "把今天的日期告訴模型。Anthropic 的文件說，它的網頁版與手機應用程式會在對話開頭提供目前日期，並註明這些系統提示詞更新不適用於 API；用 API 時，自己放日期比較保險。",
        "時效性問題開搜尋或附上資料，要求答案標出資料日期，再打開來源核對。",
    ], ordered=True),
    {"type": "callout", "tone": "warning",
     "title": "不要把模型自述的截止日當依據",
     "text": "模型自述的日期可能比實際保守，也可能是錯的。要查截止日，看供應商當天的模型頁；要確認它知不知道某件事，直接問那件事並核對來源。日期之前的事，也不保證它知道。"},
    rich("想看更多概念，可回到",
         ("AI 名詞總索引", "ai-terms-index"),
         "。"),
])


def blocks():
    out = []
    for sec in SECTIONS:
        out.extend(sec)
    return out


SOURCES = [
    ("Anthropic：Models overview（模型總覽頁，並列可靠知識截止日與訓練資料截止日兩列）", "https://platform.claude.com/docs/en/models/overview"),
    ("Anthropic：Transparency Hub 的 Model Report（各模型的 Knowledge Cutoff Date 說明）", "https://www.anthropic.com/transparency"),
    ("Anthropic：Web search tool（何時搜尋、引用、錯誤與空結果的處理）", "https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool"),
    ("Anthropic：System prompts（網頁版與手機應用程式的系統提示詞提供目前日期，不適用於 API）", "https://platform.claude.com/docs/en/release-notes/system-prompts/overview"),
    ("OpenAI：Models（模型頁的 Knowledge cutoff 欄位）", "https://developers.openai.com/api/docs/models"),
    ("OpenAI：Web search guide（模型自行決定是否搜尋、引用、完整來源清單、快取模式）", "https://developers.openai.com/api/docs/guides/tools-web-search"),
    ("Google：Gemini 3 developer guide（Knowledge Cutoff 表格欄位與常見問題）", "https://ai.google.dev/gemini-api/docs/gemini-3"),
    ("Google：Gemini 2.5 Flash 模型頁（有 Knowledge cutoff 欄位的模型頁）", "https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash"),
    ("Google：Gemini 3.8 Flash 模型頁（較新的模型頁，本次讀到的版本沒有此欄位）", "https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash"),
    ("Google：Grounding with Google Search（模型判斷是否搜尋、引用標註的結構）", "https://ai.google.dev/gemini-api/docs/google-search"),
    ("Cheng et al. 2024, Dated Data: Tracing Knowledge Cutoffs in Large Language Models（arXiv:2403.12958）", "https://arxiv.org/abs/2403.12958"),
    ("Dai, Teehan, Ren 2025, Are LLMs Prescient? A Continuous Evaluation using Daily News as the Oracle（ICML 2025，arXiv:2411.08324）", "https://arxiv.org/abs/2411.08324"),
    ("Pezik et al. 2025, LLMLagBench: Identifying Temporal Training Boundaries in Large Language Models（arXiv:2511.12116，預印本）", "https://arxiv.org/abs/2511.12116"),
]

TITLE = "知識截止日（Knowledge Cutoff）是什麼：模型知道到哪一天，又為什麼不準"
DESCRIPTION = "知識截止日是供應商標示模型訓練資料大致到哪個時間的說法，不是模型什麼都知道的保證。本文說明各家怎麼標示、訓練資料截止日與可靠知識截止日的差別，為什麼越近截止日的事越不牢靠，用虛構案例區分承認不知道、過期資訊與幻覺，再比較附上資料、檢索與搜尋工具的補救與失敗點。"


def body_parts(bl):
    parts = []
    for b in bl:
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


def length(bl):
    return sum(len(re.sub(r"\s+", "", x)) for x in body_parts(bl))


def main():
    bl = blocks()
    doc = {
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
                    "alt": "左側五排方塊由深到淺逐漸變淡，一條紅色虛線之後只剩空白的虛線方塊，一支放大鏡罩住其中一塊並讓它亮起",
                    "width": 1600,
                    "height": 900,
                },
                "blocks": bl,
                "sources": [
                    {"title": t, "url": u, "checked_on": CHECKED} for t, u in SOURCES
                ],
            }
        },
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("title chars", len(TITLE), "description chars", len(DESCRIPTION))
    print("body chars (_body_length)", length(bl))
    # without link text
    nolink = 0
    for b in bl:
        if b["type"] == "rich_paragraph":
            nolink += sum(len(re.sub(r"\s+", "", n["text"])) for n in b["inlines"] if n["type"] == "text")
        else:
            nolink += sum(len(re.sub(r"\s+", "", x)) for x in body_parts([b]))
    print("body chars excluding article link text", nolink)
    print("h2 count", sum(1 for b in bl if b["type"] == "heading" and b["level"] == 2))
    print("tables", sum(1 for b in bl if b["type"] == "table"), "callouts", sum(1 for b in bl if b["type"] == "callout"))


if __name__ == "__main__":
    main()
