---
id: 2026-09-27-video-binge-ops
title: Video binge O6: the API reads the worker's volume for compilation downloads
status: done
priority: P2
area: ops
owner: claude-fable
claimed_at: 2026-09-27T12:18:07Z
created_at: 2026-09-27T11:43:47Z
completed_at: 2026-09-27T12:20:23Z
branch: claude/keen-hamilton-plu6kp
depends_on: []
scope:
  - docker-compose.prod.yml
  - .env.example
---

# Video binge O6: the API reads the worker's volume for compilation downloads

## Why

A binge series' compilation (docs/videos/BINGE.md) is a 1080p cut of about two hours, too big
for the review store; the API serves it from the worker's work volume, mounted read-only, and
the review store takes a 720p preview of up to two hours.

## Definition of done

- [x] `docker-compose.prod.yml`: the `api` service mounts `video_work` at
      `/var/lib/mokaair/video-work:ro` and sets `VIDEO_WORK_DIR`.
- [x] `.env.example`: `VIDEO_REVIEW_MAX_FILE_BYTES` 2.5 GB, `VIDEO_REVIEW_MAX_TOTAL_BYTES` 30 GB,
      `VIDEO_WORK_DIR`, each with why.

## Steps

- [x] Compose and env example.

## How to verify

`docker compose -f docker-compose.prod.yml config` renders; after the deploy the ready-to-upload
card of a compilation offers the download.

## Notes

- 2026-09-27: done with the other binge tickets on `claude/keen-hamilton-plu6kp`. The host step
  belongs to the deploy (skill `deploy`) and the pilot ticket `2026-09-27-video-binge-pilot`: put
  the two caps in `.env`, check `docker compose exec api ls /var/lib/mokaair/video-work` lists the
  slugs, and `df` on the worker before the first pilot (about 25 GB per two-hour compilation).
