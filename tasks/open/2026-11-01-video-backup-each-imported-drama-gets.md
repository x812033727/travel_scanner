---
id: 2026-11-01-video-backup-each-imported-drama-gets
title: Video backup: each imported drama gets its own folder under drama/, and the flat backups move there
status: in-progress
priority: P2
area: api
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-11-01T15:32:18Z
created_at: 2026-11-01T15:32:17Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_backup
  - apps/api/tests/test_video_backup.py
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - docs/videos/BACKUP.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/README.md
---

# Video backup: each imported drama gets its own folder under drama/, and the flat backups move there

## Why

站主 2026-11-01：「備份時應該要整個系列放一起……不同劇要有不同資料夾，像是 我的雲端硬碟\AI\備份\drama\zhong-tian-qu-qi」.
Imported dramas have no `series_slug`, so `series_key` fell back to the category and every episode and compilation of
種田娶妻打天下 sat side by side in `AI/備份/drama/`.

## Definition of done

- [x] `apps/api/app/video_backup/target.py`: an imported drama (category `drama`, no `series_slug`, slug `<series>-e033`,
      `<series>-e001-005`, `-v2`) is filed under `drama/<series>/<episode>`; series key `<series>`.
- [x] A video backed up flat (`drama/<episode>`) gets `moved_from` in the worker config; the worker (`backup.mjs
      moveFolder`) runs `rclone moveto` first (server side, no upload), reports `pending` with the new folder, and the site
      stores it. A failed move holds that video back for the round; an absent old folder counts as moved.
- [x] Tests: `apps/api/tests/test_video_backup.py`, `tools/video/automation/backup.test.mjs`. Docs: BACKUP.md 〈資料夾排法〉.
- [ ] After deploy: the 20 zhong-tian videos listed under `AI/備份/drama/` sit in `AI/備份/drama/zhong-tian-qu-qi/`, and
      `/admin/videos?tab=settings#video-backup-settings` shows the new folders.

## How to verify

`cd apps/api && uv run pytest tests/test_video_backup.py`; `node --test tools/video/automation/backup.test.mjs`
