---
id: 2026-09-15-guides-hub-redesign-web
title: 旅遊攻略 hub 重設計：hero 搜尋、主題 tile、系列列、精選／最新、目的地分組
status: in-progress
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T01:39:46Z
created_at: 2026-09-15T13:57:48Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
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
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
---

# 旅遊攻略 hub 重設計：hero 搜尋、主題 tile、系列列、精選／最新、目的地分組

## Why

hub 目前是兩段六篇卡片加一排 chips，沒有搜尋、沒有主題導覽、沒有系列入口。

## Definition of done

- [x] `/guides`：hero（h1、導言、GET 搜尋框、篇數／主題數）、主題 tile（數量、描述、前三個子主題）、系列列、精選 howto（curated）、最新 intel、依目的地瀏覽。
- [x] 全部用 token 顏色、`min-h-11`、五語系文案。

## Steps

- [x] 三個新元件＋測試。
- [x] 重組 `guides/page.tsx`。

## How to verify

```bash
cd apps/web && npx vitest run components/guides "app/[locale]/guides/page.test.tsx"
```

## Notes

主題沒有封面圖資產；需要時再加 `cover_src`。

2026-09-16 落地（claude-fable-5-1）：`HubHero`（h1、導言、`SearchForm` GET 表單帶 `section` 隱藏欄、篇數／主題數；篇數來自
`guideSitemapSummary()`＋`sectionArticleCount()`，讀不到就不顯示）、`TopicTiles`（父主題 tile：hub 連結、篇數、導言、前三個有文章的子主題 chip、
「還有 N 個子主題」；活躍主題或其家族 tile 上色）、`SeriesRow`（`GET /guides/series` 依專區過濾；每張卡只有一個連結）。
`guides/page.tsx` 順序：hero → 主題 tile → 系列列 → 精選攻略（curated 6）→ 最新情報（6）→ 依目的地瀏覽。旅遊登錄檔目前沒有系列，列不畫。
文案 `common.guides.hubTopicCount/topicArticles/subtopicsMore/seriesRow/seriesLead/seriesEntries/allArticles` ×5。
