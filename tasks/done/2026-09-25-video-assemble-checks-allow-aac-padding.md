---
id: 2026-09-25-video-assemble-checks-allow-aac-padding
title: video assemble checks allow AAC padding and judge dense frames against their neighbours
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-25T05:02:40Z
created_at: 2026-09-25T05:02:29Z
completed_at: 2026-09-25T05:06:29Z
branch: claude/video-assemble-checks
depends_on: []
scope:
  - tools/video/assemble/plan.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
---

# video assemble checks allow AAC padding and judge dense frames against their neighbours

## Why

The pilot's first assemble (2026-09-25) failed two automatic checks although the video was right:

- The audio ran 599.900 s against 599.833 s of video. The narration is exactly the timeline's 17,995 frames; the extra 0.067 s is AAC padding to whole 1,024-sample frames. The tolerance, one video frame plus 0.03 s, did not allow for it.
- `myth-compare` scored 39.97 dB against a fixed 40 dB floor. The pilot's four densest slides (two comparisons, two tables) all scored 40 to 40.5 when right, because dense small text loses more at CRF 18. The fixture's slides had scored 47.

## Definition of done

- [x] Audio may run past the video by one frame plus three AAC frames. Audio shorter than the video by more than one frame still fails.
- [x] A frame at 44 dB or more passes; below 35 dB it fails. In between, it must beat each of the scene's other held images by 3 dB.
- [x] The pilot assembles with `ok: true`. Its dense frames score 40 against their own image and 20 to 24 against every rival.

## Steps

- [x] `plan.mjs`: `AAC_PADDING_SECONDS`, `CLEAR_PSNR`, `MIN_PSNR` 35, `PSNR_MARGIN`, `rivalImages`, `sampleProblem`.
- [x] `cli.mjs`: rivals are measured only for grey-zone frames, and `checks.json` records them.
- [x] Tests: the pilot's real numbers, a padded and a short audio stream.

## How to verify

```bash
node --test tools/video/assemble/assemble.test.mjs
node tools/video/cli.mjs assemble --slug <SLUG>
```

## Notes

- Rivals are only the scene's stills, not its one-frame transition images. A scene with a single image has no rival and passes anywhere from 35 dB up (`cost-diagram` scored 42.9).
- Only frames in the grey zone cost extra ffmpeg runs: 5 of the pilot's 51 samples, adding a few seconds.
