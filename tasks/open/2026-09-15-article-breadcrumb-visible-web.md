---
id: 2026-09-15-article-breadcrumb-visible-web
title: 每篇文章都有可見麵包屑：專區 › 父主題 › 子主題 › (系列) › 標題
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:50:37Z
created_at: 2026-09-15T13:57:48Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-topic-hub-pages-web
  - 2026-09-15-term-link-popover-related-grid-web
scope:
  - apps/web/components/guides/breadcrumb.tsx
  - apps/web/components/guides/breadcrumb.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
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

- [x] 所有文章頁有 `<nav aria-label>` 麵包屑，與 `BreadcrumbList` JSON-LD 用同一條 trail。

## Steps

- [x] 把 `article-page.tsx` 系列限定的 nav 泛化為 `Breadcrumb`。
- [x] trail 用 `guideTopicHref`；測試。

## How to verify

```bash
cd apps/web && npx vitest run components/guides/breadcrumb.test.tsx components/guides/article-page.test.tsx
```

## Notes

見 `docs/article-architecture.md`。

2026-09-16 落地：`components/guides/breadcrumb.tsx`（trail 去掉首頁、最後一項是純文字 `aria-current`）；`article-page.tsx` 每篇都畫，
trail = 首頁 › 專區（旅遊再加 kind 列表）› 父主題 hub › 子主題 hub › (系列 hub) › 標題，父主題標籤靠 `getGuideTopics(locale, section)`（React cache，一次 API 讀），
vocabulary 讀不到時只留主題本身的 crumb。同一條 trail 進 `breadcrumbs()`。文案沿用 `common.guides.breadcrumb`。
路由測試裡「交通」現在有兩個連結（麵包屑 hub＋文末 chip `?topic=`），標題出現兩次（h1 與 crumb），已對應調整。
