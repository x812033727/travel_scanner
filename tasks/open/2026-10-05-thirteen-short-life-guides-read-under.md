---
id: 2026-10-05-thirteen-short-life-guides-read-under
title: Thirteen short life guides read under the 1,500-character floor in zh-TW, zh-CN and ko
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T06:52:42Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/backup-and-restore-home-files.json
  - apps/api/app/guides/content/browser-bookmark-project-folders.json
  - apps/api/app/guides/content/desk-cable-charging-organization.json
  - apps/api/app/guides/content/digital-receipt-archive.json
  - apps/api/app/guides/content/email-triage-three-actions.json
  - apps/api/app/guides/content/file-naming-system-for-home.json
  - apps/api/app/guides/content/gadget-purchase-needs-checklist.json
  - apps/api/app/guides/content/meeting-notes-action-template.json
  - apps/api/app/guides/content/notification-focus-boundaries.json
  - apps/api/app/guides/content/phone-document-scanning-workflow.json
  - apps/api/app/guides/content/phone-photo-declutter-workflow.json
  - apps/api/app/guides/content/reading-notes-that-you-reuse.json
  - apps/api/app/guides/content/shared-household-calendar.json
---

# Thirteen short life guides read under the 1,500-character floor in zh-TW, zh-CN and ko

## Why

`2026-10-04-two-ja-life-articles-read-under` 把 `household-inventory-spreadsheet` 與 `weekly-review-reset-routine`
五語都補過 1,500 字之後，`pack_cli lint --kind life` 仍有 17 個 pack 有低於下限的 `text_length` 警告。其中四個是索引／目錄頁
（`claude-code-templates-cheatsheet`、`claude-code-tutorials`、`codex-learning-hub`、`gemini-guide`），短是設計，不在本票。
其餘 13 篇和那兩篇同一批（#468 的生活分享原創文）：zh-TW 原文約 950–1,010 字，zh-CN 跟著短，ko 多半在 1,400 上下，
少數連 ja 也低於下限。讀者拿到的是一篇偏短、缺一兩個實際操作段落的文章；這是警告不是錯誤，不擋 ingest 或 CI。

2026-10-05 在 `claude/ja-life-length` 上量的 `_body_length`（只列低於 1,500 的語言）：

| pack | 低於下限的語言 |
| --- | --- |
| `backup-and-restore-home-files` | zh-TW 1,004、ko 1,433、zh-CN 1,050 |
| `browser-bookmark-project-folders` | zh-TW 997、ko 1,455、zh-CN 1,070 |
| `desk-cable-charging-organization` | zh-TW 953、ko 1,427、zh-CN 997 |
| `digital-receipt-archive` | zh-TW 1,001、ko 1,436、zh-CN 1,075 |
| `email-triage-three-actions` | zh-TW 955、ja 1,442、ko 1,224、zh-CN 995 |
| `file-naming-system-for-home` | zh-TW 1,011、ko 1,415、zh-CN 1,018 |
| `gadget-purchase-needs-checklist` | zh-TW 974、ko 1,407、zh-CN 992 |
| `meeting-notes-action-template` | zh-TW 951、ja 1,405、ko 1,293、zh-CN 990 |
| `notification-focus-boundaries` | zh-TW 956、ja 1,445、ko 1,271、zh-CN 991 |
| `phone-document-scanning-workflow` | zh-TW 986、ko 1,412、zh-CN 1,020 |
| `phone-photo-declutter-workflow` | zh-TW 1,001、ko 1,445、zh-CN 1,011 |
| `reading-notes-that-you-reuse` | zh-TW 970、ko 1,379、zh-CN 982 |
| `shared-household-calendar` | zh-TW 966、ko 1,369、zh-CN 990 |

## Definition of done

- [ ] 每一篇要嘛五語都補到 1,500 字以上（補讀者用得到的操作段落，不是填字數、不是連結清單），要嘛在本票 Notes 寫明為什麼保留短篇。
- [ ] `pack_cli lint --kind life` 對這 13 個 slug 不再有低於下限的 `text_length` 警告，或 Notes 逐篇交代保留的理由。
- [ ] 改過的內容包在合併後由協調者經站主同意重新匯入（`guides-import --slug ... --dry-run`，再 `--publish`）。

## Steps

- [ ] 逐篇讀 zh-TW 原文，判斷缺哪一段讀者真的會用到的內容（走 skill `content-pipeline`，五語一起改，en 不要超過 6,000）。
- [ ] 新增的產品功能、數字都要有當天打開的官方來源並更新 `checked_on`；沒有新事實就只重開既有來源確認仍成立。
- [ ] 跑下方的 lint、`intake_check.py --from-content`、`docs/news-2026-batch-4/translation_checks.py`、`tests/test_guides_content_pack.py`。

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life \
  --slug backup-and-restore-home-files --slug browser-bookmark-project-folders \
  --slug desk-cable-charging-organization --slug digital-receipt-archive \
  --slug email-triage-three-actions --slug file-naming-system-for-home \
  --slug gadget-purchase-needs-checklist --slug meeting-notes-action-template \
  --slug notification-focus-boundaries --slug phone-document-scanning-workflow \
  --slug phone-photo-declutter-workflow --slug reading-notes-that-you-reuse \
  --slug shared-household-calendar
```

## Notes

- 從 `2026-10-04-two-ja-life-articles-read-under` 發現（不是拆票）。那張票的做法可以照抄：每篇加一個 H2（約 450–600 個 zh-TW 字，
  段落加一張小表或清單），內容是原文沒講到的操作規則，例如「誰在什麼時候更新」「中斷後怎麼接回來」；四語由同一份 zh-TW 對譯。
- `no_summary` 與 `intake_check.py` 的「first block is not summary」不在本票：摘要走 `2026-09-15-content-summary-howto-and-life`，
  那張票要站主逐批審 diff。
- 只補正文，不改標題：其他文章的 article inline 把這些標題存成自己的 `text`，改標題會牽動別的內容包。
