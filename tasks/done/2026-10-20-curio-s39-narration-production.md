---
id: 2026-10-20-curio-s39-narration-production
title: Produce S39 approved narration and image budget
status: done
priority: P2
area: docs
owner: codex-s39-caesar
claimed_at: 2026-10-20T00:59:35Z
created_at: 2026-10-20T00:59:34Z
completed_at: 2026-10-20T01:37:56Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/verify-9.md
---

# Produce S39 approved narration and image budget

## Why

S39 R3a script and still prompts passed independent preflight. Production needs a
hash-bound handoff, an independently checkable narration, and a complete maximum
cost before any still or music request is sent.

## Definition of done

- [x] Recommended outline A and exact audited script are recorded under the
  owner's standing delegated instruction, without suggesting personal review.
- [x] Official narrative panel import passes and narration is synthesized.
- [x] Audio check has zero flags and the measured story body lasts at least 8 minutes.
- [x] Dry-run quotes the full still and music ceiling; no paid still request starts
  before coordination with the S04 worker over the shared MiniMax hourly quota.
- [x] Production evidence, hashes, and next gates are in `verify-9.md` and
  `verify-10.md`.

## Steps

- [x] Reconfirm the R3/R3a independent evidence and locked files.
- [x] Import the blind seal into the official narrative verdict; record
  delegated outline and script approvals.
- [x] Run TTS dry-run and image dry-run.
- [x] Finish TTS, two targeted redo rounds, three audio checks, measured timing,
  music dry-run, and handoff.
- [x] Resolve the six remaining audio flags after R4 fresh script review, then
  obtain a zero-flag current audio check.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s39 --answers /tmp/curio_s39_r3_narrative_answers_cited.json`

`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs check-audio --slug curio-s39`

`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs keyframes --slug curio-s39 --dry-run`

`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs music --slug curio-s39 --dry-run`

## Notes

The first narrative import failed only because the reviewer wrote `cs001`
instead of the CLI-required `[cs001]` citation syntax. Round 2 used the same
independent judgments and the exact spoken line as a citation, and passed.
The first still dry-run quotes 86 images, US$1.16 for one take and a hard
US$3.48 ceiling at three takes. The music dry-run quotes US$0.08, for a
US$3.56 total ceiling. No paid image or music request has been sent.

The initial 87-request TTS track was 560.9 seconds and its story body was
502.27 seconds. `check-audio` flagged 15/89 lines. Targeted redos of 15 and
then 7 lines reduced that to 7 and then 6 flags; third audio check still exits
1. The final old-script audio is 561.4 seconds, with 502.77-second story body.
Its six flags are `cs010,cs021,cs036,cs049,cs079,cs084`, captured in
`docs/videos/curio-s39/verify-9.md` and `verify-10.md`. A separate narrow R4
listener rewrite task completed the exact-version independent 13/13 blind and
source/visual review, new delegated script approval, and new audio. The final
R4a track is 563.6 seconds, with 504.97-second story body; `check-audio`
reported 0/89 flags. The site audio review is pending because this is a
hand-driven episode; a delegated local audio approval on the exact timeline
is recorded without claiming the owner listened. Music cost US$0.08 and was
generated after that local gate. MiniMax images await shared quota capacity.
