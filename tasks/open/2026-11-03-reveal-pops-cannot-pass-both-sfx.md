---
id: 2026-11-03-reveal-pops-cannot-pass-both-sfx
title: Reveal pops cannot pass both sfx checks on a long two-host episode
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-03T03:23:04Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/assemble/sfx.mjs
---

# Reveal pops cannot pass both sfx checks on a long two-host episode

## Why

On `daily-ai-20261103` (Tech Signal, 21.6 min, two hosts, AI music bed looped 8×) the `techsignal` sound set could not get through `assemble`. `planSfx` (`tools/video/assemble/sfx.mjs`) puts a `pop` on every reveal, and `sfxAudibility` then fails the cut in two opposite ways:
- Where the bed swells between lines, the pop is masked (less than `SFX_ABOVE_BED_DB` = 6 dB above the bed).
- Where the voice already peaks near −1 dBTP, the pop clips (the whole mix's true peak in the window goes over `LOUDNESS.truePeak`).

The only knobs are the sound's `target_lufs` (one value for every pop) and `gain_db` (writer cues only), so no setting passes both. Across three tries (−34, −26, and a soft sine blip at −24 LUFS) the failures only moved to other cues. The episode shipped with the music bed only (`sfx` removed), and the intro theme was dropped with it.

## Definition of done

- [ ] An auto-placed cue that would mask or clip is moved or dropped (and listed in the checks), instead of failing the whole cut.
- [ ] Or: per-sound limits so a pop is placed only where the voice peak leaves room.

## Steps

- [ ] Reproduce with `daily-ai-20261103` (its video.json in the commit before "music bed only") and the `techsignal` set in `<VIDEO_WORKDIR>/_sfx/`.
- [ ] Decide between dropping/moving failing auto cues and placing pops only in quiet windows; add tests in `tools/video/assemble/sfx.test.mjs`.

## How to verify

`node --test tools/video/assemble/sfx.test.mjs`; reassemble the episode with `sfx` restored and see it pass.

## Notes

- Writer-placed cues (`sfx.cues`, e.g. the intro theme) should keep failing loudly; only automatic pops and whooshes should be movable.
