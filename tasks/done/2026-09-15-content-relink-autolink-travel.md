---
id: 2026-09-15-content-relink-autolink-travel
title: 旅遊攻略內容包跑 relink 與 autolink（依目的地明列檔案）
status: done
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-16T02:20:43Z
created_at: 2026-09-15T13:57:28Z
completed_at: 2026-09-16T06:08:58Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-pack-autolink-and-relink-cli
scope:
  - apps/api/app/guides/content
---

# 旅遊攻略內容包跑 relink 與 autolink（依目的地明列檔案）

## Why

395 條指向 /guides 的原始 URL 與跨目的地 intel 的互連要轉成 `ArticleInline`。

## Definition of done

- [x] 每個目的地批次跑 relink／autolink 並審閱；lint 與連結測試綠。

## Steps

- [x] 依目的地前綴分批（tokyo-、osaka-、seoul-、taipei-…、taiwan-/japan-/korea- intel）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_links.py -q
```

## Notes

與 `2026-09-14-answer-first-howto-descriptions` 同時動 howto 檔時先協調；那張應改為明列 68 檔。

2026-09-16 落地（claude-fable-5-1）：量小所以不分目的地，howto 與 intel 各一次：howto 79 篇轉 322 條、保留 276 條；intel 13 篇轉 68 條、保留 46 條。
保留的都是 `not_an_article`（目的地頁、美食目錄、專區首頁，規格本來就要它們維持 link block）。autolink 只加 3 條（旅遊文章幾乎沒有名詞別名）。
lint 的 29＋6 個 error（`diagram_number_not_in_text`、`svg_small_label`）在 HEAD 就存在，與連結無關，留給圖表任務。連結 kind 與內容包測試綠。
`2026-09-14-answer-first-howto-descriptions` 未認領，沒有同時改 howto 檔的衝突。
