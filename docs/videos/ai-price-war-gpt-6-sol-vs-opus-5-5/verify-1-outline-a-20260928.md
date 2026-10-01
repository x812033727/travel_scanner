# verify-1 — ai-price-war-gpt-6-sol-vs-opus-5-5

數值查核（2026-09-28，官方頁以編輯 User-Agent 抓取）。這一輪是撰稿者自查的數值與結構核對；產線的獨立查核關卡（換一個模型、新的 session）在發布前仍應照 AUTOMATION.md 跑一次。

| # | 說法 | 出處 | 判定 | before → after |
| --- | --- | --- | --- | --- |
| c1 | GPT-6 Sol 2／10 | developers.openai.com/api/docs/pricing | CONFIRMED | — |
| c2 | GPT-6 Luna 0.10／0.50，快取 0.01 | 同上 | CONFIRMED | — |
| c3 | Opus 5.5 4／20，快取讀取 0.20 | anthropic.com/pricing | CONFIRMED | — |
| c4 | 「50% vs GPT-5.6 promotional pricing」 | openai.com/index/introducing-gpt-6-sol-and-luna | CONFIRMED | 站內文章 2026-09-26 引用；公告頁本次代理抓取為 403，改以站內文章與 changelog 核對，撰稿日用瀏覽器再確認一次 |
| c5 | Opus 5.5 牌價降 20%、快取降 60%、成本估計 40% | anthropic.com/claude-opus-5-5 | CONFIRMED | 原文「Input and output tokens are $4 and $20 per million, 20% less than Opus 5」「40% less than Opus 5 on typical workloads」 |
| c6 | 快取讀取兩家皆 0.20 | 兩家定價頁 | CONFIRMED | — |
| c7 | Gemini 3.8 Flash 0.75／3.75，促銷至 2026-12-31 | ai.google.dev/gemini-api/docs/pricing | CONFIRMED | 原文「$0.75 through December 31, 2026. $1.50 starting January 1, 2027」 |
| c8 | Opus 5 對照 5／25／0.50 | anthropic.com/claude-opus-5-5（反推） | CHANGED→保留 | 直接價目表未見 Opus 5；由官方 20%／60% 降幅反推，與站內文章一致，c8 已註明 |
| c9 | 代理型 Sol 帳單 73.6，輸出佔 54%、快取佔 13% | 實算 | CONFIRMED | 12M×2＋48M×0.2＋4M×10＝24＋9.6＋40＝73.6；40÷73.6＝54.3%；9.6÷73.6＝13.0% |
| c11 | Gemini Flash 促銷價 2027-01-01 起漲 1.50／7.50 | gemini 定價頁 | CONFIRMED | — |

表格帳單全部重算通過（Sol 20／74／500、Luna 1／3.7／25、Opus 5.5 40／138／1000、Sonnet 5 20／74／500、Gemini 3.8 Flash 7.5／28／188）。

## 會很快過期

- GPT-5.6 Sol 促銷價「至少到 2026-11-21」；Gemini 3.8 Flash 促銷價到 2026-12-31。這兩個日期過了要回填。
- Opus 5 是否仍可見於定價頁（見 claims.md 的存疑）。

## 意見與立場

- 站主觀點段落標了「套用立場：1、2、6」，腳本裡的判斷（先算帳再換、看牌價不看百分比）與立場一致，且都標成建議而非投資指示。無未標記的個人經驗。

## 我懷疑但沒動的事

- 「便宜五成／四成」的口語化：narration 用「五成」「四成」「兩成」對應 50%／40%／20%，是刻意讓 TTS 好唸，數字意義不變。
