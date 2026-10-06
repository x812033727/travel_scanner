---
id: 2026-10-05-long-video-cc-from-aligned-times
title: Long video CC cues cut at measured character times when the timeline carries them
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-cc-aligned
claimed_at: 2026-10-06T00:18:30Z
created_at: 2026-10-05T16:08:23Z
completed_at:
branch: claude/long-video-cc-aligned-times
depends_on:
  - 2026-10-05-speech-align-character-timing
  - 2026-10-05-caption-translation-chain-upgrade
  - 2026-10-05-reuse-confirmed-speech-results-across-restart
scope:
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
  - tools/video/tts/synthesis.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - docs/videos/DESIGN.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Long video CC cues cut at measured character times when the timeline carries them

## Why

Long-video captions split a line's speech window among its cues by text weight
(`core/captions.mjs timePieces`): a cue starts when the weights say so, not when the first
character is spoken. With character timing from the server
(`2026-10-05-speech-align-character-timing`) every cue can start on the measured character,
which is what viewers reading CC on an 8-minute video notice most on long lines.

## Definition of done

- [ ] A line whose `timeline.json` entry carries `timing.chars` splits its cues at the measured
      times (a cue starts when its first character is spoken, ±1 frame).
- [ ] A timeline without timing produces byte-identical SRT and VTT to today (regression on
      the fixtures).
- [ ] `checkCues` reads speed from measured spans; `speech_hash` is unchanged (timing is derived
      from the audio, never an input).
- [ ] Translated locales keep their own split but inherit the zh-TW cue boundaries' times.

## Steps

- [ ] `timePieces(pieces, startMs, endMs, rules, canFit, chars = null)`; weights stay the fallback.
- [ ] `tts/synthesis.mjs` + `tts/cli.mjs`: store `timing: {source, chars}` per line in
      `timeline.json` when the server returned it; `core/stages.mjs` passes it to the captions stage.
- [ ] Tests on the fixtures (`core/captions.test.mjs`, `tts/tts.test.mjs`); `DESIGN.md` §字幕.
- [ ] Receipt increment by an independent agent (`tts/synthesis.mjs`, `tts/tts.test.mjs`, `DESIGN.md`).

## How to verify

```bash
node --test tools/video/core/captions.test.mjs tools/video/tts/tts.test.mjs
node tools/video/cli.mjs captions --slug <video>      # cues start on the spoken character
node tools/video/long-form/cli.mjs check
```

## Notes

- The long video stays CC only: no karaoke burn-in (the owner's 2026-09-29 decision).
- Bound: `tts/synthesis.mjs`, `tts/tts.test.mjs`, `docs/videos/DESIGN.md`.
- 2026-10-06: dropped `tools/video/core/stages.mjs` from `scope` and
  `2026-10-01-hand-off-owner-approved-renewed-finals` from `depends_on`. Both were there only
  for the shared captions stage in `core/stages.mjs`, which that Codex ticket holds in progress.
  It is not needed: `buildCues` (`core/captions.mjs`) reads `timeline.lines`, and
  `presentationTimeline` (`core/branding.mjs`) spreads every line (`{...entry}`), so a line's
  `timing` reaches the cues without any change to `core/stages.mjs`. A timeline without timing
  keeps byte-identical SRT/VTT, so the caption offsets of renewed finals are unaffected. The
  other three dependencies are done: speech-align and the caption chain landed in #1315,
  reuse-speech in #1302.
