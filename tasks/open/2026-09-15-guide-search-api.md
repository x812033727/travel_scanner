---
id: 2026-09-15-guide-search-api
title: 文章全文搜尋 API：索引表、pg_trgm、別名置頂、`GET /guides/search`
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-15T13:57:27Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guide-topic-hierarchy-api
scope:
  - apps/api/app/guides/models.py
  - apps/api/app/guides/search.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/service.py
  - apps/api/app/cli.py
  - apps/api/app/i18n.py
  - apps/api/migrations/versions/0077_guide_search_and_aliases.py
  - apps/api/tests/test_guides_search.py
  - apps/api/tests/test_guides.py
  - docs/travel-guides.md
---

# 文章全文搜尋 API：索引表、pg_trgm、別名置頂、`GET /guides/search`

## Why

943 篇文章沒有任何公開搜尋；後台的 `q` 只 ILIKE 草稿標題。讀者只能靠列表翻頁。中日韓文無法用 tsvector 斷詞，SQLite 測試也要跑同一謂詞，所以用 NFKC+casefold 後的子字串 LIKE，Postgres 以 pg_trgm GIN 加速。

## Definition of done

- [ ] `GET /api/v1/guides/search?locale&q&section&kind&topic&destination&country&limit&offset` 回 `{query,total,results[PublicSummary+snippet+matched],best_match,next_offset}`，只含 `published_filters()` 通過的文章。
- [ ] 發布／撤下即時更新索引；hide／過期靠 join 排除；`guides-search-reindex` 可重建。
- [ ] `機器學習` 找得到 `機器學習教學`、`ＡＩ` 找得到 `AI`、多詞 AND、`%`/`_` 逃脫、空查詢 422、別名精確命中置頂、標題權重高於內文。
- [ ] migration 只新增；Postgres 才建 extension 與 GIN，SQLite 略過。
- [ ] 每 IP 120 次/60 秒；Redis 故障時放行並記錄（不是 fail-closed）。

## Steps

- [ ] 0077：`guide_search_entries`（title/description 原文 + `*_norm` 欄 + `body_text` + `search_text` + `hero_json` + `published_at` + `revision_version`；UNIQUE(article_id, locale)）與 `guide_article_aliases`（locale+alias_norm 唯一，source term/keyword/series/editor）；dialect guard 建 `pg_trgm` 與 GIN。
- [ ] `search.py`：normalize、build_entry、index_locale/drop_locale（掛 `_write_revision`）、reindex_all、parse_query、search（分數 CASE：title 8／alias 6／description 4／headings 3／body 1）、snippet。
- [ ] router 端點 + rate limit；cli `guides-search-reindex`。
- [ ] 測試（SQLite 預設、`RUN_INTEGRATION_TESTS=1` 跑 Postgres 並確認索引存在）。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guides_search.py tests/test_guides.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_guides_search.py -q
```
部署後 `SHOW lc_ctype;` 需為 UTF-8 locale；`curl '/api/travel/guides/search?locale=zh-TW&q=機器學習'`。

## Notes

不用 ILIKE：SQLite 的 lower() 只處理 ASCII。別名種子在 `guide-aliases-seed-and-pack-field`。
