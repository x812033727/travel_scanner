# 批次 4.6（2026-09-18 起的新聞，只做 zh-TW）：對既有規格的差異

批次 4.6 沿用 4.1～4.5 的代理規格（`agents/`＝幣圈、`agents/tech/`＝科技、`agents/ai/`＝AI）與
[`DELTA-4-5.md`](DELTA-4-5.md) 的全部規則；只有下面幾件事不同或要再說一次。
**這份文件的規則優先於各垂直規格與 DELTA-4-5 裡與它衝突的句子。**

1. **只做 zh-TW。** 站主 2026-09-20 決定。內容包 `locales` 只有 `zh-TW`；研究紀錄**沒有** `translations` 欄位；
   沒有翻譯、沒有逐語審稿階段。規格裡凡是「翻譯代理」「逐語審稿」「hero_label 的五語」「圖檔五語」的段落一律跳過；
   圖檔只出 zh-TW 一份。**自檢一律不帶 `--full`**：`check_article.py <slug>`（出圖後 `check_article.py <slug> --assets`）。
   `--full` 只多加四個翻譯的檢查（腳本文件字串第 3–4 行），對 zh-TW-only 文章必然 FAIL，且不帶它不會漏掉任何 zh-TW 原文與研究紀錄的檢查。
2. **研究紀錄由專責的研究代理寫，不是探索代理。** 探索代理只交候選清單（站主圈選用）；圈選後每個 slug 一位 opus 研究代理，
   照 4.5 的 schema（範例 `docs/ai-news-2026-09-late/research/ai-news-anthropic-pace-metrics-20260917.json`）寫成 JSON。
   最終版放在各垂直工作區（同 DELTA-4-5 第 7 條）：AI `docs/ai-news-2026-09-late/research/`、
   科技 `docs/tech-news-2026/research/`、幣圈 `docs/crypto-news-2026/research/`。那一份對撰稿與查核**都有拘束力**：
   `must_not_write`、`not_said`、`unverified_or_excluded`、`live_data_warnings`、`sources[]` 照 4.3／4.5 的規則處理。
3. **沒有前期修正清單**（同 4.5 第 1 條）：`corrections_applied` 寫 `[]`。
4. **`display_order` 照指派訊息**，由 `check_article.py` 的 `RELATED` 順序決定：AI 接 **167** 起、科技接 **317** 起、幣圈接 **214** 起。

   | 垂直 | slug | display_order |
   | --- | --- | --- |
   | AI | `ai-news-anthropic-accenture-evaluation-20260918` | 167 |
   | AI | `ai-news-openai-australia-youth-safety-20260918` | 168 |
   | AI | `ai-news-gemini-notebook-study-tools-20260918` | 169 |
   | AI | `ai-news-kimi-k3-bedrock-20260918` | 170 |
   | 科技 | `tech-news-npm-stage-only-tokens-20260918` | 317 |
   | 科技 | `tech-news-cisa-kev-linux-kernel-20260918` | 318 |
   | 科技 | `tech-news-windows-cloud-rebuild-20260918` | 319 |
   | 科技 | `tech-news-iphone-duo-dev-resources-20260918` | 320 |
   | 幣圈 | （OCC 三家穩定幣信託銀行，slug 依研究紀錄） | 214 |
   | 幣圈 | （EBA 第三方風險最終指引，slug 依研究紀錄） | 215 |
   | 幣圈 | （SEC Woodcock 演講，slug 依研究紀錄） | 216 |

5. **第一個結尾連結**：索引標題**不改**，逐字照抄（同 DELTA-4-5 第 3 條）：
   - AI：`2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用` → `https://mokaair.com/zh-TW/life/ai-news-2026-january-september-index`
   - 科技：`2026 年科技新聞總整理：硬體、平台、電信與法規的重點` → `https://mokaair.com/zh-TW/life/tech-news-2026-index`
   - 幣圈：`2026 年加密貨幣新聞總整理：法規、技術與產業的重點` → `https://mokaair.com/zh-TW/life/crypto-news-2026-index`
6. **第二個結尾連結**指向指派訊息給的**既有已發布**文章，text 打開那個內容包抄它 zh-TW 的 `title`，逐字相同；
   `check_article.py` 對它不應有 FAIL。已定的：Accenture → `ai-news-pace-the-frontier-20260912`；
   iPhone Duo 開發資源 → `tech-news-iphone-duo-20260909`；OCC → `crypto-news-genius-act-occ-20260302`；
   EBA → `crypto-news-eba-psd2-mica-20260212`。其餘在指派訊息裡給。
7. **事件日與查核日**同 DELTA-4-5 第 5、6 條（台北時間；slug 後綴、`news_date`、正文第一段三者一致）。
   一個已裁決的例外要照抄、不要重新推導：**`ai-news-anthropic-accenture-evaluation-20260918` 的事件日是 2026-09-18**——
   頁面自印 Sep 18, 2026，新聞室 `publishedOn` 2026-09-18T16:00:00Z 是整點排程佔位（換算台北恰為 09-19 00:00），
   沿用上一輪對 OpenAI `00:00` 佔位時刻「不可換算」的判例；理由已寫在該篇研究紀錄的 `event_date_basis`。
8. **兩則「更新既有文章」不是新文章**：`tech-news-taiwan-matsu-cable-tm4-20260918`（補馬祖 5G 示範，moda 新聞稿 20670）與
   `tech-news-apple-september-hardware-20260909`（補 9/18 全球開賣）。更新代理只做三件事：讀既有內容包與新的一手來源、
   **只加一節**（其餘一字不動，包含 `display_order`、`news_date`、既有 sources）、把新來源加進 `sources[]` 並在研究紀錄補一段。
   `check_article.py --full` 要過；匯入時這兩篇是 `update`，要與 11 篇新文章同一次 `--slug` 匯入。
9. **網路請求**同 DELTA-4-5 第 9 條：UA 一律 `Mokaair-editorial`，**任何請求的 UA、標頭、查詢字串、表單都不得帶入任何人的 email 或個人資料**；
   `openai.com/index/*` 的 403 是間歇性的。另加一條：**NCC 官網已改成 SPA**，舊 `news.aspx` 網址失效，本批沒有 NCC 消息；
   不要拿 NCC 舊網址當來源，也不要猜它的 API 路徑。
10. **三則併一篇**：`ai-news-gemini-notebook-study-tools-20260918` 以 9/18 開學工具公告為骨架，
    「學校與企業開放（歐盟排除、個人帳號全球可用）」與「Expert Intelligence（送書限美國 18+）」各一段。
    時間線寫成「9/15 消費端公布、9/18 對企業與學校公告開放條件」，**不能寫成 9/18 才發表**。
