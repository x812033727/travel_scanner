---
id: 2026-10-02-wedding-competition-pilot-four-languages
title: Produce wedding competition pilot and four-language cast delivery
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-02T15:04:17Z
completed_at:
branch: codex/drama-competition-wedding-20261002
depends_on:
  - 2026-10-02-drama-competition-wedding-final
scope:
  - docs/videos/series-plans/competition-20261002
  - tools/video/dubs
  - tools/video/compile
  - apps/api/app/video_reviews/admin_service.py
---

# Produce wedding competition pilot and four-language cast delivery

## Why

The competition film needs four distinct character/narrator audio mixes and CC
under one YouTube video ID. Current drama dub CLI and backend reject cast dubs;
compilation does not deliver all foreign cast tracks. Planning cannot count as
media completion. The owner authorized USD 3,000 target plus USD 1,000 reserve;
views and actual production cost are evaluated separately after three months.

## Definition of done

- [x] Pair the video tool without exposing keys; verify provider status and quota.
- [ ] Author and verify an executable pilot from the source-bound competition package.
- [ ] Produce/listen/revise Chinese cast auditions and a timed animatic; record actual cost.
- [ ] Render and review the representative pilot (currently 51 seconds by audio edit) within USD 100, then E1-3 within cumulative USD 350 if accepted.
- [ ] Support locale x speaker casting, stable line IDs, translation revisions, measured per-line TTS timing and separate music/effects mix.
- [ ] After owner confirmation of the entire Chinese film and CC, produce ja/ko/en pilot voice tracks and CC timed to each accepted track; get native listening.
- [ ] Compile matched-duration multi-language cast tracks and captions with stale-input invalidation and no Chinese speech underneath.
- [ ] Prove the target channel can attach four tracks to one video before scheduling the competition release.
- [ ] Continue full-film screenplay/production only with measured costs and bounded retakes; four languages complete before public launch.

## Steps

- [x] Read `docs/videos/series-plans/competition-20261002/README.md`, handoff.json and production-readiness.md.
- [x] Check current main, open PR #1132 and other active work before claiming code paths; no shared code changed this round.
- [x] Keep this round's media and live receipts outside Git; use the cost ledger for accepted and rejected paid outputs.
- [ ] After owner confirmation of the entire Chinese film and CC, integrate multilingual drama capabilities rather than merely deleting rejection guards.
- [ ] Run focused tests for character voice routing, own-audio CC timing, stale sources, mix isolation and compilation joins.

## How to verify

Use the selected drama's source-bound review bundle and real pilot artifacts.
Document production-check, lint, real clip/voice measurements, human listening,
CC toggle/sync, identity/prop continuity, ledger receipts and player track switching
as separate outcomes. Text reviews or a passing JSON check cannot approve media.

## Notes

This task is partially executed; the remaining film and localization work stays
open. Original 40-episode source and existing reviews remain intact. No global
drama worker activation or other-series generation is authorized by a pilot run.
The owner has already accepted the budget and completed tool pairing.
Do not treat three months as ninety days, count Shorts views toward the main video,
or apply an unagreed weighted views/cost score.

2026-10-02 owner clarification: execute zh-TW only now; ja/ko/en work must wait
until the owner confirms the entire completed Chinese film. Foreign scripts remain
drafts and no foreign-language synthesis or implementation is part of this run.
Authenticated preflight: Gemini speech configured; media drama OFF; global clip
model Gemini Omni 1.1 Flash, not Lite. Tool token cannot change global settings.
A setting change is not isolated to this work; do not assume an empty next-job
snapshot makes all-worker activation safe. Chinese TTS can proceed.

2026-10-02 completed Chinese preproduction in PR #1135:
- Full E1 text: 33 lines / 42 shots, independent causal/prop review passed. Later
  22 lines and sister voice remain unrecorded; other 39 full scripts remain unwritten.
- Existing CLI-compatible voice-only document: 10 voiced scenes / 11 unchanged
  lines; stable ID mapping. Lint has 0 errors and the expected original-fiction
  no-external-sources warning. Do not use this document to render all 15 shots.
- 11 successful TTS requests / 118 billable characters / 0 retakes. Raw voices
  total 28.00 s; editorial voice preview is 51.000 s with all 5 silent action
  windows preserved. Original WAVs used without trimming or time stretching.
- zh-TW SRT/VTT follow measured placements. Independent byte/sample and caption
  checks passed; accent, emotion and caption onset/offset human listening pending.
- Standard check-audio: 11 checked, 8 exact, 2 sound matches, 1 accepted by Jev,
  0 flagged and 0 unchecked. An earlier whole-clip transcription was inconclusive;
  2 isolated follow-ups matched. No audio was rerecorded based on that output.
- Repo-external media/receipts:
  `/workspace/mokaair-work/competition-20261002/media/wedding-reckoning-pilot-voice-zh-tw/`.
  `editorial-zh-TW/opening-zh-TW-51s.mp3` is a voice preview, not an animation.
- Actual provider USD is not returned; ledger awaits invoice reconciliation.
  USD 5 reserved for this voice/check batch is not actual spending.
- Animated video generated: 0 s. No foreign-generation/implementation requests.

Next Chinese work: listen to this sample, record E1 L012-L033, retime the entire
episode, and build an executable full visual plan that retains silent shots.
Existing schema requires nonempty scene lines and current timeline follows lines;
do not add dummy TTS or silently lose S06/S07/S11/S12/S15. Coordinate shared code
with PR #1132 before changing it. Verify current backend document/script gates,
then establish isolated production using Veo 3.1 Lite 1080p / 8 s before images
or clips. The current tool token cannot modify global settings, and simply enabling
global drama may start other works. No final video or owner full-film acceptance
has been obtained; foreign work remains deferred by the owner's instruction.
