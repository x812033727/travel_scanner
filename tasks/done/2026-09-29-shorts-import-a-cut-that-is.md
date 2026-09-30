---
id: 2026-09-29-shorts-import-a-cut-that-is
title: "Shorts import: a cut that is not 30 fps fails with a misleading caption-length error"
status: done
priority: P3
area: tools
owner: claude-opus-5-5-shorts-import
claimed_at: 2026-09-30T15:40:47Z
created_at: 2026-09-29T00:08:19Z
completed_at: 2026-09-30T15:42:39Z
branch: claude/shorts-import-frame-rate
depends_on: []
scope:
  - tools/video/shorts/import.mjs
  - tools/video/shorts/pipeline.test.mjs
---

# Shorts import: a cut that is not 30 fps fails with a misleading caption-length error

## Why

`node tools/video/shorts/cli.mjs import` takes the length of the cut as its frame count divided
by 30 (`PROFILE.fps`), whatever the file's frame rate is. A 24 fps cut of 28.97 s comes out as
23.17 s, and the import stops with "the captions run to 28.97s, the cut to 23.17s", which sends
the reader to the captions when the problem is the frame rate. All twelve season-one Shorts of
PR #880 (24 fps review cuts) failed this way on 2026-09-29; re-encoding them to 30 fps first
fixed it.

## Definition of done

- [x] A cut whose frame rate is not the Shorts profile's is refused with a message that names
      the frame rate (and says to re-encode to 30 fps), before the captions are compared.
- [x] The caption comparison uses the cut's real length.
- [x] A test with a 24 fps probe.

## Steps

- [x] Check `measured.video.r_frame_rate` right after `measureFinal`, and read the length from
      the stream's duration.
- [x] Test.

## How to verify

`node --test tools/video/shorts/pipeline.test.mjs`; an import of a 24 fps cut names the frame rate.

## Notes

- The re-encode that worked (picture and sound only, content unchanged):
  `-vf fps=30,scale=1080:1920,format=yuv420p -c:v libx264 -crf 18` and a two-pass
  `loudnorm=I=-14:TP=-1.5:LRA=11` into AAC at 48 kHz. A one-pass loudnorm left a 29 s cut at
  −15.55 LUFS, outside the check's −14 ± 1.
- 2026-09-30, claude-opus-5-5-shorts-import: claimed with `--force` because the scope overlapped
  `2026-09-28-sothatswhy-shorts-from-episode` (claude-opus, `tools/video/shorts/`), a stale claim
  (54 h) whose branch `claude/knowledge-series-planning-v84n79` is gone from the remote and whose
  PRs (#904, #950, #962) are merged; no open PR touched `import.mjs`.
- Done: `frameRateProblem(video)` in `import.mjs` refuses anything but `30/1` right after the
  measurement, naming the rate (`24 fps (24/1)`, `29.97 fps (30000/1001)`) and saying to
  re-encode to 30 fps. The caption comparison and `seconds` in `timeline.json`/`checks.json` now
  use the video stream's `duration`, falling back to frames ÷ 30 only when the stream has none.
  `importShort` takes `measureImpl` (as `runQa` does) so the test feeds it ffprobe stand-ins.
