---
id: 2026-11-18-drive-links-in-admin
title: Open each video's Google Drive folder and final cut from the admin
status: done
priority: P1
area: web
owner: claude-opus-5-5-drive-links
claimed_at: 2026-11-18T02:28:23Z
created_at: 2026-11-18T02:27:50Z
completed_at: 2026-11-18T07:03:24Z
branch: claude/kind-mccarthy-5m28jo
depends_on: []
scope:
  - apps/web/lib/video-backup-messages
  - apps/web/components/admin-video-browser.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/tests/test_video_backup.py
  - apps/api/app/video_backup
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - apps/web/components/admin-video-backup.tsx
  - apps/web/components/admin-video-backup.test.tsx
  - docs/videos/BACKUP.md
---

# Open each video's Google Drive folder and final cut from the admin

## Why

The admin shows a video's Drive backup only as a path string (`AI/備份/AI劇/奇聞檔案局/H-歷史懸案/H01`); no Drive id or URL is stored anywhere, so the owner cannot click from /admin/videos to the folder or the cut, and every folder move needs moved_from code. Owner, 2026-11-18: links that open Drive directly.

## Definition of done

- [ ] Every video whose backup is done shows 在雲端硬碟開啟 (its folder) and 開成片 (final.mp4) on its backup line and in the catalog row.
- [ ] Videos backed up before this, whose host files are gone, get their links too.

## Steps

- [x] Worker: after the round's backups, look up the Drive folder id and final.mp4 id of up to N done videos the site says have none (`rclone lsjson --stat`), report them on a new tool route.
- [x] API: store `folder_id`, `final_file_id` in `video_projects.backup`; drop them when the folder changes; expose links on BackupView and the catalog's ProjectSummary.
- [x] Web: links on the backup card and the catalog row.

## How to verify

See the steps; each lands with tests.

## Notes

Phase 1 of the Drive plan (2026-11-18 session). Ids are kept in the existing JSON column, no migration.
- Claimed with `--force` (2026-11-18): the overlapping claims (2026-10-23 ready-to-upload backup,
  2026-11-02 Shorts sent by hand) describe work docs/videos/BACKUP.md records as landed; the other
  two only list the shared backup files.
