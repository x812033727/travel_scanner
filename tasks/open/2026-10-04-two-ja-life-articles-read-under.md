---
id: 2026-10-04-two-ja-life-articles-read-under
title: Two ja life articles read under the 1,500-character floor once link-only lines stopped counting
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-ja-life-length
claimed_at: 2026-10-05T06:28:37Z
created_at: 2026-10-04T15:45:25Z
completed_at:
branch: claude/ja-life-length
depends_on: []
scope:
  - apps/api/app/guides/content/household-inventory-spreadsheet.json
  - apps/api/app/guides/content/weekly-review-reset-routine.json
---

# Two ja life articles read under the 1,500-character floor once link-only lines stopped counting

## Why

`2026-10-03-body-length-link-only-paragraphs`（2026-10-04）讓只含連結的 `rich_paragraph`（文末「延伸閱讀」那種單行連結）不再算進
`_body_length`。全站 2,450 個（pack, locale）裡 2,239 個字數下降，其中兩篇 ja 從剛好過線變成低於 life 的 1,500 字下限，
`pack_cli lint --kind life` 因此多了兩個 `text_length` 警告：

| pack | locale | 之前 | 之後 |
| --- | --- | --- | --- |
| `household-inventory-spreadsheet` | ja | 1,538 | 1,496 |
| `weekly-review-reset-routine` | ja | 1,512 | 1,482 |

兩篇各只有一行站內連結被扣掉，正文本身沒變；它們的 zh-TW 原文本來就短（984 → 960、984 → 957，一直有 `text_length` 警告），
所以低於下限的 pack 數不變（前後都是 19 個），只是同一篇多了一個語言被點名。這是警告不是錯誤，不擋 ingest 或 CI。

## Definition of done

- [ ] 這兩篇的五個語言要嘛補到 1,500 字以上（補的是讀者用得到的內容，不是填字數），要嘛在本票 Notes 寫明為什麼保留短篇。
- [ ] `uv run python -m app.guides.pack_cli lint --kind life --slug household-inventory-spreadsheet --slug weekly-review-reset-routine`
      不再有 ja 的 `text_length` 警告，或 Notes 交代保留的理由。

## Steps

- [ ] 讀兩篇的 zh-TW 原文，判斷值不值得擴寫（走 skill `content-pipeline` 的改稿流程，五語一起改）。
- [ ] 擴寫或記錄保留的決定。

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life   --slug household-inventory-spreadsheet --slug weekly-review-reset-routine
```

## Notes

- 量測：2026-10-04 在 `claude/pack-ingest-body-length-render-svg` 上，用 `_body_length` 對全站每個（pack, locale）前後各算一次比對。
- 同一輪也有 25 個原本超過 6,000（intel 3,000）上限的（pack, locale）回到範圍內，例如 `ai-news-2026-january-september-index`、
  `tech-news-2026-index` 的 zh-TW。
