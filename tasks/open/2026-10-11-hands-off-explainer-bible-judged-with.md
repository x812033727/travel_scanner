---
id: 2026-10-11-hands-off-explainer-bible-judged-with
title: A hands-off explainer bible is judged with the story genre spec
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:03:47Z
completed_at:
branch:
depends_on:
  - 2026-10-11-cute-explainers-own-series-prompts
scope:
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# A hands-off explainer bible is judged with the story genre spec

## Why

When a one-off is filed hands-off, its bible is judged by the verifier variant `series-doc`
with the series' genre spec (`judgeDocument` in `tools/video/automation/series.mjs`, about line
571: the payload carries `GENRE_SPECS[series.genre]`). An explainer has no genre: its bible is a
question, a one-sentence answer, reasons and sources, and `2026-10-11-cute-explainers-own-series-prompts` already sends
`genre_spec: null` to the cute *planner* for that reason, while leaving `judgeDocument`
untouched ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 5.2 item 4, 5.8 and section 7 item 9). So a hands-off explainer's
bible is held to a story genre's rules (cast, arcs, hooks per chapter) that it cannot meet or
that mean nothing for it. The same is true of `flat-explainer` today. Reachable through the API
only: the request form does not set `hands_off`.

## Definition of done

- [ ] `judgeDocument` judges an explainer one-off's bible without the story genre spec, against
      the explainer bible's own shape (decide: `genre_spec: null` with the existing variant, or
      an explainer variant of the document judge).
- [ ] A story or long series' bible is judged exactly as before; the durable key of an
      unfinished non-explainer judgement does not move.
- [ ] A test with a hands-off explainer one-off; the receipt re-issued (`series.mjs` is bound).

## Steps

- [ ] Check whether a new verifier text is needed; if so it is a prompt change and belongs with
      the registry in `explainer-series.mjs` (widen the scope).

## How to verify

`node --test tools/video/automation/series.test.mjs`.

## Notes

- 2026-10-11 filed from the design's section 7, item 9.
