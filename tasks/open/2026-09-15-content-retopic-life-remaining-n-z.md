---
id: 2026-09-15-content-retopic-life-remaining-n-z
title: 生活分享無前綴文章重新分類（slug n–z）：審閱 retopic 提案並套用
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

# 生活分享無前綴文章重新分類（slug n–z）：審閱 retopic 提案並套用

## Why

同 `content-retopic-life-remaining-a-m`，這張處理 slug 首字 n–z。

## Definition of done

- [x] 每篇 n–z 的無前綴 life pack 都掛上至少一個子主題，或在 Notes 記下為何維持父主題。
- [x] lint 與內容包測試通過。

## Steps

- [x] `pack_cli retopic --kind life --dry-run` 匯出表，篩 slug n–z。
- [x] 逐篇審閱後套用。
- [x] 部署後匯入。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
```

## Notes

與 a–m 那張不可同時 in-progress（scope 相同）。

2026-09-16 落地（claude-fable-5-1）：`pack_cli retopic --kind life --dry-run` 367 筆提案（365 條前綴／關鍵字規則、9 條系列成員）逐列審過，
全部符合 `docs/article-architecture.md` 核准的吸收規則，`--apply` 一次套用（a–m、n–z、財經批次同一個 commit）。
邊界案例留給編輯二審（規則一致所以先套）：`ai-tools-2026-overview`、`ai-reading-list-books-2026`、`ai-for-kids/seniors/students-*` 掛 `ai-work`
（詞彙表沒有「AI 日常」子主題）；`ansoff`／`bcg`／`pestle`／`porter`／`swot`／`business-models`／`design-thinking` 等策略框架掛 `content-marketing`
（規則：`marketing-*`、`brand-*` 一律歸 content-marketing）；`ga4-*`／`google-tag-manager`／`microsoft-clarity` 掛 `web-basics`。
仍只有父主題的 21 篇全在單層主題（`productivity`、`daily`、`software`：備份、書籤、Canva、剪片、桌面整理…），詞彙表本來就不給它們子主題，維持不動。
lint 0 error；`test_guides_content_pack`／`test_guides_retopic` 綠。部署後 `guides-import --dry-run` 應列 367 筆 taxonomy update。
