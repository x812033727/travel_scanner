---
id: 2026-10-11-burn-the-channel-mark-into-new
title: Burn the channel mark into new videos
status: done
priority: P2
area: tools
owner: claude-video-watermark
claimed_at: 2026-10-11T16:02:41Z
created_at: 2026-10-11T16:02:24Z
completed_at: 2026-10-12T00:18:23Z
branch: claude/video-logo-watermark-b075f1
depends_on: []
scope:
  - tools/video/watermark
  - tools/video/cli.mjs
  - tools/video/core/watermark.mjs
  - tools/video/core/watermark.test.mjs
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - tools/video/assemble/plan.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/shorts/motion.mjs
  - tools/video/shorts/motion.test.mjs
  - tools/video/shorts/build.mjs
  - tools/video/shorts/from-drama.mjs
  - tools/video/shorts/from-drama.test.mjs
  - docs/videos/WATERMARK.md
  - docs/videos/BRANDING.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Burn the channel mark into new videos

## Why

The owner asked on 2026-10-11 for a logo or watermark on the videos, worried about copies
re-uploaded to other platforms. Today a slide carries a faint 26 px `MOKAAIR` in its top right
corner and a Shorts card a small brand line, but every full-frame picture (a drama clip, a still
under a camera move, an illustrated slides picture) carries nothing, and neither does a Short
reframed from a drama episode. A cut is per-scene segments joined with `-c copy`, so there is no
whole-film pass to add a mark in: it has to go in where each scene is drawn or encoded.

The owner decided: the mark says `Mokaair` over a smaller `YouTube @Mokaair`; it sits fixed in
the top right corner, where the slides already say MOKAAIR; only videos made from now on get it.
A finished, approved or uploaded cut is never touched. The owner was told a corner mark stops a
plain re-upload and does not stop someone who crops or covers it.

## Definition of done

- [x] A video rendered for the first time after this lands shows the mark in the same place on
      every scene of the long cut: slides, cards, clips and stills under a camera move.
- [x] Both kinds of Short (cards, and a reframed drama) show the mark inside the safe area.
- [x] A video built, approved or uploaded before this lands is byte-for-byte what it was when
      its stages run again, and nothing reschedules it.
- [x] The owner has seen sample frames and agreed to the look.

## Steps

- [x] The versioned PNG, its generator and `core/watermark.mjs` (registry, selection, pin).
- [x] Slides and cards: `chrome()` draws the PNG; render decides once and writes the manifest.
- [x] Clip and motion segments: one overlay before the dissolve; the mark in the segment keys.
- [x] `assemble` follows the manifest; the source-frame check masks the box of the mark.
- [x] Shorts: the overlay in both builders; a reframed drama keeps its window off the mark of
      its episode.
- [x] `docs/videos/WATERMARK.md`; the duration receipt re-issued by an independent reviewer.
- [x] Sample frames to the owner.
- [x] Follow-up tasks filed for what this leaves out.

## How to verify

```bash
npm run test:tools
node tools/video/assemble/smoke.mjs && node tools/video/shorts/smoke.mjs   # needs ffmpeg and Chromium
node tools/video/long-form/cli.mjs check
```

Then pull frames out of a smoke cut: the mark sits at the same pixels on a slide and on a shot,
does not brighten through a dissolve, and the last frame of a Short is its first.

## Notes

- The decision is made once, by render, and written to `frames/manifest.json`; assemble only
  follows it. Two selectors would disagree after a first assemble that failed its checks: it
  leaves `final.mp4` and `checks.json` behind, which is exactly what "already built" looks like.
- A page cannot load the PNG from the fake origin (only `apps/web/public/` and `docs/videos/`
  are served), so the slide carries it as a data URI; that also puts its bytes in the frame key.
- No vision check ever sees a frame of a finished cut: the "free of logos and watermarks"
  questions are asked of keyframes and raw clips only, so the mark must never be drawn into those.
- The owner saw the sample sheets (four long-cut pictures and two Shorts) on 2026-10-12 and said the look is fine.
- Measured on real pictures and on the smoke cuts: the mark a slide drew and the mark laid over a shot sit on the same pixels (39.6 dB against each other, 15.9 dB one pixel apart); it stays still under a push-in and does not brighten through a dissolve; the Shorts smoke ends on its first frame (loop tail 40.31 dB, cover identical).
- The duration receipt was re-issued by claude-pr-review-video-logo-watermark for tools/video/assemble/cli.mjs, the one bound file.
- Not deployed. On this Windows machine the full test:tools run does not finish (a test file crashes the runner with ERR_UNSUPPORTED_ESM_URL_SCHEME, and tools/reference-analysis.test.mjs fails in ffmpeg; neither file is touched here), so the video test directories were run one by one and the rest is left to CI.
- Left out, each with its own task: imported cuts, locate seeing the mark, an owner switch, the Shorts header naming the channel twice, render/repeat.mjs.
