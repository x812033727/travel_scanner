---
id: 2026-09-15-pack-autolink-and-relink-cli
title: autolink／relink：內文名詞自動連結與原始站內 URL 轉 ArticleInline
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:00:42Z
created_at: 2026-09-15T13:57:28Z
completed_at: 2026-09-16T06:09:28Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-aliases-seed-and-pack-field
  - 2026-09-14-pack-ingest-urlopen-scheme
scope:
  - apps/api/app/guides/autolink.py
  - apps/api/app/guides/pack_cli.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_autolink.py
  - apps/api/tests/test_guides_pack_ingest.py
  - apps/api/tests/test_guides_content_links.py
  - apps/api/app/guides/aliases.py
  - docs/travel-guides.md
---

# autolink／relink：內文名詞自動連結與原始站內 URL 轉 ArticleInline

## Why

743 篇用原始 `https://mokaair.com/...` 連結（不隨發布狀態消失、也不受 `ArticleInline` 的 kind 檢查保護）；名詞解說沒有任何自動連結。站主決定連結寫進內容包、產生可審 diff。

## Definition of done

- [x] `relink`：LinkBlock／LinkInline 的站內 URL → `ArticleInline`；無 pack 的目標保留並列出。
- [x] `autolink`：只處理 paragraph／text inline；最長匹配、ASCII 詞界、≥2 字、每目標一次、≤8/篇、不自連、不連詞條自身、決定性、重跑 no-op；輸出 diff。
- [x] lint 新增 `raw_internal_url` 警告；`no_internal_link` 也算 ArticleInline。

## Steps

- [x] `autolink.py`（`SITE_LINK` 從測試搬來並讓測試 import）。
- [x] `pack_cli autolink|relink --kind --prefix --slug --dry-run|--apply`。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_autolink.py tests/test_guides_pack_ingest.py tests/test_guides_content_links.py -q
```

## Notes

別名同語系唯一，autolink 不需在多篇之間選擇。

2026-09-16 落地：

- `autolink.py`：`SITE_LINK`（測試改 import）、`parse_site_link`、`relink_document`、`AliasIndex.build`（term＋keyword＋包 `aliases`，不含 series；同語系多篇共用者剔除；<2 字剔除）、
  `autolink_document`、`proposals／render_table／apply`（沿 `retopic.py`，只重寫 `locales.<locale>.blocks`）。
- 比對不做 NFKC：ASCII 別名用 `(?<![A-Za-z0-9_])…(?![A-Za-z0-9_])` 忽略大小寫，含 CJK 的別名原文子字串；全形變體不會被連（可接受，決定性優先）。
- 全庫 dry-run：742 篇、4,027 條可轉、552 條保留（551 非文章 URL、1 自連）；文章連結沒有帶 query 的。
- 詞庫裡有 2 字的通用詞（`參數`、`標記`、`評測`）：每篇每目標只連一次，dry-run 表要人審；若太吵可從 `aliases.json` 拿掉。
- `raw_internal_url` 是 warning：未 relink 的包會有 4,000 多個 warning，`lint` 預設不因 warning 失敗。
