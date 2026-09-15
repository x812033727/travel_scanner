# ai-search-llms-txt 查證記錄

查證日一律 **2026-09-14**。`實際讀取方式` 欄分兩種：

- **本次重讀** —— 這一輪收尾（把正文從 5,836 字砍到 2,835 字）時用 WebFetch 重新開過的頁面，或
  直接讀取的 repo 檔案。
- **沿用前查** —— 來源與 `checked_on` 由前一位代理在 2026-09-14 查妥並寫進 `pack.json`；本輪只做
  刪節，沒有新增任何主張，因此未重新抓取。砍字後每一句仍有來源支撐；失去支撐的來源已從
  `sources` 移除（見最後一節）。

## llms.txt 提案本身

| 主張 | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| 作者是 Jeremy Howard | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| 發表日期 2024 年 9 月 3 日 | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| 現在掛的是第二版（頁面標示 v2） | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| 定義：提議統一用一個 llms.txt 檔案，提供資訊協助代理使用這個網站 | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| 問題陳述：網頁為人而做、還原乾淨文字困難、每個浪費掉的 token 都是時間與金錢 | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| 唯一必填的區塊是專案／網站名稱的 H1 | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| 檔案清單每一項是 markdown 超連結，可接冒號與說明；Optional 一節可跳過 | https://llmstxt.org/ | 2026-09-14 | 沿用前查 |
| 分工：robots.txt 讓自動化工具知道哪些存取可接受，llms.txt 是代理按需使用 | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| 作者原本的預期是這個檔案主要用於推論而不是訓練（提案作者的觀察，非引擎資料） | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |
| `code` 區塊的範例骨架依原站規格整理，不是逐字複製 | https://llmstxt.org/ | 2026-09-14 | 本次重讀（WebFetch 原站） |

## 哪些引擎表態過

| 主張 | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| Google：「你不需要為了出現在 Google 搜尋（含生成式 AI 功能）而建立新的機器可讀檔案、AI 文字檔、標記或 Markdown，因為 Google 搜尋本身不使用它們」 | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | 2026-09-14 | 本次重讀（WebFetch，破除迷思一節） |
| Google：這麼做「不會傷害也不會幫助你在 Google 搜尋的能見度或排名，因為 Google 搜尋會忽略它們」 | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | 2026-09-14 | 本次重讀（WebFetch） |
| 該指南頁面標示的最後更新日期 2026-07-10（正文未使用，備查） | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | 2026-09-14 | 本次重讀（WebFetch） |
| 加上這段 llms.txt 註記的日期是 2026 年 6 月 15 日 | https://developers.google.com/search/updates | 2026-09-14 | 本次重讀（WebFetch，更新記錄該筆） |
| OpenAI 的爬蟲總覽頁通篇沒有把 llms.txt 寫成自家系統會讀取的檔案 | https://developers.openai.com/api/docs/bots | 2026-09-14 | 沿用前查 |
| Anthropic 說明中心的爬蟲說明同上 | https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler | 2026-09-14 | 沿用前查 |
| Perplexity 的爬蟲文件同上 | https://docs.perplexity.ai/docs/resources/perplexity-crawlers | 2026-09-14 | 沿用前查 |
| 這幾家的開發者文件站自己發布 llms.txt（發布者行為，不是消費行為） | https://llmstxt.org/ | 2026-09-14 | 本次重讀（提案原文背景一節點名 OpenAI、Anthropic、Gemini 的文件站） |

「沒有任何一家公布過自家系統會消費 llms.txt」是**查不到**的結論，不是任何一頁寫下的句子：以上三份
爬蟲文件加上 Google 那一份，都沒有這種說明。正文寫成「沒有表態不等於否認，但也不能當成證據」。

## robots.txt 與 RFC 9309

| 主張 | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| RFC 9309《Robots Exclusion Protocol》，2022 年 9 月，標準軌 | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-09-14 | 本次重讀（WebFetch 規範原文） |
| 「這些規則不是一種存取授權」 | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-09-14 | 本次重讀（WebFetch） |
| 「不能取代有效的內容安全措施」 | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-09-14 | 本次重讀（WebFetch） |
| robots.txt 主要用來避免網站被大量請求壓垮，不是讓網頁不出現在 Google 的機制；被擋住的網址如果有外部連結仍可能被建立索引 | https://developers.google.com/search/docs/crawling-indexing/robots/intro | 2026-09-14 | 沿用前查 |
| noindex 要生效，該網頁不能被 robots.txt 擋住，必須是爬蟲能存取的 | https://developers.google.com/search/docs/crawling-indexing/block-indexing | 2026-09-14 | 沿用前查 |

