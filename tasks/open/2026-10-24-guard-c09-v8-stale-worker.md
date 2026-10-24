---
id: 2026-10-24-guard-c09-v8-stale-worker
title: Guard C09 approved script and project from stale story worker regeneration
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-24T06:21:06Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
---

# Guard C09 approved script and project from stale story worker regeneration

## Why

C09 `script.md` and `video.json` now bind to the owner's approved v8 77-line
script and 77-scene visual plan. The generic `story.mjs` `relint()` path can
rebuild those files from older six-chapter workdir files; the current
`pilotScriptReviewProblem()` protects only two v2 pilot slugs. A worker run
could silently reintroduce the old 85-line C09 material. Keep the series paused
until an exact, tested canonical-hash guard is merged and read back on the host.

## Definition of done

- [ ] C09 generic worker cannot overwrite the approved script or render project
      when its chapter source differs from the frozen v8 evidence; the worker
      reports a precise hold instead of generating or purchasing media.
- [ ] Existing story series still follow their current regeneration path.
- [ ] Host/readback confirms the guard before the C09 series is unpaused.

## Steps

- [ ] Coordinate normal narrow release of `story.mjs` and its test path from
      overlapping tasks; do not claim with `--force`.
- [ ] Add focused positive and negative worker tests for the exact C09 hashes.
- [ ] Confirm the C09 backend series remains paused throughout this work.

## How to verify

Run the focused `story.test.mjs` suite, `npm run check:tasks`, and a local
read-only replay showing a changed C09 chapter source yields HOLD without
rewriting `script.md` or `video.json`. Verify the deployed guard and paused
series via persisted readback before permitting any pilot.

## Notes

Canonical script SHA-256:
`4445AD74BCAFBAC1DFCA65392199FEC89700C17AB8C01E665AC79DFFFC1AA3F7`.
Frozen visual JSON SHA-256:
`2235EA304C240E78F6473183E45A63502500EE20F931107843C6AF3C5AD0BF5A`.
The local offline preflight is
`docs/videos/story-everyday-patagonia-c09/preflight-v8.mjs`; it is not a
host-worker guard. At ticket creation, other open tickets owned the core paths,
including dictionary merge, 10-minute MiniMax cute-brand support, and story
worker pronunciation handling. This ticket is intentionally unclaimed.
