# 示範紀錄：三份會議紀錄的 token 數與摘要漏失

- 日期：2026-09-30
- **示範是自行執行的計算，不是任何產品介面的錄影。** 三份會議紀錄、摘要與交接單都是撰稿自己寫的虛構資料（虛構的社區管委會，不是真實社區）；影片的 `code` 卡放的是這兩段文字，`stats` 卡放的是下面的數字。沒有把任何文字送進任何模型，「只帶摘要開新對話，模型可能把維修案寫成即將施工」在影片裡是條件句，不是實測。
- 工具：Python 3.11.15、tiktoken 0.14.0（PyPI：https://pypi.org/project/tiktoken/，2026-09-30 開啟），編碼 `o200k_base`。編碼名稱只放字卡，旁白說「同一種編碼」。
- 字元數用 Python 的 `len()`，含標點、空白與換行；token 數是 `len(enc.encode(text))`。
- 指令：`python3 demo_context.py`（腳本全文在下面；在撰稿封包 `demo/` 跑過一次，撰稿當天在 `SCRATCH/ai-term-context-window/` 再跑一次，輸出 JSON 逐位元相同）。

## 輸入文字（逐字）

第 41 次紀錄（198 字元、180 token）：

```
社區管理委員會第 41 次會議紀錄（3 月）
出席：主委、財委、監委及委員共 7 人。
一、管理室屋頂漏水維修案：廠商甲報價 18 萬元，廠商乙報價 22 萬元。委員會決議「同意研究」，請管委會再向第三家廠商詢價，本案尚未核准，不得視為已通過。
二、中庭燈具更換：決議通過，由財委於 4 月底前完成採購。
三、社區年度旅遊：暫定 6 月，細節下次討論。
待辦：第三家廠商報價、燈具採購、旅遊提案。
```

第 42 次紀錄（217 字元、188 token）：

```
社區管理委員會第 42 次會議紀錄（4 月）
出席：主委、財委及委員共 6 人，監委請假。
一、管理室屋頂漏水維修案：第三家廠商丙報價 19 萬元，三家報價已齊。有委員建議先做局部防水，再評估全面翻修。決議：本案列入 5 月區分所有權人會議討論，目前仍未核准，不得先行發包。
二、中庭燈具更換：已完成採購，5 月初施工。
三、社區年度旅遊：提案日期 6 月 14 日，地點待定。
待辦：整理三家報價比較表、燈具施工通知、旅遊地點投票。
```

第 43 次紀錄（189 字元、167 token）：

```
社區管理委員會第 43 次會議紀錄（5 月）
出席：主委、財委、監委及委員共 8 人。
一、管理室屋頂漏水維修案：區分所有權人會議因人數不足流會，本案延至下次會議，仍未核准。主委提醒雨季將至，請先請廠商提供臨時防水方案報價。
二、中庭燈具更換：施工完成，驗收通過。
三、社區年度旅遊：投票結果宜蘭勝出，6 月 14 日出發。
待辦：臨時防水方案報價、下次區權會通知、旅遊報名表。
```

壞的摘要（62 字元、55 token；不含「尚未核准」「未核准」「不得發包」）：

```
前三次會議：討論管理室屋頂維修案，三家廠商報價 18 至 22 萬元；中庭燈具已更換完成；年度旅遊 6 月 14 日去宜蘭。
```

好的交接（62 字元、60 token；含「尚未核准」）：

```
維修案狀態：尚未核准，區權會流會延期，不得發包；待辦是臨時防水方案報價。燈具已驗收。旅遊 6 月 14 日宜蘭，報名表待發。
```

## 腳本（demo_context.py，逐字）

