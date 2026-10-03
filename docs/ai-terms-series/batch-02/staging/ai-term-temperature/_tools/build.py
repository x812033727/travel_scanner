"""Build pack.json for ai-term-temperature from the prose below, and count body characters.

Helper only; the _tools directory is deleted before hand-off.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "ai-term-temperature"
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


blocks = [
    P(
        "溫度（temperature）是語言模型生成文字時的取樣設定。模型每寫一個 token，"
        "都先替許多候選算出機率再抽一個；溫度決定抽籤偏向最高的候選，還是讓冷門候選也有機會。"
        "它不是正確率旋鈕，設成 0 也不保證每次一模一樣。"
    ),
    P(
        "本文依 Holtzman 等人的取樣論文，以及 OpenAI、Anthropic、Google 的官方 API 文件，"
        "用假想的早餐例子算出溫度如何改變機率，再談 top-p、失敗型態、確定性的限制與不開放調整的模型。"
        "例子的數字都是示例，沒有實測任何模型。"
    ),
    H("模型每一步給的是機率分布"),
    RP(
        T("在"),
        A("大型語言模型（LLM）", "what-is-a-large-language-model"),
        T("裡，每一步只決定下一個 "),
        A("token", "ai-term-token"),
        T(
            "：模型替詞彙表中的每個候選打分，換算成加總為 100% 的機率，"
            "程式再依機率抽出一個，接在文字後面，繼續算下一步。這個抽選動作叫取樣（sampling）。"
        ),
    ),
    P(
        "示例（未實測）：提示詞是「明天到台南，早餐我想吃」，簡化成三個候選：牛肉湯 70%、虱目魚粥 20%、鍋燒意麵 10%。"
        "真實候選是 token，可能只是半個詞，數量也遠不止三個。照這份機率抽，大約七成是牛肉湯，"
        "偶爾抽到另外兩個，同一個提示詞因此會得到不同答案。"
    ),
    H("溫度如何讓分布變尖或變平"),
    P(
        "做法是把每個候選的分數（logit）先除以溫度 t，再換算成機率。"
        "Hinton 等人的知識蒸餾論文寫明 t 通常設為 1，t 越高分布越「軟」；"
        "Holtzman 等人說明 t 小於 1 會把分布推向高機率的候選。"
    ),
    P(
        "套進示例：t=1 維持 70%、20%、10%；t=0.5 變成約 91%、7%、2%；t=2 變成約 52%、28%、20%（四捨五入）。"
        "t 趨近 0 時領先者幾乎獨占；Google 的文件寫明溫度 0 時永遠選機率最高的候選，這種選法稱為貪婪解碼（greedy decoding）。"
    ),
    P(
        "溫度只改變怎麼從這份清單裡選，不改變清單本身，也不改變模型知道什麼。"
    ),
    {
        "type": "image",
        "src": f"/guides/{SLUG}/diagram-1.svg",
        "alt": "同一份三個候選的機率，在溫度 0.5、1、2 下被改成集中或平坦的長條，下方示範 top-p 0.85 截掉最後一名",
        "width": 1600,
        "height": 900,
        "caption": "上排是同一份機率在三種溫度下的樣子，下排是 top-p 0.85 截尾的示意；數字皆為示例。",
    },
    H("top-p 與 top-k：先截掉尾巴再抽"),
    P(
        "top-k 只保留機率最高的 k 個候選。top-p 又稱 nucleus sampling，由 Holtzman 等人在 2019 年提出："
        "由高到低累加機率，取累積達到 p 的最小集合，其餘不抽，留下的重新配比。"
        "示例 top-p=0.85：牛肉湯 70% 不到 85%，加上虱目魚粥累積 90%，前兩名入選，重配後約 78% 與 22%，鍋燒意麵被排除。"
    ),
    P(
        "論文認為固定的 k 在分布平坦時太小、分布集中時太大，而 top-p 的候選數隨分布增減。論文在它的設定下"
        "（GPT-2 Large，生成 5,000 段最長 200 個 token 的文字）比較多種解碼法，作者結論是 nucleus sampling 是當時最佳的解碼策略；"
        "這不能直接推到所有現代模型。"
    ),
    P(
        "為什麼不建議同時大幅調兩個？OpenAI 的 API 參考在兩個欄位都寫一般建議只調其中一個，但沒說明原因。"
        "本文的解讀是兩者都在改變低機率候選被抽到的程度，一起調會互相疊加，也分不出是誰造成的。"
        "各家的先後順序還不同：Holtzman 等人提到先用溫度塑形再做 top-k，"
        "Google 的文件則描述先用 topK、topP 篩選，最後才用溫度取樣。"
    ),
    H("低溫與高溫各適合什麼，也各怎麼失敗"),
    P(
        "官方文件方向一致：Anthropic 建議分析或選擇題類靠近 0.0，創作類靠近 1.0；"
        "Google 說較低溫適合較確定的回答，較高溫帶來更多樣的結果。"
    ),
    {
        "type": "list",
        "ordered": False,
        "items": [
            "低溫的失敗型態是重複與呆板：Holtzman 等人在上述設定下發現，只用溫度取樣且低於 0.9 時，"
            "重複迴圈明顯增加；也可能穩定地答錯，因為最高機率的答案不一定正確。",
            "高溫的失敗型態是離題與前後不連貫：Holtzman 等人指出純取樣會抽到不可靠的尾端；"
            "Renze 與 Guven 的測試中，溫度超過 1.0 後正確率快速下降，在其測的一個模型上約 1.6 時文字已不連貫。",
        ],
    },
    RP(
        T(
            "那低溫是否更準？Renze 與 Guven 用九個模型、五種提示詞寫法、從標準評測抽出的選擇題，"
            "溫度由 0.0 掃到 1.0，未發現統計上顯著的正確率差異，作者註明只測選擇題。"
            "所以「溫度越低越準」得不到支持；想降低出錯風險，請看"
        ),
        A("AI 幻覺查核", "ai-hallucination-fact-check"),
        T("的做法。"),
    ),
    {
        "type": "table",
        "header": ["設定", "較適合", "常見失敗型態"],
        "rows": [
            ["低溫", "擷取欄位、分類、改寫", "重複、呆板、穩定地錯"],
            ["預設值附近", "沒有特別需求時先沿用", "預設值可能依模型而異"],
            ["高溫", "想標語、取名、多種寫法", "離題、前後不連貫"],
            ["top-p 調小", "砍掉低機率的尾端", "候選變少，輸出變單調"],
        ],
        "caption": "取樣設定對照；依 2026 年 10 月查證的論文與官方文件整理。",
    },
    {
        "type": "callout",
        "tone": "warning",
        "title": "溫度不是正確率旋鈕",
        "text": "調低溫度只讓輸出更集中，不會讓模型多知道事實，錯的答案還可能被更穩定地重複。"
        "重要內容要查證，一致性靠驗證與約束。",
    },
    H("設成 0 也不保證每次一樣"),
    P(
        "Google 描述選擇規則：溫度 0 時永遠選機率最高的候選。"
        "Anthropic 的 API 參考寫明，即使溫度 0.0，結果也不會完全確定。"
        "OpenAI 在 seed 參數的說明（該欄位標為 Beta 與棄用）寫道，只會盡力讓相同 seed 與參數得到相同結果，"
        "不保證確定。"
    ),
    P(
        "抽選規則可以確定，餵進這一步的機率卻可能每次略有不同。"
        "Atil 等人（預印本）在五個模型、八項任務、各跑 10 次、temperature 0、top-p 1、固定 seed 的條件下，"
        "同一任務不同次執行的準確率最多相差 15%；作者對封閉模型的原因只能推測。"
        "vLLM 官方文件則寫明，預設為了效能不保證結果可重現，要重現也只限同樣的硬體與版本。"
    ),
    RP(
        T(
            "示例（未實測）：要把旅客留言「6 月 3 日入住，兩大一小」抽成日期與人數交給程式。"
            "做法是低溫，再用"
        ),
        A("結構化輸出（Structured outputs）", "ai-term-structured-outputs"),
        T(
            "讓回應符合約定的 JSON Schema（OpenAI 官方文件的說法），同一則留言重跑 5 次比對。"
            "預期欄位一致；若某次欄位或格式亂掉，就當成流程問題，加上驗證與重試，不要只往 0 調。"
            "結構化輸出管格式，不管內容對不對。"
        ),
    ),
    H("有些模型或介面不開放調整"),
    P(
        "先查官方文件，別假設每個模型都有這個旋鈕。Anthropic 的 Messages API 參考把 temperature、top_p、top_k 標為棄用，"
        "寫明較新的模型不支援設定溫度：只接受預設值 1.0，其他值回 400 錯誤。"
        "OpenAI 的新模型指南在「不支援的參數」寫道，推理（reasoning）強度不是 none 時要移除 temperature 與 top_p。"
        "Google 對其較新一代模型強烈建議維持預設，並警告調到 1.0 以下可能重複循環，或在複雜數學與推理任務表現下降。"
    ),
    P(
        "有這個欄位的平台，範圍也不同：這幾份文件寫 0 到 1 或 0 到 2，Google 還寫明預設值隨模型而異，"
        "所以不能把一家的數字照抄到另一家。以上是 2026 年 10 月 3 日讀到的說法。"
    ),
    RP(
        T("更多相關詞彙見"),
        A("AI 名詞總索引", "ai-terms-index"),
        T("。"),
    ),
]

sources = [
    ("Holtzman et al.：The Curious Case of Neural Text Degeneration（arXiv:1904.09751，ICLR 2020）",
     "https://arxiv.org/abs/1904.09751"),
    ("Hinton et al.：Distilling the Knowledge in a Neural Network（arXiv:1503.02531，softmax 溫度的定義）",
     "https://arxiv.org/abs/1503.02531"),
    ("Renze & Guven：The Effect of Sampling Temperature on Problem Solving in Large Language Models（arXiv:2402.05201）",
     "https://arxiv.org/abs/2402.05201"),
    ("Atil et al.：Non-Determinism of \"Deterministic\" LLM Settings（arXiv:2408.04667，預印本）",
     "https://arxiv.org/abs/2408.04667"),
    ("OpenAI API reference：Chat Completions create（temperature、top_p、seed）",
     "https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create"),
    ("OpenAI API 官方指南：最新模型使用說明（「不支援的參數」段落）",
     "https://developers.openai.com/api/docs/guides/latest-model"),
    ("OpenAI：Structured Outputs 指南",
     "https://developers.openai.com/api/docs/guides/structured-outputs"),
    ("Anthropic：Messages API 參考（temperature、top_p、top_k）",
     "https://platform.claude.com/docs/en/api/messages/create"),
    ("Google：Gemini API generateContent 參考（GenerationConfig）",
     "https://ai.google.dev/api/generate-content"),
    ("Google：Gemini API 提示策略（temperature、topK、topP 說明）",
     "https://ai.google.dev/gemini-api/docs/prompting-strategies"),
    ("vLLM 官方文件：Reproducibility",
     "https://docs.vllm.ai/en/latest/usage/reproducibility/"),
]

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
            "title": "溫度（Temperature）是什麼：AI 回答變化程度的取樣參數",
            "description": (
                "溫度（temperature）是文字生成時調整取樣的參數，讓模型從下一個 token 的機率分布裡抽得更集中或更分散。"
                "本文用假想的台南早餐示例算出低溫與高溫的差別，說明 top-p、top-k 的來源，"
                "並依官方文件與論文指出：調低溫度不代表更準，設成 0 也不保證每次相同，部分模型還不開放調整。"
            ),
            "hero": {
                "src": f"/guides/{SLUG}/hero.jpg",
                "alt": "中間一個冷暖兩色的旋鈕，左邊是一高兩低的長條，右邊是三根高度相近的長條",
                "width": 1600,
                "height": 900,
            },
            "blocks": blocks,
            "sources": [{"title": t, "url": u, "checked_on": CHECKED} for t, u in sources],
        }
    },
}


def body_parts(bs):
    parts = []
    for b in bs:
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


def count(bs):
    return sum(len(re.sub(r"\s+", "", p)) for p in body_parts(bs))


if __name__ == "__main__":
    loc = doc["locales"]["zh-TW"]
    (ROOT / "pack.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = count(blocks)
    link_chars = sum(
        len(n["text"]) for b in blocks if b["type"] == "rich_paragraph" for n in b["inlines"] if n["type"] == "article"
    )
    print("title len", len(loc["title"]), "desc len", len(loc["description"]))
    print("body chars (_body_length, incl. link text):", total, "| without link text:", total - link_chars)
    for b in blocks:
        if b["type"] == "heading":
            print("##", b["text"])
        else:
            ps = body_parts([b])
            if ps:
                print("   ", b["type"], sum(len(re.sub(r"\s+", "", p)) for p in ps))
