---
id: 2026-09-15-article-reading-polish-web
title: 文章閱讀打磨：卡片變體、摘要卡字體、名詞連結樣式、延伸閱讀格距、系列上下篇
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:49Z
completed_at:
branch:
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
---

# 文章閱讀打磨：卡片變體、摘要卡字體、名詞連結樣式、延伸閱讀格距、系列上下篇

## Why

前面幾張把功能放進文章頁之後，需要一次視覺收斂：卡片密度、摘要卡、名詞連結虛線與 popover 陰影、系列上下篇雙欄。

## Definition of done

- [ ] `GuideCard` 有 `compact`／`featured` 變體；`globals.css` 只新增以 token 寫的 `.app-term-link`、`.app-summary-card` 規則；三種色板×深淺模式都檢查過。

## Steps

- [ ] 逐項調整與截圖比對。

## How to verify

```bash
npm run lint:web && npm run test:web
```

## Notes

見 `docs/article-architecture.md`。
