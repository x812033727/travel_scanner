---
id: 2026-10-05-media-locate-subject-boxes
title: POST /video/media/locate: subject boxes for a stored picture, booked like a judge call
status: done
priority: P2
area: api
owner: claude-fable-5-1-locate
claimed_at: 2026-10-05T16:23:43Z
created_at: 2026-10-05T16:08:25Z
completed_at: 2026-10-05T16:34:55Z
branch: claude/media-locate-subject-boxes
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

- [x] `POST /video/media/locate {slug, sha256, labels?}` returns `{boxes: [{label, box: [ymin,
      xmin, ymax, xmax] (0–1000), score}], width, height, model}` for a png / jpeg / webp in the
      media store, counted on the judge meter (`JUDGE_CALLS`) and the judge per-hour limit; the
      web proxy's `[...path]` catch-all needs no change.
- [x] Tests cover the Gemini JSON shape, an empty answer, and a clip sha256 (refused: the tool
      extracts a frame first).
- [x] `tools/video/media/client.mjs locate()` with a fake-site test.

## Steps

- [x] `locate.py` (request body with a `box_2d` response schema, verdict parsing), `schemas.py`,
      the route in `admin_api.py`, metering in `meter.py`; tests.
- [x] `client.mjs locate()`; `DRAMA.md` §端點.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_locate.py tests/test_video_media_api.py -q
node --test tools/video/media/media.test.mjs
```

## Notes

- No bound file. US$0.01-class call, booked like a judge call; per-video cap handling comes
  with `2026-10-05-media-budget-estimate-reserve-reconcile`.

### Done (2026-10-05, branch `claude/media-locate-subject-boxes`)

- `locate.py` mirrors `judge.py` on purpose: same model and key
  (`hotspot_guide_gemini_model` / `_api_key`), the base URL pinned in `Settings`, the same
  `video_media_inline_judge_bytes` cap, `temperature: 0`, JSON mode with a response schema
  `{boxes: [{label, box_2d, score}]}`. The HTTP call is duplicated rather than factored out of
  `judge.py`, which is outside this ticket's scope; a later ticket may share it.
- The answer is normalised here, never trusted: each `box_2d` is rounded, clamped to 0–1000
  and ordered (`ymin <= ymax`, `xmin <= xmax`); a box with no area, the wrong length, a
  boolean or a non-dict entry is dropped; `score` is clamped to 0–1 (a missing one reads 0.0);
  a missing label reads `subject`; at most 20 boxes, in the model's order. `{boxes: []}` is a
  plain answer; a non-JSON or box-less answer is 502 `video_media_locate_failed`.
- `width` / `height` come from Pillow's header read (`Image.open(...).size`, no pixels
  decoded); Pillow is already an API dependency and the API image has WebP support (checked
  with `features.check("webp")`). An unreadable header is 422 `video_media_invalid`, the same
  code a clip gets (the type is sniffed from the stored bytes, as everywhere in the store).
- Booking: `meter.reserve_judge_call` / `release_judge_call` are now used by both the judge
  and locate routes, on `JUDGE_CALLS` and the owner's `monthly_judge_calls_budget`, and both
  routes share the `video_media_judge` per-hour bucket (`JUDGES_PER_HOUR`). A `LocateError`
  gives the unit back, like a `JudgeError`. `month_usd` therefore prices locate calls at
  `JUDGE_USD_PER_CALL` without a change.
- Codes: `video_media_invalid` (422, new), `video_media_file_not_found` (404),
  `video_media_judge_too_large` (413, same cap as the judge), `video_media_locate_unavailable`
  (503, no key; an owner code in `client.mjs`), `video_media_locate_failed` (502, retried by
  `client.mjs` like `video_media_judge_failed`), `video_media_upstream_busy` (429 with
  `Retry-After`). `video_media_invalid` is a tool code in `client.mjs` (exit 2): the tool
  extracts a frame and uploads it, it does not retry.
- `GET /status` now lists `limits.locate_labels` (8): a tool asks for boxes only of a server
  that says so, the way `judge_checks` works.
- Tool side: `client.mjs locate()` and a small `scaleBox(box, width, height)` that turns one
  box into clamped pixel edges, which the vertical-cut and smart-crop consumers will need.
- Not measured live: this container has no Gemini key, so the prompt wording follows Google's
  object-detection guidance (`box_2d` as `[ymin, xmin, ymax, xmax]`, 0–1000) and the first
  real call should check the boxes against a keyframe by eye; `thinkingBudget` is left unset
  as in the judge. `apps/api/tests/test_video_media_api.py` is outside the scope, so the
  401 route list there does not name `/locate`; `test_video_media_locate.py` checks it.
- Deferred: a CLI command and the vertical-cut / Shorts crop consumers are their own tickets;
  per-video cap handling comes with `2026-10-05-media-budget-estimate-reserve-reconcile`.
