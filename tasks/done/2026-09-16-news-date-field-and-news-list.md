---
id: 2026-09-16-news-date-field-and-news-list
title: "News date field; news shown as a dated list, newest 20 on the lifestyle hub"
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-16T12:26:15Z
created_at: 2026-09-16T10:05:00Z
completed_at: 2026-09-16T23:54:09Z
branch: claude/news-date-list
depends_on: []
scope:
  - apps/api/app/guides/models.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/service.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/content_pack.py
  - apps/api/app/guides/search.py
  - apps/api/migrations/versions/0079_guide_news_date.py
  - apps/api/tests/test_guides_news_date.py
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides-admin.ts
  - apps/web/components/guides/news-list.tsx
  - apps/web/components/guides/news-list.test.tsx
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/components/guides/topic-hub-page.test.tsx
  - apps/web/components/guides/listing-toolbar.tsx
  - apps/web/app/[locale]/guides/[kind]/page.tsx
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/api/app/guides/content/ai-news-anthropic-threat-report-20260910.json
  - apps/api/app/guides/content/ai-news-chatgpt-free-thinking-20260806.json
  - apps/api/app/guides/content/ai-news-chatgpt-health-20260107.json
  - apps/api/app/guides/content/ai-news-chatgpt-images-20-20260421.json
  - apps/api/app/guides/content/ai-news-chatgpt-images-25-20260908.json
  - apps/api/app/guides/content/ai-news-chatgpt-work-20260709.json
  - apps/api/app/guides/content/ai-news-claude-fable-5-access-20260609.json
  - apps/api/app/guides/content/ai-news-claude-fable-51-20260901.json
  - apps/api/app/guides/content/ai-news-claude-interactive-visuals-20260312.json
  - apps/api/app/guides/content/ai-news-claude-opus-46-20260205.json
  - apps/api/app/guides/content/ai-news-claude-opus-5-20260724.json
  - apps/api/app/guides/content/ai-news-claude-sonnet-5-20260630.json
  - apps/api/app/guides/content/ai-news-deepseek-v41-flash-20260910.json
  - apps/api/app/guides/content/ai-news-eu-transparency-20260802.json
  - apps/api/app/guides/content/ai-news-gemini-31-pro-20260219.json
  - apps/api/app/guides/content/ai-news-gemini-36-flash-20260721.json
  - apps/api/app/guides/content/ai-news-gemini-38-flash-20260902.json
  - apps/api/app/guides/content/ai-news-gemini-live-20260826.json
  - apps/api/app/guides/content/ai-news-gemini-omni-20260519.json
  - apps/api/app/guides/content/ai-news-gemini-personal-intelligence-20260114.json
  - apps/api/app/guides/content/ai-news-gemini-spark-20260519.json
  - apps/api/app/guides/content/ai-news-google-assistant-gemini-20260904.json
  - apps/api/app/guides/content/ai-news-gpt-53-codex-20260205.json
  - apps/api/app/guides/content/ai-news-gpt-54-20260305.json
  - apps/api/app/guides/content/ai-news-gpt-55-20260423.json
  - apps/api/app/guides/content/ai-news-gpt-56-price-cut-20260730.json
  - apps/api/app/guides/content/ai-news-gpt-56-sol-preview-20260626.json
  - apps/api/app/guides/content/ai-news-gpt-6-astra-20260903.json
  - apps/api/app/guides/content/ai-news-gpt-live-voice-20260708.json
  - apps/api/app/guides/content/ai-news-lyria-3-pro-20260325.json
  - apps/api/app/guides/content/ai-news-lyria-35-gemini-20260904.json
  - apps/api/app/guides/content/ai-news-meta-muse-spark-20260408.json
  - apps/api/app/guides/content/ai-news-nvidia-rubin-20260105.json
  - apps/api/app/guides/content/ai-news-openai-agents-api-20260910.json
  - apps/api/app/guides/content/ai-news-pace-the-frontier-20260912.json
  - apps/api/app/guides/content/ai-news-project-glasswing-20260407.json
  - apps/api/app/guides/content/ai-news-qwen-35-20260216.json
  - apps/api/app/guides/content/ai-news-siri-ai-ios-27-20260914.json
  - docs/travel-guides.md
  - docs/article-architecture.md
  - tasks/open/2026-09-15-content-summary-howto-and-life.md
---

# News date field; news shown as a dated list, newest 20 on the lifestyle hub

## Why

站主看生活分享首頁的「最新新聞」區塊後要求：

1. 標題下那句「模型發布、價格變動與政策：只記錄查證過的事實與日期。」不用顯示。
2. 新聞要一條一條顯示，不是卡片。
3. 顯示**新聞日期**最新的前 20 條 —— 站主特別強調「不是更新日期，是新聞的日期」。
4. 「看全部」連到的 `/life/topics/ai-news` 也照同樣方式：依新聞日期由新到舊、一條一行。

現況：首頁取 `ai-news` 主題**依發布時間**的前 6 篇、畫成卡片。新聞是分批匯入的，同一批的發布時間幾乎一樣，
所以線上順序跟新聞本身的日期對不上（9/14、9/12、9/10、7 月、9/4…）。

資料庫沒有「新聞日期」。日期只編在 slug 尾巴（`ai-news-siri-ai-ios-27-20260914`）：`ai-news` 42 篇裡 38 篇有，
而且和描述裡寫的日期全部一致；另外 4 篇是沒有日期的常青文（總整理、時間軸、資訊來源、炒作與現實）。
站主選擇加一個正式欄位，而不是從網址推算。

