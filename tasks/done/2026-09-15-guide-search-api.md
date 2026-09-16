---
id: 2026-09-15-guide-search-api
title: 文章全文搜尋 API：索引表、pg_trgm、別名置頂、`GET /guides/search`
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-15T16:38:09Z
created_at: 2026-09-15T13:57:27Z
completed_at: 2026-09-16T06:09:10Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-topic-hierarchy-api
scope:
  - apps/api/app/guides/models.py
  - apps/api/app/guides/search.py
  - apps/api/app/guides/search_cli.py
  - apps/api/app/guides/aliases.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/service.py
  - apps/api/app/cli.py
  - apps/api/app/i18n.py
  - apps/api/migrations/versions/0077_guide_search_and_aliases.py
  - apps/api/tests/test_guides_search.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_guides_migration.py
  - docs/travel-guides.md
  - docs/article-architecture.md
---

# 文章全文搜尋 API：索引表、pg_trgm、別名置頂、`GET /guides/search`

## Why

943 篇文章沒有任何公開搜尋；後台的 `q` 只 ILIKE 草稿標題。讀者只能靠列表翻頁。中日韓文無法用 tsvector 斷詞，SQLite 測試也要跑同一謂詞，所以用 NFKC+casefold 後的子字串 LIKE，Postgres 以 pg_trgm GIN 加速。

## Definition of done

- [x] `GET /api/v1/guides/search?locale&q&section&kind&topic&destination&country&limit&offset` 回 `{query,total,results[PublicSummary+snippet+matched],best_match,next_offset}`，只含 `published_filters()` 通過的文章。
- [x] 發布／撤下即時更新索引；hide／過期靠 join 排除；`guides-search-reindex` 可重建。
- [x] `機器學習` 找得到 `機器學習教學`、`ＡＩ` 找得到 `AI`、多詞 AND、`%`/`_` 逃脫、空查詢 422、別名精確命中置頂、標題權重高於內文。
- [x] migration 只新增；Postgres 才建 extension 與 GIN，SQLite 略過。
- [x] 每 IP 120 次/60 秒；Redis 故障時放行並記錄（不是 fail-closed）。

## Steps

- [x] 0077：`guide_search_entries`（title/description 原文 + `*_norm` 欄 + `body_text` + `search_text` + `hero_json` + `published_at` + `revision_version`；UNIQUE(article_id, locale)）與 `guide_article_aliases`（article_id+locale+alias_norm 唯一，source term/keyword/series/editor；見 Notes）；dialect guard 建 `pg_trgm` 與 GIN。
- [x] `search.py`：normalize、build_entry、index_locale/drop_locale（掛 `_write_revision`）、reindex_all、parse_query、search（分數 CASE：title 8／alias 6／description 4／headings 3／body 1）、snippet。
- [x] router 端點 + rate limit；cli `guides-search-reindex`。
- [x] 測試（SQLite 預設、`RUN_INTEGRATION_TESTS=1` 跑 Postgres 並確認索引存在）。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guides_search.py tests/test_guides.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_guides_search.py -q
```
部署後 `SHOW lc_ctype;` 需為 UTF-8 locale；`curl '/api/travel/guides/search?locale=zh-TW&q=機器學習'`。

## Notes

不用 ILIKE：SQLite 的 lower() 只處理 ASCII。

落地時與原規劃不同的兩點：

- 別名唯一鍵改為（article_id, locale, alias_norm）而不是（locale, alias_norm）：系列 lesson 的 `aliases` 是關鍵字提示，
  同語系 1,284 個裡有 346 個重複（`cli`、`code`、`手機`…），若逐語系唯一，先到先贏會把「手機」釘在某一課上。
  現在共用別名只在排序加權（6），`best_match` 只在恰好一篇可見文章帶該別名時才成立。
- 別名種子 CLI（`guides-aliases-seed`，`app/guides/aliases.py`）這次一併做了，因為索引的 `aliases_norm` 欄需要它才有意義；
  `guide-aliases-seed-and-pack-field` 剩內容包欄位、後台欄位與 suffix-keywords 來源。

其他要知道的：索引只在發布時寫，部署 0077 後要跑一次 `guides-search-reindex`；`revision_version` 必須等於
`published_version` 才可見，所以漏掉 hook 的寫入路徑會讓文章從搜尋消失而不是顯示舊文。`entry.body_text` 是 NFKC 後的原文，
`snippet()` 只在 casefold／lower 不改長度時切片，否則退回描述。PostgreSQL leg（`RUN_INTEGRATION_TESTS=1`）在 CI 跑；
本地只驗 SQLite。