```python
import json, tiktoken, datetime
R1 = """社區管理委員會第 41 次會議紀錄（3 月）
出席：主委、財委、監委及委員共 7 人。
一、管理室屋頂漏水維修案：廠商甲報價 18 萬元，廠商乙報價 22 萬元。委員會決議「同意研究」，請管委會再向第三家廠商詢價，本案尚未核准，不得視為已通過。
二、中庭燈具更換：決議通過，由財委於 4 月底前完成採購。
三、社區年度旅遊：暫定 6 月，細節下次討論。
待辦：第三家廠商報價、燈具採購、旅遊提案。"""
R2 = """社區管理委員會第 42 次會議紀錄（4 月）
出席：主委、財委及委員共 6 人，監委請假。
一、管理室屋頂漏水維修案：第三家廠商丙報價 19 萬元，三家報價已齊。有委員建議先做局部防水，再評估全面翻修。決議：本案列入 5 月區分所有權人會議討論，目前仍未核准，不得先行發包。
二、中庭燈具更換：已完成採購，5 月初施工。
三、社區年度旅遊：提案日期 6 月 14 日，地點待定。
待辦：整理三家報價比較表、燈具施工通知、旅遊地點投票。"""
R3 = """社區管理委員會第 43 次會議紀錄（5 月）
出席：主委、財委、監委及委員共 8 人。
一、管理室屋頂漏水維修案：區分所有權人會議因人數不足流會，本案延至下次會議，仍未核准。主委提醒雨季將至，請先請廠商提供臨時防水方案報價。
二、中庭燈具更換：施工完成，驗收通過。
三、社區年度旅遊：投票結果宜蘭勝出，6 月 14 日出發。
待辦：臨時防水方案報價、下次區權會通知、旅遊報名表。"""
SUMMARY = "前三次會議：討論管理室屋頂維修案，三家廠商報價 18 至 22 萬元；中庭燈具已更換完成；年度旅遊 6 月 14 日去宜蘭。"
GOOD_HANDOFF = "維修案狀態：尚未核准，區權會流會延期，不得發包；待辦是臨時防水方案報價。燈具已驗收。旅遊 6 月 14 日宜蘭，報名表待發。"
enc = tiktoken.get_encoding("o200k_base")
n = lambda t: len(enc.encode(t))
records = [R1, R2, R3]
total = n("\n\n".join(records))
out = {"date": datetime.date.today().isoformat(), "encoding": "o200k_base",
       "records": [{"chars": len(r), "tokens": n(r)} for r in records],
       "all_three": {"chars": sum(len(r) for r in records), "tokens": total},
       "summary": {"text": SUMMARY, "chars": len(SUMMARY), "tokens": n(SUMMARY),
                   "keeps_not_approved": ("尚未核准" in SUMMARY) or ("未核准" in SUMMARY)},
       "good_handoff": {"text": GOOD_HANDOFF, "chars": len(GOOD_HANDOFF), "tokens": n(GOOD_HANDOFF),
                        "keeps_not_approved": "尚未核准" in GOOD_HANDOFF},
       "fits": {}}
for window in [200_000, 1_000_000]:
    per = total / 3
    out["fits"][str(window)] = {"records_of_this_size": int(window // per), "years_of_monthly_meetings": round(window / per / 12, 1)}
json.dump(out, open("demo-context.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
```

注意：`all_three.tokens` 是三份用兩個換行接起來一起編碼的數（535），不是三份各自的和（180 + 188 + 167 = 535，這次剛好相等）。`fits` 的算式是 視窗 ÷（535 ÷ 3），份數取整數，年數是份數 ÷ 12 取一位小數。

## 輸出（demo-context.json，逐字）

```json
{
 "date": "2026-09-30",
 "encoding": "o200k_base",
 "records": [
  {
   "chars": 198,
   "tokens": 180
  },
  {
   "chars": 217,
   "tokens": 188
  },
  {
   "chars": 189,
   "tokens": 167
  }
 ],
 "all_three": {
  "chars": 604,
  "tokens": 535
 },
 "summary": {
  "text": "前三次會議：討論管理室屋頂維修案，三家廠商報價 18 至 22 萬元；中庭燈具已更換完成；年度旅遊 6 月 14 日去宜蘭。",
  "chars": 62,
  "tokens": 55,
  "keeps_not_approved": false
 },
 "good_handoff": {
  "text": "維修案狀態：尚未核准，區權會流會延期，不得發包；待辦是臨時防水方案報價。燈具已驗收。旅遊 6 月 14 日宜蘭，報名表待發。",
  "chars": 62,
  "tokens": 60,
  "keeps_not_approved": true
 },
 "fits": {
  "200000": {
   "records_of_this_size": 1121,
   "years_of_monthly_meetings": 93.5
  },
  "1000000": {
   "records_of_this_size": 5607,
   "years_of_monthly_meetings": 467.3
  }
 }
}
```

## 影片裡怎麼用

| 影片 | 數字 | 出處 |
| --- | --- | --- |
| `desk-stats`（stats）| 535 token；178 平均每份；1,121 份、約 93 年；5,607 份、約 467 年 | `all_three.tokens`、535 ÷ 3、`fits` |
| 旁白 `three-records-desk` | 六百零四個字元 | `all_three.chars` |
| `two-texts`（code）| 壞摘要 62 字元 55 token；好交接 62 字元 60 token；差別在「尚未核准」 | `summary`、`good_handoff` |
| 旁白 `sticky-note-falls` | token 數只差五個 | 60 − 55 |
| 旁白 `three-stamped`、`calendar-three-meetings` | 三次都尚未核准；同意研究／列入區權會／流會延期 | 三份紀錄全文 |

二十萬與一百萬 token 是官方文件列出的兩個視窗級距（見 `claims.md` c6），只放字卡並標「以官網為準」；換一種編碼或換一個版本的 tiktoken，數字都要重算。
