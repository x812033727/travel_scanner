---
id: 2026-10-30-clip-qc-camera-move
title: Clip QC measures the camera move and flags drift against the shot's camera field
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-30T06:39:16Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/camera-motion.mjs
  - tools/video/media/camera-motion.test.mjs
---

# Clip QC measures the camera move and flags drift against the shot's camera field

## Why

The owner wants the camera work of the H3 clips strengthened (2026-10-30). Nothing measures today
whether a clip did the move its shot asked for: H3 drifts on locked shots unless told `holds a static
shot` (`.agents/skills/minimax-h3-colab/references/motion-quality.md` §5), and a `push in` can come
back static or as a pan. Every later camera improvement (first/last frames, ControlNet) needs this
measurement to show it helped.

## Definition of done

- [ ] `tools/video/media/camera-motion.mjs` estimates the global camera motion of a clip from ffmpeg
      (e.g. downscaled grey frames and phase correlation or block matching per frame pair): per-frame
      translation (pan/tilt) and scale (push/pull), and a summary class: static, push in, pull out,
      pan left/right, tilt up/down, mixed.
- [ ] It compares the class with the shot's `camera` field as craft reads it
      (`tools/video/core/craft.mjs` `cameraMove`) and reports mismatches: drift on a locked shot above a
      threshold, a missing push, the wrong pan direction.
- [ ] Tested on synthetic clips made with ffmpeg (zoompan, crop pans, still) so the thresholds are
      pinned, plus the three e030 pilot clips as a manual check.

## Steps

- [ ] Prototype the estimator and its thresholds on synthetic clips.
- [ ] Wire it as a separate check first; joining `qc.mjs` belongs to a follow-up (that file is in
      `2026-10-30-clip-qc-spike-cuts-and-seam`).

## How to verify

```bash
node --test tools/video/media/camera-motion.test.mjs
```

## Notes

- Characters moving inside the frame must not read as camera motion: estimate on the border band or
  with a robust median over blocks.
