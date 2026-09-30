# 示範紀錄：ai-term-token（token 計數）

- 日期：2026-09-30（示範 JSON 的 `date` 欄位同日）。
- **示範是自行執行的計算，不是任何產品介面的錄影**：影片的 chat 卡是自製對話卡，左邊標「示意回覆」，回覆文字是編的；表格與 stats 卡上的每個數字都來自下面這次執行。
- 工具：開源計數工具 tiktoken **0.14.0**（`tiktoken.__version__`）。PyPI JSON 端點 https://pypi.org/pypi/tiktoken/json 2026-09-30 查到最新版 0.14.0，0.14.0 於 2026-08-17T19:48:31 上傳；HTML 頁 https://pypi.org/project/tiktoken/ 對抓取工具回 200 但內容是「Client Challenge」驗證頁。
- 編碼：`o200k_base` 與 `cl100k_base`（tiktoken 內建的兩種 OpenAI 編碼）。哪個較新的官方說明頁（GitHub）對我們的 UA 回 403，沒讀到，所以旁白只說「兩種編碼」。
- 指令：在放著 `demo_token.py` 的目錄執行 `python3 demo_token.py`（需要 `pip install tiktoken==0.14.0`；第一次執行會下載編碼檔）。輸出寫到 `demo-token.json`，下面逐字抄錄。
- 公告是編的範例，不含任何人的個資。

## 輸入文字

完整公告（`FULL`，172 個字元，不含空白 149）：

```
親愛的各位社員大家好！！！🌟🌟🌟
又到了每個月最期待的時刻～～～
【社團郊遊公告】
時間：10 月 18 日（星期六）上午 8 點 30 分
集合地點：捷運象山站 2 號出口
攜帶物品：水壺、雨具、環保餐具
費用：每人 150 元，現場收費
下雨取消，改期另行通知。
報名截止：10 月 15 日
歡迎揪朋友一起來～～～期待見到大家！！！💖💖💖
```

精簡版（`TRIM`，107 個字元，不含空白 87；刪掉兩行客套話、裝飾符號、【】與（）、把「集合地點」「攜帶物品」縮成「集合」「攜帶」）：

```
社團郊遊公告
時間：10 月 18 日星期六上午 8 點 30 分
集合：捷運象山站 2 號出口
攜帶：水壺、雨具、環保餐具
費用：每人 150 元，現場收費
下雨取消，改期另行通知。
報名截止：10 月 15 日
```

那句要求（`INSTRUCTION`，23 個字元）：

```
請整理成繁體中文公告，保留所有日期與否定條件。
```

完整請求 ＝ `INSTRUCTION + "\n" + FULL`；精簡請求 ＝ `INSTRUCTION + "\n" + TRIM`。

九個字的句子（`SENTENCE`）：`週六臺北見，帶雨傘`；裝飾（`deco`，12 個字元）：`！！！🌟🌟🌟～～～💖💖💖`

## 結果（影片用到的數字）

| 文字 | 字元（含空白／不含） | o200k_base | cl100k_base |
| --- | --- | --- | --- |
| 完整公告 | 172／149 | 142 | 200 |
| 精簡版 | 107／87 | 86 | 115 |
| 那句要求 | 23 | 18 | 31 |
| 完整請求 | — | 160 | 231 |
| 精簡請求 | — | 104 | 146 |
| 「週六臺北見，帶雨傘」 | 9 | 10 | 16 |
| 裝飾 | 12 | 15 | 20 |

- 精簡請求比完整請求少 56 個（o200k_base），約 35%，旁白說「大約三分之一」。
- 完整公告換編碼：200 ÷ 142 ＝ 1.41，旁白說「多了四成」。
- 精簡版仍含「下雨取消」「報名截止」「150 元」：{'下雨取消': True, '報名截止': True, '150 元': True}。
- 九個字在 o200k_base 的片段：['週', '六', '臺', '北', '見', '，', '帶', '雨', '<e582>', '<98>']（「傘」是 `<e582>` `<98>` 兩個位元組片段）；在 cl100k_base 的片段：['<e980>', '<b1>', '<e585>', '<ad>', '<e887>', '<ba>', '北', '見', '，', '<e5b8>', '<b6>', '<e99b>', '<a8>', '<e5>', '<82>', '<98>']（週、六、臺、帶、雨、傘都拆成位元組片段）。`<…>` 是解碼不成完整字元的位元組，以十六進位標示。

## 腳本（`demo_token.py`，逐字）

