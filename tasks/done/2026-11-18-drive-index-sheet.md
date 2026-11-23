---
id: 2026-11-18-drive-index-sheet
title: Generate a daily Google Drive index sheet of every show and episode
status: done
priority: P2
area: tools
owner: claude-opus-5-5-drive-index
claimed_at: 2026-11-18T04:42:22Z
created_at: 2026-11-18T02:27:51Z
completed_at: 2026-11-18T07:03:25Z
branch: claude/kind-mccarthy-5m28jo
depends_on:
  - 2026-11-18-drive-links-in-admin
scope:
  - tools/video/automation/backup.test.mjs
  - tools/video/automation/review-package.test.mjs
  - apps/api/app/video_backup/admin_status.py
  - apps/api/app/video_backup/admin_api.py
  - apps/api/app/video_backup/schemas.py
  - apps/api/tests/test_video_backup.py
  - tools/video/automation/backup.mjs
  - tools/video/automation/drive-index.mjs
  - tools/video/automation/drive-index.test.mjs
  - docs/videos/BACKUP.md
  - docs/videos/ai-drama-drive/BACKUP-LOG.md
---

# Generate a daily Google Drive index sheet of every show and episode

## Why

Nothing lists what is on Drive: the explainer catalog (`docs/videos/ai-drama-drive/catalog.py`) covers only 奇聞檔案局/原來如此事務所 and is uploaded by hand; the dramas, Shorts and other series have none, and 製作檔/ has no manifest, so a session cannot tell whether reference art already exists (2026-11-12-tai-nainai-e009-e060-missing-refs).

## Definition of done

- [x] A Google Sheet (or CSV) under `AI/備份/_總表`, refreshed daily, one tab a show: code, title, topic, state, YouTube, Drive folder link, backup state, size.
- [ ] Moved to 2026-11-18-drive-single-writer-shared-assets: each 製作檔 upload leaves a manifest.json (it changes todrive.sh, which that task owns).

## Steps

- [x] API: GET /video/automation/backup/index, rows grouped by series with labels and Drive links.
- [x] Worker: drive-index.mjs, once a day after the backup round, one CSV per show plus 全部, uploaded with `--drive-import-formats csv` into `<prefix>/_總表/` so Drive keeps them as Google Sheets.
- [x] catalog.py stays for its repo-only columns; docs point to the new index.

## How to verify

See the steps; each lands with tests.

## Notes

Phase 2 of the Drive plan.
- Claimed with `--force` (2026-11-18) only past its dependency: the owner chose phase 2 next while phase 1 waits to merge on the same branch.
- A successful index is recorded in `_backup-index.json`, not logged: the deploy check
  (.agents/skills/deploy/scripts/host-verify.sh) treats unknown `backup:` lines next to a capped
  exit as failures. `VIDEO_BACKUP_INDEX_HOURS=0` turns the index off; tests that run whole backup
  rounds set it.
