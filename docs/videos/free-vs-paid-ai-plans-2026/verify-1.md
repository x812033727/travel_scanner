# verify-1 — free-vs-paid-ai-plans-2026

事實查核（2026-09-28）。撰稿者自查；產線的獨立查核關卡在發布前仍應照 AUTOMATION.md 跑一次，而且**這支必須在能連上 openai.com 的環境跑**。

| # | 說法 | 出處 | 判定 | before → after |
| --- | --- | --- | --- | --- |
| c2 | ChatGPT 免費版每天 3 檔 | OpenAI 說明中心 | NOT FOUND（403） | 保留，標 PENDING |
| c3 | Claude 5 小時重置、每週上限跨所有模型 | Claude 說明中心 | CHANGED | 刪掉「網頁、桌面、手機與 Claude Code 共用同一額度」：當天頁面沒找到 → 改成「每週上限所有模型一起算」 |
| c4 | Gemini 上下文 32k／128k／100 萬 | Gemini Apps Help | CONFIRMED | — |
| c5 | ChatGPT Go 8、Plus 20 | OpenAI | NOT FOUND（403） | 保留，標 PENDING |
| c6 | Claude Pro 17／20、含 Claude Code | Anthropic 定價頁 | CONFIRMED | — |
| c7 | AI Plus NT$165、2 倍、Flow 200、只列月費 | Gemini 台灣頁 | CONFIRMED | — |
| c8 | AI Pro NT$650、4 倍、Flow 1,000；美國 4.99／19.99 | Gemini 台灣頁、美國頁 | CONFIRMED | — |
| c11 | Claude Max 100 起、Pro 的 5 或 20 倍 | Anthropic 定價頁 | CONFIRMED | — |
| c12 | 月繳、隨時取消 | 各家取消說明頁 | NOT FOUND 當天（OpenAI 403） | 依站內文章，標 PENDING |

changed_facts：1（已改）；PENDING：3（c2、c5、c12），合成旁白前要清掉。

## 會很快過期

- 三家方案與價格；Gemini 台灣頁的點數與用量倍數。

## 意見與立場

- 站主觀點「套用立場：1、5、6」：從卡住的額度出發、先用滿免費版兩週、不下單一結論，腳本一致。
