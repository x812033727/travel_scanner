---
id: 2026-10-11-sothatswhy-planned-episodes-move-to-cute
title: Move So That's Why's 192 planned episodes from flat-explainer to cute-cartoon with image-01
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T04:03:01Z
completed_at:
branch:
depends_on:
  - 2026-10-11-cute-explainers-own-series-prompts
scope:
  - docs/videos/long-form/plans.json
  - tools/video/long-form/plans.mjs
  - tools/video/long-form/admin-catalog.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Move So That's Why's 192 planned episodes from flat-explainer to cute-cartoon with image-01

## Why

On 2026-10-10 the owner decided So That's Why is from now on drawn by MiniMax in the cute
cartoon look. The explainer-route change keeps every existing thing where it is (decision 4 in
docs/videos/explainer-route/DECISIONS.md): the 192 planned episodes in
`docs/videos/long-form/plans.json` stay on `flat-explainer`, and `tools/video/long-form/plans.mjs`
and `admin-catalog.mjs` are untouched ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 1). Until they move, an episode started
from the plan catalogue on the host is still the old flat look drawn by Gemini at US$0.134 a
picture rather than `image-01` at US$0.0035.

## Definition of done

- [ ] The owner has approved the first MiniMax episode, `sothatswhy-b26` (at the publish gate on
      2026-10-10), and said the planned episodes may move.
- [ ] The planned So That's Why episodes carry `cute-cartoon`, and a request made from one is
      stored with `image-01`.
- [ ] Episodes already started or finished keep their preset, look hash and pictures.
- [ ] `node tools/video/long-form/cli.mjs check` passes and the receipt is re-issued by an
      independent agent (`plans.json` is the receipt's subject).

## Steps

- [ ] Count which of the 192 are already started on the host before changing anything.
- [ ] Read how `plans.mjs` and `admin-catalog.mjs` carry the preset to the request.

## How to verify

`node tools/video/long-form/cli.mjs check`; on the host a request made from a planned So That's
Why episode shows `cute-cartoon` and `MiniMax image-01`.

## Notes

- 2026-10-11 filed from the design's section 7, item 4. Blocked on the owner, not on code.
