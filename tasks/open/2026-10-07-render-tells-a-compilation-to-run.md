---
id: 2026-10-07-render-tells-a-compilation-to-run
title: Render tells a compilation to run keyframes again when its thumbnail source changed, which a compilation cannot do
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-render-msg
claimed_at: 2026-10-07T10:05:06Z
created_at: 2026-10-07T09:55:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
---

# Render tells a compilation to run keyframes again when its thumbnail source changed, which a compilation cannot do

## Why

`tools/video/render/cli.mjs` `refuseChangedBackgrounds` refuses a thumbnail whose background file
is missing, has no hash, or no longer matches `keyframes/manifest.json`. It ends its message with
"run keyframes again or restore the approved picture". A compilation's thumbnail background is
`keyframes/thumb-source.png`, which the worker copies from an episode keyframe when it plans the
metadata (`tools/video/automation/compilation.mjs` `copyThumbSource`). `keyframes` refuses a
compilation, which has no drawn shots, so the advice cannot be followed.

The compilation's own hint (line 282: "the worker copies an episode's keyframe there when it plans
the metadata") is printed only when the manifest has no `shots.thumb`.

Since `2026-10-07-the-compilation-thumbnail-copies-an-episode`, the copy is checked against the
episode's approved hash before it is written, so this refusal should be rare.

## Definition of done

- [x] For a compilation, the changed-background refusal says what to do: plan the metadata again
  (the worker does this when its metadata step is reset), not run `keyframes`.

## Steps

- [x] In `refuseChangedBackgrounds`, when `isCompilation(doc)`, end the message with the
  compilation's remedy instead of "run keyframes again".
- [x] A test in `render.test.mjs`: a compilation whose `thumb-source.png` changed exits 2 with
  the compilation's remedy.

## How to verify

`node --test tools/video/render/render.test.mjs`.

## Notes

- Found by the review of `2026-10-07-the-compilation-thumbnail-copies-an-episode` (2026-10-07).
- 2026-10-07 (claude-opus-5-5-render-msg). `render/cli.mjs` `refuseChangedBackgrounds` takes
  `{ compilation }`, passed by the full render and by `--thumbnails-only`. For a compilation it
  ends with: delete `keyframes/manifest.json` so the worker plans the compilation's metadata
  again and copies an approved episode keyframe to `keyframes/thumb-source.png`
  (docs/videos/BINGE.md). That is what reopens the step: `core/state.mjs` counts "metadata
  planned" done only while the manifest lists `shots.thumb`. Every other video keeps "run
  keyframes again or restore the approved picture".
- Test (`render.test.mjs`, failing on the old code): a compilation sandbox with an English
  thumbnail of its own and a `thumb-source.png` drawn over. Both `render` and `render
  --thumbnails-only` exit 2 with the compilation's remedy and never "run keyframes again", and no
  renderer opens. The illustrated video's existing test pins the other wording. Mutations
  (dropping the flag at either call site, or always giving the compilation remedy) each fail a
  test.
