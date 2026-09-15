---
id: 2026-09-15-article-search-results-page-web
title: 文章搜尋結果頁 /search/articles（noindex、純 GET 表單）
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:27Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guide-search-api
  - 2026-09-15-topic-hub-pages-web
scope:
  - apps/web/app/[locale]/search/articles
  - apps/web/components/guides/search-form.tsx
  - apps/web/components/guides/search-form.test.tsx
  - apps/web/components/guides/search-results.tsx
  - apps/web/components/guides/search-results.test.tsx
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - docs/seo.md
---

# 文章搜尋結果頁 /search/articles（noindex、純 GET 表單）

## Why

有了搜尋 API 之後需要一個伺服器渲染、無 JS 也能用的結果頁，作為 header 搜尋框的落點。

## Definition of done

- [ ] `/{locale}/search/articles?q=&section=` 伺服器渲染結果：best match 卡、snippet 加 `<mark>`、專區 chips（全部／旅遊／生活）保留 q、offset 上下頁。
- [ ] 空結果列出有文章的父主題與系列；422 顯示「請輸入更完整的關鍵字」；API 故障顯示「搜尋暫時無法使用」。
- [ ] `robots: noindex, follow`，`metadata.articleSearchTitle`；`docs/seo.md` 註記。

## Steps

- [ ] `loadGuideSearch()`、`articleSearchHref()`、型別與 guard。
- [ ] `search-form.tsx`（`<form method="get">`）、`search-results.tsx`。
- [ ] 頁面 + 測試四件套。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

`/search` 是機票／住宿搜尋，兩者互不干擾；本頁沿用它的 noindex 規則。
