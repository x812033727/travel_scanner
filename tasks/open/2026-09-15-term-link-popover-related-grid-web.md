---
id: 2026-09-15-term-link-popover-related-grid-web
title: 內文名詞連結定義卡與「同主題延伸閱讀」格
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:47Z
completed_at:
branch:
depends_on:
  - 2026-09-15-article-links-table-and-related-api
  - 2026-09-14-heading-anchors-for-h3
  - 2026-09-14-aio-article-citations-and-llms-txt
scope:
  - apps/web/components/guides/term-link.tsx
  - apps/web/components/guides/term-link.test.tsx
  - apps/web/components/guides/related-grid.tsx
  - apps/web/components/guides/related-grid.test.tsx
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/lib/guide-series.ts
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
---

# 內文名詞連結定義卡與「同主題延伸閱讀」格

## Why

名詞連結目前只是一般底線連結；讀者要離開文章才知道那個詞是什麼。相關文章只有旅遊三篇。

## Definition of done

- [ ] `ArticleInline` 有 description 時渲染為虛線底線 `<a>`＋定義卡（hover 150ms、觸控首次點開卡、Esc 關、`aria-expanded`），無 JS 仍是可爬的 `<a>`。
- [ ] life 文章在 `TravelCrosslinks` 前有「同主題延伸閱讀」（≤4 卡）；旅遊文章 `related` 非空時取代 `relatedTravel`。
- [ ] 可選的「引用本文的文章」列。

## Steps

- [ ] 型別與 loader 讀 related/backlinks/aliases/term。
- [ ] `term-link.tsx`（client）、`related-grid.tsx`。
- [ ] 接進 `content-blocks.tsx`／`article.tsx`／`article-page.tsx`；messages；測試。

## How to verify

```bash
cd apps/web && npx vitest run components/guides components/content-blocks.test.tsx
```

## Notes

等 heading-anchors 與 aio 兩張合併後才能動 `content-blocks.tsx`、`article-page.tsx`。
