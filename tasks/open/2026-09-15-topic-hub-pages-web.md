---
id: 2026-09-15-topic-hub-pages-web
title: 主題 hub 頁：/guides/topics/{topic} 與 /life/topics/{topic}（可索引、含子主題）
status: review
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-15T13:58:35Z
created_at: 2026-09-15T13:57:26Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-topic-hierarchy-api
scope:
  - apps/web/app/[locale]/guides/topics
  - apps/web/app/[locale]/life/topics
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/components/guides/topic-hub-page.test.tsx
  - apps/web/components/guides/topic-chips.tsx
  - apps/web/components/guides/topic-chips.test.tsx
  - apps/web/components/guides/filters.tsx
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/app/[locale]/guides/[kind]/page.tsx
  - apps/web/app/[locale]/guides/[kind]/page.test.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - docs/seo.md
  - apps/web/vitest.setup.tsx
---

# 主題 hub 頁：/guides/topics/{topic} 與 /life/topics/{topic}（可索引、含子主題）

## Why

今天主題只是列表上的 `?topic=` 篩選，而且刻意 noindex。有了兩層主題後，每個主題應有一頁有導言、子主題與文章格的 hub，可索引、進 sitemap，讓讀者與搜尋引擎都有落點。

## Definition of done

- [x] `/{locale}/guides/topics/{topic}`、`/{locale}/life/topics/{topic}` 可開，h1 為主題名、有導言、父／子主題 chips、24 篇/頁與 cursor。
- [x] 該語系有已發布文章才可索引；主題未知、0 篇或帶 cursor 時 `noindex, follow`；alternates 只列有文章的語系。
- [x] 舊 `?topic=` 列表維持 noindex 並 canonical 指向主題 hub；`GuideFilters` chips 改指向 hub。
- [x] sitemap 依各語系 count 列出主題 hub；`docs/seo.md` 索引表更新。

## Steps

- [x] `guideTopicHref`、`GuideTopic` 型別加 parent/count/counts/description。
- [x] `topic-hub-page.tsx` 共用 metadata 與內容；兩個薄殼路由。
- [x] `topic-chips.tsx` 用 `ChipRow`。
- [x] sitemap 主題列；messages 五語系；測試四件套。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```
開 `/zh-TW/life/topics/ai-terms`、`/en/life/topics/ai-terms`（noindex）檢查 canonical、robots、JSON-LD。

## Notes

- 2026-09-15 落地。`vitest.setup.tsx` 加了 `metadata` 目錄，主題 hub 的 metadata 測試才看得到真正的標題模板。未知主題 404、詞彙讀不到時渲染「暫時無法取得」並 noindex。
`llms.txt` 由 `2026-09-14-aio-article-citations-and-llms-txt` 持有，主題／系列列由 `llms-txt-topic-hubs-and-series` 接手。排序切換等 `2026-09-14-guide-listing-curated-order`。
