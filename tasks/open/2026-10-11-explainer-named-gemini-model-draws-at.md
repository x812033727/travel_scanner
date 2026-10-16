---
id: 2026-10-11-explainer-named-gemini-model-draws-at
title: An explainer that names a Gemini image model is drawn at 1K while 'same as the settings' draws at 2K
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-11T04:03:23Z
completed_at:
branch:
depends_on:
  - 2026-10-11-explainer-request-names-its-image-model
scope:
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# An explainer that names a Gemini image model is drawn at 1K while 'same as the settings' draws at 2K

## Why

After `2026-10-11-explainer-request-names-its-image-model` an explainer request may name its image model. `imageStatus` in
`tools/video/media/stages.mjs` nulls the 2K price for any overridden model, because the
catalogue rows the worker receives (`MediaOptionView`) carry no `usd_per_image_2k`; with no 2K
price the picture is asked for at 1K. So choosing "Gemini 3 Pro Image" by name gives a softer
picture under a camera move than leaving the field on "same as the drama settings", at the same
US$0.134, and a cute video on Gemini is always 1K because the cute presets have no "same as the
settings" entry ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 4.7 and section 7 item 6; `orders/order-pr2.json` risks).

## Definition of done

- [ ] `MediaOptionView` carries `usd_per_image_2k` where the catalogue has one (`schemas.py`,
      `settings.py`), and `imageStatus` keeps the named model's own 2K price.
- [ ] An explainer naming a Gemini model is drawn at the same size as one following the
      settings; `image-01` (no 2K price) is still drawn at 1K with no `size` in the request.
- [ ] Image cache keys of videos that name no model do not move. Tests on both sides; the
      receipt re-issued (`schemas.py` and `settings.py` are bound).

## Steps

- [ ] Check what a changed size does to `keyframeKey` for an explainer already drawn at 1K
      under a named Gemini model (it should redraw only if the owner asks).

## How to verify

`node --test tools/video/media/stages.test.mjs tools/video/media/look-keyframes.test.mjs`;
`cd apps/api && uv run pytest tests/test_video_automation_settings.py`; `keyframes --dry-run`
on such a video prints `pictures at 2K`.

## Notes

- 2026-10-11 filed from the design's section 7, item 6.
