---
id: 2026-10-05-video-slides-prompt-repair-format
title: Preserve slides format in keyframe prompt repair
status: done
priority: P1
area: tools
owner: codex-news-video-stall-fixes
claimed_at: 2026-10-05T10:26:04Z
created_at: 2026-10-05T10:18:55Z
completed_at: 2026-10-05T10:47:36Z
branch: codex/news-video-stall-fixes-20261005
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Preserve slides format in keyframe prompt repair

## Why

At 2026-10-05 10:14:58 UTC, production and this checkout both ran
7318edc7fe24ed1a0cd2495f6e5356d06e16c05b. Two illustrated slides videos,
ai-agent-travel-booking-instinct and
cloudflare-workers-per-worker-permissions-ai-agent, repeatedly submitted
keyframe prompt repairs as drama writer jobs although their backend and
video.json formats are slides. The global drama switch is intentionally off.

Teaching drafts omit state.format in flow.mjs:924-938. report() defaults it
to slides (line 452), but fixPrompts() defaults it to drama (line 1626).
The API therefore rejects the repair before model dispatch. The client then
removes the failed receipt and the oldest-first lanes select the same videos
again on the next five-minute round. The snapshot has 410 settled
video_ai_drama_disabled failures, all recent failures with null dispatched_at;
these are not 410 paid generations. Both projects still appear active with
the last successful narration-approved backend status.

## Definition of done

- [x] A slides keyframe repair uses the actual slides format even when an old
      or newly created auto.json omits format. Backend reports and model calls
      agree, without activating drama or altering paid settings.
- [x] Explicit drama and story repairs retain their existing format and policy
      checks. Reject conflicting identities rather than silently converting a
      different production route.
- [x] Coordinate with the existing deterministic-policy-hold task so a settled
      refusal is retained, reported, and cannot monopolize the lanes.
- [x] Retain the original failed policy receipt across restarts, block/report
      the affected project, and require a fresh validated owner retry before
      archiving a policy hold. Scope includes the client and receipt store for
      this repair; pending/uncertain paid outputs remain recoverable.
- [x] Preserve prior scripts, approvals and receipts. An authorized production
      continuation is a separate step after the reviewed code is deployed.

## Steps

- [x] Check current main, active claims, worktrees and PRs before claiming the
      shared flow scope; coordinate with its owners without force claiming.
- [x] Unify effective format handling for newly created and historical states.
- [x] Add meaningful offline regression cases and have the implementation
      independently reviewed before any production use.

## How to verify

Use the real Automation with an illustrated slides video.json and auto.json
without format. Force keyframes to request a prompt repair and capture the
writer request: format must be slides, variant must remain illustrated, and
drama_enabled=false must stay unchanged. Cover an explicit drama state, a story
state, identity conflicts and the backend report. No live model call is needed.
Run affected automation tests and npm run test:tools with compatible Node.

## Notes

- 2026-10-05 repair authorization: the owner said "修" after the production
  diagnosis. This claim covers the related format and deterministic refusal
  fix, plus an independently authored duration receipt. The original policy
  task's implementation dependency #1182 is merged, but its unrelated seven
  video deployment acceptance is still open; no other owner's task is released
  or force claimed. Active flow claims were absent. PR #1242/#1271 touches
  stopped-audio handling elsewhere in flow; preserve and recheck those changes
  before pushing or rebasing.

- Latest independently read job requests at approximately 10:17 UTC carried
  format=drama and payload.fix.kind=keyframes: 15 targets for Cloudflare Workers
  and 35 for the travel-booking video. Both returned video_ai_drama_disabled
  with null dispatched_at. This confirms the specific fixPrompts path rather
  than a general provider outage.
- Existing related task: 2026-10-04-retain-video-policy-holds-without-new handles
  failed receipt retention and project-local holds, not this incorrect format
  fallback. The two fixes must be coordinated.
- Three unrelated videos are already blocked by the US$20 slides cap:
  gemini-4-argon-who-can-use-it (US$21.28),
  gemini-skills-replace-gems-move-checklist (US$25.40), and
  sec-ai-trading-bot-whatsapp-scam (US$20.38). Do not increase their budgets as
  part of this fix.
- Initial diagnosis involved no production write, retry, generation, restart or
  publish. The owner subsequently authorized the code repair with "修".
- Repair: new slides drafts persist their format; legacy prompt repair resolves
  the saved video format, and explicit conflicting identities block the project.
  A deterministic drama-disabled refusal is journaled across restarts and parked
  on its project, including failed backend-report recovery. Other eligible
  projects retain access to the worker lanes. STOP, dropped projects, changed
  source files and still-disabled fresh settings prevent owner retry.
- Native client and receipt tests passed 35/35, including one POST across
  repeated rounds/restart, direct HTTP policy rejection retention, fresh route
  validation, guarded corrected-slides recovery and original receipt archives.
  The full automation suite passed 102/102; the two later native-policy and
  authorized-retry cases also passed individually. Combined checks and
  independent duration review are recorded in the final handoff below.
- The owner independently raised the slides cap to US$40 at 10:17 UTC; a read-only
  production check confirmed it. This implementation does not change the cap or
  mint retry requests for the three previously budget-blocked videos.
- Production deployment and continuation remain distinct from offline validation.
  Prior scripts, source-bound approvals and paid artifacts are retained; no
  production write or paid request has been made by this repair branch.
- Independent video review found and verified repairs for legacy saved
  video.json without format and ambiguous multi-receipt policy retries. The
  final client/receipt suite passed 36/36. Independent duration review commit
  562b2d718 covers the eleven changed bound files: baseline SHA-256 matches,
  473 plans PASS, review tests 2/2, duration/plan tests 16/16 and the new
  automation tests 28/28. Production activation remains a separate owner
  PR/SHA decision; full branch validation and CI are in the PR handoff.
