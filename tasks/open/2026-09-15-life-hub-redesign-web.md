---
id: 2026-09-15-life-hub-redesign-web
title: 生活分享 hub 重設計：與旅遊 hub 同構，三段手寫 aside 改由系列列取代
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:49Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guides-hub-redesign-web
scope:
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
---

# 生活分享 hub 重設計：與旅遊 hub 同構，三段手寫 aside 改由系列列取代

## Why

`/life` 用三段手寫 aside 連 Codex／Gemini／Claude Code hub；財經 hub 上線後又要再加一段。

## Definition of done

- [ ] `/life` 用 `HubHero`／`TopicTiles`／`SeriesRow`；保留 `filterGeminiArticleLinks` 投影；精選排序。

## Steps

- [ ] 重組頁面與測試。

## How to verify

```bash
cd apps/web && npx vitest run "app/[locale]/life/page.test.tsx"
```

## Notes

見 `docs/article-architecture.md`。
