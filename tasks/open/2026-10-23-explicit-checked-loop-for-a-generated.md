---
id: 2026-10-23-explicit-checked-loop-for-a-generated
title: Explicit checked loop for a generated music bed shorter than its cut
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-23T19:07:52Z
created_at: 2026-10-23T19:07:35Z
completed_at:
branch: claude/music-checked-loop
depends_on: []
scope:
  - tools/video/core/music-loop.mjs
  - tools/video/assemble/sound.mjs
  - tools/video/assemble/music-loop.test.mjs
  - tools/video/media/music.mjs
  - tools/video/core/state.mjs
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Explicit checked loop for a generated music bed shorter than its cut

## Why

On 2026-10-23 the owner's dub retry of `story-adapt-a4-paper-size` (ja) was blocked with
`dub ja failed: … the dub cannot carry the music bed: generated music has no fully decoded actual
duration`. The C-series music guard (ade8410ff, from #1669) holds generated music without a
decoded length, or shorter than the cut, and asks for "an explicit checked loop or another
licensed track"; no such loop existed. Every brand story of 2026-10 has a ~3-minute generated
bed (A4 171 s, Dolby 169 s, Michelin 175 s, Seiko 177 s) under a ~10-minute cut, which every
mix already plays with `-stream_loop -1` (`assemble/drama.mjs` `soundGraph`). So no published
video with such a bed could get a dub. The owner chose: published videos' dubs reuse the loop
their approved cut was mixed with.

## Definition of done

- [x] `music --slug <slug> --loop`: no provider call; checks the retained file's SHA-256, a full
  decode (>= 30 s), and that the cut on disk was assembled with these music settings; writes
  `loop` into `music/manifest.json`.
- [x] `musicInputs` (assemble and dub) and status accept a short bed only with a loop recorded for
  that file, that decoded length and a cut no longer than the recorded one.
- [x] Duration review increment for `core/state.mjs` (`claude-pr-review-music-loop-20261024`, PASS).
- [ ] Merged, deployed; `music --loop` run for A4 on the host and its block cleared; the ja/ko/es/id
  dubs made.

## How to verify

`node --test tools/video/assemble/music-loop.test.mjs` (4, needs FFmpeg); with
`core/state.test.mjs`, `dubs/dubs.test.mjs`, `media/music-duration.test.mjs`,
`assemble/drama.test.mjs`: 67 pass.

## Notes

- The paid-speech-before-music-check gap stays in `2026-10-23-preflight-music-before-paid-dub-synthesis`.
- Dolby, Michelin and Seiko need their own `--loop` before any dub or re-cut.
