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
  - apps/api/app/guides/content/crypto-news-taiwan-vasp-act-20260630.json
  - apps/web/public/guides/crypto-news-taiwan-vasp-act-20260630
  - apps/api/app/guides/content/crypto-news-mica-transition-ends-20260701.json
  - apps/web/public/guides/crypto-news-mica-transition-ends-20260701
  - apps/api/app/guides/content/crypto-news-sec-crypto-interpretation-20260323.json
  - apps/web/public/guides/crypto-news-sec-crypto-interpretation-20260323
  - apps/api/app/guides/content/crypto-news-sec-regulation-crypto-assets-20260821.json
  - apps/web/public/guides/crypto-news-sec-regulation-crypto-assets-20260821
  - apps/api/app/guides/content/crypto-news-eba-psd2-mica-20260212.json
  - apps/web/public/guides/crypto-news-eba-psd2-mica-20260212
  - apps/api/app/guides/content/crypto-news-genius-act-occ-20260302.json
  - apps/web/public/guides/crypto-news-genius-act-occ-20260302
  - apps/api/app/guides/content/crypto-news-stablecoin-aml-20260410.json
  - apps/web/public/guides/crypto-news-stablecoin-aml-20260410
  - apps/api/app/guides/content/crypto-news-fdic-genius-act-20260410.json
  - apps/web/public/guides/crypto-news-fdic-genius-act-20260410
  - apps/api/app/guides/content/crypto-news-ncua-genius-act-20260518.json
  - apps/web/public/guides/crypto-news-ncua-genius-act-20260518
  - apps/api/app/guides/content/crypto-news-jfsa-working-group-20260216.json
  - apps/web/public/guides/crypto-news-jfsa-working-group-20260216
  - apps/api/app/guides/content/crypto-news-jfsa-cybersecurity-20260723.json
  - apps/web/public/guides/crypto-news-jfsa-cybersecurity-20260723
  - apps/api/app/guides/content/crypto-news-2026-index.json
  - apps/web/public/guides/crypto-news-2026-index
  - docs/crypto-news-2026
---

# News batch 4.1: crypto regulation, technology and industry news

## 站主圈選結果（2026-09-16）

站主的指示是「**幣圈和科技的先全部寫，AI 挑補漏那幾則**」。

**幣圈：候選清單 C1–C11 全部寫，11 篇。**

C6–C9 是美國 GENIUS Act 的四個主管機關版本，候選清單原本寫「可以合成一篇」。
站主說全部寫，所以**四篇分開**，各自寫自己主管機關管到誰、要求什麼；
四篇互相連結，不要四篇重複解釋一次 GENIUS Act 是什麼。

**沒有納入**：新加坡 MAS 那則（這個容器連不到 MAS，兩個網址都回 service unavailable）。
要寫必須在別的環境先驗過，現在納入就是照抄線索。
以太坊 2026 年升級那則維持 ❌ 查否：官方把日期列為 TBD，整合站的 Q3 2026 沒有官方依據。

| 代號 | 事件日 | slug | 題目 |
| --- | --- | --- | --- |
| C1 | 2026-06-30 | `crypto-news-taiwan-vasp-act-20260630` | 台灣《虛擬資產服務法》三讀通過 |
| C2 | 2026-07-01 | `crypto-news-mica-transition-ends-20260701` | 歐盟 MiCA 過渡期結束 |
| C3 | 2026-03-23 | `crypto-news-sec-crypto-interpretation-20260323` | CFTC 與 SEC 聯名的加密資產證券法解釋令 |
| C4 | 2026-08-21 | `crypto-news-sec-regulation-crypto-assets-20260821` | SEC 提出 Regulation Crypto Assets（草案） |
| C5 | 2026-02-12 | `crypto-news-eba-psd2-mica-20260212` | EBA 對 PSD2 與 MiCA 銜接的意見書 |
| C6 | 2026-03-02 | `crypto-news-genius-act-occ-20260302` | GENIUS Act 落地：OCC |
| C7 | 2026-04-10 | `crypto-news-stablecoin-aml-20260410` | 穩定幣發行商的洗錢防制與制裁遵循 |
| C8 | 2026-04-10 | `crypto-news-fdic-genius-act-20260410` | GENIUS Act 落地：FDIC |
| C9 | 2026-05-18 | `crypto-news-ncua-genius-act-20260518` | GENIUS Act 落地：NCUA |
| C10 | 2026-02-16 | `crypto-news-jfsa-working-group-20260216` | 日本 FSA 金融審議會工作小組報告 |
| C11 | 2026-07-23 | `crypto-news-jfsa-cybersecurity-20260723` | 日本 FSA：加密資產業者的資安問題與對策 |

`scope` 已經照這份清單逐篇填好（每篇兩行）。工作區是 `docs/crypto-news-2026/`。

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
