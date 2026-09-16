"""Builds pack.json for ai-model-comparison-table-2026.

Every number here comes from notes.md, which records the official page and the
date it was read. Nothing is written from memory.
"""
import json

SLUG = "ai-model-comparison-table-2026"

def art(text, slug):
    return {"type": "article", "text": text, "kind": "life", "slug": slug}

def txt(text):
    return {"type": "text", "text": text}

TIER_HEADER = ["廠商", "模型", "上下文／最大輸出", "每百萬 token 輸入／輸出", "官方自報分數"]

flagship = [
    ["OpenAI", "gpt-6-astra", "1.05M／128K", "10.00 美元／50.00 美元", "GPQA Diamond 96.0%"],
    ["Anthropic", "Claude Fable 5.1", "1M／128K", "10 美元／50 美元", "官網未列分數"],
    ["Anthropic", "Claude Opus 5", "1M／128K", "5 美元／25 美元", "官網未列分數"],
    ["OpenAI", "gpt-5.6-sol", "1.05M／128K", "4.00 美元／20.00 美元", "官網未公布"],
    ["Moonshot", "kimi-k3", "1.05M／官網未公布", "3.00 美元／15.00 美元", "官網未公布"],
    ["Google", "gemini-3.1-pro-preview", "1M／64K", "2.00 美元／12.00 美元", "GPQA Diamond 94.3%、SWE-Bench Verified 80.6%"],
    ["xAI", "grok-4.6", "50 萬／官網未公布", "2.00 美元／6.00 美元", "官網用另一組 benchmark"],
    ["阿里雲百鍊", "qwen3.8-max", "1M／官網未公布", "2 美元／6 美元", "官網未列分數"],
    ["Z.AI", "GLM-5.3", "官網未公布", "1.40 美元／4.40 美元", "官網未公布"],
    ["DeepSeek", "deepseek-v4-pro", "1M／384K", "1.32 美元／3.96 美元", "官網未列分數"],
    ["Mistral", "Mistral Large 3", "官網未公布", "0.50 美元／1.50 美元", "官網未公布"],
    ["MiniMax", "MiniMax-M3", "51.2 萬／官網未公布", "0.30 美元／1.20 美元", "官網未公布"],
]

mid = [
    ["OpenAI", "gpt-5.6-terra", "1.05M／128K", "2.00 美元／12.00 美元", "官網未公布"],
    ["Anthropic", "Claude Sonnet 5", "1M／128K", "2 美元／10 美元", "官網未列分數"],
    ["Google", "gemini-3.5-flash", "官網未公布", "1.50 美元／9.00 美元", "官網未公布"],
    ["Mistral", "Mistral Medium 3.5", "官網未公布", "1.50 美元／7.50 美元", "官網未公布"],
    ["xAI", "grok-4.3", "1M／官網未公布", "1.25 美元／2.50 美元", "官網用另一組 benchmark"],
    ["Moonshot", "kimi-k2.7-code", "26.2 萬／官網未公布", "0.95 美元／4.00 美元", "官網未公布"],
    ["Google", "gemini-3.8-flash", "官網未公布", "0.75 美元／3.75 美元", "官網未公布"],
    ["阿里雲百鍊", "qwen3.7-plus", "1M／官網未公布", "0.40 美元起／1.60 美元起", "官網未列分數"],
    ["MiniMax", "MiniMax-M2.7", "官網未公布", "0.30 美元／1.20 美元", "官網未公布"],
    ["DeepSeek", "deepseek-flash", "1M／384K", "0.30 美元／1.20 美元", "官網未列分數"],
]

