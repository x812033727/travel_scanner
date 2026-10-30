---
id: 2026-10-30-clip-qc-camera-move
title: Clip QC measures the camera move and flags drift against the shot's camera field
status: review
priority: P2
area: tools
owner: claude-opus-5-5-camera-qc
claimed_at: 2026-10-30T06:42:48Z
created_at: 2026-10-30T06:39:16Z
completed_at:
branch: claude/clip-qc-camera-move
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

- [x] `tools/video/media/camera-motion.mjs` estimates the global camera motion of a clip from ffmpeg
      (e.g. downscaled grey frames and phase correlation or block matching per frame pair): per-frame
      translation (pan/tilt) and scale (push/pull), and a summary class: static, push in, pull out,
      pan left/right, tilt up/down, mixed.
- [x] It compares the class with the shot's `camera` field as craft reads it
      (`tools/video/core/craft.mjs` `cameraMove`) and reports mismatches: drift on a locked shot above a
      threshold, a missing push, the wrong pan direction.
- [x] Tested on synthetic clips made with ffmpeg (zoompan, crop pans, still) so the thresholds are
      pinned, plus the three e030 pilot clips as a manual check.

## Steps

- [x] Prototype the estimator and its thresholds on synthetic clips.
- [x] Wire it as a separate check first; joining `qc.mjs` belongs to a follow-up (that file is in
      `2026-10-30-clip-qc-spike-cuts-and-seam`).

## How to verify

```bash
node --test tools/video/media/camera-motion.test.mjs
```

## Notes

- Characters moving inside the frame must not read as camera motion: estimate on the border band or
  with a robust median over blocks.

### 2026-10-30: built (claude-opus-5-5-camera-qc)

- `tools/video/media/camera-motion.mjs`: ffmpeg grey frames at 320x180, block matching (24 px
  blocks, ±10 px, sub-pixel parabola) between frames 4 apart, a least-squares fit of one zoom about
  the centre plus one translation, refitted on the best 70% of blocks so a subject crossing the frame
  does not count. Whole-clip totals: zoom ratio, pan and tilt as fractions of the frame (camera
  direction, i.e. the reverse of the picture's slide). Classes: locked, push, pull, pan left/right,
  tilt up/down, drift (between 1.5% and 3% travel or 2% and 4% zoom), mixed (pan and tilt together).
- A push or pull with travel is still a push or pull; the travel goes to `also`. The e030 pilot's
  pushes on faces above the centre measured zoom 1.08 with a 5% tilt (s21) and 1.07 with a 4.5% pan
  (s42); the locked insert (s34) measured 0.4% zoom. Stage-2 refines measured the same as their
  drafts, so the refine does not change the camera.
- `compareMove` judges against craft's `cameraMove` (locked, push, pull, pan, tilt) and a named
  direction; `track` and shots naming no move are not judged.
- CLI: `node tools/video/media/camera-motion.mjs clip.mp4 --camera "Close-up, slow push in"` prints
  the report and exits 1 on a problem. Not yet called by `qc.mjs` or `clips import` (follow-up; that
  file belongs to `2026-10-30-clip-qc-spike-cuts-and-seam`).
- Tests build eight synthetic clips with ffmpeg (still, zoompan in and out, crop pans both ways, a
  tilt, a box crossing a locked frame, a 0.5% creep) and skip when ffmpeg is missing; about 15 s.
