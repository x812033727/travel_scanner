---
id: 2026-10-15-video-backup-worker
title: Video backup round in the worker and the tidy hold
status: done
priority: P1
area: tools
owner: claude-festive-archimedes
claimed_at: 2026-10-19T16:20:20Z
created_at: 2026-10-15T02:13:56Z
completed_at: 2026-10-19T16:35:56Z
branch: claude/festive-archimedes-9ntb36
depends_on:
  - 2026-10-15-video-backup-api
scope:
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
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

- [x] ~~`recordVideoId` (flow.mjs) writes `auto.json.backup = {state: "pending"}`;~~ a scan
      queues any video with a YouTube ID and no backup record (covers Shorts, the backfill of
      videos uploaded before this ships, and a video `recordVideoId` just recorded, in the same
      round). flow.mjs is left alone; see Notes.
- [x] `backup.mjs` round, run from `cli.mjs` before `tidyAfterRound`, at most
      `VIDEO_BACKUP_PER_ROUND` (default 2) videos, oldest first, skipped when backup is
      disabled or a `STOP` file exists:
  - [x] builds the file list for the tier (basic: `upload/` final, metadata, descriptions
        → `descriptions/`, captions, dubs, plus `thumbnail.jpg`; full adds `clips/`,
        `keyframes/`, `characters/`, `timeline.json`, `narration.wav` and the series
        `_series/<series>/characters` once under `_共用/`), sha256 and sizes, and
        `files_hash`;
  - [x] `rclone about` quota check: free < needed + 2 GB → `blocked_quota`;
  - [x] `rclone copy --checksum --drive-chunk-size 64M --tpslimit 5 --retries 5` with
        `--backup-dir <ep>/_舊版/<ts>/`; never `sync`, never deletes remote files;
  - [x] `rclone check --one-way --download=false`, then uploads `backup.json`, then writes
        `auto.json.backup = {state: "done", at, bytes, files_hash}` and reports to the API;
  - [x] a changed `files_hash` (dubs or captions approved later) re-queues it;
  - [x] 3 consecutive failures → `failed`, then one retry every 6 hours;
  - [x] files already removed by tidy → copies what exists, `partial: true` with the
        missing list.
- [x] Answers the API's test request: writes and deletes `_probe-<ts>.txt`, reports free
      space; reports `VIDEO_BACKUP_LOCK_PATH` on start.
- [x] tidy `judge` holds a video while backup is enabled and its state is not `done` or the
      current `files_hash` differs; the hold reason appears in tidy's log.
- [x] `ops/video/Dockerfile` installs a pinned rclone; `docker-compose.prod.yml` mounts
      `/etc/travel-scanner/rclone-videos.conf` read-only into `video-worker` and sets
      `VIDEO_BACKUP_LOCK_PATH`, `RCLONE_CONFIG`. A missing config file means "backup not
      configured", reported once, never a crash.

## Steps

- [x] `backup.mjs` with an injected runner and fs; tests with a fake rclone (no network):
      happy path, quota block, check mismatch, re-queue on new dub, partial, retries.
- [x] tidy hold + its tests.
- [x] Dockerfile and compose.

## How to verify

```bash
npm run test:tools
node --test tools/video/automation/backup.test.mjs
```

## Notes

- Do not copy `segments/`, `build/`, `frames/`, `review/`, `media/` or `audio/`.
- rclone exit code must be checked directly; do not pipe it through `tail`.
- API contract (landed with `2026-10-15-video-backup-api`, see its Notes): read
  `GET /api/video/automation/backup/config` and copy only when `remote_prefix` is not null
  (it is the configured path relative to the remote's root). A `done` report must include
  `contents` as `app/video_backup/schemas.py` `BackupContents` describes; the site turns a
  report that lacks a chosen language's file into `partial`, so tidy keeps the files.
- The basic tier should copy the whole `upload/` tree, not only the files listed above:
  `package` also writes `thumbnails/<locale>.jpg` and the `thumbnail-b.jpg`/`-c.jpg`
  variants there, and `thumbnail.jpg` lives in `upload/`, not the work directory's root
  (`tools/video/package/check.mjs`). A Short's `upload/` holds `final.mp4`, `zh-TW.srt`,
  `cover.png` and `titles.json`.
- Done 2026-10-19 (claude-festive-archimedes), in `tools/video/automation/backup.mjs`:
  `backupRound` runs once a round from `cli.mjs` before the tidy, also when automatic drafts
  are off, and hands the tidy a gate. The hand-run `tidy` judges with `copy: false`.
- **Where the state lives:** `<workdir>/backup-state.json` (state, attempts, error,
  `site_state`, missing), not `auto.json.backup`, so a lane saving an older copy of
  `auto.json` can never erase it. `<workdir>/backup.json` is the manifest of what Drive holds
  (path, size, mtime, sha256 per file). It is uploaded last, and its cached hashes mean a round
  re-reads only files whose size or mtime changed. The staging folder is
  `<base>/_backup-stage/<slug>/` (hard links, removed after each copy); the tidy skips `_` names.
- **Requeue rule:** a video is copied again when a file in the tier's plan is new or its
  sha256 differs from backup.json. Files the tidy removed do not count (Drive keeps them; copy
  never deletes), so a tidied video is not re-queued forever.
- **The tidy may clear a video only when** the backup is done **and** the site answered done
  for the same report (`site_state`). Partial, pending, failed, blocked by quota, a done the
  site has not heard, new files, a site that cannot answer, or rclone not configured while
  backups are on: all hold the video, and the round prints how many are held.
  Backups switched off, or a site from before these routes (404 on the config): the tidy works
  as before.
- **Config mount changed from the plan:** compose mounts the folder
  `/etc/travel-scanner/rclone-videos/` read-only at `/etc/mokaair/rclone-videos/`
  (`VIDEO_BACKUP_RCLONE_CONFIG=/etc/mokaair/rclone-videos/rclone.conf`). Mounting a single
  file that does not exist yet makes Docker create a folder in its place, which would block the
  host setup. The file must be readable by uid 1001 (pwuser): `install -o 1001 -g 1001 -m 0600`.
  The worker copies it to `/tmp/rclone-videos.conf` each run, so rclone can save a refreshed
  token without writing the host's file. `/etc/travel-scanner` is already in the nightly
  config bundle (`ops/backup/manifest-paths.txt` line 5).
- rclone v1.74.4, pinned by version and by the SHA-256 from downloads.rclone.org's
  SHA256SUMS (amd64 and arm64). The smoke stage checks `rclone version`.
- Verified with the real rclone v1.74.4 against a local `alias` remote: copy into the series
  folder, `--backup-dir <ep>/_舊版/<ts>` with `--exclude /_舊版/**` (rclone refuses an
  overlapping backup-dir without that filter), `check --one-way` exits 1 for a differing or
  missing file, the probe copyto + deletefile. Unit tests use a fake rclone over real folders.
- `rclone check` takes no `--download=false` flag; without `--download` it compares hashes
  (Drive and local both have md5), so nothing is downloaded.
