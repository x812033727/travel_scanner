---
id: 2026-09-15-listing-toolbar-web
title: 列表 sticky 工具列：ChipRow 主題 chips、目的地／國家、排序切換、結果數、空狀態
status: done
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T01:39:47Z
created_at: 2026-09-15T13:57:49Z
completed_at: 2026-09-16T06:09:24Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-topic-hub-pages-web
  - 2026-09-14-guide-listing-curated-order
scope:
  - apps/web/components/guides/listing-toolbar.tsx
  - apps/web/components/guides/listing-toolbar.test.tsx
  - apps/web/components/guides/filters.tsx
  - apps/web/app/[locale]/guides/[kind]/page.tsx
  - apps/web/app/[locale]/guides/[kind]/page.test.tsx
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/components/guides/topic-hub-page.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/components/guides/topic-chips.tsx
  - apps/web/app/[locale]/guides/topics/[topic]/page.tsx
  - apps/web/app/[locale]/life/topics/[topic]/page.tsx
  - apps/web/app/globals.css
---

# 列表 sticky 工具列：ChipRow 主題 chips、目的地／國家、排序切換、結果數、空狀態

## Why

`GuideFilters` 自己畫 chips，主題一多就爆行；沒有排序切換與結果數。

## Definition of done

- [x] 列表與主題 hub 共用 sticky 工具列（`bg-[var(--surface)]`），主題 chips 用 `ChipRow` 折疊，排序 `?sort=curated|latest` 為連結，空狀態含建議主題與搜尋框。

## Steps

- [x] `listing-toolbar.tsx`；`filters.tsx` 縮為 re-export。
- [x] 接進兩種頁面；測試。

## How to verify

```bash
cd apps/web && npx vitest run components/guides "app/[locale]/guides/[kind]/page.test.tsx"
```

## Notes

見 `docs/article-architecture.md`。

2026-09-16 落地（claude-fable-5-1）：`ListingToolbar`（`TopicChips` 摺疊 chips＋排序連結 `?sort=curated|latest`＋結果數）與 `ListingEmpty`
（空狀態：說明、提示看上方主題、專區搜尋 GET 表單）。`.app-listing-toolbar` 在 md 以上 sticky 於 header 之下
（`top: calc(var(--ad-anchor-top) + 4.75rem)`，手機 header 可能換行所以不 sticky）。
`/guides/{kind}`：howto 預設 curated、intel 預設 latest，`?sort=` 覆寫（noindex），排序連結保留 topic／destination／country、丟 cursor；
未篩選時結果數取自 `guideSitemapSummary()`。主題 hub：預設 latest，`?sort=curated` 另一個順序，結果數用 `topic.count`；兩個主題路由帶 `sort`。
`filters.tsx` 縮為 re-export。文案 `sortLabel/sortCurated/sortLatest/emptyHint` ×5。
