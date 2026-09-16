---
id: 2026-09-15-guides-hub-destinations-by-country-web
title: 旅遊攻略 hub 依國家分組列出目的地與篇數
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-15T13:58:36Z
created_at: 2026-09-15T13:57:27Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-topic-hierarchy-api
scope:
  - apps/web/components/guides/destination-groups.tsx
  - apps/web/components/guides/destination-groups.test.tsx
  - apps/web/app/[locale]/guides/page.tsx
  - apps/web/app/[locale]/guides/page.test.tsx
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
---

# 旅遊攻略 hub 依國家分組列出目的地與篇數

## Why

旅遊文章的第二軸是目的地，但 hub 只有主題 chips；33 個目的地沒有入口，讀者要找「日本」的攻略只能逐城市猜。

## Definition of done

- [x] `/guides` 有「依目的地瀏覽」區：國家 → 城市 pill（含篇數），城市連到 `/guides/howto?destination=`，國家連到 `/guides/howto?country=`。
- [x] 0 篇的城市不顯示；API 失敗時整區不顯示。

## Steps

- [x] `loadDestinationFacets(locale, section)` 讀 `/guides/destinations`。
- [x] `destination-groups.tsx` 分組渲染；接進 `guides/page.tsx`。
- [x] messages 與測試。

## How to verify

```bash
cd apps/web && npx vitest run components/guides/destination-groups.test.tsx "app/[locale]/guides/page.test.tsx"
```

## Notes

- 2026-09-15 落地：`destination-groups.tsx` 依 `country` 分組，0 篇城市不顯示，API 失敗整區不畫。
篩選視圖維持 noindex（`docs/seo.md`）。
