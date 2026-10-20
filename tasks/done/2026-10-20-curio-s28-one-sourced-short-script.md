---
id: 2026-10-20-curio-s28-one-sourced-short-script
title: Curio S28 one sourced Short script
status: done
priority: P2
area: docs
owner: codex-s07-shorts
claimed_at: 2026-10-20T05:31:56Z
created_at: 2026-10-20T05:31:53Z
completed_at: 2026-10-20T05:37:40Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s28/shorts.json
  - docs/videos/curio-s28/short-verify-1.md
---

# Curio S28 one sourced Short script

## Why

The Curio series requires one sourced vertical Short per episode. S28's completed
long film has verified source notes and finished keyframes but no `shorts.json`.
This task adds only the no-spend script and its source/check receipt; making or
publishing the Short is a later media step.

## Definition of done

- [x] One 25–55-second target script focuses on the source-checked distinction
      between Sima Guang's stated age at reading and the unstated age at rescue.
- [x] Every selected shot belongs to S28 and resolves to an existing, reviewed
      keyframe with a matching evidence hash.
- [x] The Curio one-Short episode checker accepts the draft after its separate
      validator fix lands; no paid TTS or build starts in this task.

## Steps

- [x] Check the cited 《宋史》 passage against `research.md`, `claims.md`, and
      the long film's approved wording.
- [x] Draft six ordered beats, verify schema, shot identities, evidence hashes,
      metadata length, and prohibited calls to action.
- [x] Run `from-episode --check` once the validator task lands and record the
      result in `short-verify-1.md`.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/shorts/cli.mjs from-episode --slug curio-s28 --check`;
`npm run check:tasks`. This task makes no paid media call.

## Notes

《宋史》卷 336 first says seven-year-old Sima Guang listened to lectures on
《左氏春秋》, then recounts the jar rescue without a new age. The Short must not
claim the rescue certainly happened at seven. It uses the long film's AI cartoon
shots as illustration, not historical evidence. `source.url` is intentionally
absent while the long film has no YouTube video ID; the Shorts package inserts
the full-film link once that ID exists. Until then upload metadata will flag
the missing destination.

Validator commit `68dbe714` landed; `from-episode --check` reports one valid
Short and all selected keyframe hashes match. Its focused unit tests passed 7/7.
The next media task may build the Short only after the S34 producer releases
its server voice/ASR call window, to avoid overlapping rate limits.
