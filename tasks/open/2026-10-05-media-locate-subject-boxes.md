---
id: 2026-10-05-media-locate-subject-boxes
title: POST /video/media/locate: subject boxes for a stored picture, booked like a judge call
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T16:08:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_media/locate.py
  - apps/api/tests/test_video_media_locate.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/schemas.py
  - apps/api/app/video_media/meter.py
  - tools/video/media/client.mjs
  - tools/video/media/media.test.mjs
  - docs/videos/DRAMA.md
---

# POST /video/media/locate: subject boxes for a stored picture, booked like a judge call

## Why

Nothing in the pipeline knows where the subject is in a picture: the judge returns scores or
yes/no answers and free text, never coordinates, and no face or object detector exists. A
vertical cut of a 16:9 drama episode, a smart crop for a Short and any later reframing all
need one call that answers "where is the main character". Gemini returns `box_2d` boxes in
JSON mode; booking the call like a judge call keeps it inside the existing budget and limits.

## Definition of done

- [ ] `POST /video/media/locate {slug, sha256, labels?}` returns `{boxes: [{label, box: [ymin,
      xmin, ymax, xmax] (0–1000), score}], width, height, model}` for a png / jpeg / webp in the
      media store, counted on the judge meter (`JUDGE_CALLS`) and the judge per-hour limit; the
      web proxy's `[...path]` catch-all needs no change.
- [ ] Tests cover the Gemini JSON shape, an empty answer, and a clip sha256 (refused: the tool
      extracts a frame first).
- [ ] `tools/video/media/client.mjs locate()` with a fake-site test.

## Steps

- [ ] `locate.py` (request body with a `box_2d` response schema, verdict parsing), `schemas.py`,
      the route in `admin_api.py`, metering in `meter.py`; tests.
- [ ] `client.mjs locate()`; `DRAMA.md` §端點.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_locate.py tests/test_video_media_api.py -q
node --test tools/video/media/media.test.mjs
```

## Notes

- No bound file. US$0.01-class call, booked like a judge call; per-video cap handling comes
  with `2026-10-05-media-budget-estimate-reserve-reconcile`.
