---
id: 2026-11-03-approved-upload-confirmations-take-the-full
title: Approved upload confirmations take the full backup tier on a resend
status: done
priority: P1
area: api
owner: claude-opus-5-5-backup-rules
claimed_at: 2026-11-03T07:22:19Z
created_at: 2026-11-03T07:22:18Z
completed_at: 2026-11-03T07:24:07Z
branch: claude/video-backup-attach-approved
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/clips.py
  - apps/api/app/video_backup/admin_status.py
  - apps/api/app/video_backup/schemas.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_backup.py
  - tools/video/automation/review-package.mjs
  - tools/video/automation/review-package.test.mjs
  - docs/videos/BACKUP.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Approved upload confirmations take the full backup tier on a resend

## Why

站主 2026-11-03：上架前每支影片在 VPS 都要有完整的一份。#1998 讓 `review-push --gate publish` 帶上完整層級，但 B01、B02
的上架確認在那之前就核准了；網站對已核准的同一份（同一個 metadata.json 雜湊）重送只回傳原紀錄、不收新檔。要另送一筆新的
上架確認得改 metadata.json 內容，而且新的核准會讓已核准的語言批次失效（language_package `_source` 綁上架確認），站主每支要
再核准兩次。站主選「補送，我再核准一次」；改成讓已核准的那筆收下只有備份讀的檔，站主不用再按。

## Definition of done

- [x] 已核准的上架確認重送時，只有備份讀的角色（kf_、clip_、recording_、keyframes_manifest、full_narration、full_timeline、
      recordings_manifest）加進那筆審核；其他檔與核准的一模一樣才收；payload、狀態、核准都不動；重送兩次只加一次。
- [x] worker 在 review_package 的檔數變了時再抓一次。
- [ ] 部署後重送 B01、B02 的上架確認，確認網站上檔數變多、worker 抓回 keyframes／narration.wav。

## Steps

- [x] `clips.backup_tier_role`；`admin_service._attach_backup_tier`；`ReviewPackage.files`；`review-package.mjs` 比對 `listed`。
- [x] 測試、BACKUP.md、時長審查重簽 admin_service.py。

## How to verify

`pytest tests/test_video_reviews.py tests/test_video_backup.py`；`node --test tools/video/automation/review-package.test.mjs`。

## Notes
