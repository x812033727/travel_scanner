---
id: 2026-09-15-article-search-results-page-web
title: 文章搜尋結果頁 /search/articles（noindex、純 GET 表單）
status: review
priority: P1
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-15T16:38:10Z
created_at: 2026-09-15T13:57:27Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-search-api
  - 2026-09-15-topic-hub-pages-web
scope:
  - apps/web/app/[locale]/search/articles
  - apps/web/components/guides/search-form.tsx
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
  - apps/web/app/[locale]/robots-directives.test.ts
  - docs/seo.md
---

# 文章搜尋結果頁 /search/articles（noindex、純 GET 表單）

## Why

有了搜尋 API 之後需要一個伺服器渲染、無 JS 也能用的結果頁，作為 header 搜尋框的落點。

## Definition of done

- [x] `/{locale}/search/articles?q=&section=` 伺服器渲染結果：best match 卡、snippet 加 `<mark>`、專區 chips（全部／旅遊／生活）保留 q、offset 上下頁。
- [x] 空結果列出有文章的父主題與系列；422 顯示「請輸入更完整的關鍵字」；API 故障顯示「搜尋暫時無法使用」。
- [x] `robots: noindex, follow`，`metadata.articleSearchTitle`；`docs/seo.md` 註記。

## Steps

- [x] `loadGuideSearch()`、`articleSearchHref()`、型別與 guard。
- [x] `search-form.tsx`（`<form method="get">`）、`search-results.tsx`。
- [x] 頁面 + 測試四件套。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

`/search` 是機票／住宿搜尋，兩者互不干擾；本頁沿用它的 noindex 規則。

- `search-form.tsx` 沒有自己的測試檔：它是純 server 表單，頁面測試（`page.test.tsx`）已驗 method/action/hidden section。
- `<mark>` 用 `lib/guides.ts` 的 `highlight()`：逐字 NFKC+lower 並記錄對映回原文的位置，因為 NFKC 不保長度
  （`…` 變三個句點、`İ` 變兩個 code unit）；先前整串折疊再依 index 切片會標錯位置。
- `loadGuideSearch` 靠新的 `fetchJsonWithStatus` 分辨 422（`invalid`）與其他失敗（`available:false`）；`fetchJson` 改為它的包裝，行為不變。
- 表單 `action` 直接用 `/${locale}/search/articles`（routing 是 `localePrefix: "always"`），不走 `getPathname`：測試環境的 `@/i18n/navigation` mock 沒有它。
