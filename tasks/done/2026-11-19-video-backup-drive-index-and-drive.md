---
id: 2026-11-19-video-backup-drive-index-and-drive
title: Video backup: Drive index and Drive ids never reach the site
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-11-19T07:19:07Z
created_at: 2026-11-19T07:18:44Z
completed_at: 2026-11-19T07:19:10Z
branch:
depends_on: []
scope:
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - apps/web/app/api/video/automation/backup/index/route.ts
  - apps/web/app/api/video/automation/backup/[slug]/drive/route.ts
  - apps/web/app/api/video/automation/backup/route.test.ts
---

# Video backup: Drive index and Drive ids never reach the site

## Why

Since #2150 the video worker logs, every round on the production host (seen 2026-11-19 after
deploying 0c92132e3):

- `backup: the Drive index could not be read from the site (HTTP 404)`: the worker calls the site
  through the web container, and the web BFF had no `GET /api/video/automation/backup/index` route
  (nor `POST .../[slug]/drive`), though the API has both. The daily `_總表/` sheets were never
  written, and Drive ids could never be reported.
- `backup: <slug>: the id of its Drive folder could not be read` for every video asking for ids:
  `rclone lsjson --stat <folder>` (rclone 1.74) answers a folder as the root of its own listing,
  with no `ID`. Files do carry one. The folders are there (e.g. `ai-news/openai-devday-2026-recap`).

## Definition of done

- [x] The worker reads the index and reports Drive ids through the web BFF.
- [x] A backed-up video's folder id is read from its parent's listing; final.mp4 keeps `--stat`.

## Steps

- [x] Add the `index` (GET) and `[slug]/drive` (POST) proxy routes, slug checked like `report`.
- [x] `driveFolderId()` lists the parent with `lsjson --dirs-only` and takes the one folder of
      that name (none or several: null, tried again next round).
- [x] The fake rclone in backup.test.mjs answers a folder's `--stat` without an ID, like the real one.

## How to verify

`npm run test:tools`, `npx vitest run app/api/video/automation/backup` in apps/web. After the
deploy, `docker logs travel_scanner-video-worker-1` no longer shows either line, and
`/admin/videos` links the videos' Drive folders.

## Notes

- Inside the worker: `rclone --config /etc/mokaair/rclone-videos/rclone.conf lsjson --dirs-only videobackup:ai-news`
  shows each folder's `ID`; `--stat` on the same folder does not.
- Every rclone call also prints `Failed to save config ... read-only file system`: the config is
  mounted read-only, so a refreshed access token is not saved. Harmless today; not changed here.
