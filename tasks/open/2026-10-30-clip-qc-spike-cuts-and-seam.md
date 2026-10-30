---
id: 2026-10-30-clip-qc-spike-cuts-and-seam
title: Clip QC catches cuts between look-alike shots, and two takes join at the closest frame
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-30T06:28:34Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/qc.mjs
  - tools/video/media/media.test.mjs
---

# Clip QC catches cuts between look-alike shots, and two takes join at the closest frame

## Why

Our clip QC (`tools/video/media/qc.mjs`) misses a cut inside a clip when the two shots look alike.
Henge (alisson-anjos/Henge, MIT, `backend/comfy_nodes/henge/__init__.py` `scene_cuts`) adds an
isolated-spike rule for exactly that case, and joins two takes of one shot at the frame where they
match best (`video_join.overlap_match`: a hard cut at the lowest pixel error inside the overlap, no
crossfade, total frame count verified).

## Definition of done

- [ ] QC flags a cut when a frame difference is above 0.1 and more than 8x the median of the 6
      frames on each side, in addition to the existing threshold (Henge: 18x32 grey thumbnails,
      threshold 0.18 or 4x median, cuts at least 6 frames apart).
- [ ] A seam helper picks the join frame with the lowest error inside an overlap and checks the
      joined frame count.
- [ ] Tests in `tools/video/media/media.test.mjs`, including two look-alike shots.

## How to verify

```bash
node --test tools/video/media/media.test.mjs
```

## Notes

- Henge's comment records a real look-alike cut scoring 0.16, under its 0.18 threshold; the spike
  rule caught it.
