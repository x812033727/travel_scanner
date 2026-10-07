---
id: 2026-10-04-native-video-project-stop-and-producer-exclusion
title: Honor project STOP and share producer ownership before native video mutations
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-project-lease
claimed_at: 2026-10-07T01:30:43Z
created_at: 2026-10-04T15:39:59Z
completed_at:
branch: claude/sharp-bardeen-ob6fn9
depends_on:
  - 2026-10-03-video-worker-narration-takes-made-stale
  - 2026-09-30-video-worker-moves-two-videos-at
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/core/project-lease.mjs
  - tools/video/core/project-lease.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/keyframes.test.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Honor project STOP and share producer ownership before native video mutations

## Why

The bounded Argon/SEC image repair must preserve the current source, selected
takes, passed images and paid accounting while the native worker continues
other videos. The existing worker and manual recovery have no shared atomic
project ownership. Empty job/lock tables or a process-local busy set are
snapshots, not producer exclusion.

A canonical project STOP also does not currently provide complete exclusion.
At inspected head 7132cd7d5e6bb4f85c7bb9b2627991ea83aa783c:

- flow selection (649-667) checks process-local busy state but not project STOP.
- advance (1266-1284) reads pipelineStatus.stop without rejecting it.
- fixPrompts (1608-1627) can write a new script under STOP.
- keyframes (453-457) writes the manifest from its stopped branch.
- Stage.generate / judge check STOP before awaiting submit; those checks do not
  serialize another producer or prevent a later source mutation.

Do not clear or create a live STOP as a substitute for an actual exclusion
contract. The proposed three-shot repair remains offline and held until a
safe producer boundary is verified.

## Acceptance

- [ ] Claim only after every overlapping active owner has handed off or released
      the relevant scope. The dependency implementations have landed, but their
      claims and production verification remain open; do not close them for
      their owners.
- [ ] A project STOP blocks a new writer, canonical source/manifest mutation,
      and paid dispatch at each entry and immediately before the operation.
- [ ] A response to an already accepted paid request is durably preserved under
      its original intent even if STOP arrives; no next call or automatic
      uncertain retry follows.
- [ ] Normal auto, native media CLI and manual recovery participate in the same
      atomic project lease across processes. Contention and stale/ambiguous
      ownership cause zero paid dispatches and zero canonical writes.
- [ ] Source, current effective owner/choices, selected settings, accounting,
      STOP and drop guards remain in force before and after awaits; a lease is
      not evidence of owner approval.
- [ ] Existing or another producer's STOP/lease is preserved. Crash recovery
      retains unknown intents and paid receipts rather than resetting them.
- [ ] Tests run the actual consumers with two competing processes, a STOP
      arriving during an awaited provider result, and each canonical mutation
      path. Other projects can continue while one project is held.
- [ ] Validate tools/media checks and the normal workflow review contract.
      Freeze and independently review the change before any production use.

## State

This ticket records an independently reviewed code finding. No implementation,
lease acquisition, STOP change, source mutation, paid dispatch or deployment
was performed. The existing native-language durable-units task is separate:
it covers stage/checkpoint adoption and progress; this task covers shared
ownership and canonical mutation fencing.

The three-shot candidate remains at
TEMP/mokaair-quality-five-holds-independent-offline-candidate-20261004.json,
SHA256 29B646EB9B842251F1F73A8D215AE7C8D72FBCC217EF85E21A4B5A15AE025608.
Its proposed USD 0.0405 phase ceiling does not establish producer safety or
authorize a fourth attempt with the same payload.
