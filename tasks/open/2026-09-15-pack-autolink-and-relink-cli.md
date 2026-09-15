---
id: 2026-09-15-pack-autolink-and-relink-cli
title: autolink／relink：內文名詞自動連結與原始站內 URL 轉 ArticleInline
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
  - 2026-09-14-pack-ingest-urlopen-scheme
scope:
  - apps/api/app/guides/autolink.py
  - apps/api/app/guides/pack_cli.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_autolink.py
  - apps/api/tests/test_guides_pack_ingest.py
  - apps/api/tests/test_guides_content_links.py
  - docs/travel-guides.md
---

# autolink／relink：內文名詞自動連結與原始站內 URL 轉 ArticleInline

## Why

743 篇用原始 `https://mokaair.com/...` 連結（不隨發布狀態消失、也不受 `ArticleInline` 的 kind 檢查保護）；名詞解說沒有任何自動連結。站主決定連結寫進內容包、產生可審 diff。

## Definition of done

- [ ] `relink`：LinkBlock／LinkInline 的站內 URL → `ArticleInline`；無 pack 的目標保留並列出。
- [ ] `autolink`：只處理 paragraph／text inline；最長匹配、ASCII 詞界、≥2 字、每目標一次、≤8/篇、不自連、不連詞條自身、決定性、重跑 no-op；輸出 diff。
- [ ] lint 新增 `raw_internal_url` 警告；`no_internal_link` 也算 ArticleInline。

## Steps

- [ ] `autolink.py`（`SITE_LINK` 從測試搬來並讓測試 import）。
- [ ] `pack_cli autolink|relink --kind --prefix --slug --dry-run|--apply`。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_autolink.py tests/test_guides_pack_ingest.py tests/test_guides_content_links.py -q
```

## Notes

別名同語系唯一，autolink 不需在多篇之間選擇。
