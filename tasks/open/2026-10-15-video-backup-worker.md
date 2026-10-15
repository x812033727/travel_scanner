---
id: 2026-10-15-video-backup-worker
title: Video backup round in the worker and the tidy hold
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-15T02:13:56Z
completed_at:
branch:
depends_on:
  - 2026-10-15-video-backup-api
scope:
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - tools/video/automation/tidy.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/cli.mjs
  - ops/video/Dockerfile
  - docker-compose.prod.yml
---

# Video backup round in the worker and the tidy hold

## Why

Only `video-worker` can write `video_work`, owns `auto.json` and runs tidy, so the copy to
Google Drive happens there, before tidy in each round. Design and folder layout:
`docs/videos/BACKUP.md`.

## Definition of done

- [ ] `recordVideoId` (flow.mjs) writes `auto.json.backup = {state: "pending"}`; a scan also
      queues any video with a YouTube ID and no `backup` (covers Shorts and the backfill of
      videos uploaded before this ships).
- [ ] `backup.mjs` round, run from `cli.mjs` before `tidyAfterRound`, at most
      `VIDEO_BACKUP_PER_ROUND` (default 2) videos, oldest first, skipped when backup is
      disabled or a `STOP` file exists:
  - [ ] builds the file list for the tier (basic: `upload/` final, metadata, descriptions
        → `descriptions/`, captions, dubs, plus `thumbnail.jpg`; full adds `clips/`,
        `keyframes/`, `characters/`, `timeline.json`, `narration.wav` and the series
        `_series/<series>/characters` once under `_共用/`), sha256 and sizes, and
        `files_hash`;
  - [ ] `rclone about` quota check: free < needed + 2 GB → `blocked_quota`;
  - [ ] `rclone copy --checksum --drive-chunk-size 64M --tpslimit 5 --retries 5` with
        `--backup-dir <ep>/_舊版/<ts>/`; never `sync`, never deletes remote files;
  - [ ] `rclone check --one-way --download=false`, then uploads `backup.json`, then writes
        `auto.json.backup = {state: "done", at, bytes, files_hash}` and reports to the API;
  - [ ] a changed `files_hash` (dubs or captions approved later) re-queues it;
  - [ ] 3 consecutive failures → `failed`, then one retry every 6 hours;
  - [ ] files already removed by tidy → copies what exists, `partial: true` with the
        missing list.
- [ ] Answers the API's test request: writes and deletes `_probe-<ts>.txt`, reports free
      space; reports `VIDEO_BACKUP_LOCK_PATH` on start.
- [ ] tidy `judge` holds a video while backup is enabled and its state is not `done` or the
      current `files_hash` differs; the hold reason appears in tidy's log.
- [ ] `ops/video/Dockerfile` installs a pinned rclone; `docker-compose.prod.yml` mounts
      `/etc/travel-scanner/rclone-videos.conf` read-only into `video-worker` and sets
      `VIDEO_BACKUP_LOCK_PATH`, `RCLONE_CONFIG`. A missing config file means "backup not
      configured", reported once, never a crash.

## Steps

- [ ] `backup.mjs` with an injected runner and fs; tests with a fake rclone (no network):
      happy path, quota block, check mismatch, re-queue on new dub, partial, retries.
- [ ] tidy hold + its tests.
- [ ] Dockerfile and compose.

## How to verify

```bash
npm run test:tools
node --test tools/video/automation/backup.test.mjs
```

## Notes

- Do not copy `segments/`, `build/`, `frames/`, `review/`, `media/` or `audio/`.
- rclone exit code must be checked directly; do not pipe it through `tail`.
