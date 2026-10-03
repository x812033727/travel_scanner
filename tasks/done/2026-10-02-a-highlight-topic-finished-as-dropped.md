---
id: 2026-10-02-a-highlight-topic-finished-as-dropped
title: A highlight topic finished as dropped leaves its empty Short in the making list
status: done
priority: P3
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-02T13:41:57Z
created_at: 2026-10-02T09:27:00Z
completed_at: 2026-10-02T13:55:49Z
branch: claude/shorts-drop-empty-video
depends_on:
  - 2026-09-28-video-shorts-worker-cut
scope:
  - apps/api/app/video_shorts/jobs.py
  - apps/api/tests/test_video_shorts_automation.py
---

# A highlight topic finished as dropped leaves its empty Short in the making list

## Why

The server writes two highlight topics for every tutorial that goes public (`cut-1`, `cut-2`,
`apps/api/app/video_shorts/topics.py` `ensure_auto_topics`). The worker (`tools/video/shorts/cut.mjs`)
chooses the tutorial's passages once; when the planner finds only one passage that stands alone,
or none, the topic without a passage is finished with `POST shorts/{topic}/done`
`{ outcome: "dropped", note }`.

`finish_topic` (`apps/api/app/video_shorts/jobs.py`) only accepts a topic that is `making`, so the
worker has to `start` it first, and `start_topic` creates a `VideoProject` for it. Dropping the
topic leaves that video as it is: no final review, no upload package, not dropped. The Shorts tab
counts a video with no approved upload package as 製作中, so every tutorial with a single highlight
leaves an empty Short in the making list for the owner to drop by hand.

## Definition of done

- [x] A topic finished as `dropped` whose video has no review yet has that video dropped too
      (`dropped_at`, with the topic's note as the reason), so it leaves 製作中 and the calendar.
- [x] A topic finished as `dropped` whose video already has a review keeps the video as it is.
- [x] Sending the same `done` again stays a no-op.

## Steps

- [x] Read `finish_topic` and how the owner's drop sets `dropped_at` on a video
      (`apps/api/app/video_reviews/admin_service.py`).
- [x] Drop the empty video in `finish_topic`; a test for both cases.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts_automation.py -q
```

## Notes

- Found while wiring the highlights line (PR for `2026-09-28-video-shorts-worker-cut`); the worker
  side reports the video's stage as `not made` when it drops a topic, which is all it can do.
- 2026-10-02 (claude-opus-5-5): `finish_topic` with `outcome: dropped` calls
  `_drop_empty_video`: it locks the topic's video and, if it is not dropped and has no
  review at all, sets `dropped_at`, `dropped_note` (the topic's note, or a fixed reason) and
  releases its slots like the owner's drop does, with an `AdminAuditLog`
  `video_project_dropped` row (actor null, `by: shorts_topic_dropped`). A video with any
  review is left alone. A repeated `done` returns before reaching it. Test with both cases
  and the repeat; suite 31 passed; ruff, format, mypy clean.
