---
id: 2026-09-16-news-batch-4-3-ai-news
title: News batch 4.3: AI news catch-up and backfill
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-16T13:21:40Z
completed_at:
branch:
depends_on:
  - 2026-09-16-news-batch-4-0-crypto-and
scope:
  - apps/api/app/guides/content/ai-news-openai-astral-20260319.json
  - apps/web/public/guides/ai-news-openai-astral-20260319
  - apps/api/app/guides/content/ai-news-openai-funding-20260331.json
  - apps/web/public/guides/ai-news-openai-funding-20260331
  - apps/api/app/guides/content/ai-news-gpt-55-instant-20260505.json
  - apps/web/public/guides/ai-news-gpt-55-instant-20260505
  - apps/api/app/guides/content/ai-news-chatgpt-ads-20260505.json
  - apps/web/public/guides/ai-news-chatgpt-ads-20260505
  - apps/api/app/guides/content/ai-news-frontier-governance-20260528.json
  - apps/web/public/guides/ai-news-frontier-governance-20260528
  - apps/api/app/guides/content/ai-news-openai-s1-20260608.json
  - apps/web/public/guides/ai-news-openai-s1-20260608
  - apps/api/app/guides/content/ai-news-openai-broadcom-chip-20260624.json
  - apps/web/public/guides/ai-news-openai-broadcom-chip-20260624
  - apps/api/app/guides/content/ai-news-chatgpt-financial-services-20260910.json
  - apps/web/public/guides/ai-news-chatgpt-financial-services-20260910
  - apps/api/app/guides/content/ai-news-gpt-live-1-api-20260910.json
  - apps/web/public/guides/ai-news-gpt-live-1-api-20260910
  - apps/api/app/guides/content/ai-news-chatgpt-storage-scale-20260911.json
  - apps/web/public/guides/ai-news-chatgpt-storage-scale-20260911
  - apps/api/app/guides/content/ai-news-gemini-38-live-20260915.json
  - apps/web/public/guides/ai-news-gemini-38-live-20260915
  - apps/api/app/guides/content/ai-news-nvidia-hugging-face-20260903.json
  - apps/web/public/guides/ai-news-nvidia-hugging-face-20260903
  - docs/ai-news-2026-09-late
---

# News batch 4.3: AI news catch-up and backfill

## 站主圈選結果（2026-09-16）

站主的指示是「**幣圈和科技的先全部寫，AI 挑補漏那幾則**」。

**AI：只寫補漏，12 篇。**

核心是候選清單「1/1 起的補漏」那 10 則（B1–B10，全部來自 OpenAI 官方 feed 的確認日期）。
另外保留兩則，因為它們是站主最初就確認的範圍、而且同樣是缺口：
**A1 Gemini 3.8 Live（9/15）**補的是「AI 新聞查核止於 9/14」那個缺口，
**A3 NVIDIA 併購 Hugging Face（9/3）**是既有 38 篇裡完全沒有的併購題材。
候選清單裡的 A2（同日開發者側）**併進 A1**，不單獨成篇。

**索引沿用既有 slug** `ai-news-2026-january-september-index`，URL 不動，
只改五語的 title／description 與月份表格。

### ⚠️ 這 12 篇裡有 10 篇的來源被擋，開稿前先看研究結果

`openai.com/index/*` 在這個容器**對所有客戶端都回 403**（curl、WebFetch、
甚至 headless Chromium 都一樣，是 Cloudflare 擋的），`help.openai.com` 也是 403。
官方 feed（`openai.com/news/rss.xml`）可用，但每則只有約 150 字元的官方描述。

**這不代表可以改用整合站。** BRIEF 的規則是「查到的事實如果只存在於被擋的頁面後面，那就不寫」。
研究階段正在逐篇試官方替代管道（Astral 自己的部落格、Broadcom 新聞稿、
EDGAR 全文檢索 API、`cdn.openai.com` 的資產路徑、`platform.openai.com` 的 API 文件），
**每篇會回報 full／partial／blocked**。blocked 的篇目要回報給站主決定砍掉或改角度，
不可以硬寫。

