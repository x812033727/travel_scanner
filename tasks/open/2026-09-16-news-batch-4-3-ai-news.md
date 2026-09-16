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
  - docs/ai-news-2026-09-late
---

# News batch 4.3: AI news catch-up and backfill

## Why

既有 38 篇 `ai-news-*` 的事件日止於 2026-09-14，查核止於 09-15。
這張票補兩種：**9/15 起的缺口**，以及 **1/1 起真正沒寫過的事件**。

## 動筆前必讀

[`docs/news-2026-batch-4/ai.md`](../../docs/news-2026-batch-4/ai.md) 裡有一張
**由內容包直接產生的既有篇目表**（38 篇的 slug 與 zh-TW 標題）。
逐一比對過再定題，補漏批次最容易重寫別人寫過的事。

## 候選題目

- **9/15 缺口已驗**：Gemini 3.8 Live 與 3.8 Live Extended Thinking（Google 官方頁，
  97 種語言、逐項開放範圍，但**官方沒說地區**，要照實寫）。
- **NVIDIA 併購 Hugging Face（9/3，$12,930,300,000）** 已驗。既有 38 篇沒有任何一篇寫併購。
- **10 則已由 OpenAI 官方 feed 確認日期**、內容待讀原文，含 3/19 併購 Astral
  （`uv`／`ruff` 的開發商，本站 API 就在用）、6/8 的 S-1 送件
  （**角度必須是「對使用者代表什麼」，不可寫成投資題材**）。
- **次要新聞 8 則**（8/1–9/16），含 ChatGPT 廣告那條線、ChatGPT for Teens、
  Zero Data Retention。

**❌ 已查否**：OpenAI 在 9/15–9/16 沒有發布任何消息（官方 feed 最後一筆是 9/14）。
整合站說的「Microsoft MAI／Altman 談 IPO」兩則都拿不到合格一手來源。

## 索引要改，但 slug 不能改

`ai-news-2026-january-september-index` 的 slug **永遠不動**。要改的是標題、
description 與月份表格，而且**篇數要拿掉**（站主 2026-09-16 的決定：
讀者看得到的地方不顯示會增加的數字）。

**⚠️ 改標題會波及 30 個內容包、142 份語系文件**的連結文字（2026-09-16 實測）。
動手前重數一次，並在 scope 裡把那 30 個 slug 逐一列出。
改的時候**走 JSON 結構**，不要對檔案下正規表示式。

## 這張票還不能認領

`tasks/open/2026-09-15-content-summary-howto-and-life`（`in-progress`，
scope 是**整個 `apps/api/app/guides/content` 目錄**）擋住所有內容包任務。
它的認領在 **2026-09-17T03:39Z** 變 stale，屆時才能 claim。
**不要用 `--force` 繞過**——那條規則正是用來擋兩個 agent 互相覆蓋的。

## scope 還沒填完

目前只有工作區目錄。**站主圈完題目之後**，要把每篇的兩行路徑補進 `scope`：

```
apps/api/app/guides/content/<slug>.json
apps/web/public/guides/<slug>
```

比照 `tasks/done/2026-09-15-ai-news-batch-3-seven-mid.md`。
**絕對不要用整個 `content/` 目錄當 scope**，否則就變成現在擋住這張票的那個問題。

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
