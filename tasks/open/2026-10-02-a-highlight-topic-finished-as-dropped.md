---
id: 2026-10-02-a-highlight-topic-finished-as-dropped
title: A highlight topic finished as dropped leaves its empty Short in the making list
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-02T09:27:00Z
completed_at:
branch:
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

- [ ] A topic finished as `dropped` whose video has no review yet has that video dropped too
      (`dropped_at`, with the topic's note as the reason), so it leaves 製作中 and the calendar.
- [ ] A topic finished as `dropped` whose video already has a review keeps the video as it is.
- [ ] Sending the same `done` again stays a no-op.

## Steps

- [ ] Read `finish_topic` and how the owner's drop sets `dropped_at` on a video
      (`apps/api/app/video_reviews/admin_service.py`).
- [ ] Drop the empty video in `finish_topic`; a test for both cases.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts_automation.py -q
```

## Notes

- Found while wiring the highlights line (PR for `2026-09-28-video-shorts-worker-cut`); the worker
  side reports the video's stage as `not made` when it drops a topic, which is all it can do.
