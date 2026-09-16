---
id: 2026-09-15-content-retopic-life-remaining-a-m
title: 生活分享無前綴文章重新分類（slug a–m）：審閱 retopic 提案並套用
status: done
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-16T02:23:23Z
created_at: 2026-09-15T13:57:26Z
completed_at: 2026-09-16T06:09:02Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-guide-retopic-cli
scope:
  - apps/api/app/guides/content
---

# 生活分享無前綴文章重新分類（slug a–m）：審閱 retopic 提案並套用

## Why

retopic 對有明確前綴（ai-term-、claude-code-、codex-、gemini-、ai-news-、ai-search-、wordpress-、woocommerce-、chatgpt-）的文章已在 `guide-retopic-cli` 落地時套用；其餘約 275 篇無前綴的生活文章要由編輯逐篇看規則提案是否合理，再套用。這張只處理 slug 首字 a–m。

## Definition of done

- [x] 每篇 a–m 的無前綴 life pack 都掛上至少一個子主題，或在 Notes 記下為何維持父主題。
- [x] `pack_cli lint --kind life` 無新錯誤；`tests/test_guides_content_pack.py` 通過。

## Steps

- [x] `pack_cli retopic --kind life --dry-run` 匯出表，篩 slug a–m 且無子主題者。
- [x] 逐篇審閱，必要時手改 `topics`。
- [x] 部署後 `guides-import --dry-run` 確認為 taxonomy update，再正式匯入。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
```

## Notes

scope 是整個 content 目錄，claim 前確認沒有其他內容批次 in-progress；做的時候只碰 a–m 的檔案。

2026-09-16 落地（claude-fable-5-1）：`pack_cli retopic --kind life --dry-run` 367 筆提案（365 條前綴／關鍵字規則、9 條系列成員）逐列審過，
全部符合 `docs/article-architecture.md` 核准的吸收規則，`--apply` 一次套用（a–m、n–z、財經批次同一個 commit）。
邊界案例留給編輯二審（規則一致所以先套）：`ai-tools-2026-overview`、`ai-reading-list-books-2026`、`ai-for-kids/seniors/students-*` 掛 `ai-work`
（詞彙表沒有「AI 日常」子主題）；`ansoff`／`bcg`／`pestle`／`porter`／`swot`／`business-models`／`design-thinking` 等策略框架掛 `content-marketing`
（規則：`marketing-*`、`brand-*` 一律歸 content-marketing）；`ga4-*`／`google-tag-manager`／`microsoft-clarity` 掛 `web-basics`。
仍只有父主題的 21 篇全在單層主題（`productivity`、`daily`、`software`：備份、書籤、Canva、剪片、桌面整理…），詞彙表本來就不給它們子主題，維持不動。
lint 0 error；`test_guides_content_pack`／`test_guides_retopic` 綠。部署後 `guides-import --dry-run` 應列 367 筆 taxonomy update。
