---
id: 2026-09-15-term-link-popover-related-grid-web
title: 內文名詞連結定義卡與「同主題延伸閱讀」格
status: review
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:00:43Z
created_at: 2026-09-15T13:57:47Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-article-links-table-and-related-api
  - 2026-09-14-heading-anchors-for-h3
  - 2026-09-14-aio-article-citations-and-llms-txt
scope:
  - apps/web/components/guides/term-link.tsx
  - apps/web/components/guides/term-link.test.tsx
  - apps/web/components/guides/related-grid.tsx
  - apps/web/components/guides/related-grid.test.tsx
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/lib/guides-admin.ts
  - apps/web/lib/gemini-series-content.ts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
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

- [x] `ArticleInline` 有 description 時渲染為虛線底線 `<a>`＋定義卡（hover 150ms、觸控首次點開卡、Esc 關、`aria-expanded`），無 JS 仍是可爬的 `<a>`。
- [x] life 文章在 `TravelCrosslinks` 前有「同主題延伸閱讀」（≤4 卡）；旅遊文章 `related` 非空時取代 `relatedTravel`。
- [x] 可選的「引用本文的文章」列。

## Steps

- [x] 型別與 loader 讀 related/backlinks/aliases/term。
- [x] `term-link.tsx`（client）、`related-grid.tsx`。
- [x] 接進 `content-blocks.tsx`／`article.tsx`／`article-page.tsx`；messages；測試。

## How to verify

```bash
cd apps/web && npx vitest run components/guides components/content-blocks.test.tsx
```

## Notes

aio（#512）已在 main；heading-anchors 在本票同一分支順手做掉，所以可以直接動 `content-blocks.tsx`、`article-page.tsx`。

2026-09-16 落地：

- `<TermLink>`（client）：`relative inline` 包 `<a decoration-dotted aria-expanded aria-controls>` 與 `role="note"` 的卡；pointerenter 150ms（`useRef` timer）／focus 立即開；blur、Esc（`preventDefault` 讓外層 sheet 不搶）、外部 pointerdown 關；
  `matchMedia("(hover: none)")` 時首次 click `preventDefault` 開卡、第二次導頁。只在目標 `description` 存在且頁面給了 `termLabels` 才用，否則維持純 `<a>`。
- `article-page.tsx`：`related` 節點 = `<RelatedGrid exclude={series.related}>` + `<Backlinks>` + handover（life 保留旅遊 handover；travel 有 grid 時不再打 `relatedTravel` 的兩次列表 API）。
- 後台分類表單多「別名（此語言）」與「延伸閱讀」（逗號分隔），PUT 只送目前語系的別名。
- `content-blocks.tsx` 的標題 id 改為渲染前一次算好（`headingIds` Map）：repo 的 eslint 不准在 render 內重新指派變數。
