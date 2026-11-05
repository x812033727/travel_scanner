---
id: 2026-11-05-shorts-build-leave-true-peak-headroom
title: Shorts build: leave true-peak headroom for the AAC encode
status: done
priority: P2
area: tools
owner: claude-opus-tech-signal
claimed_at: 2026-11-05T06:24:40Z
created_at: 2026-11-05T06:24:34Z
completed_at: 2026-11-05T06:27:07Z
branch: claude/dazzling-wright-pqolfx
depends_on: []
scope:
  - tools/video/shorts/build.mjs
  - tools/video/shorts/build.test.mjs
---

# Shorts build: leave true-peak headroom for the AAC encode

## Why

`shorts/cli.mjs build` on `daily-ai-20261104-short-1` (narration only, no music bed) stopped after the encode with
`final loudness failed: the true peak -0.65 dBTP is above −0.8`. The narration-only branch aimed loudnorm at
TP −1, and the AAC encode that follows adds overshoot, so a target one-fifth of a dB from the gate fails on some
voices. No Short with a bed hit it.

## Definition of done

- [x] A narration-only Short whose two-pass loudnorm lands near −1 dBTP still passes the −0.8 gate after the AAC encode.

## Steps

- [x] Aim the narration-only loudnorm (both passes) at TP −1.5 (`NARRATION_LOUDNORM`, `narrationLoudnormFilter` in build.mjs).
- [x] Test the filter's target and that the gate still refuses −0.65.

## How to verify

`node --test tools/video/shorts/build.test.mjs`; `node tools/video/shorts/cli.mjs build --file docs/videos/daily-ai-20261104/short-1.json --workdir <dir>` now finishes (2026-11-05, check-audio 8/8 clean).

## Notes

- The mixed branch (`mixArgs`, with a music bed) and `from-drama.mjs` still aim at TP −1; neither has failed the gate. Change them the same way if one does.
