---
id: 2026-09-16-news-batch-4-3-ai-news
title: News batch 4.3: AI news catch-up and backfill
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-17T22:16:02Z
created_at: 2026-09-16T13:21:40Z
completed_at: 2026-09-18T03:22:59Z
branch: claude/news-batch-4-3-ai
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
  - docs/news-2026-batch-4
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/ai-model-release-timeline-2026.json
  - apps/api/app/guides/content/ai-news-anthropic-threat-report-20260910.json
  - apps/api/app/guides/content/ai-news-chatgpt-health-20260107.json
  - apps/api/app/guides/content/ai-news-chatgpt-images-20-20260421.json
  - apps/api/app/guides/content/ai-news-chatgpt-work-20260709.json
  - apps/api/app/guides/content/ai-news-claude-fable-5-access-20260609.json
  - apps/api/app/guides/content/ai-news-claude-interactive-visuals-20260312.json
  - apps/api/app/guides/content/ai-news-claude-opus-46-20260205.json
  - apps/api/app/guides/content/ai-news-claude-sonnet-5-20260630.json
  - apps/api/app/guides/content/ai-news-deepseek-v41-flash-20260910.json
  - apps/api/app/guides/content/ai-news-gemini-31-pro-20260219.json
  - apps/api/app/guides/content/ai-news-gemini-36-flash-20260721.json
  - apps/api/app/guides/content/ai-news-gemini-omni-20260519.json
  - apps/api/app/guides/content/ai-news-gemini-personal-intelligence-20260114.json
  - apps/api/app/guides/content/ai-news-gemini-spark-20260519.json
  - apps/api/app/guides/content/ai-news-google-assistant-gemini-20260904.json
  - apps/api/app/guides/content/ai-news-gpt-53-codex-20260205.json
  - apps/api/app/guides/content/ai-news-gpt-54-20260305.json
  - apps/api/app/guides/content/ai-news-gpt-55-20260423.json
  - apps/api/app/guides/content/ai-news-gpt-56-sol-preview-20260626.json
  - apps/api/app/guides/content/ai-news-gpt-live-voice-20260708.json
  - apps/api/app/guides/content/ai-news-lyria-3-pro-20260325.json
  - apps/api/app/guides/content/ai-news-meta-muse-spark-20260408.json
  - apps/api/app/guides/content/ai-news-nvidia-rubin-20260105.json
  - apps/api/app/guides/content/ai-news-openai-agents-api-20260910.json
  - apps/api/app/guides/content/ai-news-pace-the-frontier-20260912.json
  - apps/api/app/guides/content/ai-news-project-glasswing-20260407.json
  - apps/api/app/guides/content/ai-news-qwen-35-20260216.json
  - apps/api/app/guides/content/ai-news-siri-ai-ios-27-20260914.json
  - apps/api/app/guides/content/ai-news-sources-to-follow.json
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
| B8 | 2026-09-10 | `ai-news-chatgpt-financial-services-20260910` | ChatGPT for Financial Services（**不掛 finance**，理由見 `ai.md`） |
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

## 進度（2026-09-18）

- [x] 12 篇 zh-TW 撰稿（sonnet）、每篇兩輪獨立查核（opus；第一輪 87–138 條主張、改 15–30 處，第二輪再改 6–25 處），報告在 `docs/news-2026-batch-4/factcheck-draft/ai-news-*.md`
- [x] 協調者通讀 12 篇、改 `hero.alt`／圖上文字、兩篇改標題（B4、B7），修訂記在 `coordinator-corrections.json`
- [x] 五語翻譯（sonnet ×12）、`translation_checks.py` 0 命中、逐語審稿 4 語 × 3 組（opus ×12，採用 429 筆，記在 `translation-corrections.json`）、文體修正（B7 ko、B5 ja 改回敬體）
- [x] 既有索引 `ai-news-2026-january-september-index` 原地改版（`update_index.py ai`：拿掉篇數、加 12 篇連結、五語新標題），連帶改 30 個既有包的連結文字（scope 已逐一列出）
- [x] `related`（延伸閱讀）、`pack_cli relink` ×12、`build_assets.py ai`（60 張圖＋contact sheet 已逐張看過）
- [x] 驗證：12 篇 `check_article.py --full --assets` 全 OK、`pack_cli lint --kind life` 0 error、內容測試 164 passed、`check:tasks` OK
- [x] 站主 2026-09-18 明確選「合併並發布」：PR #548 squash 為 `d5a97c6f`（樹與 PR head 相同）→ 部署 `deploy_20260918_031614`（03:16–03:19Z，無 migration，health 3/3、alembic `0080_crypto_and_tech_topics`、首頁 200）
  → `guides-import --slug` ×43 同一次匯入（先 `--dry-run --publish`：43 篇、create 60、update 147、無別的 slug、新篇全是 create 才 publish；`taxonomy_updated` 12、`failed: null`）
  → 正式站驗證：65 個網址（12 篇＋索引 × 5 語）全數 200、可索引、都在 sitemap、主圖 65 張 200；12 篇都有 `#article-summary` 與 FAQPage；索引標題已是「1 月至 9 月」、頁面上 50 個 ai-news 連結、沒有任何篇數字樣；
  既有文章（例 `ai-news-gpt-54-20260305`）指向索引的連結文字已更新；新篇的延伸閱讀已套上（例 gpt-live-1-api → gemini-38-live、gpt-live-voice、storage-scale）
- [ ] 留給站主決定的事（HANDOVER 第 1c 節；都是發布後仍可修訂的，不擋結案）

## 交接（2026-09-17）

（以下是開工前的狀態，留作紀錄。）還沒開始寫任何一篇。站主指定先交幣圈（4.1）驗收，幣圈目前的狀態與整條流程踩過的坑在
[`docs/news-2026-batch-4/HANDOVER.md`](../../docs/news-2026-batch-4/HANDOVER.md)；這張票照同一條線跑。
AI 垂直的索引是既有的 `ai-news-2026-january-september-index`（網址不變、原地改標題），`update_index.py` 裡 AI 那幾條
`TODO` 要先寫好；三篇 `partial` 的研究（`openai.com/index/*` 對所有客戶端回 403）開稿時若撐不起完整文章要回報站主。
代理規格在 `docs/news-2026-batch-4/agents/`。研究、獨立查核與 `corrections-ai.md` 都在 PR #544 裡，要等它合併。
因為停手而 `release`，不是做完。