## 三類爬蟲的官方描述

| 主張 | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| Google-Extended：發布者用來管理抓到的內容是否可用於訓練未來的 Gemini 模型；不影響在 Google 搜尋的收錄，也不是排名訊號 | https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers | 2026-09-14 | 沿用前查 |
| 使用者觸發的擷取器通常會忽略 robots.txt 規則，因為取用由使用者要求 | https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers | 2026-09-14 | 沿用前查 |
| GPTBot 抓取可能用於訓練生成式 AI 基礎模型的內容 | https://developers.openai.com/api/docs/bots | 2026-09-14 | 沿用前查 |
| OAI-SearchBot 用於搜尋，讓網站出現在 ChatGPT 搜尋功能的結果中；退出者不會出現在 ChatGPT 的搜尋答案裡 | https://developers.openai.com/api/docs/bots | 2026-09-14 | 沿用前查 |
| ChatGPT-User 由使用者發起，robots.txt 規則可能不適用 | https://developers.openai.com/api/docs/bots | 2026-09-14 | 沿用前查 |
| ClaudeBot 收集可能有助於模型訓練的網頁內容；Claude-SearchBot 為改善搜尋結果品質而索引；Claude-User 代使用者取用 | https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler | 2026-09-14 | 沿用前查 |
| PerplexityBot 為了在 Perplexity 的結果中呈現並連結網站，且不用於為 AI 基礎模型抓取內容；Perplexity-User 通常忽略 robots.txt | https://docs.perplexity.ai/docs/resources/perplexity-crawlers | 2026-09-14 | 沿用前查 |
| Apple：停用 Applebot-Extended 的網頁仍可出現在搜尋結果裡（擋訓練 token 不影響收錄） | https://support.apple.com/en-us/119829 | 2026-09-14 | 沿用前查 |

## 本站目前的做法（repo 檔案，非外部來源）

| 主張 | 來源 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| 拒絕名單目前有 **11 個** user-agent：GPTBot、ClaudeBot、anthropic-ai、CCBot、Google-Extended、Applebot-Extended、Bytespider、Amazonbot、meta-externalagent、PerplexityBot、Diffbot | `apps/web/app/robots.ts` | 2026-09-14 | 本次直接讀檔（只讀，未修改），逐項數過 |
| ChatGPT-User 與 OAI-SearchBot 刻意不在名單上 | `apps/web/app/robots.ts` | 2026-09-14 | 本次直接讀檔（`CONTENT_HARVESTERS` 註解明寫 deliberately absent） |
| 給所有爬蟲的那一組允許整站，只擋 `/api/`、`/*/admin`、`/*/out/`、`/*/share/`、`/*/share-target`、`/*/line/`、`/*/account/confirm` | `apps/web/app/robots.ts` | 2026-09-14 | 本次直接讀檔 |
| 會員頁面保持可被抓取、改用頁面上的 noindex，理由就是「被擋的網址讀不到 noindex」 | `apps/web/app/robots.ts`（檔頭註解） | 2026-09-14 | 本次直接讀檔 |
| 取捨理由：拒絕收集頁面拿去訓練或把內容轉售成答案的爬蟲，放行代使用者取用並附出處的那一類 | `apps/web/app/robots.ts`（`CONTENT_HARVESTERS` 註解） | 2026-09-14 | 本次直接讀檔 |
| 代價：Google-Extended 是訓練專用 token，Googlebot 不會參考它 | 同上註解＋Google 常見爬蟲頁 | 2026-09-14 | 本次直接讀檔＋沿用前查 |

本站沒有做過任何曝光或引用量測，正文也沒有任何一句宣稱這份設定改變了本站的能見度。

## 這一輪刪掉的來源

砍字後沒有任何一句話再依賴它們，已從 `pack.json` 的 `sources` 移除（15 → 12）：

- `https://llmstxt.org/changes.html` —— 原本支撐「第二版另外建議提供 .md 版本、用連結關係宣告」
  那兩條清單項；清單砍掉後不再使用（「現在掛的是第二版」由原站首頁支撐）。
- `https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt` —— 原本支撐
  Lighthouse llms.txt 稽核那一段，整段刪除。
- `https://commoncrawl.org/ccbot` —— CCBot 現在只以名字出現在本站自己的拒絕名單裡，
  那一條由 `apps/web/app/robots.ts` 支撐，不需要 Common Crawl 的說明頁。

## 圖上的數字

`diagram-1.svg` 只畫標籤，唯一的數字是右下角製圖年份 2026，正文（含 `2026 年 9 月 14 日`）帶得到。
`hero.svg` 不放任何數字，只有一行 9 個字的標題。
