---
id: 2026-09-14-guides-pack-lint-catalogue-life
title: guides-pack lint --catalogue 把系列外的 life 文章報成缺漏
status: review
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-16T02:39:27Z
created_at: 2026-09-14T04:56:18Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on: []
scope:
  - apps/api/tests/test_guides_pack_ingest.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/app/guides/pack_cli.py
---

# guides-pack lint --catalogue 把系列外的 life 文章報成缺漏

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [x] The observable outcome, not the implementation.

## Steps

- [x] First sub-task.
- [x] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Why

`guides-pack lint --kind life --catalogue docs/life-ai-series.md` 會把**所有** life 內容包拿去跟總表比對。
但總表只列 AI 系列的 220 篇；站上另有不屬於這個系列的生活分享文章（例如 #468 併進來的十五篇效率與居家主題）。
結果是每跑一次 lint 就噴十五行 `pack_not_in_catalogue` 警告，訊息還寫「add it to the list」——但它們本來就不該進這張總表。
真正的缺漏（系列裡還沒寫的篇）被這些雜訊蓋住，`--catalogue` 這個旗標就失去用處。

## Definition of done

- [x] `--catalogue` 只在「總表有、內容包沒有」時報缺漏；內容包不在總表裡不再報警告，
      或改成一行摘要（例如「另有 N 篇 life 文章不屬於這張總表」）而不是每篇一行。
- [x] `tests/test_guides_pack_ingest.py` 加一個案例：總表外的 life 內容包不產生 per-slug 警告。
- [x] 跑 `lint --kind life --catalogue ../../docs/life-ai-series.md`，輸出只剩真正的缺漏。

## Notes

- 相關實作在 `apps/api/app/guides/pack_ingest.py` 的 `catalogue_slugs` 與 `lint_all`。
- 另一個獨立的觀察（不在這張票）：#468 那十五篇的正文約 1,000 字，低於 life 的 1,500 字下限，每篇都會噴
  `text_length` 警告。那是內容問題不是工具問題，要補字數或調下限都該另外開票。

2026-09-16 落地（claude-fable-5-1）：`lint_all` 的 `--catalogue` 只對「總表有、內容包沒有」發 `catalogue_missing_pack` 警告；
不在總表的 life 內容包改為一行 `info: packs_outside_catalogue`（列前五個 slug 與總數），`Level` 多 `info`，`--warnings` 不算 info。
測試補在 `test_lint_all_compares_the_packs_with_the_catalogue`。
