---
id: 2026-09-15-article-links-table-and-related-api
title: 文章連結表：發布時實體化站內連結、編輯指定 related、延伸閱讀與反向連結 API
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-15T13:57:28Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guide-aliases-seed-and-pack-field
  - 2026-09-15-series-registry
scope:
  - apps/api/app/guides/models.py
  - apps/api/app/guides/links.py
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

- [ ] 0078 `guide_article_links`（source/target/locale/relation inline|related|prerequisite/position）；發布時從 ArticleInline 與站內 URL 實體化，撤下時刪除。
- [ ] `ArticlePack.related ≤4` 走 taxonomy 路徑；`PublicArticle += related, backlinks, aliases, term`；`ArticleReference += description`。
- [ ] `related_articles()`：curated → 同子主題 → 同父主題 → 同目的地 → 同系列群，不自連。
- [ ] `guides-links-check --locale` 列出指向未發布目標的連結，退出碼 1；發布時對此只警告（審計 metadata）不拒絕。

## Steps

- [ ] migration、models、`links.py`。
- [ ] `_write_revision` 掛 materialize；`update_article` 寫 related。
- [ ] service 組 PublicArticle；cli；測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_links.py tests/test_guides.py -q
```

## Notes

`ArticleReference.description` 由 `series.published_documents` 直接取 document.description，零額外查詢。