| 代號 | 事件日 | slug | 題目 |
| --- | --- | --- | --- |
| B1 | 2026-03-19 | `ai-news-openai-astral-20260319` | OpenAI 併購 Astral（uv／ruff） |
| B2 | 2026-03-31 | `ai-news-openai-funding-20260331` | OpenAI 新一輪募資 |
| B3 | 2026-05-05 | `ai-news-gpt-55-instant-20260505` | GPT-5.5 Instant 成為預設模型 |
| B4 | 2026-05-05 | `ai-news-chatgpt-ads-20260505` | ChatGPT 廣告怎麼賣（含 8/11、8/18 兩則） |
| B5 | 2026-05-28 | `ai-news-frontier-governance-20260528` | OpenAI Frontier Governance Framework |
| B6 | 2026-06-08 | `ai-news-openai-s1-20260608` | 保密送件 S-1（不可寫成投資題材） |
| B7 | 2026-06-24 | `ai-news-openai-broadcom-chip-20260624` | OpenAI 與 Broadcom 的推論晶片 |
| B8 | 2026-09-10 | `ai-news-chatgpt-financial-services-20260910` | ChatGPT for Financial Services（帶 finance，必附免責） |
| B9 | 2026-09-10 | `ai-news-gpt-live-1-api-20260910` | GPT-Live-1 進 API |
| B10 | 2026-09-11 | `ai-news-chatgpt-storage-scale-20260911` | 十億使用者的儲存架構 |
| A1 | 2026-09-15 | `ai-news-gemini-38-live-20260915` | Gemini 3.8 Live 與 Extended Thinking（併入開發者側那篇） |
| A3 | 2026-09-03 | `ai-news-nvidia-hugging-face-20260903` | NVIDIA 併購 Hugging Face |

`scope` 已經照這份清單逐篇填好（每篇兩行）。工作區是 `docs/ai-news-2026-09-late/`。

## Why

既有 38 篇 `ai-news-*` 的事件日止於 2026-09-14，查核止於 09-15。
這張票補兩種：**9/15 起的缺口**，以及 **1/1 起真正沒寫過的事件**。

## 動筆前必讀

[`docs/news-2026-batch-4/ai.md`](../../docs/news-2026-batch-4/ai.md) 裡有一張
**由內容包直接產生的既有篇目表**（38 篇的 slug 與 zh-TW 標題）。
逐一比對過再定題，補漏批次最容易重寫別人寫過的事。

## 索引要改，但 slug 不能改

`ai-news-2026-january-september-index` 的 slug **永遠不動**。要改的是標題、
description 與月份表格，而且**篇數要拿掉**（站主 2026-09-16 的決定：
讀者看得到的地方不顯示會增加的數字）。

**⚠️ 改標題會波及 30 個內容包、142 份語系文件**的連結文字（2026-09-16 實測）。
動手前重數一次，並在 scope 裡把那 30 個 slug 逐一列出。
改的時候**走 JSON 結構**，不要對檔案下正規表示式。

## scope 已填好，但認領還要等兩件事

`scope` 已經照上面的圈選結果逐篇填好。認領之前還缺兩件事：

1. **`depends_on` 的 4.0 還沒 done**（`2026-09-16-news-batch-4-0-crypto-and`，
   目前 `review`，等 PR #536 合併）。詞彙、migration 與財經免責 lint 都在那張票裡，
   沒有它寫出來的內容包過不了 lint。
2. **`apps/api/app/guides/content` 整個目錄被
   `2026-09-15-content-summary-howto-and-life`（`in-progress`）持有**，
   在 2026-09-17T03:39Z 變 stale。

**兩件都不要用 `--force` 繞過。** 第 1 條會讓內容包 lint 失敗，
第 2 條正是用來擋兩個 agent 互相覆蓋的規則。

在那之前可以做、而且已經在做的是**研究**：工作區目錄不在任何人的 scope 裡，
研究紀錄先寫在那裡，鎖一讓出來就能直接開稿。

## 流程

照 [`docs/news-2026-batch-4/BRIEF.md`](../../docs/news-2026-batch-4/BRIEF.md)：
一篇一個撰稿代理 → **獨立查核代理**（不可省：批次 3 每篇 56–102 條主張、
每篇都改了 15–38 處）→ 翻譯（五語）→ 逐語系審稿 → 圖像 → 索引 → 驗證。

每篇必帶 `summary` 與 `faq` 區塊——這批是站上第一批全面帶的
（845 篇 life 只有 5 篇有 summary、1 篇有 faq）。

## 已知會擋路的兩件事

- **這個容器沒有 headless 瀏覽器**，而 `build_assets.py` 要靠它把 hero SVG 轉成 JPEG。
  圖像階段開始前先確認 Chromium 可用（環境有 `/opt/pw-browsers/chromium`，
  但 `build_assets.py` 目前找的是 Edge／Chromium 的路徑，要確認能不能指過去）。
- **`pack_cli ingest` 會拒絕帶子主題的內容包**（`_known_topics()` 只回父主題）。
  批次 3 是直接寫進 `content/` 不走 `ingest`，這批照做。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life    # 0 error
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py
npm run check:tasks
```
