---
id: 2026-11-18-video-shelf-self-heal
title: Admin video catalog files old videos under their show on its own
status: done
priority: P1
area: api
owner: claude-opus-5-5-video-shelf
claimed_at: 2026-11-18T10:04:49Z
created_at: 2026-11-18T10:04:04Z
completed_at: 2026-11-19T00:12:03Z
branch: claude/kind-mccarthy-5m28jo
depends_on: []
scope:
  - apps/api/tests/test_video_reviews.py
  - apps/api/app/video_reviews/shelf.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/tests/test_video_shelf.py
---

# Admin video catalog files old videos under their show on its own

## Why

After #2150 deployed, 奇聞檔案局 still sat under 觀念解說（其他）: videos written before migration
0147 have no `series_key` until `video-shelf-backfill` runs on the host, and the owner chose
(2026-11-18) not to run it by hand.

## Definition of done

- [x] Opening 全部影片 files the old rows under their show; nothing to run on the host.

## Steps

- [x] `shelf.heal`: candidates (no series_key, not a Short, a series slug, a drama `-e` slug or a
      series prefix from `target.SLUG_PREFIXES`) refreshed, committed only when one changed.
- [x] `GET /admin/videos/browse` calls it before listing (admin_api.py, not the duration-bound
      admin_service.py).
- [x] Tests: integration in test_video_shelf.py; route tests stub it.

## How to verify

After the deploy, open /admin/videos: 奇聞檔案局 and 原來如此事務所 have their own counts.

## Notes

- Claimed with `--force` (owner approved): four 2026-10-12 to 2026-11-03 claims list admin_api.py.
- `video-shelf-backfill` stays for recomputing every row when a rule changes.
