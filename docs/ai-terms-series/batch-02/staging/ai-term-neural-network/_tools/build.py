"""Builds pack.json for ai-term-neural-network. Delete _tools/ before handing in."""
import json
import re
import sys
from pathlib import Path

SLUG = "ai-term-neural-network"
OUT = Path(__file__).resolve().parent.parent / "pack.json"
MAXSEC = int(sys.argv[1]) if len(sys.argv) > 1 else 99
DAY = "2026-10-03"


def T(text):
    return {"type": "text", "text": text}


def A(text, slug):
    return {"type": "article", "text": text, "kind": "life", "slug": slug}


def P(text):
    return {"type": "paragraph", "text": text}


def RP(*inlines):
    return {"type": "rich_paragraph", "inlines": list(inlines)}


def H(text):
    return {"type": "heading", "level": 2, "text": text}


def L(items, ordered=False):
    return {"type": "list", "items": items, "ordered": ordered}


intro = [
    RP(
        T("神經網路是"),
        A("機器學習", "ai-term-machine-learning"),
        T(
            "裡的一種模型：它把輸入一層一層轉成輸出，每個單元先做加權加總，"
            "再經過一道非線性轉換。網路能做什麼，取決於一組叫權重的數字；"
            "這些數字不是人逐一寫入，而是用資料反覆調整出來的。"
        ),
    ),
    P(
        "本篇用「兩個開關控制一盞燈」的小任務，手算一次前向計算與一步權重更新，"
        "說明訓練與使用為什麼是兩個階段，並交代生物神經元的比喻只用到哪裡。"
        "示例的數字是手算的教學設定，沒有實際訓練過。"
    ),
]

sec1 = [
    H("單元只做兩件事：加權加總與轉換"),
    P(
        "依 Google 機器學習術語表，神經元做兩步：把每個輸入乘上權重再加總，再把總和交給激活函數（activation function）。"
        "偏差是另一個由訓練決定的常數。單元排成層：輸入層、輸出層，"
        "以及夾在中間、值不直接對外的隱藏層。"
    ),
    P(
        "生物神經元的比喻要放對位置。Rosenblatt 把感知器（perceptron）說成假設的神經系統或機器，"
        "目的是說明智慧系統的基本性質，不深陷特定生物體常屬未知的條件；"
        "Google 術語表則說這種單元「模仿」腦中神經元的行為。但兩邊給的運作定義，都只是加總後再做一次轉換。"
        "像不像真實神經元要靠神經科學證據回答，本文只把它當命名的由來。"
    ),
]

sec2 = [
    H("從感知器到多層網路：中間層會不會學"),
    P(
        "Rosenblatt 的感知器靠獎懲調整單元的「值」，他自己也寫下限制：辨認刺激之間的關係會變得極難。"
        "Rumelhart 等人指出，感知器中間那層的連線是事先固定的，不算會學的隱藏單元；"
        "他們的反向傳播讓隱藏單元自己學出需要的特徵。LeCun 等人補充，這個做法在 1970 到 1980 年代被多組人各自發現。"
    ),
]

sec3 = [
    H("為什麼一定要有非線性轉換"),
    P(
        "Google 教材示範過：加了隱藏層、但單元只做加權加總，整個網路仍是線性的，"
        "因為線性接線性還是線性，多加幾層也學不到非線性關係。所以每個單元後面要接非線性的激活函數。"
    ),
    P(
        "常見的有 sigmoid、tanh 與 ReLU，ReLU 是輸入小於 0 就輸出 0，否則原樣輸出。"
        "LeCun 等人 2015 年寫到 ReLU 在多層網路通常學得較快，Google 教材至今仍建議先試 ReLU。"
        "Cybenko（1989）證明，單一隱藏層、連續 sigmoid 型非線性、有限個單元的前饋網路，"
        "能把單位超立方體上的連續函數逼近到任意精度；這是「能表示」，訓練找不找得到是另一回事。"
    ),
]

sec4 = [
    H("示例：兩個開關控制一盞燈"),
    P(
        "示例（未實測，手算）：走廊兩端各有開關 a 與 b，往上記 1、往下記 0，恰好一個往上燈才亮。"
        "(1,0) 與 (0,1) 要輸出 1，(0,0) 與 (1,1) 要輸出 0。單一單元做不到："
        "把兩個該亮的組合相加、兩個該滅的組合相加，會得到互相矛盾的不等式。"
    ),
    P(
        "網路採 2 個輸入、2 個隱藏神經元、1 個輸出，共 9 個參數。手挑權重：隱藏一的權重 1、1，偏差 0；"
        "隱藏二的權重 1、1，偏差 −1，兩者都用 ReLU；輸出的權重 1 與 −2，偏差 0，不加激活函數。"
    ),
    L(
        [
            "(0,0)：隱藏值 0 與 0，輸出 0，燈滅。",
            "(1,0) 或 (0,1)：隱藏值 1 與 0，輸出 1，燈亮。",
            "(1,1)：隱藏值 2 與 1，輸出 2 − 2 = 0，燈滅。",
        ]
    ),
    P("權重是手挑的；真實訓練從隨機權重開始，答案也不只一組。"),
]

