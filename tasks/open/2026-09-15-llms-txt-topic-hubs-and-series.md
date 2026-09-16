---
id: 2026-09-15-llms-txt-topic-hubs-and-series
title: llms.txt 列出父主題與系列 hub
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T01:39:48Z
created_at: 2026-09-15T13:57:27Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-topic-hub-pages-web
  - 2026-09-15-series-registry
  - 2026-09-14-aio-article-citations-and-llms-txt
scope:
  - apps/web/app/llms.txt
  - docs/seo.md
  - apps/web/app/llms.txt/route.test.ts
---

# llms.txt 列出父主題與系列 hub

## Why

`/llms.txt` 只列 `/guides` 與 `/life` 兩行，AI 搜尋抓不到主題與教學中心的結構。

## Definition of done

- [x] 「Guides and lifestyle」段落下每個父主題一行（含篇數）、「Series」小節列所有已發布 hub。

## Steps

- [x] 讀 `getGuideTopics(en, …)` 與 `getSeriesIndex(en)`；沿用 `entry()` 格式。
- [x] 更新 `docs/seo.md` llms.txt 段。

## How to verify

```bash
cd apps/web && npx vitest run app/llms.txt
```

## Notes

等 aio 任務合併後才能動這個路由。

2026-09-16 落地（claude-fable-5-1）：「Guides and lifestyle」段下多 `### Topics`（每個父主題一行，連到篇數最多的語系 hub，平手英文優先，附篇數、語言與導言；
全語系都 0 篇的不列）與 `### Series`（每個 hub 一次，英文優先的第一個有發布的語系，附課數）。讀取失敗只少這兩小節。`docs/seo.md` llms.txt 段已補。
