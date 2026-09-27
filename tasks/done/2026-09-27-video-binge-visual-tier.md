---
id: 2026-09-27-video-binge-visual-tier
title: Video binge T3: still shots with camera motion (visual tiers)
status: done
priority: P1
area: tools
owner: claude-fable
claimed_at: 2026-09-27T11:44:56Z
created_at: 2026-09-27T11:43:45Z
completed_at: 2026-09-27T12:29:25Z
branch: claude/keen-hamilton-plu6kp
depends_on: []
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/fixtures/drama
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/assemble
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Video binge T3: still shots with camera motion (visual tiers)

## Why

Every drama shot is an image-to-video clip at US$0.15 a second, so a two-hour compilation
costs about US$1,900 in clips alone and the month's clip budget covers eleven episodes. The
owner chose the hybrid tier for binge series (docs/videos/BINGE.md): about four shots in ten
are clips, the rest are the shot's keyframe with a camera move, cut into the same segment
chain. The tools had no notion of a still shot.

## Definition of done

- [x] A drama shot may carry `visual: "clip" | "still"` (default clip). `visualTierProblems`
      holds a script to its series' tier (`TIER_CLIP_SHARE_MAX`: clips 1, hybrid 0.4,
      stills 0.1) in lint, before any clip is bought.
- [x] `clips` skips still shots and records them in the manifest as `{still: true, file,
      sha256}`, so `clips generated` is about clip shots only and an all-still episode still
      writes a manifest.
- [x] `assemble` cuts a still shot from its keyframe with ffmpeg `zoompan` (push-in,
      pull-back, pan left/right, tilt up/down, hold, read from the shot's `camera`), the
      same x264 settings as a clip segment so `-c copy` joins hold, with its own
      encoder version and segment cache key; the check compares frame 0 of a push-in to the
      keyframe and counts frames for the other moves.
- [x] A compilation episode's lint refuses a title card in the cold open.
- [x] The drama fixture and `smoke.mjs --fixture drama` carry a still shot.

## Steps

- [x] `core/drama.mjs`: `VISUAL_MODES`, `shotVisual`, `isClipShot`, `clipShotScenes`,
      `stillShotScenes`, `VISUAL_TIERS`, `visualTierProblems`; `core/lint.mjs` reads the tier
      from `series.json`.
- [x] `media/clips.mjs`: stills in the manifest without a generation call.
- [x] `assemble/drama.mjs`, `assemble/cli.mjs`: `motionMove`, `zoompanExpr`,
      `motionSegmentArgs`, `motionSegmentKey`, `motionFramePsnrArgs`, layout kind `motion`.
- [x] Tests in `drama.test.mjs`, `clips.test.mjs`, `lint.test.mjs`, `assemble/drama.test.mjs`;
      `synthetic.mjs` and `smoke.mjs` updated.

## How to verify

```bash
node --test tools/video/core/drama.test.mjs tools/video/core/lint.test.mjs tools/video/media/clips.test.mjs tools/video/assemble/drama.test.mjs
node tools/video/assemble/smoke.mjs --fixture drama   # needs ffmpeg and Chromium; CI video-tooling.yml runs it
```

## Notes

- 2026-09-27: done on `claude/keen-hamilton-plu6kp`. The zoompan expressions use `on`
  (the output frame number) over the segment's frame count, so the move lands exactly on
  the last frame and the segment has exactly `frames` frames; the keyframe is upscaled to
  2400x1350 first so a 12 % push-in never shows a soft edge.
- The visual share is a lint error above the cap and, for `stills`, a warning below 5 %,
  so a writer who forgot the tier is caught before the clip stage spends anything.
