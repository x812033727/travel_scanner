---
id: 2026-09-15-guide-retopic-cli
title: retopic：依 slug 前綴與系列成員提案生活文章的兩層主題
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-15T13:58:35Z
created_at: 2026-09-15T13:57:26Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-topic-hierarchy-api
scope:
  - apps/api/app/guides/retopic.py
  - apps/api/app/guides/pack_cli.py
  - apps/api/tests/test_guides_retopic.py
---

# retopic：依 slug 前綴與系列成員提案生活文章的兩層主題

## Why

0076 之後生活分享有子主題，但 818 篇內容包的 `topics` 仍是 `ai`/`tutorial` 等八個舊值。逐篇手改不可行，也不該由匯入時猜。需要一個可 dry-run、輸出可審表格、只改 `topics` 陣列的工具，套用後靠既有 `guides-import` 的 taxonomy-only update 進 DB。

## Definition of done

- [x] `python -m app.guides.pack_cli retopic --kind life --dry-run` 印出「slug｜目前｜建議｜命中規則」表，不寫任何檔案。
- [x] `--apply` 只改各 pack 的 `topics`，保留縮排與其他欄位；重跑無變更。
- [x] 規則從不移除 `finance`、從不指派旅遊 slug、只作用於 `kind=life`。
- [x] `docs/article-architecture.md` 的子主題表與規則一致。

## Steps

- [x] `retopic.py`：RULES（前綴、`series.catalogues()` 成員、`apps/web/lib/guide-series.json`、`docs/ai-terms-series/catalogue.json`、既有 topic 組合）。
- [x] `pack_cli.py` 加 `retopic` 子命令（`--kind --prefix --slug --dry-run|--apply`）。
- [x] 測試：決定性、dry-run 不寫檔、apply 只動 topics、重跑 no-op。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_retopic.py -q
cd apps/api && uv run python -m app.guides.pack_cli retopic --kind life --prefix ai-term- --dry-run
```

## Notes

- 2026-09-15 落地，並對 `ai-term-`、`claude-code-`、`codex-`、`gemini-`、`ai-news-`、`ai-search-`、`wordpress-`、`woocommerce-`、`chatgpt-` 共 430 篇 `--apply`（獨立 commit）。全部 818 篇 dry-run 有 795 篇會變，未套用的交給 `content-retopic-*`。
若 `pack_cli.py` 被 review 中的任務持有，改以 `python -m app.guides.retopic` 入口。套進 DB：`python -m app.cli guides-import --dry-run` 應顯示 `taxonomy: update`。
