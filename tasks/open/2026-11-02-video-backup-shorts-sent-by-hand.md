---
id: 2026-11-02-video-backup-shorts-sent-by-hand
title: Video backup: Shorts sent by hand are fetched from the review store like imported videos
status: in-progress
priority: P2
area: api
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-11-02T12:18:06Z
created_at: 2026-11-02T12:18:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_backup/admin_status.py
  - apps/api/tests/test_video_backup.py
  - docs/videos/BACKUP.md
---

# Video backup: Shorts sent by hand are fetched from the review store like imported videos

## Why

The 25 Shorts of 種田娶妻打天下 (`zhong-tian-qu-qi-eNNN-short`) were made in a cloud session and sent with
`shorts/cli.mjs push` (payload `hand_pushed`). Their upload packages are approved and still in the review store, but the
host's `video_work` never had their files, and `admin_status.review_packages` left every Short out ("in video_work
already"), so none of them was ever backed up (no backup record at all, 2026-11-02).

## Definition of done

- [x] `review_packages` names the newest approved package of a Short whose payload is `hand_pushed`; the worker's own
      Shorts (lab, cut lines) stay out. A work directory the worker did not fill is still never written over.
- [x] Test in `apps/api/tests/test_video_backup.py`; BACKUP.md 〈匯入的影片〉 says so.
- [ ] After deploy: the 25 Shorts are backed up under `AI/備份/Shorts/zhong-tian-qu-qi/`.

## How to verify

`cd apps/api && uv run pytest tests/test_video_backup.py`
