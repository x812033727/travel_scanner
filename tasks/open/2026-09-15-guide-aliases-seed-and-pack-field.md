---
id: 2026-09-15-guide-aliases-seed-and-pack-field
title: 文章別名：內容包欄位、後台欄位、由詞彙表與關鍵字表產生種子
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-15T13:57:27Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guide-search-api
scope:
  - apps/api/app/guides/aliases.py
  - apps/api/app/guides/content_pack.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/cli.py
  - apps/api/tests/test_guides_aliases.py
  - apps/api/tests/test_guides_content_pack.py
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# 文章別名：內容包欄位、後台欄位、由詞彙表與關鍵字表產生種子

## Why

搜尋置頂與名詞自動連結都要「別名 → 文章」對照。資料已存在：`docs/ai-terms-series/aliases.json`（78 詞 135 別名）、`docs/ai-suffix-keywords.md`（約 90 列）、系列 lesson 的 `aliases`，但沒有進 DB 也沒有編輯入口。

## Definition of done

- [ ] `ArticlePack.aliases: {locale: [alias]}`（≤12/語系）走 taxonomy-only import；後台可編輯；同語系別名已屬別篇時 409。
- [ ] `guides-aliases-seed --dry-run` 列出將寫入與衝突；正式跑後 reindex。

## Steps

- [ ] schemas/content_pack/admin_service 欄位與寫入。
- [ ] `aliases.py` 種子來源三合一。
- [ ] cli 與測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_aliases.py tests/test_guides_content_pack.py -q
```

## Notes

種子 `source` 保留（term/keyword/series），編輯欄位只覆蓋 `editor` 列。