sec5 = [
    H("訓練：損失、反向傳播與梯度下降"),
    P("訓練是反覆執行四步："),
    L(
        [
            "前向計算：用目前權重算出預測。",
            "損失：量預測離答案多遠；Rumelhart 等人用 E = ½ Σ (y − d)²，y 是輸出、d 是想要的值。",
            "反向傳播：用連鎖律由輸出往回算，每個權重變動一點，損失會增減多少（梯度）；白話是問每個權重該為誤差負多少責任。",
            "梯度下降：把權重往梯度的反方向改一小步，步幅由學習率決定；學習率是人設的超參數。",
        ],
        ordered=True,
    ),
    P(
        "接上例（示例，手算）：輸出層權重為 1 與 −1.2、偏差 0，輸入 (1,1) 時隱藏值 2 與 1，輸出 0.8，想要 0，損失 0.32。"
        "損失對輸出的變化率是 0.8，乘上各自流過的隱藏值，兩個權重的梯度是 1.6 與 0.8，偏差的梯度是 0.8。學習率取 0.1，"
        "權重變成 0.84 與 −1.28、偏差 −0.08，輸出降到 0.32。隱藏層的權重，則要把誤差乘上輸出權重、"
        "再看 ReLU 有沒有啟動，一路往回傳，這就是「反向」。"
    ),
    P(
        "但同一步也牽動別的輸入：(0,1) 原本輸出 1，現在變成 0.76。權重被所有輸入共用，改一筆會牽動其他筆，"
        "所以要看一批樣本的平均梯度、小步重複許多輪；LeCun 等人說的隨機梯度下降，每次只用一小批樣本估計梯度。"
    ),
    RP(
        T("訓練完成後權重固定，使用時只做前向計算，不算損失、不改權重。Google 術語表說，訓練是決定權重，"),
        A("推論", "ai-term-inference"),
        T("（inference）是用學好的權重做預測。之後若要更新權重，是另一次訓練。"),
    ),
    {
        "type": "image",
        "src": f"/guides/{SLUG}/diagram-1.svg",
        "alt": "上方是訓練迴圈：前向計算、損失、反向傳播、梯度下降並重複；中間是權重與偏差；下方是推論，只讀取權重做前向計算",
        "width": 1600,
        "height": 900,
        "caption": "訓練反覆改寫中間的權重，推論只讀取它。",
    },
]

sec6 = [
    H("參數、神經元與能力是三件事"),
    RP(
        T(
            "上例只有 3 個會計算的單元，卻有 9 個參數：每個隱藏神經元 2 個權重加 1 個偏差，輸出單元也是 2 加 1。"
            "隱藏層若加到 100 個神經元，參數就是 100 × (2 + 1) + (100 + 1) = 401。"
            "Google 術語表把參數定義為訓練中學到的權重與偏差，學習率則是人給的超參數；詳見"
        ),
        A("模型參數", "ai-term-model-parameters"),
        T("。"),
    ),
    P(
        "參數多不代表能力強，還要看架構、訓練資料與損失的設計。LeCun 等人的檢驗，是用訓練時沒看過的測試集量泛化能力；"
        "Cybenko 的結果也只說夠大的網路能表示，不保證訓練找得到。看到神經元、參數、層數，"
        "應再問：在你的任務、沒見過的資料上表現如何。"
    ),
    {
        "type": "table",
        "header": ["名詞", "示例裡", "常見誤解"],
        "rows": [
            ["神經元", "會計算的單元", "等同生物神經細胞"],
            ["權重與偏差", "9 個要學的數字", "人手寫的規則"],
            ["激活函數", "隱藏層後的 ReLU", "可有可無"],
            ["學習率", "0.1，由人設定", "網路自己學出來"],
        ],
        "caption": "概念對照；來源查證於 2026 年 10 月。",
    },
]