## Definition of done

- [x] `guide_articles.news_date`（nullable date）＋migration；內容包、後台、公開 API 都帶這個欄位。
- [x] `GET /guides?sort=news`：`news_date` 由新到舊（沒有日期的排最後），再依發布時間、slug；游標可以翻頁不重複不漏。
- [x] 38 篇新聞內容包補上 `news_date`（等於 slug 尾巴的日期）並重新匯入。
- [x] 首頁「最新新聞」：沒有主題描述句、一條一行（日期＋標題）、依新聞日期最新 20 條、只列有日期的。
- [x] `/life/topics/ai-news`：依新聞日期一條一行；常青文沒有日期、排在最後；沒有排序切換。
- [x] 後台分類表單可以看與改「新聞日期」。

## Steps

- [x] API：model、migration、schemas（`ListSort` 加 `news`）、`public_list` 的排序與游標、summary／article／search 帶欄位、
      admin 建立與更新、內容包比對與寫入。
- [x] 測試：`tests/test_guides_news_date.py`（migration、排序、游標、後台、內容包日期與 slug 一致）。
- [x] Web：型別與 guard、`NewsList` 元件、首頁與主題頁、後台欄位與五語系字串。
- [x] 38 個內容包補欄位。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guides_news_date.py tests/test_guides.py tests/test_guides_content_pack.py
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

部署後以 `--slug` 限定匯入 38 篇（不帶 `--slug` 會發布暫緩的 206 篇），再看 `/zh-TW/life` 與 `/zh-TW/life/topics/ai-news`。

## Notes

**`news_date` 在後台更新裡是「沒送就不動」**，跟 `valid_until` 不同：後台儲存分類是整包 PUT，
如果沒送當成清空，舊版頁面或之後任何沒帶這個欄位的呼叫端存一次檔，就會把新聞日期洗掉。
要清空就明確送 `null`。

**migration 編號與別的分支撞號**：`claude/brave-hopper-8ezxba`（幣圈與科技新聞，2026-09-16 尚未開 PR）
也有 `0079_crypto_and_tech_topics`，同樣接在 `0078_guide_article_links` 之後。兩個都合併就會有兩個 head，
部署時 `alembic upgrade head` 會失敗。**後合併的那一個要把 `down_revision` 改成先合併的那一個**，
並把檔名與 revision id 往後編號；strict branch protection 要求分支跟上 main，CI 會在後合併的 PR 上抓到。

那個分支在做科技與幣圈新聞：它的新聞內容包也要帶 `news_date`，否則不會出現在依新聞日期的清單裡。
`tests/test_guides_news_date.py` 會擋下「slug 以日期結尾、掛 `ai-news`、卻沒有 `news_date`」的包；
新的新聞主題若要同樣呈現，把主題 slug 加進 `apps/web/lib/guides.ts` 的 `NEWS_TOPICS`。

`apps/api/app/guides/content` 被 `2026-09-15-content-summary-howto-and-life` 佔著，這張票只在 38 個包的頂層加一行，
站主已決定照做；以 `--force` claim 並在那張票留言。

做完後補記：

- 文件原本寫「讀者永遠看不到日期」（`docs/travel-guides.md`）。新聞清單是刻意的例外，理由寫進同一段：
  新聞發生的日期是新聞內容的一部分，發布時間只會讓仍然正確的文章看起來過時。
- `ListingToolbar` 的排序切換型別改成只有 `curated`／`latest`；`news` 不是選項，一般主題與旅遊列表收到
  `?sort=news` 會退回預設順序。
- 首頁在「部署完、還沒匯入」的空檔看不到新聞區塊（每篇 `news_date` 都還是 null），有測試固定這個行為；
  部署後要立刻匯入。
- 本機完整 API 測試 3,873 通過；`test_guides_autolink.py` 與 `test_warning_codes.py` 在 Windows 預設編碼下會紅，
  `PYTHONUTF8=1` 重跑就過，CI 是綠的。

2026-09-16 23:52 UTC 部署 `406ce742`（含 #537、#536 的 `0080_crypto_and_tech_topics`；對方已把它改接在
`0079_guide_news_date` 之後，alembic 單一 head `0080`）。部署前自動備份 `travel_scanner_predeploy_20260916_234901.dump`。
以 `--slug` 限定匯入 38 篇、不帶 `--publish`：dry-run 38 篇 taxonomy `update`、190 個語系版本 `unchanged`、0 新建；
套用 taxonomy_updated 38、published 0、failed 無。

正式站驗證（直接打容器內的 web 與 API）：`sort=news` 42 篇，38 篇有日期且由新到舊，4 篇常青文全在最後；
`/zh-TW/life` 新聞區塊 20 條全有日期、由新到舊、沒有主題描述句、沒有卡片；`/zh-TW/life/topics/ai-news`
一條一行、沒有排序切換，第 2 頁 18 條（14 條有日期、4 篇常青文在最後）；`/topics/ai-terms` 仍是卡片與排序切換；
`/guides/howto?sort=news` 退回卡片。截圖：桌機 1280 一行日期＋標題；手機 390 日期在上、標題在下，
`scrollWidth` 390、連結點擊高度 44px。

#540 帶上線的 `ai-model-comparison-table-2026` 內容包沒有匯入 —— 那張票寫明匯入時機由站主決定。
