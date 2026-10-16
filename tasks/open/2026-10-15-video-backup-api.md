---
id: 2026-10-15-video-backup-api
title: Video backup settings and status in the API
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-15T02:13:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_backup
  - apps/api/tests/test_video_backup.py
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/migrations/versions
---

# Video backup settings and status in the API

## Why

Published videos exist only on the VPS, and tidy deletes `final.mp4`, dubs and clips seven
days after upload. The owner wants every uploaded video copied to Google Drive under
`AI/備份/<series>/`, grouped by series (design: `docs/videos/BACKUP.md`). The API holds
the setting the owner edits and the per-video backup status the admin shows; the worker
(`2026-10-15-video-backup-worker`) does the copying.

## Definition of done

- [ ] A private ProviderConfig row `video_backup`, modelled on
      `apps/api/app/video_youtube/vps_settings.py`: `enabled`, `path` (normalised to
      `AI/備份` from any of `G:\我的雲端硬碟\AI\備份\`, `G:\My Drive\AI\備份`, `/AI/備份/`),
      `tiers` overrides `{series_key: basic|full|off}`, `folder_names`
      `{series_key: display name}` with the defaults in BACKUP.md. Optimistic
      `expected_updated_at`, audit log on save, `settings.manage` to save,
      `content.read` to read. Not shown in the generic provider editor.
- [ ] Path validation: rejects empty, `..`, and anything not equal to or below the lock
      path the worker last reported (`VIDEO_BACKUP_LOCK_PATH`); the error says the rclone
      remote on the host must be changed for that.
- [ ] Default tier rule: `category in {drama, long-drama, anime}` → `full`, else `basic`;
      overrides win. One pure function, `resolve_target(project)` → `{series_key, folder,
      tier}`, following the order `series_slug` → `shorts_series` (under `Shorts/`) → slug
      prefix (`curio-`, `ai-term-`, `sothatswhy-`) → `category` → `其他`. Once
      `video_projects.backup.folder` is set it is returned unchanged.
- [ ] `video_projects.backup` JSON column (migration; take the next free number on
      origin/main right before pushing): `state` (pending|done|failed|blocked_quota|partial),
      `folder`, `tier`, `bytes`, `at`, `error`, `attempts`, `files_hash`.
- [ ] Admin routes: `GET/PUT /admin/video-backup/settings`, `POST /admin/video-backup/test`
      (records a test request; the worker answers it), `GET` test result.
- [ ] Worker (tool) routes: `GET automation/backup/config` (settings + resolved target per
      pending slug, plus any open test request), `POST automation/backup/{slug}/report`
      (writes `video_projects.backup`), `POST automation/backup/test/{id}` (result + free
      space), `POST automation/backup/lock` (the lock path the worker runs with).
- [ ] `backup` is in the admin video list/detail response.

## Steps

- [ ] Settings module and normaliser with unit tests (all path spellings above, Windows
      backslashes, trailing slash, `..` rejected).
- [ ] `resolve_target` with a table test covering curio, ou-de-jianghu episodes, Shorts,
      ai-term, plain category, nothing.
- [ ] Migration + model field; routes; register the routers.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_backup.py
```

## Notes

- Owner decisions 2026-10-15: location `AI/備份`; rclone with full `drive` scope locked by
  `root_folder_id` to that folder (plan A); drama/anime full, others basic. Drive plan
  and quota not decided yet.
- The Drive token never enters the database; it lives in `/etc/travel-scanner/rclone-videos.conf`
  on the host and only the worker reads it.
- Tool routes live next to `tool_router` in `apps/api/app/video_automation/admin_api.py`
  (e.g. `series/{slug}/episodes/{number}/done` at :989); a separate router in
  `video_backup` keeps this task out of that file.
