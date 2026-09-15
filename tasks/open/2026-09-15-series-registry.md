---
id: 2026-09-15-series-registry
title: 系列登錄：一個讀取端點列出所有教學中心／系列 hub
status: review
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-15T13:58:35Z
created_at: 2026-09-15T13:57:26Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-topic-hierarchy-api
scope:
  - apps/api/app/guides/series_registry.json
  - apps/api/app/guides/series.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/router.py
  - apps/api/tests/test_guide_series.py
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/lib/guide-series.ts
---

# 系列登錄：一個讀取端點列出所有教學中心／系列 hub

## Why

系列 hub 分散在三種機制：API `series_data/*.json`（claude-code、codex）、web `lib/guide-series.json`（Gemini）、docs 目錄（ai-terms、ai-search）。`/life` 用三段手寫 aside 各自連過去，搜尋空狀態與 hub 重設計也需要同一份清單。

## Definition of done

- [x] `GET /api/v1/guides/series?locale` 回每個 hub 文章在該語系已發布的系列（slug、section、hub 文章參照、來源、對應主題、篇數）。
- [x] 登錄檔測試：api-series 都有目錄、hub slug 都有 pack、無重複。
- [x] web `getSeriesIndex(locale)` 可用。

## Steps

- [x] `series_data/registry.json` + `series.registry()`（lru_cache、StrictModel）。
- [x] `public_series_index()` 以 `published_documents` 判定可見。
- [x] router 在 `/series/{slug}` 前宣告 `/series`。
- [x] web loader 與 type guard。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guide_series.py -q
cd apps/web && npx vitest run lib/guides.server.test.ts
```

## Notes

- 2026-09-15 落地於 PR「文章架構 Phase 1」；`GET /guides/series` 只列 hub 文章在該語系已發布的系列，`entries` 只有 api-series 有數字。
財經 hub（`personal-finance-tutorials`）之後由 `2026-09-14-life-finance-series-hub` 加進登錄檔。
