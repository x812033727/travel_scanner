---
id: 2026-10-11-series-endpoints-cute-default-and-key
title: POST /series (one-off) and PATCH /series/{slug} bypass the cute image-model default and the key check
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-11T04:03:14Z
completed_at:
branch:
depends_on:
  - 2026-10-11-explainer-request-names-its-image-model
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/tests/test_video_series_image_model.py
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# POST /series (one-off) and PATCH /series/{slug} bypass the cute image-model default and the key check

## Why

`2026-10-11-explainer-request-names-its-image-model` stores a cute request with `image-01` and refuses a request whose model's vendor has no
key, but only on the drama-request route (`create_drama_request`). `POST /series` with kind
one-off and `PATCH /series/{slug}` go through `SeriesIn` / `SeriesPatch`, which accept any
catalogue model for any kind and apply neither rule ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 4.7 and section 7 item 5;
`orders/order-pr2.json` risks). Consequences, all reachable by API only today (no web form uses
these routes for a one-off):

- a cute one-off created by `POST /series` with no model is drawn by the settings' Gemini model
  at 2K from a look written for MiniMax;
- a cute one-off PATCHed to a cast preset before its bible exists keeps `image-01`, a model that
  cannot hold a face from reference sheets;
- neither route checks that the vendor has a key.

## Definition of done

- [ ] `POST /series` (kind one-off) applies `PRESET_IMAGE_MODELS` and the same 409
      `video_drama_image_model_not_configured` as the request route, from one shared helper.
- [ ] `PATCH /series/{slug}` applies them when the preset or the model changes, and clears
      `image_model` when a one-off leaves the explainer family.
- [ ] Long series and brand stories are unaffected. Tests for each case; the receipt re-issued
      if a bound file changes (`schemas.py` and `series.py` are bound).

## Steps

- [ ] Read `create_drama_request` and `patch_problem` as they stand after pull requests 1 and 2.

## How to verify

`cd apps/api && uv run pytest tests/test_video_series_image_model.py tests/test_video_series.py`.

## Notes

- 2026-10-11 filed from the design's section 7, item 5.
