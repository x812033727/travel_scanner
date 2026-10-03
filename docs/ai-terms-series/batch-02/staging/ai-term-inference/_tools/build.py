#!/usr/bin/env python3
"""Build pack.json for ai-term-inference from the prose below; also counts body characters."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "pack.json"
SLUG = "ai-term-inference"


def P(text):
    return {"type": "paragraph", "text": text}


def H2(text):
    return {"type": "heading", "level": 2, "text": text}


def RP(*parts):
    """parts: str -> text inline; (text, slug) tuple -> article inline."""
    inlines = []
    for part in parts:
        if isinstance(part, str):
            inlines.append({"type": "text", "text": part})
        else:
            inlines.append({"type": "article", "text": part[0], "kind": "life", "slug": part[1]})
    return {"type": "rich_paragraph", "inlines": inlines}


def LIST(*items):
    return {"type": "list", "items": list(items), "ordered": False}


TITLE = "推論（Inference）是什麼：模型訓練完之後，每次回答都在做的計算"
DESCRIPTION = (
    "推論是用已訓練好的模型處理新輸入、產生輸出的過程，權重在這個階段固定不變。"
    "本文拆開語言模型推論的兩段：讀入提示（prefill）與逐個產生（decode），"
    "說明首個 token 時間、完整回答時間與吞吐量的差別，分清推論與推理、雲端與本機，"
    "並看懂批次、量化與快取各自省在哪裡。"
)

CHECKED = "2026-10-03"
SOURCES = [
    {"title": "Google：Machine Learning Glossary（inference、training 等條目）", "url": "https://developers.google.com/machine-learning/glossary", "checked_on": CHECKED},
    {"title": "Google：機器學習詞彙表（繁體中文版，inference 譯為推論）", "url": "https://developers.google.com/machine-learning/glossary?hl=zh-tw", "checked_on": CHECKED},
    {"title": "Kwon 等：Efficient Memory Management for LLM Serving with PagedAttention（vLLM，SOSP 2023）", "url": "https://arxiv.org/abs/2309.06180", "checked_on": CHECKED},
    {"title": "Pope 等：Efficiently Scaling Transformer Inference（2022）", "url": "https://arxiv.org/abs/2211.05102", "checked_on": CHECKED},
    {"title": "NVIDIA：NIM LLMs Benchmarking，Metrics（TTFT、ITL、吞吐量的定義）", "url": "https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html", "checked_on": CHECKED},
    {"title": "Anthropic：Reducing latency（官方文件）", "url": "https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency", "checked_on": CHECKED},
    {"title": "OpenAI：Latency optimization（官方文件）", "url": "https://platform.openai.com/docs/guides/latency-optimization", "checked_on": CHECKED},
    {"title": "llama.cpp：專案說明（本機推論的官方實作文件）", "url": "https://github.com/ggml-org/llama.cpp", "checked_on": CHECKED},
    {"title": "國家教育研究院樂詞網：inference 條目（各學科詞表的譯名對照）", "url": "https://terms.naer.edu.tw/detail/8bc45e654bd178e8380ebefabc5e389b/", "checked_on": CHECKED},
]

blocks = []

# ---- 導言 -------------------------------------------------------------------------------
blocks += [
    P(
        "推論（inference）是用訓練好的模型處理新的輸入、產生輸出。你每按一次送出，"
        "模型從讀入提示詞到產生最後一個 token，整段計算都是推論；權重等模型參數在這段時間固定不變，"
        "調整權重是訓練的事。另一個常被混用的詞是推理（reasoning），指模型多步推導的能力；"
        "本站用「推論」對應 inference、「推理」對應 reasoning，原因在文末說明。"
    ),
    P(
        "本文用虛構的民宿訂位助理，說明一次回答如何分成兩段、為什麼輸出越長通常越久、"
        "兩種延遲指標的差別，以及批次、量化、快取各省哪一部分。依據是 Google 的詞彙表、兩篇論文與三家的官方文件；"
        "不列價格或速度數字，那些會隨模型與硬體改變。"
    ),
]

# ---- 一、推論與訓練 ---------------------------------------------------------------------
blocks += [
    H2("推論和訓練差在哪裡"),
    P(
        "Google 機器學習詞彙表的定義是：傳統機器學習中，推論是把訓練好的模型套用到未標記樣本上做預測；"
        "在大型語言模型中，則是用訓練好的模型針對輸入提示產生回應。訓練是決定模型參數（權重與偏差）的過程，"
        "系統讀入範例並逐步調整參數。分界在於參數有沒有被改動。"
    ),
    P(
        "推論時，權重不會因為你的這一次提問而改變。提示詞裡放幾個範例，模型能照格式回答，"
        "但範例只是這次計算的輸入。服務商是否保存對話、日後拿去訓練，是產品條款與設定的問題，不屬於推論本身。"
    ),
    {
        "type": "table",
        "header": ["面向", "訓練", "推論"],
        "rows": [
            ["權重", "逐步調整", "固定，只用來計算"],
            ["發生頻率", "集中在模型完成前，或更新版本時", "每個請求都要算"],
            ["成本結構", "模型完成前的運算與資料投入", "隨請求數與長度累加"],
        ],
        "caption": "依 Google 機器學習詞彙表與 Pope 等人的論文整理；查證於 2026 年 10 月。",
    },
]

# ---- 二、兩段 ---------------------------------------------------------------------------
blocks += [
    H2("一次回答的兩段：讀入提示，再逐個產生"),
    P(
        "以大型語言模型為例，一次推論分兩段。第一段是讀入提示（prefill）：提示詞的 token 全部已知，能一起平行處理，"
        "同時算出第一個新 token 的機率，並存下每個位置的中間結果（key 與 value，合稱 KV 快取）。"
        "vLLM 論文稱這段為 prompt phase，Pope 等人稱 prefill。"
    ),
    P(
        "第二段是逐個產生（decode）：每一步只把上一個新 token 送進模型、算出下一個，直到遇到結束符號或長度上限。"
        "前面 token 的 KV 快取已存好，每步只補算新的一個，但後一步要等前一步，無法平行。"
        "vLLM 論文指出這段不易用滿 GPU 的運算能力、受記憶體讀取限制，並佔單一請求延遲的大部分。"
    ),
    P(
        "這就是輸出越長越久的原因：token 越多，要重複的步數越多，每步都要讀取模型權重與 KV 快取。"
        "輸入變長則主要加重那一次 prefill。OpenAI 的延遲指南同樣指出，產生 token 幾乎總是延遲最高的一步，"
        "輸入除非非常長，通常不是主因。"
    ),
    {
        "type": "image",
        "src": f"/guides/{SLUG}/diagram-1.svg",
        "alt": "時間軸圖：排隊與網路、讀入提示（prefill）、逐個產生 token（decode），上方標示完整回答時間，下方標示首個 token 時間與產生時間",
        "width": 1600,
        "height": 900,
        "caption": "完整回答時間等於首個 token 時間加上產生時間；輸入長度主要影響前段，輸出長度主要影響後段。",
    },
]

# ---- 三、示例 ---------------------------------------------------------------------------
blocks += [
    H2("示例：同一個助理，兩種問法"),
    P(
        "以下是示例，未實測。問法 A：貼入很長的入住須知，問「幾點退房」，輸入長、輸出一句。"
        "問法 B：不貼資料，只要求寫一篇很長的周邊散步介紹，輸入短、輸出長。預期 A 的第一個字較晚出現，"
        "因為要先讀完須知，但很快答完；B 的第一個字很快出現，完整回答時間卻主要花在逐個產生大量 token。"
    ),
    P(
        "若實測與預期不同，別硬套這個模型。首個 token 時間偏長，可能是排隊、網路來回，或提示詞比想像的長；"
        "產生很慢，可能是同時處理的請求多，或輸出比預期長。NVIDIA 的文件指出 TTFT 通常包含排隊、prefill 與網路延遲，要分段量。"
    ),
]

# ---- 四、延遲指標 -----------------------------------------------------------------------
blocks += [
    H2("兩種慢：首個 token 時間與完整回答時間"),
    P(
        "首個 token 時間（time to first token，TTFT）是從送出請求到收到第一個 token；完整回答時間"
        "（end-to-end latency）算到最後一個 token，NVIDIA 的文件把它寫成 TTFT 加產生時間。"
        "Anthropic 的文件指出 TTFT 在串流輸出時特別重要：串流讓使用者先看到開頭，改善感受上的速度，"
        "但 token 總數沒有變。"
    ),
    P(
        "吞吐量（throughput）看整個系統每秒能產生多少 token。NVIDIA 的文件說明，同時處理的請求變多，"
        "系統總吞吐量會上升到用滿資源為止，但每位使用者各自的速度會下降。所以延遲與吞吐量是取捨。"
    ),
    {
        "type": "callout",
        "tone": "warning",
        "title": "比較速度前，先對齊量法",
        "text": "各工具的量法不同，例如每個 token 的間隔是否把首個 token 算進去，就有分歧。NVIDIA 的文件提醒，定義一致才能比較；看到別人的數字，先問怎麼量的。",
    },
]

# ---- 五、降低成本 -----------------------------------------------------------------------
blocks += [
    H2("降低成本：批次、量化與快取"),
    P(
        "每次請求的成本，來自它佔用多少硬體時間。Pope 等人在 TPU v4 上分析大型 Transformer 時指出，批次小，延遲可較低，"
        "但每個 token 的成本較高；離線處理加大批次通常最划算。降本做法常見三類，這裡只點名："
    ),
    LIST(
        "批次處理（batching）：多個請求合併計算。vLLM 論文指出，KV 快取很大且動態增減，浪費的記憶體會限制批次大小，因此提出 PagedAttention。",
        "量化（quantization）：用較低精度的數值表示權重，減少記憶體需求。Pope 等人的 PaLM 實驗用了 int8 權重量化。",
        "快取（caching）：重用已算好的結果，例如相同字首的 KV 快取，OpenAI 的指南建議把會變動的內容放在提示詞後段。",
    ),
    RP(
        "詳見",
        ("量化（Quantization）", "ai-term-quantization"),
        "與",
        ("提示詞快取（Prompt Caching）", "ai-term-prompt-caching"),
        "；快取只省讀入提示那段，不縮短逐個產生。",
    ),
]

# ---- 六、雲端與本機 ---------------------------------------------------------------------
blocks += [
    H2("雲端與本機：誰的硬體，誰在排隊"),
    P(
        "雲端推論在服務商的叢集上執行、同時服務很多人：請求要排隊、可能與他人的請求合併批次，還要經過網路來回，"
        "都算進你等的時間。你能調的多半是提示詞與輸出長度、是否串流、模型大小，Anthropic 與 OpenAI 的延遲文件都列了這些。"
    ),
    P(
        "本機推論通常少了網路往返與他人的請求，但運算與記憶體要自備，模型大小受裝置限制。"
        "llama.cpp 專案自述以各種硬體上的本機與雲端推論為目標，提供整數量化以降低記憶體用量。"
        "兩邊都有 prefill 與 decode，差別在資源誰出、多少人共用。"
    ),
]

# ---- 七、用語 ---------------------------------------------------------------------------
blocks += [
    H2("用語：推論、推理與推論時計算"),
    P(
        "繁體中文裡，inference 與 reasoning 的譯名並不整齊。Google 機器學習詞彙表繁體中文版把 inference 譯為推論，"
        "並以「推理」描述模型的推導；國家教育研究院樂詞網的詞表則兩個詞都用：統計學名詞譯為推論，"
        "電子計算機名詞譯為推理，inference engine 是「推理引擎」或「推理機」。所以「推論＝inference、推理＝reasoning」"
        "是本站為分開兩件事的用法，不是詞典規定；讀到「推理引擎」要看上下文。"
    ),
    RP(
        "相鄰概念：",
        ("推理模型（Reasoning Model）", "ai-reasoning-models-explained"),
        "是針對多步問題設計的一類模型，回答時做的仍是推論；",
        ("推論時計算（Test-time Compute）", "ai-term-test-time-compute"),
        "是在推論階段多投入算力的策略。其他名詞見",
        ("AI 名詞總索引", "ai-terms-index"),
        "。",
    ),
]


def body_parts(bs):
    parts = []
    for b in bs:
        t = b["type"]
        if t == "paragraph":
            parts.append(b["text"])
        elif t == "rich_paragraph":
            parts.append("".join(i["text"] for i in b["inlines"]))
        elif t == "list":
            parts.extend(b["items"])
        elif t == "table":
            parts.extend(b["header"])
            for r in b["rows"]:
                parts.extend(r)
        elif t == "callout":
            parts.extend((b["title"], b["text"]))
    return parts


def count(bs):
    return sum(len(re.sub(r"\s+", "", p)) for p in body_parts(bs))


if __name__ == "__main__":
    print("body chars so far:", count(blocks), "| description chars:", len(DESCRIPTION), "| title chars:", len(TITLE))
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
                    "alt": "一疊提示文字送進鎖住權重的模型方塊，右側輸出一個接一個出現的小方塊",
                    "width": 1600,
                    "height": 900,
                },
                "blocks": blocks,
                "sources": SOURCES,
            }
        },
    }
    OUT.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT)
