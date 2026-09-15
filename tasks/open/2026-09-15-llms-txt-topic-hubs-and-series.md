---
id: 2026-09-15-llms-txt-topic-hubs-and-series
title: llms.txt 列出父主題與系列 hub
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:27Z
completed_at:
branch:
depends_on:
  - 2026-09-15-topic-hub-pages-web
  - 2026-09-15-series-registry
  - 2026-09-14-aio-article-citations-and-llms-txt
scope:
  - apps/web/app/llms.txt
  - docs/seo.md
---

# llms.txt 列出父主題與系列 hub

## Why

`/llms.txt` 只列 `/guides` 與 `/life` 兩行，AI 搜尋抓不到主題與教學中心的結構。

## Definition of done

- [ ] 「Guides and lifestyle」段落下每個父主題一行（含篇數）、「Series」小節列所有已發布 hub。

## Steps

- [ ] 讀 `getGuideTopics(en, …)` 與 `getSeriesIndex(en)`；沿用 `entry()` 格式。
- [ ] 更新 `docs/seo.md` llms.txt 段。

## How to verify

```bash
cd apps/web && npx vitest run app/llms.txt
```

## Notes

等 aio 任務合併後才能動這個路由。
