---
id: 2026-10-11-image-status-reads-slides-image-key
title: keyframes --dry-run: imageStatus reads the key state from status.slides_image too
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:03:36Z
completed_at:
branch:
depends_on:
  - 2026-10-11-explainer-request-names-its-image-model
scope:
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
---

# keyframes --dry-run: imageStatus reads the key state from status.slides_image too

## Why

For a video whose `series.json` names an image model, `imageStatus` in
`tools/video/media/stages.mjs` looks for the vendor's key state only among `status.image`,
`status.clip` and `status.music`. On a site whose only MiniMax choice is the slides' image
model (the production site: `slides_image_model` is `image-01`, the drama's is Gemini), the dry
run of a cute explainer therefore prints
`server: minimax image-01 (provider key checked on submit)` instead of `ready`, although the
key is there ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 4.7 and section 7 item 8). Cosmetic: filing already checked the
key. It also means a missing key is not reported as NO KEY by the dry run.

## Definition of done

- [ ] `imageStatus` also reads the vendor's key state from `status.slides_image`, so the dry
      run says `ready` or NO KEY for a model whose vendor is configured only there.
- [ ] A unit case in `stages.test.mjs`. Any test that pins the
      `(provider key checked on submit)` line for that situation is updated on purpose.

## Steps

- [ ] Read `imageStatus` after `2026-10-11-explainer-request-names-its-image-model` has landed (it adds a unit case there).

## How to verify

`node --test tools/video/media/stages.test.mjs`; `node tools/video/cli.mjs keyframes --dry-run`
on a cute explainer prints `minimax image-01 ready`.

## Notes

- 2026-10-11 filed from the design's section 7, item 8.
