---
id: 2026-09-15-summary-and-faq-blocks-api
title: 文件新增 summary（重點摘要）與 faq 區塊，lint 警告缺摘要
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-15T13:57:48Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guide-search-api
  - 2026-09-14-pack-ingest-urlopen-scheme
scope:
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/app/guides/search.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_guides_pack_ingest.py
  - apps/api/tests/test_guides_search.py
  - docs/travel-guides.md
---

# 文件新增 summary（重點摘要）與 faq 區塊，lint 警告缺摘要

## Why

AEO／GEO 需要文章開頭就有可直接引用的答案。現有文件沒有摘要區塊；FAQ 之前被否決是因為沒有內容，這張只加機制，內容由編輯另寫。

## Definition of done

- [ ] `SummaryBlock{items 2..5}`（至多一個，首段前後）、`FaqBlock{items 2..10}`（至多一個）進 `GuideBlock`；既有 943 篇仍合法。
- [ ] lint 警告 `no_summary`（life 與 howto）；搜尋索引納入摘要（權重同 description）與 FAQ 問題（同 headings）。

## Steps

- [ ] schemas 與 `_validate_document` 規則。
- [ ] lint 與索引。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides.py tests/test_guides_pack_ingest.py -q
```

## Notes

**上線順序**：web 渲染器（`summary-faq-definedterm-jsonld-web`）先部署，再發布含新區塊的內容，否則頁面會被判不可用而 noindex。