light = [
    ["Anthropic", "Claude Haiku 4.5", "200K／64K", "1 美元／5 美元", "官網未列分數"],
    ["OpenAI", "gpt-5.4-mini", "官網未公布", "0.75 美元／4.50 美元", "官網未公布"],
    ["Google", "gemini-3.5-flash-lite", "官網未公布", "0.30 美元／2.50 美元", "官網未公布"],
    ["Google", "gemini-3.1-flash-lite", "官網未公布", "0.25 美元／1.50 美元", "官網未公布"],
    ["OpenAI", "gpt-5.6-luna", "1.05M／128K", "0.20 美元／1.20 美元", "官網未公布"],
    ["阿里雲百鍊", "qwen3.8-flash", "1M／官網未公布", "0.15 美元／0.47 美元", "官網未列分數"],
    ["Mistral", "Mistral Small 4", "官網未公布", "0.15 美元／0.60 美元", "官網未公布"],
    ["Z.AI", "GLM-5.3-Flash", "官網未公布", "0.15 美元／0.50 美元", "官網未公布"],
    ["Google", "gemini-2.5-flash-lite", "官網未公布", "0.10 美元／0.40 美元", "官網未公布"],
    ["Mistral", "Ministral 3（3B）", "官網未公布", "0.10 美元／0.10 美元", "官網未公布"],
    ["OpenAI", "gpt-5-nano", "官網未公布", "0.05 美元／0.40 美元", "官網未公布"],
]

disclosure = [
    ["OpenAI", "有，列了分數", "GPQA Diamond（gpt-6-astra 96.0%）"],
    ["Google", "有，列了分數", "GPQA Diamond、SWE-Bench Verified、長上下文與多模態各項"],
    ["xAI", "有，列了分數", "AA Intelligence Index、Terminal-Bench v3.0、CursorBench v3.2、APEX-SWE 等十項"],
    ["Anthropic", "有提到項目，沒有數字", "Frontier-Bench v0.1、ARC-AGI 3、OSWorld 2.0、GDPval-AA v2 等，只給相對說法"],
    ["阿里雲百鍊", "有，但用自家測試環境", "SWE-Bench 系列，官方註明用自家 agent scaffold、20 萬 token 上下文"],
    ["DeepSeek", "API 文件沒有跑分表", "官網未公布"],
]

