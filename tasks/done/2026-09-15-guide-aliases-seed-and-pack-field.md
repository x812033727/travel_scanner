---
id: 2026-09-15-guide-aliases-seed-and-pack-field
title: 文章別名：內容包欄位、後台欄位、由詞彙表與關鍵字表產生種子
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:00:41Z
created_at: 2026-09-15T13:57:27Z
completed_at: 2026-09-16T06:09:06Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-search-api
scope:
  - apps/api/app/guides/aliases.py
  - apps/api/app/guides/alias_store.py
  - apps/api/app/guides/search.py
  - apps/api/app/guides/search_cli.py
  - apps/api/tests/test_guides_search.py
  - apps/web/lib/guides-admin.ts
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

- [x] `ArticlePack.aliases: {locale: [alias]}`（≤12/語系）走 taxonomy-only import；後台可編輯；~~同語系別名已屬別篇時 409~~（Phase 2 決策：共用只加權，見 Notes）。
- [x] `guides-aliases-seed --dry-run` 列出將寫入與衝突；正式跑後 reindex。

## Steps

- [x] schemas/content_pack/admin_service 欄位與寫入。
- [x] `aliases.py` 種子來源三合一。
- [x] cli 與測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_aliases.py tests/test_guides_content_pack.py -q
```

## Notes

種子 `source` 保留（term/keyword/series），編輯欄位只覆蓋 `editor` 列。

2026-09-15 更新：`guides-aliases-seed`（`app/guides/aliases.py`、`app/guides/search_cli.py`）已在 `guide-search-api` 先做，
讀 `docs/ai-terms-series/aliases.json` 與 `series_data` 的 lesson `aliases`；表的唯一鍵是（article_id, locale, alias_norm），
共用別名只加權不置頂。本票剩：`ArticlePack.aliases` 欄位（taxonomy-only import）、後台編輯、`docs/ai-suffix-keywords.md` 來源
（`source="keyword"`），以及把 seed 改為也吃內容包欄位。

2026-09-16 落地：

- `ArticlePack.aliases`／`ArticleUpdate.aliases: dict[Locale, list[str]] | None`：`None` 不動、列出的語系整批取代 `editor` 列（`[]` 清空）；
  與其他 source 同 `alias_norm` 者不重複寫；寫完 `search.refresh_aliases`。內容包匯入時對包內每個語系都送（未列出＝清空該語系 editor 列），所以冪等。
- 讀取拆到 `app/guides/alias_store.py`（`editor_aliases`、`public_aliases`），因為 `search.py` 匯入 `service.py`，`service.py` 不能反過來匯入 `search.py`。
- `keyword_aliases()` 解析 `docs/ai-suffix-keywords.md`：主關鍵字＋`、`分隔的變體 → 反引號 slug（`；`分隔；`備 ` 前綴只在主要落點無包時用）；語系＝包語系 ∩ {zh-TW, zh-CN}；目前 161 列。
- 沒有 409：唯一鍵是（article_id, locale, alias_norm），共用別名只加權、`best_match` 要恰好一篇。
- `pack_ingest` 寫新包時省略空的 `aliases`／`related`，943 包 round-trip 不變。
