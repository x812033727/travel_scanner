---
id: 2026-09-14-sitemap-split-before-1000-rows
title: sitemap 拆成 sitemap index：926 列已過 800 警戒線
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-14T23:07:00Z
completed_at:
branch:
depends_on:
  - 2026-09-14-claude-code-tutorial-center
  - 2026-09-14-pack-ingest-urlopen-scheme
scope:
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
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
---

# sitemap 拆成 sitemap index：926 列已過 800 警戒線

## Why

`guides-pack lint` 現在算到 926 個 (article, locale) 列，早就過了 `SITEMAP_WARN_ROWS = 800`
（`apps/api/app/guides/pack_ingest.py`）的警戒線；兩個專區共用一個 1,000 列的 sitemap（`SITEMAP_LIMIT`
在 `apps/api/app/guides/service.py`、`SITEMAP_GUIDE_ENTRY_LIMIT` 在 `apps/web/lib/guides.server.ts`），新的先進、
舊的被擠出，被擠出的文章仍可索引但不再被 sitemap 宣告、也沒有 `lastmod`。生活分享 AI 系列批次 08–11 還有 80 篇、
批次 12 有 11 篇要進來，926＋91 會在批次 11 落地時超過 1,000。

`GET /guides/sitemap`（`apps/api/app/guides/router.py`）沒有分頁參數，所以不能只在 web 端拆；`docs/seo.md`
寫的「No sitemap index is needed」與 `docs/travel-guides.md` 的「Still open」都要一起改。

## Definition of done

- [ ] `/sitemap.xml` 變成 sitemap index，靜態路由一個子 sitemap、文章依專區或依語系分成多個子 sitemap，每個子檔不超過 1,000 列，沒有文章被擠掉。
- [ ] API 提供可分頁或依專區／語系篩選的 sitemap 讀法，web 端逐頁讀完；API 失敗時退回靜態子 sitemap，不出空檔。
- [ ] `robots.ts` 指向 sitemap index；`e2e/seo.spec.ts` 與 `apps/web/app/sitemap.test.ts` 更新；`pack_ingest.py` 的 `SITEMAP_WARN_ROWS` 警語改成對子 sitemap 的上限說話。
- [ ] `docs/seo.md`、`docs/travel-guides.md` 改寫預算段落。

## Steps

- [ ] 決定切法（建議依專區：`guides`、`life`，再依語系）並寫進 `docs/seo.md`。
- [ ] API：`SitemapEntry` 讀法加 `section`／`locale`／`cursor` 參數，保留舊呼叫相容。
- [ ] Web：`sitemap.ts` 用 Next 的 `generateSitemaps` 或自訂 index route 產出多檔。
- [ ] 測試與文件。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
cd apps/api && uv run pytest tests/test_guides.py -q
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
```

部署後抓 `/sitemap.xml` 與每個子 sitemap，確認總列數等於已發布的 (article, locale) 數。

## Notes

- `guides.server.ts` 與 `pack_ingest.py` 目前被 review 中的 `2026-09-14-claude-code-tutorial-center`、`2026-09-14-pack-ingest-urlopen-scheme` 持有，所以先 depends_on 那兩張。
- `2026-09-14-guide-listing-curated-order` 也會改 `service.py`；先合併的那張，後面那張要 rebase。
- 來源：`docs/travel-guides.md`「Both sections share one 1,000-row sitemap budget」；Google 單一 sitemap 上限 50,000 列，這裡的 1,000 是自訂預算。