blocks = [
    {"type": "summary", "items": [
        "同級距的 token 規格與價格可以攤開直接比：這篇把十家官網 2026 年 9 月 16 日當天的數字，依旗艦、中階、輕量排成三張欄位一致的表。",
        "效能比不了。查了六家官網，OpenAI 與 Google 公布 GPQA Diamond，Anthropic 只給相對說法不給數字，xAI 換了一整組 benchmark，DeepSeek 的 API 文件根本沒有跑分表。",
        "要省錢先看級距而不是廠牌：同一家從旗艦到輕量的價差，常常比不同家的同級距之間還大。",
    ]},
    {"type": "paragraph", "text": "想比較各家模型的時候，真正能攤在同一張表上的只有一半：上下文視窗、最大輸出與每百萬 token 的輸入輸出價，各家官網都寫得清楚，欄位對得起來；但是效能不行。這篇把十家官網當天的模型排成三張分級表，效能欄只抄官網自己公布的分數，抄不到的就寫「官網未公布」，不從第三方比價站或排行榜補。"},
    {"type": "paragraph", "text": "讀完你會知道三件事：同一個級距裡各家的 token 規格差多少、同一個級距裡各家的價差有多大，以及為什麼「同級距的效能」這個問題，用官網資料回答不了。最後一件事不是這篇偷懶，是查證的結果，後面有一張表把六家官網的揭露情況列出來。"},

    {"type": "heading", "level": 2, "text": "這張表怎麼分級"},
    {"type": "paragraph", "text": "級距用的是各家自己的命名習慣，不是本站的評分：每家都有一個最貴、標榜最強的旗艦，一個主打速度與能力平衡的中階，以及一個為跑量與即時回應設計的輕量。分級的意義在於同級距的模型通常被拿來做同一類工作，所以放在一起比才有意義；跨級距比價格沒有結論，因為那本來就是兩種用途。"},
    {"type": "list", "ordered": False, "items": [
        "上下文視窗：單次請求能塞進去的總量，輸入與輸出共用，數字越大能一次讀完的文件越長。",
        "最大輸出：單次回應最多能生成多少 token。這一欄很多家的定價頁不寫，要翻到模型文件才有，翻不到就是「官網未公布」。",
        "價格：照官網幣別（都是美元）沒有換算，也沒有套用快取、批次與離峰折扣。DeepSeek 用的是尖峰、快取未命中的價；MiniMax-M3 用的是官網標「永久五折」之後的價。",
        "官方自報分數：只有廠商自己在官網或官方模型卡公布的數字才會出現在這一欄。",
    ]},

    {"type": "heading", "level": 2, "text": "旗艦級：十家攤在同一張表上"},
    {"type": "paragraph", "text": "旗艦這一級最值得注意的不是誰最強，是這一級內部的價差。同樣掛著旗艦名字，最貴的每百萬輸出 token 要 50 美元，最便宜的 1.20 美元，中間差了四十倍以上。上下文視窗反而趨於一致，多數已經站上 100 萬 token。"},
    {"type": "table", "header": TIER_HEADER, "rows": flagship,
     "caption": "十家官網 2026 年 9 月 16 日當天的標準價，未套用快取、批次與離峰折扣。分數為廠商自報、測試條件不同，不可直接相減排名次。"},
    {"type": "paragraph", "text": "有幾個欄位要小心讀。gemini-3.1-pro-preview 與 grok-4.6 的價格是 20 萬 token 以內的價，超過門檻兩欄都會往上跳。deepseek-v4-pro 寫的是尖峰價，離峰對折，而且官網的輸入價分「快取命中」與「快取未命中」兩欄，表上用的是未命中那一欄。kimi-k3 同樣有快取命中價，未命中是 3.00 美元、命中只要 0.30 美元。Mistral 的命名跟價位帶對不上：掛著 Large 的 Mistral Large 3 反而比掛著 Medium 的便宜。"},

    {"type": "heading", "level": 2, "text": "中階級：多數正式產品實際在用的一層"},
    {"type": "paragraph", "text": "中階是實際流量最常落在的一層，因為它通常已經夠用，而價格只有旗艦的幾分之一。這一級的價差比旗艦收斂，輸出價大致落在每百萬 token 1.20 到 12 美元之間。"},
    {"type": "table", "header": TIER_HEADER, "rows": mid,
     "caption": "同上，2026 年 9 月 16 日各家官網標準價。gemini-3.8-flash 的 0.75 美元與 3.75 美元官網標到 2026 年 12 月 31 日，之後回到 1.50 美元與 7.50 美元。"},

    {"type": "heading", "level": 2, "text": "輕量級：跑量、分類與即時回應"},
    {"type": "paragraph", "text": "輕量級是量大、單次任務簡單時的選擇，例如分類、抽取欄位、改寫短句。這一級的價格已經低到跟旗艦不是同一個數量級：最便宜的輸入價每百萬 token 0.05 美元，是旗艦最高價的兩百分之一。要注意的是這一級的上下文視窗官網多半不在定價頁寫，得自己翻模型文件確認。"},
    {"type": "table", "header": TIER_HEADER, "rows": light,
     "caption": "同上，2026 年 9 月 16 日各家官網標準價。Z.AI 另有 GLM-4.7-Flash 與 GLM-4.5-Flash 官網標免費，沒有列進表。"},

    {"type": "heading", "level": 2, "text": "效能為什麼比不了：六家用的不是同一組 benchmark"},
    {"type": "paragraph", "text": "上面三張表的效能欄大量出現「官網未公布」，這不是漏抄。2026 年 9 月 16 日逐一打開六家官網之後，結論是各家連量的東西都不一樣，所以沒有一把尺能把它們排在一起。"},
    {"type": "table", "header": ["廠商", "官網有沒有列跑分", "用的是哪一組 benchmark"], "rows": disclosure,
     "caption": "2026 年 9 月 16 日各家官方發布頁、模型卡與 API 文件的揭露情況。"},
    {"type": "image", "src": f"/guides/{SLUG}/diagram-1.svg",
     "alt": "左側三個由大到小的方塊代表旗艦、中階與輕量三個級距，每個方塊右邊接出兩條線，一條通往標示可比的規格欄位，一條通往標示不可比的效能欄位",
     "width": 1, "height": 1,
     "caption": "同一張表裡有兩種欄位：左半的 token 規格與價格各家寫法一致，可以直接比；右半的效能欄各家量的東西不同，只能各自看。"},
    {"type": "callout", "tone": "warning", "title": "不要把這三張表的分數欄拿來排名次",
     "text": "就算兩家都寫了 GPQA Diamond，測試條件也不一定相同：給不給工具、給不給推理預算、取樣幾次、用誰的 agent scaffold，每一項都會動到分數，而官網通常只寫結果不寫全部條件。阿里雲百鍊在自己的 blog 就註明 SWE-Bench 系列是用自家 agent scaffold、20 萬 token 上下文、temperature 1.0 跑出來的。分數欄的用途是知道廠商宣稱到哪裡，不是拿來相減。"},
    {"type": "rich_paragraph", "inlines": [
        txt("跑分本身怎麼讀、有哪些常見陷阱，站上另外寫過一篇"),
        art("模型跑分怎麼看", "ai-benchmarks-explained"),
        txt("。想知道旗艦、中階、輕量這三個級距在使用上的實際差別，可以看"),
        art("同一家為什麼有好幾個模型", "ai-model-tiers-explained"),
        txt("；只想看價格、不看規格與分數的話，"),
        art("API 價格比較", "ai-api-pricing-comparison-2026"),
        txt(" 那篇把快取價、批次折扣與免費層條款寫得更細。"),
    ]},

    {"type": "heading", "level": 2, "text": "開放權重與授權，這篇沒有做成表"},
    {"type": "rich_paragraph", "inlines": [
        txt("原本這篇要多一張開放權重表，實際查證之後拿掉了，理由寫在這裡。第一，Meta 的 llama.com 當天轉到 developer.meta.com，該頁只在導覽列出現 Llama 4 與 Llama 3，沒有版本、上下文或授權；模型頁回 404，官方 blog 也沒有提到現行版本，所以查不到就不寫。第二，Z.AI、MiniMax、Moonshot 與 Mistral 的 API 定價頁都不寫權重授權，湊出來的表會整欄都是「官網未公布」。開放權重與閉源的差別、各家授權條款怎麼看，站上分別有"),
        art("開源 vs 閉源模型", "ai-open-vs-closed-models"),
        txt("、"),
        art("Llama 模型家族", "llama-models-explained"),
        txt("與"),
        art("MiniMax M 系列模型", "minimax-m-series-models-explained"),
        txt("，那三篇比一張空表有用。中國系幾家的整體比較則在"),
        art("中國系 AI 模型比較", "chinese-ai-models-comparison"),
        txt("。"),
    ]},

    {"type": "heading", "level": 2, "text": "這張表什麼時候會過期"},
    {"type": "rich_paragraph", "inlines": [
        txt("很快。光是 2026 年 1 月到 9 月，各家就發了三十次以上的模型，節奏可以看"),
        art("2026 年 AI 模型大事記", "ai-model-release-timeline-2026"),
        txt("。表格 caption 裡的日期就是這張表的有效期起點：看到這篇時若已經過了幾個月，把要用的那一列拿去官網對一次再下決定，特別是價格與上下文視窗這兩欄，改動最頻繁。另外兩個名詞如果還不熟，"),
        art("token", "ai-term-token"),
        txt("與"),
        art("上下文視窗", "ai-context-window-explained"),
        txt("各有一篇。"),
    ]},
]

