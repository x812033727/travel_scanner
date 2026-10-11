---
id: 2026-10-10-host-writer-prompt-forbids-photo
title: Host writer prompt: name photo beside diagram and screenshot as a card it cannot use
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-10T15:13:24Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
---

# Host writer prompt: name photo beside diagram and screenshot as a card it cannot use

## Why

#1425 added the `photo` template for locally made videos. The host's writer is still told only
「Do not use diagram or screenshot: automated videos have no image files」
(`tools/video/automation/prompts.mjs`, about line 168) and "no assets" (about line 285); the
showcase it is sent has the photo scene filtered out (`workerShowcase`). But the planner and the
writer also receive the whole of `docs/videos/README.md` as the payload's `channel`
(`flow.mjs`, about lines 1811 and 2689), and that file now has a `photo` row describing
caption, credit and tilt. Before #1425 a writer that tried `photo` got a schema error and the
free lint repair round removed it. Now `schema.mjs` accepts it and lint only checks how the
image path is spelled; `settle()` empties `assets[]` on every save (`flow.mjs`, about line
462), so the scene is refused only at render ("is not in assets[]"), after the narration and
the pictures were paid for, and the video stops at "render failed". The same already happens
when a model misuses `screenshot`; `photo` is the one image template the README introduces and
the prompt does not name. Drama and explainer formats are not affected (their card lists
exclude it in `drama.mjs`).

## Definition of done

- [ ] The host's slides writer prompt names `photo` with `diagram` and `screenshot` as
      templates an automated video cannot use, or lint refuses an image template on the
      automated route before any paid step (whichever is smaller).
- [ ] A prompt test pins it. `prompts.mjs` is bound by the duration receipt: an independent
      reviewer re-issues it.

## Steps

- [ ] Check whether `2026-10-10-explainer-route-takes-a-series-look` is changing the same
      lines; fold this in there if it is.

## How to verify

`node --test tools/video/automation/prompts.test.mjs`; in the worker container the composed
writer instructions contain the three template names in the forbidding sentence.

## Notes

- 2026-10-10 filed from the pre-deploy review of #1425. Rated low: the template guide in the
  prompt does not list `photo`, and the README row itself says an unregistered photograph is
  refused. The cost when it happens is one video's narration and pictures.
