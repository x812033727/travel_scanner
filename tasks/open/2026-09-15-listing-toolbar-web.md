---
id: 2026-09-15-listing-toolbar-web
title: 列表 sticky 工具列：ChipRow 主題 chips、目的地／國家、排序切換、結果數、空狀態
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:49Z
completed_at:
branch:
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
---

# 列表 sticky 工具列：ChipRow 主題 chips、目的地／國家、排序切換、結果數、空狀態

## Why

`GuideFilters` 自己畫 chips，主題一多就爆行；沒有排序切換與結果數。

## Definition of done

- [ ] 列表與主題 hub 共用 sticky 工具列（`bg-[var(--surface)]`），主題 chips 用 `ChipRow` 折疊，排序 `?sort=curated|latest` 為連結，空狀態含建議主題與搜尋框。

## Steps

- [ ] `listing-toolbar.tsx`；`filters.tsx` 縮為 re-export。
- [ ] 接進兩種頁面；測試。

## How to verify

```bash
cd apps/web && npx vitest run components/guides "app/[locale]/guides/[kind]/page.test.tsx"
```

## Notes

見 `docs/article-architecture.md`。