sec7 = [
    H("和深度學習、Transformer 的關係"),
    RP(
        T(
            "Google 術語表稱隱藏層多於一層的神經網路為深度模型；LeCun 等人把深度學習定義為疊起多個簡單非線性模組、"
            "由資料學出各層表示的方法。簡單說，神經網路是結構，"
        ),
        A("深度學習", "ai-term-deep-learning"),
        T(
            "是用多層結構學出表示的做法。各家界線略有不同：Google 定義神經網路「至少一個隱藏層」，"
            "中間層連線固定的原始感知器多半不算，讀時先確認對方定義。"
        ),
    ),
    P(
        "Transformer 是網路的一種排法。Vaswani 等人（2017）稱它為完全建立在注意力機制上的網路架構，"
        "每層除了自注意力，還有由兩個線性轉換夾一個 ReLU 組成的前饋網路，正是前面的加權加總加非線性。"
        "後來的語言模型是否採用、怎麼改，要看各自的技術文件。所以神經網路是上位類別，"
        "聊天機器人只是一種用途，分類照片的小網路也是。"
    ),
    {
        "type": "callout",
        "tone": "warning",
        "title": "訓練時答對，不代表學會了",
        "text": (
            "示例只有四種輸入，列舉得完；真實任務列不完，網路可能只是記住了訓練資料。"
            "要用沒參與訓練的測試資料另外量，再換不同來源的資料測，才知道它對新輸入可不可靠。"
        ),
    },
    RP(
        T("想看其他名詞，可以從"),
        A("AI 名詞總索引", "ai-terms-index"),
        T("找起。"),
    ),
]

SOURCES = [
    ("Rosenblatt 1958：The Perceptron（Psychological Review 65(6)，感知器原始論文）", "https://doi.org/10.1037/h0042519"),
    ("Rumelhart、Hinton、Williams 1986：Learning representations by back-propagating errors（Nature 323）", "https://www.nature.com/articles/323533a0"),
    ("LeCun、Bengio、Hinton 2015：Deep learning（Nature 521）", "https://www.nature.com/articles/nature14539"),
    ("Cybenko 1989：Approximation by superpositions of a sigmoidal function（Math. Control Signals Systems 2）", "https://link.springer.com/article/10.1007/BF02551274"),
    ("Vaswani 等人 2017：Attention Is All You Need（arXiv:1706.03762，Transformer 原始論文）", "https://arxiv.org/abs/1706.03762"),
    ("Google Machine Learning Crash Course：Neural networks（單元總覽）", "https://developers.google.com/machine-learning/crash-course/neural-networks"),
    ("Google Machine Learning Crash Course：Nodes and hidden layers", "https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers"),
    ("Google Machine Learning Crash Course：Activation functions", "https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions"),
    ("Google Machine Learning Crash Course：Training using backpropagation", "https://developers.google.com/machine-learning/crash-course/neural-networks/backpropagation"),
    ("Google Machine Learning Glossary（neural network、neuron、weight、parameter、backpropagation 等條目）", "https://developers.google.com/machine-learning/glossary"),
]

TITLE = "神經網路（Neural Network）是什麼：由層與權重組成、能從資料學習的函數"
DESCRIPTION = (
    "神經網路是由多層簡單單元組成的函數：每個單元做加權加總，再經非線性轉換，權重由資料調整。"
    "本文用雙開關走廊燈的手算示例，說明前向計算、損失、反向傳播與梯度下降，區分訓練與推論，"
    "並釐清參數數量、神經元數量與能力的差別，以及它與深度學習、Transformer 的關係。"
)

sections = [sec1, sec2, sec3, sec4, sec5, sec6, sec7]
blocks = list(intro)
for s in sections[:MAXSEC]:
    blocks.extend(s)

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
                "alt": "三排圓點以粗細不同的線連成網路，旁邊有一顆球沿山谷滾向最低點",
                "width": 1600,
                "height": 900,
            },
            "blocks": blocks,
            "sources": [
                {"title": t, "url": u, "checked_on": DAY} for t, u in SOURCES
            ],
        }
    },
}
OUT.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def n(s):
    return len(re.sub(r"\s+", "", s))


tool_total = sum(n(p) for p in parts(blocks))
link_chars = sum(
    n(i["text"]) for b in blocks if b["type"] == "rich_paragraph" for i in b["inlines"] if i["type"] == "article"
)
print("sections written:", min(MAXSEC, len(sections)))
print("title chars:", len(TITLE), "description chars:", len(DESCRIPTION))
print("body chars (tool _body_length):", tool_total)
print("link text chars:", link_chars, "-> excluding link text:", tool_total - link_chars)
print("h2 count:", sum(1 for b in blocks if b["type"] == "heading"))
