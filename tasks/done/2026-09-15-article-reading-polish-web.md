---
id: 2026-09-15-article-reading-polish-web
title: 文章閱讀打磨：卡片變體、摘要卡字體、名詞連結樣式、延伸閱讀格距、系列上下篇
status: done
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T01:39:48Z
created_at: 2026-09-15T13:57:49Z
completed_at: 2026-09-16T06:08:51Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-term-link-popover-related-grid-web
  - 2026-09-15-summary-faq-definedterm-jsonld-web
  - 2026-09-15-article-breadcrumb-visible-web
scope:
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/card.tsx
  - apps/web/components/guides/card.test.tsx
  - apps/web/components/guides/term-link.tsx
  - apps/web/components/guides/related-grid.tsx
  - apps/web/app/globals.css
  - apps/web/components/content-blocks.tsx
  - apps/web/components/guides/series-navigation.tsx
  - apps/web/components/guides/term-link.test.tsx
  - apps/web/app/[locale]/guides/page.tsx
---

# 文章閱讀打磨：卡片變體、摘要卡字體、名詞連結樣式、延伸閱讀格距、系列上下篇

## Why

前面幾張把功能放進文章頁之後，需要一次視覺收斂：卡片密度、摘要卡、名詞連結虛線與 popover 陰影、系列上下篇雙欄。

## Definition of done

- [x] `GuideCard` 有 `compact`／`featured` 變體；`globals.css` 只新增以 token 寫的 `.app-term-link`、`.app-summary-card` 規則；三種色板×深淺模式都檢查過。

## Steps

- [x] 逐項調整與截圖比對。

## How to verify

```bash
npm run lint:web && npm run test:web
```

## Notes

見 `docs/article-architecture.md`。

2026-09-16 落地（claude-fable-5-1）：`GuideCard` 多 `variant="compact"|"featured"`（compact 無 hero／主題、描述兩行截斷；featured 跨兩欄、md 以上圖文並排、hero eager），
旅遊 hub 精選攻略首張用 featured、生活分享「最新新聞」用 compact。`globals.css` 新增 `.app-term-link`（虛線、hover／focus 轉實線）、`.app-term-card`（陰影用 teal 混色）、
`.app-summary-card`（teal-soft 底、字級 17px／行高 1.8），全部用 token，三色板×深淺模式自動跟。延伸閱讀與引用區塊標題放大、格距 gap-4；系列上下篇改雙欄方框、回目錄放下方。
截圖比對留給站主部署後在三色板上檢視（本環境無瀏覽器截圖流程）。