sources = [
    ("OpenAI API 定價頁（gpt-6-astra、gpt-5.6 系列與 gpt-5 系列的每百萬 token 標準價）", "https://developers.openai.com/api/docs/pricing"),
    ("OpenAI 模型頁（gpt-6-astra 與 gpt-5.6 系列的上下文視窗與最大輸出）", "https://developers.openai.com/api/docs/models"),
    ("OpenAI GPT-6 Astra 發布頁（GPQA Diamond 96.0%）", "https://openai.com/index/gpt-6-astra/"),
    ("Anthropic Claude 平台定價頁（各模型每百萬 token 價與快取倍率）", "https://platform.claude.com/docs/en/about-claude/pricing"),
    ("Anthropic Claude 模型總覽頁（Fable 5.1、Opus 5、Sonnet 5、Haiku 4.5 的上下文視窗與最大輸出）", "https://platform.claude.com/docs/en/about-claude/models/overview"),
    ("Anthropic Claude Opus 5 發布頁（列出 benchmark 項目但未列數字）", "https://www.anthropic.com/news/claude-opus-5"),
    ("Gemini API 定價頁（各 Gemini 模型的標準價與分段計價）", "https://ai.google.dev/gemini-api/docs/pricing"),
    ("Google DeepMind Gemini 3.1 Pro 模型卡（GPQA Diamond 94.3%、SWE-Bench Verified 80.6%、1M 輸入與 64K 輸出）", "https://deepmind.google/models/model-cards/gemini-3-1-pro/"),
    ("xAI 開發者文件：模型頁（Grok 各型號的上下文與分段價）", "https://docs.x.ai/developers/models"),
    ("xAI Grok 4.6 發布頁（官方跑分表，未列 GPQA Diamond 與 SWE-bench Verified）", "https://x.ai/news/grok-4-6"),
    ("DeepSeek API 文件：模型與定價（快取命中與未命中、尖峰與離峰四欄價）", "https://api-docs.deepseek.com/quick_start/pricing/"),
    ("Mistral API 定價頁（Large 3、Medium 3.5、Small 4 與 Ministral 3 的每百萬 token 價）", "https://mistral.ai/pricing/api/"),
    ("阿里雲 Model Studio（百鍊）模型計費頁（qwen3.8-max、qwen3.7-plus、qwen3.8-flash 新加坡站美元價與上下文）", "https://www.alibabacloud.com/help/en/model-studio/model-pricing"),
    ("Qwen 官方 blog：Qwen3.8-Max（SWE-Bench 系列用自家 agent scaffold 與 20 萬 token 上下文）", "https://qwen.ai/blog?id=qwen3.8"),
    ("MiniMax API 文件：隨用隨付定價（MiniMax-M3 的永久五折價與 51.2 萬 token 分段）", "https://platform.minimax.io/docs/guides/pricing-paygo"),
    ("Moonshot Kimi 平台文件：對話模型定價（kimi-k3 與 k2.7-code 的上下文與快取命中／未命中價）", "https://platform.kimi.ai/docs/pricing/chat"),
    ("Z.AI 文件：定價總覽（GLM-5.3 與 GLM-5.3-Flash 的每百萬 token 價）", "https://docs.z.ai/guides/overview/pricing"),
    ("Meta 開發者 AI 頁（當天查不到現行 Llama 版本、上下文與授權）", "https://developer.meta.com/ai/"),
]

