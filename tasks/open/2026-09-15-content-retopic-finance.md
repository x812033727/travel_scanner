---
id: 2026-09-15-content-retopic-finance
title: 財經系列依批次掛上 finance 子主題（finance-basics／banking／credit／tax-insurance／investing）
status: review
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-16T02:23:24Z
created_at: 2026-09-15T13:57:26Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-retopic-cli
scope:
  - apps/api/app/guides/content
---

# 財經系列依批次掛上 finance 子主題（finance-basics／banking／credit／tax-insurance／investing）

## Why

財經系列 120 篇的批次（`docs/life-finance-series.md` 批次 01–06）就是子主題的分界，但 slug 沒有統一前綴，retopic 只能靠關鍵字猜。由編輯依總表逐批指派最準。

## Definition of done

- [x] 已落地的財經 pack 每篇掛一個 finance 子主題；`docs/life-finance-series.md` 各批次段落註明對應子主題。

## Steps

- [x] 對照總表批次 → 子主題：01→finance-basics、02→banking/credit、03–04→tax-insurance、05–06→investing。
- [x] 改 `topics`，跑 lint 與測試，部署後匯入。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue docs/life-finance-series.md
```

## Notes

尚未落地的批次（03–06）在各自的批次任務裡直接帶子主題，不必回頭補。

2026-09-16 落地（claude-fable-5-1）：`pack_cli retopic --kind life --dry-run` 367 筆提案（365 條前綴／關鍵字規則、9 條系列成員）逐列審過，
全部符合 `docs/article-architecture.md` 核准的吸收規則，`--apply` 一次套用（a–m、n–z、財經批次同一個 commit）。
邊界案例留給編輯二審（規則一致所以先套）：`ai-tools-2026-overview`、`ai-reading-list-books-2026`、`ai-for-kids/seniors/students-*` 掛 `ai-work`
（詞彙表沒有「AI 日常」子主題）；`ansoff`／`bcg`／`pestle`／`porter`／`swot`／`business-models`／`design-thinking` 等策略框架掛 `content-marketing`
（規則：`marketing-*`、`brand-*` 一律歸 content-marketing）；`ga4-*`／`google-tag-manager`／`microsoft-clarity` 掛 `web-basics`。
仍只有父主題的 21 篇全在單層主題（`productivity`、`daily`、`software`：備份、書籤、Canva、剪片、桌面整理…），詞彙表本來就不給它們子主題，維持不動。
lint 0 error；`test_guides_content_pack`／`test_guides_retopic` 綠。部署後 `guides-import --dry-run` 應列 367 筆 taxonomy update。
