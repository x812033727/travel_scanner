---
id: 2026-09-15-robots-ai-crawler-switch
title: robots.ts 的 AI 爬蟲政策改為可設定，預設放行會引用來源的搜尋型爬蟲
status: done
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:50:38Z
created_at: 2026-09-15T13:57:48Z
completed_at: 2026-09-16T06:09:30Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-14-sitemap-split-before-1000-rows
scope:
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - docs/seo.md
  - .env.example
  - apps/api/app/guides/content/ai-search-llms-txt.json
---

# robots.ts 的 AI 爬蟲政策改為可設定，預設放行會引用來源的搜尋型爬蟲

## Why

站主 2026-09-15 決定：GEO 要讓 Perplexity／ChatGPT 搜尋／Claude 等會引用來源的引擎抓得到文章，但純訓練用爬蟲（GPTBot、CCBot、Google-Extended、Bytespider…）續封。今天 `CONTENT_HARVESTERS` 一律封鎖。

## Definition of done

- [x] `AI_CRAWLER_POLICY=block|allow-search|allow`（預設 `allow-search`）於請求時讀取；`allow-search` 放行 PerplexityBot、OAI-SearchBot、ChatGPT-User、ClaudeBot，其餘續封。
- [x] `robots.test.ts` 三種政策各一組斷言；`docs/seo.md` 記錄決策與日期。

## Steps

- [x] 拆 `CONTENT_HARVESTERS` 為訓練用與搜尋用兩組。
- [x] 環境變數與測試。
- [x] 覆核 `ai-search-*` 文章引用舊政策的段落（在 Notes 列出需要改的 slug）。

## How to verify

```bash
cd apps/web && npx vitest run app/robots.test.ts
```
部署後 `curl https://mokaair.com/robots.txt`。

## Notes

`robots.ts` 由 sitemap-split 任務持有，先等它合併。（同一分支，已一併做）

2026-09-16 落地：`TRAINING_CRAWLERS`（9 個）與 `SEARCH_CRAWLERS`（PerplexityBot、ClaudeBot）；`aiCrawlerPolicy()` 讀 `AI_CRAWLER_POLICY`（不認得的值回預設）；
`export const dynamic = "force-dynamic"` 讓 robots.txt 每次請求算，改環境變數不用重建。ChatGPT-User／OAI-SearchBot 從未在名單上，三種政策都放行。
覆核 ai-search-* 文章：只有 `ai-search-llms-txt` 一句陳述「拒絕名單 11 個含 ClaudeBot」，已改寫為新政策；其餘四篇只是泛談各家爬蟲，不涉本站政策。