```python
import json, tiktoken, datetime
FULL = """親愛的各位社員大家好！！！🌟🌟🌟
又到了每個月最期待的時刻～～～
【社團郊遊公告】
時間：10 月 18 日（星期六）上午 8 點 30 分
集合地點：捷運象山站 2 號出口
攜帶物品：水壺、雨具、環保餐具
費用：每人 150 元，現場收費
下雨取消，改期另行通知。
報名截止：10 月 15 日
歡迎揪朋友一起來～～～期待見到大家！！！💖💖💖"""
TRIM = """社團郊遊公告
時間：10 月 18 日星期六上午 8 點 30 分
集合：捷運象山站 2 號出口
攜帶：水壺、雨具、環保餐具
費用：每人 150 元，現場收費
下雨取消，改期另行通知。
報名截止：10 月 15 日"""
INSTRUCTION = "請整理成繁體中文公告，保留所有日期與否定條件。"
SENTENCE = "週六臺北見，帶雨傘"
encs = {name: tiktoken.get_encoding(name) for name in ["o200k_base", "cl100k_base"]}
def count(text): return {n: len(e.encode(text)) for n, e in encs.items()}
def chars(text): return {"all": len(text), "no_ws": len("".join(text.split()))}
out = {"date": datetime.date.today().isoformat(), "tiktoken": tiktoken.__version__,
       "full": {"chars": chars(FULL), "tokens": count(FULL)},
       "trim": {"chars": chars(TRIM), "tokens": count(TRIM)},
       "instruction": {"chars": chars(INSTRUCTION), "tokens": count(INSTRUCTION)},
       "full_request": {"tokens": count(INSTRUCTION + "\n" + FULL)},
       "trim_request": {"tokens": count(INSTRUCTION + "\n" + TRIM)},
       "keeps": {"下雨取消": "下雨取消" in TRIM, "報名截止": "報名截止" in TRIM, "150 元": "150 元" in TRIM},
       "sentence": {"text": SENTENCE, "chars": len(SENTENCE)}}
for n, e in encs.items():
    ids = e.encode(SENTENCE)
    pieces = []
    for t in ids:
        b = e.decode_single_token_bytes(t)
        try: pieces.append(b.decode("utf-8"))
        except UnicodeDecodeError: pieces.append("<%s>" % b.hex())
    out["sentence"][n] = {"count": len(ids), "pieces": pieces}
# emoji and decorations alone
deco = "！！！🌟🌟🌟～～～💖💖💖"
out["decorations"] = {"text": deco, "chars": len(deco), "tokens": count(deco)}
json.dump(out, open("demo-token.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
```

## 輸出（`demo-token.json`，逐字）

```json
{
 "date": "2026-09-30",
 "tiktoken": "0.14.0",
 "full": {
  "chars": {
   "all": 172,
   "no_ws": 149
  },
  "tokens": {
   "o200k_base": 142,
   "cl100k_base": 200
  }
 },
 "trim": {
  "chars": {
   "all": 107,
   "no_ws": 87
  },
  "tokens": {
   "o200k_base": 86,
   "cl100k_base": 115
  }
 },
 "instruction": {
  "chars": {
   "all": 23,
   "no_ws": 23
  },
  "tokens": {
   "o200k_base": 18,
   "cl100k_base": 31
  }
 },
 "full_request": {
  "tokens": {
   "o200k_base": 160,
   "cl100k_base": 231
  }
 },
 "trim_request": {
  "tokens": {
   "o200k_base": 104,
   "cl100k_base": 146
  }
 },
 "keeps": {
  "下雨取消": true,
  "報名截止": true,
  "150 元": true
 },
 "sentence": {
  "text": "週六臺北見，帶雨傘",
  "chars": 9,
  "o200k_base": {
   "count": 10,
   "pieces": [
    "週",
    "六",
    "臺",
    "北",
    "見",
    "，",
    "帶",
    "雨",
    "<e582>",
    "<98>"
   ]
  },
  "cl100k_base": {
   "count": 16,
   "pieces": [
    "<e980>",
    "<b1>",
    "<e585>",
    "<ad>",
    "<e887>",
    "<ba>",
    "北",
    "見",
    "，",
    "<e5b8>",
    "<b6>",
    "<e99b>",
    "<a8>",
    "<e5>",
    "<82>",
    "<98>"
   ]
  }
 },
 "decorations": {
  "text": "！！！🌟🌟🌟～～～💖💖💖",
  "chars": 12,
  "tokens": {
   "o200k_base": 15,
   "cl100k_base": 20
  }
 }
}
```
