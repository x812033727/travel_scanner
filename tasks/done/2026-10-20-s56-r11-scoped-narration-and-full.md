---
id: 2026-10-20-s56-r11-scoped-narration-and-full
title: S56 R11 scoped narration and full audio gate
status: done
priority: P2
area: docs
owner: codex-s56-r11-audio-gate
claimed_at: 2026-10-20T22:57:23Z
created_at: 2026-10-20T22:57:19Z
completed_at: 2026-10-20T23:07:50Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s56/review/r11-audio-gate
  - docs/videos/curio-s56/verify-11.md
---

# S56 R11 scoped narration and full audio gate

## Why

S56 R11 has a new frozen script after the R6 narration ended with 21 machine audio flags. Its independent source review, formal two-reader narrative merge, and Jev policy passed. The old audio does not certify this exact script; synthesize only uncached requests, check every R11 line, and preserve any remaining flags for the next author.

## Definition of done

- [x] Exact frozen creative hashes and all three pre-audio gates recorded.
- [x] Cached TTS, full audio checks, and two bounded scoped retakes archived with raw flags and WAV scope evidence.
- [x] Final R11 audio HOLD, measured timing, costs, and next step stated without claiming a site approval.

## Steps

- [x] Verify R11 five-file freeze, independent source PASS, OR narrative 13/13 PASS, Jev policy PASS, and lint 0/0.
- [x] Claim this narrow task and dry-run TTS: 121 requests, 25 new, about 559 billable characters.
- [x] Finish TTS and run full 154-line check-audio.
- [x] Perform two scoped retake rounds with a full 154-line recheck after each: 9 → 2 → 2 flags.
- [x] Archive source-bound receipts, note final gate, and run docs/task checks.

## How to verify

With `VIDEO_WORKDIR=/workspace/.video-work`, `NODE_USE_ENV_PROXY=1`, and `NODE_NO_WARNINGS=1`, run `node tools/video/cli.mjs tts --slug curio-s56 --dry-run`, then cached `tts --slug curio-s56` and `check-audio --slug curio-s56`. The archived `review/r11-audio-gate/` logs and SHA manifests bind results to the R11 freeze. `npm run test:docs-videos` and `npm run check:tasks` check the repo handoff.

## Notes

The R6 review (`docs/videos/curio-s56/review/r6-audio-gate.md`) documents the older 21 flags. R11's final two flags are `s56096` and `s56174`; their intended/heard lines and narrow source-safe wording directions are in `docs/videos/curio-s56/review/r11-audio-gate/oral-wording-handoff.md`. The final narration is 12:11.10, with a 54.53-second opening and 11:16.57 of subsequent spoken audio. New R11 TTS billed 789 characters across 36 requests; 154/154 lines were checked on all three rounds. The two retake SHA audits show only flagged WAV IDs changed. The private `STOP` marker is present; no human listening, site audio approval, art, music or final cut is claimed. Exact hashes and raw outputs are in `review/r11-audio-gate/run-receipt.json` and `summary.md`.
