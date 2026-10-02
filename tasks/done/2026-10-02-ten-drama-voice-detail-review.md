---
id: 2026-10-02-ten-drama-voice-detail-review
title: Review ten drama voices and production detail contracts
status: done
priority: P1
area: tools
owner: codex-ten-drama-voice-review
claimed_at: 2026-10-02T09:11:14Z
created_at: 2026-10-02T08:57:04Z
completed_at: 2026-10-02T10:05:25Z
branch: codex/ten-drama-backend-sync-20261002
depends_on: []
scope:
  - tools/video/production/voice-audit.mjs
  - tools/video/production/cli.mjs
  - tools/video/production/design.mjs
  - tools/video/production/design.test.mjs
  - tools/video/production/voice-audit.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/timeline.mjs
  - tools/video/tts/requests.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/production/audio-contract.mjs
  - tools/video/production/audio-contract.test.mjs
  - docs/videos/series-plans/binge-five-20260928/wedding-reckoning/production-design.json
  - docs/videos/series-plans/binge-five-20260928/wedding-reckoning/production-review.md
  - docs/videos/series-plans/binge-five-20260928/seventh-passenger/production-design.json
  - docs/videos/series-plans/binge-five-20260928/seventh-passenger/production-review.md
  - docs/videos/series-plans/binge-five-20260928/scapegoat-empress/production-design.json
  - docs/videos/series-plans/binge-five-20260928/scapegoat-empress/production-review.md
  - docs/videos/series-plans/binge-five-20260928/city-owes-a-light/production-design.json
  - docs/videos/series-plans/binge-five-20260928/city-owes-a-light/production-review.md
  - docs/videos/series-plans/binge-five-20260928/remembered-by-rival/production-design.json
  - docs/videos/series-plans/binge-five-20260928/remembered-by-rival/production-review.md
  - docs/videos/series-plans/claude-binge-five-20260928/reload-first-day/production-design.json
  - docs/videos/series-plans/claude-binge-five-20260928/reload-first-day/production-review.md
  - docs/videos/series-plans/claude-binge-five-20260928/before-the-hammer/production-design.json
  - docs/videos/series-plans/claude-binge-five-20260928/before-the-hammer/production-review.md
  - docs/videos/series-plans/claude-binge-five-20260928/three-needles/production-design.json
  - docs/videos/series-plans/claude-binge-five-20260928/three-needles/production-review.md
  - docs/videos/series-plans/claude-binge-five-20260928/taste-of-the-throne/production-design.json
  - docs/videos/series-plans/claude-binge-five-20260928/taste-of-the-throne/production-review.md
  - docs/videos/series-plans/claude-binge-five-20260928/ghost-at-his-side/production-design.json
  - docs/videos/series-plans/claude-binge-five-20260928/ghost-at-his-side/production-review.md
  - docs/videos/series-plans/production-20261002-voice-review
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Review ten drama voices and production detail contracts

## Why

The owner requested a further voice and production-detail review of all ten
dramas. Confirmed faults include a wrong speaker, Taiwan name pronunciations,
paper-versus-token props, and instructions that confuse voice identity with
reuse of an identical recorded take. Offline audition materials omit later
injury/aging states, and pronunciation directions do not reach TTS requests.

## Definition of done

- [x] Correct confirmed source-versus-design discrepancies without changing plots.
- [x] Prepare auditions using actual episode voice styles and source-bound cues.
- [x] Carry pronunciation hints and explicit same-take references to TTS safely.
- [x] Validate offline; retain selectable CC and independent future language audio.
- [x] Sync a fresh pending backend revision if live preconditions still hold.

## Steps

- [x] Review all ten works and implement confirmed corrections.
- [x] Test pronunciation/cache binding and explicit recorded-take reuse.
- [x] Build review bundles and record remaining actual-audio acceptance questions.
- [x] Refresh production state, sync under guards, and update draft PR #1122.

## How to verify

Run production-check/build, both source validators, focused Node tests, and
task validation. Production synchronization requires exact live row/document
hashes, generation disabled, preserved historical rows and full readback.

## Notes

- Worktree: `ten-drama-production`; branch: `codex/ten-drama-backend-sync-20261002`.
- Narrow sidecar scopes overlap two stale 2026-09-28 claims owned by this chat's
  earlier `codex-ten-drama` work. Those claims/branches are preserved. Their
  recorded repairs landed in PR #978; there is no other active drama worktree
  or open drama PR beyond this chat's #1122. Claim with --force is limited to
  this follow-up, using the user's existing authorization to fix confirmed
  findings on an independent branch; no other owner's claim is released.
- This task performs no paid synthesis, generation, approval or publication.
- The single production pronunciation assignment in flow.mjs also overlaps the
  stale 2026-09-30 worker claim. Its branch and claim remain intact, and main's
  current flow bytes match this branch's baseline. This follows the same prior
  owner authorization for independent backend repairs; no queue/retry logic changes.
- Independent agents checked all ten voices/details, 93 new Codex source refs,
  source-bound script samples, WAV reference/cache behavior, and duration policy.
  Source story hashes are unchanged. Actual audition, SFX, pilot/film acceptance
  and localization remain outside this offline repair.
- Final offline tools run: 1,224 passed, zero failures, two existing environment
  skips. Both source validators pass. The two old Codex full-story receipts remain
  stale after #1095; independent delta evidence preserves that honest boundary.
  Duration-only review renewed by a different agent for the five changed bound
  files, with the original report and receipt archived byte-for-byte.
- Production v3 synchronization: source a47f0d1c6e8d4a0c9b8948cf55ed2dba006178fb,
  canonical plan 5e3d105d878d3cb79c3bfb2428f0e1c31cfb10d84d029b02389567d87ababb32.
  All 60 new pending revisions and normal admin serializer bodies matched;
  120 historical v1/v2 rows remained exact. Ten read-only replays were unchanged.
  Global settings, target episodes, approvals and publication stayed unchanged.
  Browser rendering and runtime deployment were not performed.
- Other open PRs #1124/#1125/#1126 also update the shared duration report.
  Their branches/claims are untouched; central receipt bindings must be reconciled
  when these drafts merge. This task's own checked branch is preserved.
