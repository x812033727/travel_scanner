---
id: 2026-10-11-render-repeat-draws-a-marked-video
title: Render repeat draws a marked video without its mark
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T16:51:06Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/render/repeat.mjs
---

# Render repeat draws a marked video without its mark

## Why

`tools/video/render/repeat.mjs` draws a video's slide states several times and says which
frames differ between runs. It plans with `renderPlan(doc, themeHash(), ROOT)` and has no work
directory, so it cannot read the video's `watermark.json`: a video that carries the channel
mark (docs/videos/WATERMARK.md) is planned without it. Its comment says "the whole video is
planned, so the keys are render's"; for a marked video they no longer are, and the frames it
proves repeatable are not the frames the video uses.

## Definition of done

- [ ] `repeat.mjs --workdir D` reads the video's pin and plans with the same mark render used.
- [ ] Without `--workdir` it says the frames are drawn without the mark.

## Steps

- [ ] `readWatermarkPin` (tools/video/core/watermark.mjs) and the `watermark` option of
      `renderPlan`.
- [ ] A test of `drawOnce`'s plan for a pinned work directory.

## How to verify

`node tools/video/render/repeat.mjs --slug <slug> --workdir <dir> --channel msedge`: the stills
it writes with `--out` show the mark.

## Notes

- The mark is a data URI inside the page, so it draws from memory and should not add a source
  of difference between runs; worth confirming once.