pack = {
    "slug": SLUG,
    "kind": "life",
    "destination_id": None,
    "topics": ["ai", "software"],  # ai-plans re-added after ingest; see the filed task on pack_ingest._known_topics
    "valid_until": None,
    "featured": False,
    "display_order": 100,
    "related": [
        "ai-api-pricing-comparison-2026",
        "ai-benchmarks-explained",
        "ai-model-tiers-explained",
        "ai-model-release-timeline-2026",
    ],
    "locales": {
        "zh-TW": {
            "title": "各家 AI 模型總表：同級距的 token 規格與官方自報分數",
            "description": "把 OpenAI、Anthropic、Google、xAI、阿里雲百鍊、Mistral、MiniMax、DeepSeek、Moonshot、Z.AI 十家官網當天的模型攤成一張表，依旗艦、中階、輕量分級，每一列同時給上下文視窗、最大輸出與每百萬 token 輸入輸出價。效能欄只抄官網自己公布的分數，並說明為什麼這些分數不能直接排名次：六家官網用的 benchmark 幾乎沒有交集。",
            "hero": {"src": f"/guides/{SLUG}/hero.jpg", "alt": "三個由大到小的圓角方塊並排，每個方塊上有數量不同的小圓點，右側一條縱線把畫面分成可比與不可比兩半", "width": 1, "height": 1},
            "blocks": blocks,
            "sources": [{"title": t, "url": u, "checked_on": "2026-09-16"} for t, u in sources],
        }
    },
}

with open("pack.json", "w", encoding="utf-8") as fh:
    json.dump(pack, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

body = sum(len(b.get("text", "")) for b in blocks if b["type"] == "paragraph")
body += sum(len(i.get("text", "")) for b in blocks if b["type"] == "rich_paragraph" for i in b["inlines"])
body += sum(len(x) for b in blocks if b["type"] == "list" for x in b["items"])
body += sum(len(b.get("text", "")) for b in blocks if b["type"] == "callout")
print("blocks:", len(blocks))
print("headings level 2:", sum(1 for b in blocks if b["type"] == "heading"))
print("tables:", sum(1 for b in blocks if b["type"] == "table"))
print("sources:", len(pack["locales"]["zh-TW"]["sources"]))
print("description chars:", len(pack["locales"]["zh-TW"]["description"]))
print("title chars:", len(pack["locales"]["zh-TW"]["title"]))
print("approx body chars:", body)
print("document json chars:", len(json.dumps(pack["locales"]["zh-TW"], ensure_ascii=False)))
