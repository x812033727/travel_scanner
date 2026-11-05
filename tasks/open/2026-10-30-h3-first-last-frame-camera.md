---
id: 2026-10-30-h3-first-last-frame-camera
title: H3 first and last frame cut from one wide plate for exact push-ins and pans
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-30T06:39:18Z
completed_at:
branch:
depends_on:
  - 2026-10-30-h3-colab-three-stage
scope:
  - .agents/skills/minimax-h3-colab/scripts/camera_frames.py
  - .agents/skills/minimax-h3-colab/assets/h3_keyframes.ipynb
  - .agents/skills/minimax-h3-colab/references/camera-control.md
  - tools/minimax-h3-camera.test.mjs
---

# H3 first and last frame cut from one wide plate for exact push-ins and pans

## Why

Camera moves written as words are followed loosely. H3 can be pinned at both ends:
`MiniMaxH3ImageToVideo` takes an optional `last_frame` next to `first_frame`, and `MiniMaxH3AddGuide`
anchors an image at any frame (ComfyUI `comfy_extras/nodes_minimax_h3.py`, core nodes, no extra
model). If one wide plate (larger than the canvas) is painted per shot, the first and last frames can
be cut from it: a push-in ends on a centre crop, a pan on a shifted crop, a tilt on a raised crop.
The start and end compositions are then exact, and the prompt only has to fill the motion between.
The upstream draft notebook sends only a first frame.

## Definition of done

- [ ] `scripts/camera_frames.py` cuts first/last (and optional middle) frames from a plate for
      `push_in`, `pull_out`, `pan_left`, `pan_right`, `tilt_up`, `tilt_down` with an amount, at the canvas
      size, and writes the manifest fields.
- [ ] `assets/h3_keyframes.ipynb` runs H3 FL2VA with first and last frame (and AddGuide anchors), same
      model and profiles as the draft; a runner like `refine.py`.
- [ ] `references/camera-control.md` states which moves work, the amounts that hold, and the failure
      modes, from a paid pilot on the e030 shots measured with
      `2026-10-30-clip-qc-camera-move`.
- [ ] Offline tests in `tools/minimax-h3-camera.test.mjs`.

## Steps

- [ ] Crop geometry and its tests (no GPU).
- [ ] Notebook and runner; check the last-frame path on one shot before a batch.
- [ ] Pilot: push-in, pan and locked on three shots, against prompt-only takes with the same seed.

## How to verify

```bash
node --test tools/minimax-h3-camera.test.mjs   # Linux/macOS
```

## Notes

- `last_frame` is a "follower" in the node: it is cover-cropped to the canvas, while `first_frame` is
  stretched; the crops must already be the canvas size so neither is changed.
- Official H3 FL2VA wording for shots with an end frame: `.agents/skills/animation-camera/references/model-misreads.md` §6.
- The animation-camera skill should point to the result once it is measured.
