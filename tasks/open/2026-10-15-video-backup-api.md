---
id: 2026-10-15-video-backup-api
title: Video backup settings and status in the API
status: in-progress
priority: P1
area: api
owner: claude-festive-archimedes
claimed_at: 2026-10-19T12:27:00Z
created_at: 2026-10-15T02:13:53Z
completed_at:
branch: claude/festive-archimedes-9ntb36
depends_on: []
scope:
  - apps/api/app/video_backup
  - apps/api/tests/test_video_backup.py
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/migrations/versions/0135_video_backup.py
  - apps/api/tests/test_migration_0135_video_backup.py
  - apps/web/app/api/video/automation/backup
---

# Video backup settings and status in the API

## Why

Published videos exist only on the VPS, and tidy deletes `final.mp4`, dubs and clips seven
days after upload. The owner wants every uploaded video copied to Google Drive under
`AI/備份/<series>/`, grouped by series (design: `docs/videos/BACKUP.md`). The API holds
the setting the owner edits and the per-video backup status the admin shows; the worker
(`2026-10-15-video-backup-worker`) does the copying.

## Definition of done

- [x] A private ProviderConfig row `video_backup`, modelled on
      `apps/api/app/video_youtube/vps_settings.py`: `enabled`, `path` (normalised to
      `AI/備份` from any of `G:\我的雲端硬碟\AI\備份\`, `G:\My Drive\AI\備份`, `/AI/備份/`),
      `tiers` overrides `{series_key: basic|full|off}`, `folder_names`
      `{series_key: display name}` with the defaults in BACKUP.md. Optimistic
      `expected_updated_at`, audit log on save, `settings.manage` to save,
      `content.read` to read. Not shown in the generic provider editor.
- [x] Path validation: rejects empty, `..`, and anything not equal to or below the lock
      path the worker last reported (`VIDEO_BACKUP_LOCK_PATH`); the error says the rclone
      remote on the host must be changed for that.
- [x] Default tier rule: `category in {drama, long-drama, anime}` → `full`, else `basic`;
      overrides win. One pure function, `resolve_target(project)` → `{series_key, folder,
      tier}`, following the order `series_slug` → `shorts_series` (under `Shorts/`) → slug
      prefix (`curio-`, `ai-term-`, `sothatswhy-`) → `category` → `其他`. Once
      `video_projects.backup.folder` is set it is returned unchanged.
- [x] `video_projects.backup` JSON column (migration; take the next free number on
      origin/main right before pushing): `state` (pending|done|failed|blocked_quota|partial),
      `folder`, `tier`, `bytes`, `at`, `error`, `attempts`, `files_hash`.
- [x] Admin routes: `GET/PUT /admin/video-backup/settings`, `POST /admin/video-backup/test`
      (records a test request; the worker answers it), `GET` test result.
- [x] Worker (tool) routes: `GET automation/backup/config` (settings + resolved target per
      pending slug, plus any open test request), `POST automation/backup/{slug}/report`
      (writes `video_projects.backup`), `POST automation/backup/test/{id}` (result + free
      space), `POST automation/backup/lock` (the lock path the worker runs with).
- [x] ~~`backup` is in the admin video list/detail response.~~ Replaced by
      `GET /admin/video-backup/status` and `/status/{slug}` (see Notes): the list's
      `video_reviews/schemas.py` and `admin_service.py` are held by two active tasks.

## Steps

- [x] Settings module and normaliser with unit tests (all path spellings above, Windows
      backslashes, trailing slash, `..` rejected).
- [x] `resolve_target` with a table test covering curio, ou-de-jianghu episodes, Shorts,
      ai-term, plain category, nothing.
- [x] Migration + model field; routes; register the routers.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_backup.py tests/test_migration_0135_video_backup.py
cd apps/web && npx vitest run app/api/video/automation/backup
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
- Done 2026-10-19 (claude-festive-archimedes). Code in `apps/api/app/video_backup/`
  (`target.py` pure rules, `settings.py` the card, `status.py` reports and summary,
  `admin_api.py` routes), migration `0135_video_backup` (follows 0133; 0134 is the story
  pilot's planned number), and the web pass-throughs under
  `apps/web/app/api/video/automation/backup/` (the worker reaches the API only through web).
- **The site does not take "done" on trust.** A `done` report must carry `files_hash`,
  `bytes`, `files` and `contents` (what `rclone check` confirmed in Drive, by kind:
  `final`, `metadata`, `thumbnail`, `descriptions`/`captions`/`dubs` locale lists,
  `skipped` with the locales the package skipped with a reason, `clips`, `keyframes`).
  `target.missing_files` counts it against `final.mp4` + `metadata.json` (a Short: only
  `final.mp4`; its card package has no metadata.json) and the owner's language choice in
  `video_projects.locales`; anything missing turns the report into `partial` with the list,
  so tidy keeps the files. A complete backup reads `stale` when the owner later chooses
  another language or a fuller tier.
- `GET /admin/video-backup/status` answers "is every uploaded video in AI/備份":
  `all_backed_up` is true only when backups are on and every video with a YouTube id is
  `done` (series set to off aside); `counts` by state, including `not_queued` (never
  reported) and `stale`; `overdue` marks a video queued for over 24 h. `?all=true` lists
  every video. The web card (`2026-10-15-video-backup-web`) should read this, not the list.
- The optimistic stamp is `config.saved_at`, not the row's `updated_at`: the worker's lock,
  test answer and free-space writes bump `updated_at` and must not make the owner's next
  save a conflict.
- Shorts are always filed under `Shorts/<shorts_series or shorts_line>/<slug>`, even with a
  `series_slug`, matching BACKUP.md's folder layout rather than the order listed above.
  Tier overrides key on the same series key, so a Shorts series sharing a key with a long
  series shares its override.
- The worker config lists every video with a YouTube id (not only pending ones), each with
  its `folder`, `shared_folder`, `tier`, `expected` parts and last `backup` record, so the
  worker can notice a changed `files_hash` on a video that was done.
- The PostgreSQL half of `tests/test_migration_0135_video_backup.py` was not run here (no
  local PostgreSQL); it runs in CI with `RUN_INTEGRATION_TESTS=1`.
