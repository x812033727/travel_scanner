---
id: 2026-10-11-long-series-own-image-model-disagreement
title: A long series whose row names its own image model: the worker and the server disagree on the model
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:03:28Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
  - docs/videos/SERIES.md
---

# A long series whose row names its own image model: the worker and the server disagree on the model

## Why

The server draws an episode with the series row's `image_model` when it has one
(`video_media/jobs.py` `_series_image_model`), while the worker learns the model only from the
episode's `series.json`. `2026-10-11-explainer-request-names-its-image-model` makes `draftEpisode` write the key for a **one-off** only. A
long series whose row names a model different from the settings' is still broken as it was on
main before the change: no key in `series.json`, so the picture is booked failed as
`video_media_model_changed`, or refused 422 `video_media_model_not_allowed` when the worker asks
for 2K from a model that has no 2K ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 4.7 and section 7 item 7;
`orders/order-pr2.json` risks). It was left alone on purpose: writing the key for new episodes
of a running series flips `imageSelectionVersion` and stops them reusing the series' character
sheets.

## Definition of done

- [ ] A decision, written in `docs/videos/SERIES.md`: either a long series may not name its own
      image model (refused at `SeriesIn` / `SeriesPatch`, and existing rows listed), or it may,
      with a stated rule for character-sheet reuse when the key first appears.
- [ ] The code follows the decision, with a test for a series row that names a model.
- [ ] No running series loses its character sheets without the owner being told beforehand.

## Steps

- [ ] On the host, list series rows with a non-null `image_model` and kind other than one-off.
- [ ] Put the choice to the owner with what each option costs a running series.

## How to verify

`node --test tools/video/automation/series.test.mjs`; an episode of such a series draws its
first picture with the row's model and no `video_media_model_changed`.

## Notes

- 2026-10-11 filed from the design's section 7, item 7. Widen the scope to the API files if the
  decision is to refuse.
