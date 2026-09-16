---
id: 2026-09-16-news-batch-4-1-crypto-regulation
title: News batch 4.1: crypto regulation, technology and industry news
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-16T13:21:39Z
completed_at:
branch:
depends_on:
  - 2026-09-16-news-batch-4-0-crypto-and
scope:
  - docs/crypto-news-2026
---

# News batch 4.1: crypto regulation, technology and industry news

## Why

站上目前**零篇**幣圈內容。這是全新的垂直領域，
詞彙（`crypto` 掛在 `finance` 底下）與免責機制（`finance_no_disclaimer`，error 級）
都由 PR #536 帶進來了，候選題目也查證完畢。

## 界線（站主定的，不是建議）

**只寫法規、技術與產業，不碰行情。** 明文禁止：幣價、漲跌幅、市值、交易量、
ETF 資金流、買賣時機、殖利率／質押報酬／空投、任何具體標的、交易所費率比較。
完整規則見 [`docs/news-2026-batch-4/crypto.md`](../../docs/news-2026-batch-4/crypto.md)。

**每篇必帶免責 callout**，逐字含該語言的標記字串
（`pack_ingest.FINANCE_DISCLAIMER_MARKERS`，五語各一）。
`finance_no_disclaimer` 是 **error**，CI 會擋。

**機器只擋得住樣板。**「有沒有變相推薦標的」「風險講得夠不夠」要人逐篇看，
這是這張票 Definition of done 的一部分，不要指望 lint。

## 候選題目

[`docs/news-2026-batch-4/candidates-crypto.md`](../../docs/news-2026-batch-4/candidates-crypto.md)
有 **11 則已回一手來源驗過**（C1–C11），含台灣《虛擬資產服務法》三讀、
歐盟 MiCA 過渡期結束、CFTC 與 SEC 聯名的解釋令、美國 GENIUS Act 四個機關的實施規則、
日本 FSA 兩則。**重要新聞的量已經到了。**

次要新聞目前 0 則——在「不碰行情」的界線內，8/1–9/16 查證後確實稀薄，
建議把窗口放寬到全年再挑份量輕的。

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
