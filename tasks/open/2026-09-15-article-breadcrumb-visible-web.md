---
id: 2026-09-15-article-breadcrumb-visible-web
title: 每篇文章都有可見麵包屑：專區 › 父主題 › 子主題 › (系列) › 標題
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:48Z
completed_at:
branch:
depends_on:
  - 2026-09-15-topic-hub-pages-web
  - 2026-09-15-term-link-popover-related-grid-web
scope:
  - apps/web/components/guides/breadcrumb.tsx
  - apps/web/components/guides/breadcrumb.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
---

# 每篇文章都有可見麵包屑：專區 › 父主題 › 子主題 › (系列) › 標題

## Why

只有系列文章有可見麵包屑；一般文章只有「回列表」。主題 hub 上線後麵包屑才有落點。

## Definition of done

- [ ] 所有文章頁有 `<nav aria-label>` 麵包屑，與 `BreadcrumbList` JSON-LD 用同一條 trail。

## Steps

- [ ] 把 `article-page.tsx` 系列限定的 nav 泛化為 `Breadcrumb`。
- [ ] trail 用 `guideTopicHref`；測試。

## How to verify

```bash
cd apps/web && npx vitest run components/guides/breadcrumb.test.tsx components/guides/article-page.test.tsx
```

## Notes

見 `docs/article-architecture.md`。
