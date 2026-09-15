---
id: 2026-09-15-content-relink-autolink-travel
title: 旅遊攻略內容包跑 relink 與 autolink（依目的地明列檔案）
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-15T13:57:28Z
completed_at:
branch:
depends_on:
  - 2026-09-15-pack-autolink-and-relink-cli
scope:
  - apps/api/app/guides/content
---

# 旅遊攻略內容包跑 relink 與 autolink（依目的地明列檔案）

## Why

395 條指向 /guides 的原始 URL 與跨目的地 intel 的互連要轉成 `ArticleInline`。

## Definition of done

- [ ] 每個目的地批次跑 relink／autolink 並審閱；lint 與連結測試綠。

## Steps

- [ ] 依目的地前綴分批（tokyo-、osaka-、seoul-、taipei-…、taiwan-/japan-/korea- intel）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_links.py -q
```

## Notes

與 `2026-09-14-answer-first-howto-descriptions` 同時動 howto 檔時先協調；那張應改為明列 68 檔。
