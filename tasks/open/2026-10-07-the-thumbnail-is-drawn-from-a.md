---
id: 2026-10-07-the-thumbnail-is-drawn-from-a
title: The thumbnail is drawn from a keyframe file without checking its bytes
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T04:00:00Z
completed_at:
branch:
depends_on:
  - 2026-10-05-video-consumer-selected-image-hashes
scope:
  - tools/video/render/plan.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
---

# The thumbnail is drawn from a keyframe file without checking its bytes

## Why

A video's thumbnail can use a shot's keyframe as its background
(`thumbnail.data.shot`). `tools/video/render/plan.mjs` `drawThumbnail` takes the picture
from `keyframes/manifest.json` and keys the render on the manifest's `sha256`. It never reads
the file itself.

Later keyframe takes reuse file names. So once a later take has drawn over the selected file, the
thumbnail can be rendered from bytes nobody approved, while its key still looks current.

`2026-10-05-video-consumer-selected-image-hashes` closed the same gap for direct `clips` and
`assemble`. Its code review (2026-10-07) found this one, and it is outside that ticket's scope.

## Definition of done

- [ ] Render refuses to draw a thumbnail when the selected keyframe's bytes differ from the manifest's sha256 or the file is missing. It names the file, and nothing is drawn or cached under the old key.
- [ ] An unchanged picture renders and reuses its cached thumbnail as before.

## Steps

- [ ] Reuse `core/state.mjs keyframeProblems`, or hash the one file, before `drawThumbnail` uses it.
- [ ] Run `node tools/video/long-form/cli.mjs check`. If a bound file changes, an independent reviewer adds an increment.

## How to verify

```bash
node --test tools/video/render/*.test.mjs
npm run test:tools
```

## Notes

- `media/clips.mjs` `uploadApproved` and `assemble/cli.mjs` `mediaInputs` show the pattern: hash the file right before it is used, against the record that names it.
