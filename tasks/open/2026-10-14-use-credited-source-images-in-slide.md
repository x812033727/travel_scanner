---
id: 2026-10-14-use-credited-source-images-in-slide
title: Use credited source images in slide thumbnails
status: in-progress
priority: P2
area: tools
owner: codex-gpt6-curio-thumb
claimed_at: 2026-10-14T07:13:29Z
created_at: 2026-10-14T07:13:23Z
completed_at:
branch: codex/curio-h04-h06-v2-20261014
depends_on: []
scope:
  - tools/video/render/plan.mjs
  - tools/video/render/render.test.mjs
---

# Use credited source images in slide thumbnails

## Why

The slide thumbnail template can show a screencast still or generated shot keyframe, but a
source-led episode has neither. Its right picture area stays blank even when the project already
has a credited photograph in `assets[]`. The renderer needs a narrow way to reuse that local image
without changing narration or any video scene.

## Definition of done

- [x] A thumbnail may opt in with `data.asset` pointing to a credited local raster image already
  in `assets[]`; both repository and fetched `stock/` images render through the fake origin.
- [x] Missing, unlisted, uncredited, unsafe, and conflicting asset references fail render lint.
- [x] Replacing the picture bytes invalidates the thumbnail cache; unflagged thumbnails, video
  scene plans, timeline, and speech hash remain unchanged.

## Steps

- [x] Validate the thumbnail asset and resolve its repository or work-directory file.
- [x] Include picture bytes in the thumbnail key and cover both routes and rejection cases.

## How to verify

`node --test --test-name-pattern="opted-in|thumbnail assets require|credited stock thumbnail" --test-reporter=tap tools/video/render/render.test.mjs`

`git diff --check -- tools/video/render/plan.mjs tools/video/render/render.test.mjs`

## Notes

The new field is opt-in and accepts raster assets under the same repository roots already served
by the renderer, or the existing `stock/<sha256>.<ext>` work-directory route. The `assets[]` entry
must have nonempty `source` and `license`; `data.asset` cannot coexist with `capture` or `shot`.
The full `render.test.mjs` currently exits on Windows with code 3221226505 in an existing
CLI render integration test, including when only that old test is selected. The three new focused
tests pass independently; the full-suite process exit needs separate environment investigation.
