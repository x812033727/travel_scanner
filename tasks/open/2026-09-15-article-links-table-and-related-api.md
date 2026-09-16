---
id: 2026-09-15-article-links-table-and-related-api
title: 文章連結表：發布時實體化站內連結、編輯指定 related、延伸閱讀與反向連結 API
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:00:43Z
created_at: 2026-09-15T13:57:28Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-aliases-seed-and-pack-field
  - 2026-09-15-series-registry
scope:
  - apps/api/app/guides/models.py
  - apps/api/app/guides/links.py
  - apps/api/app/guides/links_cli.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_guide_series.py
  - apps/api/tests/test_guides_migration.py
  - apps/api/app/guides/series.py
  - apps/api/app/guides/service.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/content_pack.py
  - apps/api/app/cli.py
  - apps/api/migrations/versions/0078_guide_article_links.py
  - apps/api/tests/test_guides_links.py
  - apps/api/tests/test_guides.py
  - docs/travel-guides.md
---

# 文章連結表：發布時實體化站內連結、編輯指定 related、延伸閱讀與反向連結 API

## Why

相關文章只有系列目錄與自動規則，沒有編輯指定，也沒有「誰連到我」。已知 25 條站內連結指向未發布文章，沒有工具能列出。

## Definition of done

- [x] 0078 `guide_article_links`（source/target/locale/relation inline|related/position；prerequisite 留在系列目錄）；發布時從 ArticleInline 實體化（站內 URL 由 relink 先轉成 inline），撤下時刪除。
- [x] `ArticlePack.related ≤4` 走 taxonomy 路徑；`PublicArticle += related, backlinks, aliases`（`term` 併入 aliases＋主題，Phase 4 的 DefinedTerm 由此推導）；`ArticleReference += description`。
- [x] `related_articles()`：curated → 同子主題 → 同父主題 → 同目的地 → 同系列群，不自連。
- [x] `guides-links-check --locale` 列出指向未發布目標的連結，退出碼 1；發布時對此只警告（審計 metadata）不拒絕。

## Steps

- [x] migration、models、`links.py`。
- [x] `_write_revision` 掛 materialize；`update_article` 寫 related。
- [x] service 組 PublicArticle；cli；測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_links.py tests/test_guides.py -q
```

## Notes

`ArticleReference.description` 由 `series.published_documents` 直接取 document.description，零額外查詢。

2026-09-16 落地：

- `links.py` 只依賴 models／publication／schemas／series，`service.py` 匯入它；rebuild／check 需要 `_published_document` 所以放 `links_cli.py`。
- related 列 `locale` 為 NULL（語系無關），唯一性靠 delete+insert（同 `_set_topics`）；inline 列有 UNIQUE。
- `related_articles` 五層：curated → 同子主題 → 同父主題家族（父自己＋其他子主題）→ 同目的地 → 同系列群（只 life，`catalogue_for_article` 只比 slug）；每層 published_at desc；`references_for` 只回可見文章（title／description 直接讀 revision JSON）。
- `_write_revision` 的 audit `metadata_json["unresolved_links"]` 記指向不存在文章的 inline；指向「存在但未發布」的照樣建列（目標發布後自動完成）。
- `guides-links-check` 分五類 + `raw_url`；`guides-links-rebuild` 冪等並刪掉沒有已發布翻譯支撐的 inline 列。
- `tests/test_guide_series.py` 的 `/guides/series` 整段相等期望值加了 `hub.description`。
