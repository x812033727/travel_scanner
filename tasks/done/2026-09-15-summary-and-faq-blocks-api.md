---
id: 2026-09-15-summary-and-faq-blocks-api
title: 文件新增 summary（重點摘要）與 faq 區塊，lint 警告缺摘要
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:50:36Z
created_at: 2026-09-15T13:57:48Z
completed_at: 2026-09-16T06:09:36Z
branch: claude/travel-article-structure-search-sr9jiq
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
  - apps/api/app/guides/series.py
  - apps/api/app/guides/service.py
  - apps/api/tests/test_guide_series.py
  - docs/travel-guides.md
---

# 文件新增 summary（重點摘要）與 faq 區塊，lint 警告缺摘要

## Why

AEO／GEO 需要文章開頭就有可直接引用的答案。現有文件沒有摘要區塊；FAQ 之前被否決是因為沒有內容，這張只加機制，內容由編輯另寫。

## Definition of done

- [x] `SummaryBlock{items 2..5}`（至多一個，首段前後）、`FaqBlock{items 2..10}`（至多一個）進 `GuideBlock`；既有 943 篇仍合法。
- [x] lint 警告 `no_summary`（life 與 howto）；搜尋索引納入摘要與 FAQ 問題（皆同 headings 權重 3，見 Notes）、FAQ 答案同內文。

## Steps

- [x] schemas 與 `_validate_document` 規則。
- [x] lint 與索引。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides.py tests/test_guides_pack_ingest.py -q
```

## Notes

**上線順序**：web 渲染器（`summary-faq-definedterm-jsonld-web`）先部署，再發布含新區塊的內容，否則頁面會被判不可用而 noindex。

2026-09-16 落地：

- 摘要權重用 headings（3）而非 description（4）：`description_norm` 是 `String(500)`，PostgreSQL 會截斷／拒絕；新開欄位要 migration，差一級不值得。
- 位置規則在 `GuideDocument.one_summary_one_faq`（model validator）：至多一個 summary、至多一個 faq、summary 必須在第一個 heading 之前；`_validate_document` 不需改。
- `_body_length` 計入摘要與 FAQ；`series.public_series` 的分鐘估算用 `getattr(block, "text", "")` 自然跳過。
- 順手加 `PublicArticle.term_set`（`series.term_set_for`：registry 中 `source=catalogue` 且主題相符、hub 已發布；hub 自己不算），供 web 的 DefinedTerm。
- 既有 943 篇都沒有這兩種區塊，lint 對 life／howto 會多 `no_summary` warning（不擋 CI）。
