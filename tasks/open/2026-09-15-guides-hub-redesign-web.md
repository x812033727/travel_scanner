---
id: 2026-09-15-guides-hub-redesign-web
title: 旅遊攻略 hub 重設計：hero 搜尋、主題 tile、系列列、精選／最新、目的地分組
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:48Z
completed_at:
branch:
depends_on:
  - 2026-09-14-guide-listing-curated-order
  - 2026-09-15-series-registry
  - 2026-09-15-topic-hub-pages-web
  - 2026-09-15-guides-hub-destinations-by-country-web
  - 2026-09-15-article-search-results-page-web
scope:
  - apps/web/app/[locale]/guides/page.tsx
  - apps/web/app/[locale]/guides/page.test.tsx
  - apps/web/components/guides/hub-hero.tsx
  - apps/web/components/guides/hub-hero.test.tsx
  - apps/web/components/guides/topic-tiles.tsx
  - apps/web/components/guides/topic-tiles.test.tsx
  - apps/web/components/guides/series-row.tsx
  - apps/web/components/guides/series-row.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
---

# 旅遊攻略 hub 重設計：hero 搜尋、主題 tile、系列列、精選／最新、目的地分組

## Why

hub 目前是兩段六篇卡片加一排 chips，沒有搜尋、沒有主題導覽、沒有系列入口。

## Definition of done

- [ ] `/guides`：hero（h1、導言、GET 搜尋框、篇數／主題數）、主題 tile（數量、描述、前三個子主題）、系列列、精選 howto（curated）、最新 intel、依目的地瀏覽。
- [ ] 全部用 token 顏色、`min-h-11`、五語系文案。

## Steps

- [ ] 三個新元件＋測試。
- [ ] 重組 `guides/page.tsx`。

## How to verify

```bash
cd apps/web && npx vitest run components/guides "app/[locale]/guides/page.test.tsx"
```

## Notes

主題沒有封面圖資產；需要時再加 `cover_src`。
