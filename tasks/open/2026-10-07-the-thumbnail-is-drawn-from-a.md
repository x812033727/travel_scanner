---
id: 2026-10-07-the-thumbnail-is-drawn-from-a
title: The thumbnail is drawn from a keyframe file without checking its bytes
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-thumb-bytes
claimed_at: 2026-10-07T06:29:09Z
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

- [x] Render refuses to draw a thumbnail when the selected keyframe's bytes differ from the manifest's sha256 or the file is missing. It names the file, and nothing is drawn or cached under the old key.
- [x] An unchanged picture renders and reuses its cached thumbnail as before.

## Steps

- [x] Reuse `core/state.mjs keyframeProblems`, or hash the one file, before `drawThumbnail` uses it.
- [x] Run `node tools/video/long-form/cli.mjs check`. If a bound file changes, an independent reviewer adds an increment.

## How to verify

```bash
node --test tools/video/render/*.test.mjs
npm run test:tools
```

## Notes

- `media/clips.mjs` `uploadApproved` and `assemble/cli.mjs` `mediaInputs` show the pattern: hash the file right before it is used, against the record that names it.
- 2026-10-07 (claude-opus-5-5-thumb-bytes). `render/cli.mjs` `changedBackgrounds()` hashes the
  keyframe each thumbnail sits on: the thumbnail, its test variants and the caption locales' own,
  each picture once. It compares the bytes with the sha256 the plan took from
  `keyframes/manifest.json`, and a file that is missing, or recorded without a hash, counts as
  changed.
- The full render and `--thumbnails-only` both call it right after the "not drawn yet" checks,
  before the browser opens. A mismatch exits 2 and names the file ("run keyframes again or restore
  the approved picture"). Nothing is drawn, `frames/manifest.json` keeps its key and
  `thumbnail.jpg` stays.
- The compilation thumbnail (`keyframes/thumb-source.png`, which the worker copies and hashes in
  `automation/compilation.mjs`) is checked the same way.
- Test (`render.test.mjs`, illustrated fixture, thumbnail on shot `podium`): the approved bytes
  render; a take drawn over the file, and the file gone, are refused by both commands with nothing
  drawn or rewritten; restored, both render again. It fails on the old code.
