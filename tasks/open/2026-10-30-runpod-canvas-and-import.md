---
id: 2026-10-30-runpod-canvas-and-import
title: H3 manifests and clips import accept RunPod canvases and a runpod provider
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-30T00:37:22Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/minimax-h3-colab/scripts/check_manifest.py
  - .agents/skills/minimax-h3-colab/scripts/images.py
  - tools/minimax-h3-colab.test.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/core/lint.mjs
  - docs/videos/long-form/review.json
---

# H3 manifests and clips import accept RunPod canvases and a runpod provider

## Why

`check_manifest.py` and `images.py` hard-code Colab's 1344×768 area limit, and `clips import` has
no `runpod` provider, so RunPod clips would be refused or mislabelled as `external`.

## Definition of done

- [ ] `check_manifest.py` / `images.py` take `--backend colab|runpod` and `--canvas 736p|1088p`;
      Colab keeps 1344×768; RunPod 1088p allows 1920×1088 (both multiples of 32).
- [ ] `clips import --provider runpod` exists; a 1920×1088 source is cropped 4 px top and bottom
      to 1920×1080; the note carries `route=runpod-h3 canvas=… upscale=… profile=… seed=…`.
- [ ] Profile-bound works still refuse with exit 3 (that decision stays with
      `2026-10-04-profile-works-external-clip-route`).
- [ ] Incremental review receipt for the SHA-bound files in `docs/videos/long-form/review.json`.

## Steps

- [ ] Checker flags and tests in `tools/minimax-h3-colab.test.mjs`.
- [ ] `IMPORT_PROVIDERS` and the crop in `clips.mjs`, tests in `clips.test.mjs`.
- [ ] Review receipt.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/video/media/clips.test.mjs tools/video/long-form/review.test.mjs
```

## Notes

- Whether an upscaled 736p clip counts as "native 1080p" for profile works is the owner's call in
  `2026-10-04-profile-works-external-clip-route`; do not decide it here.
