---
id: 2026-10-03-body-length-link-only-paragraphs
title: _body_length counts link-only paragraphs although its docstring excludes link labels
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-03T12:04:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guide_rich_blocks.py
---

# _body_length counts link-only paragraphs although its docstring excludes link labels

## Why

`_body_parts` 的 docstring 寫它算的是 running text，「not the title, captions or link labels」；`link` 區塊確實不算，
但一個只含一個 `article` inline 的 `rich_paragraph`（站內「延伸閱讀」那種單行連結）整段算進正文。
後果：連結多的頁面字數被高估。`ai-terms-index` 有 105 條這種連結，正文因此一度跑到 5,910 字逼近 life 的 6,000 警告線，
2026-10-03 只好把連結文字縮成名詞本身。

## Definition of done

- [ ] 只含連結 inline、沒有其他文字的 `rich_paragraph` 不算進 `_body_length`（句子中的連結照算，因為它是句子的一部分）。
- [ ] 測試涵蓋兩種情況；全站 `pack_cli lint` 沒有新的 `text_length` 警告（低於 1,500 的那端要看一下）。

## Steps

- [ ] 改 `_body_parts`、加測試、跑全站 lint 比對前後字數。

## How to verify

`uv run pytest tests/test_guide_rich_blocks.py tests/test_guides_pack_ingest.py -q`；`pack_cli lint --kind life`。

## Notes

- `pack_ingest.py` 在 `2026-09-14-codex-learning-series`（blocked）的 scope 裡，要先協調。
