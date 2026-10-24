---
id: 2026-10-20-s56-r12-scoped-narration-and-full
title: S56 R12 scoped narration and full audio gate
status: done
priority: P2
area: docs
owner: codex-s56-r12-audio-gate
claimed_at: 2026-10-20T23:19:03Z
created_at: 2026-10-20T23:19:00Z
completed_at: 2026-10-20T23:23:51Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s56/review/r12-audio-gate
  - docs/videos/curio-s56/verify-12.md
---

# S56 R12 scoped narration and full audio gate

## Why

R11's 154-line full audio check remained HOLD after two scoped retakes (`s56096`, `s56174`). R12's author changed only those two spoken lines, and independent source, formal narrative, and policy gates passed on the new five-file freeze. R11 audio and gate receipts do not certify R12; synthesize only changed requests, check all lines, and preserve exact evidence.

## Definition of done

- [x] Exact R12 five-file SHA and pre-audio gate receipts verified; R11 STOP and all pre-R12 WAV hashes preserved.
- [x] R12 cached TTS, full 154-line audio check and WAV scope audit archived; zero flags meant no retake.
- [x] Truthful machine PASS handoff, measured timing and pending site review recorded without claiming human approval.

## Steps

- [x] Verify freeze, source PASS, formal OR narrative 13/13 PASS, Jev policy PASS, and lint 0/0.
- [x] Dry-run TTS, preserve R11 STOP/pre-WAV manifest, then synthesize R12 changed requests.
- [x] Run full check-audio: 154/154, zero flags; no `tts --redo` required.
- [x] Archive receipts and status; submit outline, R12 script and audio site cards, then pull pending status. Run docs/task checks.

## How to verify

With `VIDEO_WORKDIR=/workspace/.video-work`, `NODE_USE_ENV_PROXY=1`, and `NODE_NO_WARNINGS=1`, run `node tools/video/cli.mjs tts --slug curio-s56 --dry-run` and `check-audio --slug curio-s56`. Compare R12 `review/r12-audio-gate/` logs, SHA manifests, and gate receipt to the exact five-file freeze. Run `npm run test:docs-videos` and `npm run check:tasks`.

## Notes

R11 receipts remain under `docs/videos/curio-s56/review/r11-audio-gate/`; this task owns only R12 media receipts and `verify-12.md`. The R12 TTS call cost 37 billable characters in two requests, reused 119, and changed only the two revised line WAVs; 174 others remained identical. The 154-line check recorded 116 exact, 33 same-sound/filler, 5 previously Jev-accepted, zero flagged. Narration 12:11.67, opener 54.53 seconds, body 11:17.13. Site outline, script and audio cards returned pending; `review-pull` returned exit 3, waiting for owner. No creative edits, human listening, site approval, art, music, or final cut are claimed. See `docs/videos/curio-s56/review/r12-audio-gate/summary.md` and `run-receipt.json`.
