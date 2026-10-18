---
id: 2026-10-11-explainer-shorts-saved-before-the-checker
title: Explainer Shorts are saved before the checker runs, so a corrected number stays wrong in shorts.json
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:03:57Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Explainer Shorts are saved before the checker runs, so a corrected number stays wrong in shorts.json

## Why

The explainer writer returns the long video and its two Shorts in one answer, and the worker
saves the Shorts (`shorts.json`) before the fact-checker runs. When the checker then corrects a
number or a claim in the long video, the same sentence in `shorts.json` stays as the writer
wrote it: the Short can publish a figure the long video no longer makes. Found while designing
the cute explainers' checker texts ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 7 item 11); it is the same for
`flat-explainer` today.

## Definition of done

- [ ] After the checker changes the long video, the Shorts cut from it carry the corrected
      text: either the Shorts are saved (or re-derived) after the last check round, or the
      checker is given the Shorts and its corrections are applied to both.
- [ ] A Short whose source sentence the checker removed is dropped or rewritten, never
      published as written.
- [ ] A test with a checker answer that changes a number quoted in a Short. If the checker's
      payload or instructions change, every explainer variant's digest is re-pinned on purpose
      and the deploy has no explainer run unfinished.

## Steps

- [ ] Find where the writer's Shorts are saved in `flow.mjs` relative to the verify rounds, and
      reproduce with the existing one-off end-to-end test in `series.test.mjs`.

## How to verify

`node --test tools/video/automation/automation.test.mjs tools/video/automation/series.test.mjs`.

## Notes

- 2026-10-11 filed from the design's section 7, item 11. Widen the scope if the fix is in the
  Shorts module or the prompts.
