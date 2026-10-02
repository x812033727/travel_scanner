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
- [ ] Render and review the representative pilot (currently 51 seconds by audio edit) within USD 100, then the currently requested E1-2 within cumulative USD 350 if accepted; do not automatically add E3.
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

Historical opening-only checkpoint before the subsequent two-episode request (PR #1135):
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

Historical next work at that checkpoint: listen to this sample, record E1 L012-L033, retime the entire
episode, and build an executable full visual plan that retains silent shots.
Existing schema requires nonempty scene lines and current timeline follows lines;
do not add dummy TTS or silently lose S06/S07/S11/S12/S15. Coordinate shared code
with PR #1132 before changing it. Verify current backend document/script gates,
then establish isolated production using Veo 3.1 Lite 1080p / 8 s before images
or clips. The current tool token cannot modify global settings, and simply enabling
global drama may start other works. No final video or owner full-film acceptance
has been obtained; foreign work remains deferred by the owner's instruction.

Current two-episode checkpoint, 2026-10-02 (supersedes opening-only next steps):
- Owner explicitly requested all optimization followed by two episodes, Chinese only.
- All 40 editorial directives independently checked; E1/E2 full scripts complete.
  E3-E40 full dialogue and actual film are still unfinished.
- E1 33 lines / 40 editorial shots / 144.86 s; E2 34 / 41 / 159.05 s.
  All 83 original shot IDs and 17 silent action windows retained; two E1 merges
  fit measured voice and keep the reply offscreen. No freeze/voice stretching.
- 67 unique spoken lines; first 11 reused. Total 68 successful TTS requests,
  900 billable characters including one 2-character retake. Both old/new takes
  preserved. Two ASR flags per episode remain; human listening has not happened.
- Sample-exact assembly/stem/CC independent review passed; MP3 previews and raw
  media remain outside Git. 81 x 8-second Veo first-pass estimate is USD 51.84,
  not spent. Actual provider USD unknown, USD 10 reserve includes the earlier 5.
  The prior USD 3,000 included unmeasured high retakes; it is not a spend target.
- Full script review submissions created for the two competition slugs only:
  E1 b909e8f3-0cfd-4488-b323-1d81dbaa0dce; E2 e0c54172-1349-40fa-b29f-0da3422e84cb.
  Both read back pending, subject null, no decision. No source doc approval,
  Series/worker/global setting change, images or animation generation occurred.
- Isolated runner in sibling task has 42 focused offline tests and independent
  review; not deployed. Host/port and permitted connection are unavailable in
  this workspace. Existing backend series_script_gate remains true.
- Continue from episodes/scoped-production-runbook.md after actual doc/script
  approval and admin host access; look/storyboard acceptance then first clip.
  No full-film owner acceptance, foreign work, publication or competition start.

2026-10-03 Windows takeover:
- Checked out PR #1135 at 117a867ac; its 10 CI checks were successful and it was
  still a draft. Host connectivity is now verified; prior missing-host text above
  describes the cloud environment, not this new execution environment.
- Revalidated 10 source and 49 package hashes, 15 required inputs, both measured
  edits and source binding. All match Git and working-tree bytes. Original runner
  42 tests and audio-builder 19 tests passed without provider requests.
- Live source series is still `setting`; latest setting/outline/chapter 1 v3 are
  `review`, and E1/E2 script reviews remain `pending`. No look/storyboard or media
  jobs exist for the production slugs. Global drama stays OFF.
- The original `/workspace/.../transfer/` media tar.gz and checksum are absent
  from this Windows environment; checked local media/download locations and VPS
  `/root` did not contain that bundle. The owner has been asked for a reachable
  path/link. Do not rerun TTS to replace the missing transfer.
- Exact source archive, runtime schema, safe live snapshot and offline evidence
  are preserved outside Git under the local competition handoff directory.
  Public continuation details: `episodes/vps-handoff-preflight-20261003.md`.
- Four listening flags remain and no animation, native listening, full-film
  owner acceptance, foreign work or publication is claimed.

2026-10-03 02:07 Taipei transfer recovery (supersedes the missing-media blocker):
- Original production chat had uploaded the archive to the authenticated media
  store as `wedding-reckoning-transfer-20261003`; the physical filename is its
  SHA, explaining why searching for the archive's original name missed it.
- Retrieved directly with existing SSH/SCP access, no pairing, token transfer or
  TTS requests. Original VPS bytes retained. Archive is 79,095,367 bytes and SHA
  `48d6c4ccfb7d59cdc6349a4a69abef80e931f23950968de6bc5db710e7856e29`.
- All 146 transfer-manifest entries passed size/hash/set equality. Archive has
  147 regular files including the manifest, no unsafe or duplicate paths; safely
  extracted into a new private repo-external directory.
- Refreshed live DB read still shows source series setting, v3 documents review,
  both scripts pending, no production media jobs, global drama OFF. Media
  recovery does not authorize or satisfy any pending owner review.
- Independent recovered-content verification passed 539/539 checks: all 67
  source WAVs/cache, 2 masters, 7 cast stems, SRT/VTT 67 cues each, the 51-second
  pilot and old/new take match. Pure request planning is 67/67 cache hits. MP3s
  decode completely, all 147 recovered files remain byte-identical, and no new
  TTS/provider request was made. Four listening flags remain unchanged.

2026-10-03 production closing checkpoint (supersedes earlier next steps):
- The owner's repeated two-episode request is still in progress, zh-TW only.
  Source setting/outline/chapter 1 v3 and both scripts now have normal approvals;
  chapter 1 marked E1-E10 ready, but execution remains scoped to E1/E2 only.
- Zhitang pantsuit look B and Gu Chengchuan look A are normally approved. The
  latest approved storyboard contains S01 R02 and S03 R03 first frames only.
  Existing voice/audio/source/timing artifacts were reused, not regenerated.
  E2 S34 first-frame visual metadata alone was corrected; its timing is unchanged.
- S01 R03 was rejected for a second watch and extra hand action. R04 yielded an
  actual five-second existing-voice preview and a sampled usable-window opinion,
  but the normal judge remains 6.72/failed. The 37-frame blink audit did not change
  that result. The owner has not answered the retain-or-retake choice; pilot is
  not accepted, and no full batch is released.
- S03 R01 clip was rejected for extra hand/pen/watch and prop changes. R02 remains
  ready as a generated file but fails the planned 0-4.5 second window: the hand
  lifts and rotates the pen near horizontal at about 0.75-1.75 seconds, beyond
  the required small tremor. Independent QA decoded all 192 frames and viewed
  45 unique frames; no full playback or audio acceptance is claimed.
- S04 R01 was rejected for framing/hair drift; R02 was rejected because its
  page-pointing wrist wears the watch while the accepted S03 pen-holding wrist
  wears it. The source does not prescribe wrist side. Neither frame was approved.
- Final read-only audit at 2026-10-02 19:42:44 UTC found 16 generation jobs, all
  terminal (14 ready, 2 failed), global drama OFF and unchanged settings hash.
  All jobs are E1; E2 has no generated images/clips. There are no final/publish
  reviews. The round stopped additional paid requests after the begun retake.
- Ledger adds 10 image and 6 clip reservation rows plus 2 actual judge calls.
  Conservative exposure is USD 15.180 = 1.340 images + 3.840 clips + 10 manual
  reserve. The judges' USD 0.02 estimate is covered by that manual reserve; do not
  add it twice. Actual provider bills remain unknown; failed/rejected reserves
  are retained. The fsync-before-POST abort and one explicit recovery are preserved.
- Follow `episodes/production-run-20261003.md` and `handoff.json.current_production_run`
  for exact job/review/image hashes and repo-external receipt locations. The
  coordinator's latest GitHub read reports PR #1135 is no longer a draft; this
  checkpoint does not merge, deploy, publish, or complete the production task.
- Remaining: owner S01 quality decision, bounded S03 motion correction and S04
  reference-continuity plan, then each remaining shot and final audiovisual QA.
  Four listening flags and E2 S06 lip sync remain; foreign work still waits for
  owner acceptance of the entire Chinese film and CC. Keep this ticket open.
