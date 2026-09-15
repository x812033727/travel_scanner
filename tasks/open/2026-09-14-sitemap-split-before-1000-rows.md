---
id: 2026-09-14-sitemap-split-before-1000-rows
title: sitemap 拆成 sitemap index：986 列，下一批 20 篇就破 1,000
status: review
priority: P1
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-15T15:42:44Z
created_at: 2026-09-14T23:07:00Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-14-claude-code-tutorial-center
  - 2026-09-14-pack-ingest-urlopen-scheme
scope:
  - apps/web/app/sitemaps
  - apps/web/app/llms.txt/route.ts
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/api/app/guides/service.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guides.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_pack_ingest.py
  - docs/seo.md
  - docs/travel-guides.md
  - apps/web/app/sitemap.xml
  - apps/web/e2e/seo.spec.ts
  - tools/e2e-runtime-api.mjs
  - apps/api/tests/test_gemini_series.py
---

# sitemap 拆成 sitemap index：986 列，下一批 20 篇就破 1,000

## Why

`guides-pack lint` 現在算到 986 個 (article, locale) 列（#513 之後，含 #515 財經系列的 40 篇與 #516 批次 08 的 20 篇），早就過了 `SITEMAP_WARN_ROWS = 800`
（`apps/api/app/guides/pack_ingest.py`）的警戒線；兩個專區共用一個 1,000 列的 sitemap（`SITEMAP_LIMIT`
在 `apps/api/app/guides/service.py`、`SITEMAP_GUIDE_ENTRY_LIMIT` 在 `apps/web/lib/guides.server.ts`），新的先進、
舊的被擠出，被擠出的文章仍可索引但不再被 sitemap 宣告、也沒有 `lastmod`。生活分享 AI 系列批次 09–11 還有 60 篇、批次 12 有 11 篇、
財經系列（`docs/life-finance-series.md`）還有 80 篇要進來：986 列再加任何一批 20 篇就超過 1,000，全部進來會到 1,137。

`GET /guides/sitemap`（`apps/api/app/guides/router.py`）沒有分頁參數，所以不能只在 web 端拆；`docs/seo.md`
寫的「No sitemap index is needed」與 `docs/travel-guides.md` 的「Still open」都要一起改。

## Definition of done

- [x] `/sitemap.xml` 變成 sitemap index，靜態路由一個子 sitemap、文章依專區或依語系分成多個子 sitemap，每個子檔不超過 1,000 列，沒有文章被擠掉。
- [x] API 提供可分頁或依專區／語系篩選的 sitemap 讀法，web 端逐頁讀完；API 失敗時退回靜態子 sitemap，不出空檔。
- [x] `robots.ts` 指向 sitemap index；`e2e/seo.spec.ts` 與 `apps/web/app/sitemap.test.ts` 更新；`pack_ingest.py` 的 `SITEMAP_WARN_ROWS` 警語改成對子 sitemap 的上限說話。
- [x] `docs/seo.md`、`docs/travel-guides.md` 改寫預算段落。

## Steps

- [x] 決定切法（建議依專區：`guides`、`life`，再依語系）並寫進 `docs/seo.md`。
- [x] API：`SitemapEntry` 讀法加 `section`／`locale`／`cursor` 參數，保留舊呼叫相容。
- [x] Web：`sitemap.ts` 用 Next 的 `generateSitemaps` 或自訂 index route 產出多檔。
- [x] 測試與文件。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
cd apps/api && uv run pytest tests/test_guides.py -q
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
```

部署後抓 `/sitemap.xml` 與每個子 sitemap，確認總列數等於已發布的 (article, locale) 數。

## Notes

- 2026-09-15 落地（claude-fable-5-1）。實況比票面更急：repo 內容包已有 1,375 列（travel 185、life 1,190），不是 986。
- 切法：`/sitemap.xml` 改為手寫 `<sitemapindex>`（`app/sitemap.xml/route.ts`），子檔 `app/sitemaps/sitemap.ts` + `generateSitemaps` 固定 11 個 id
  （`static` + 專區×語系），URL `/sitemaps/sitemap/<id>.xml`。Next 16 不會產生 index；`app/sitemap.ts` 與 `app/sitemap.xml/route.ts` 同時存在時
  `next build` 報 "Conflicting route and metadata at /sitemap.xml"（即使前者有 `generateSitemaps`），所以子檔模組搬到子資料夾。
  id 常數化是因為 `next build` 會呼叫 `generateSitemaps` 而建置時沒有 API。
- 每子檔上限提高到 5,000（Google 上限 50,000），API 每頁 500 逐 cursor 讀；`life-zh-TW` 今天 818 列，排隊的批次進來仍有餘裕。
  lint 改為每子檔 4,000 警告並指名子檔（之前的算法把 `--kind` 篩過的清單和全部混用）。
- `pack_ingest.py` 由 `2026-09-14-pack-ingest-urlopen-scheme`（review、claim 已過 24h、修正在 HEAD #496）持有，claim 時 `--force`。
- 相依 `2026-09-14-guide-listing-curated-order` 也改 `service.py`；後合併者 rebase。
- 2026-09-15 提到 P1：#515 財經系列一次加了 40 列、#516 批次 08 再加 20 列，986 已經離上限 14 列，任何一批 20 篇落地就會開始把最舊的文章擠出 sitemap。

- `guides.server.ts` 與 `pack_ingest.py` 目前被 review 中的 `2026-09-14-claude-code-tutorial-center`、`2026-09-14-pack-ingest-urlopen-scheme` 持有，所以先 depends_on 那兩張。
- `2026-09-14-guide-listing-curated-order` 也會改 `service.py`；先合併的那張，後面那張要 rebase。
- 來源：`docs/travel-guides.md`「Both sections share one 1,000-row sitemap budget」；Google 單一 sitemap 上限 50,000 列，這裡的 1,000 是自訂預算。
