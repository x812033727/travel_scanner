---
id: 2026-09-15-robots-ai-crawler-switch
title: robots.ts 的 AI 爬蟲政策改為可設定，預設放行會引用來源的搜尋型爬蟲
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:48Z
completed_at:
branch:
depends_on:
  - 2026-09-14-sitemap-split-before-1000-rows
scope:
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - docs/seo.md
  - .env.example
---

# robots.ts 的 AI 爬蟲政策改為可設定，預設放行會引用來源的搜尋型爬蟲

## Why

站主 2026-09-15 決定：GEO 要讓 Perplexity／ChatGPT 搜尋／Claude 等會引用來源的引擎抓得到文章，但純訓練用爬蟲（GPTBot、CCBot、Google-Extended、Bytespider…）續封。今天 `CONTENT_HARVESTERS` 一律封鎖。

## Definition of done

- [ ] `AI_CRAWLER_POLICY=block|allow-search|allow`（預設 `allow-search`）於請求時讀取；`allow-search` 放行 PerplexityBot、OAI-SearchBot、ChatGPT-User、ClaudeBot，其餘續封。
- [ ] `robots.test.ts` 三種政策各一組斷言；`docs/seo.md` 記錄決策與日期。

## Steps

- [ ] 拆 `CONTENT_HARVESTERS` 為訓練用與搜尋用兩組。
- [ ] 環境變數與測試。
- [ ] 覆核 `ai-search-*` 文章引用舊政策的段落（在 Notes 列出需要改的 slug）。

## How to verify

```bash
cd apps/web && npx vitest run app/robots.test.ts
```
部署後 `curl https://mokaair.com/robots.txt`。

## Notes

`robots.ts` 由 sitemap-split 任務持有，先等它合併。
