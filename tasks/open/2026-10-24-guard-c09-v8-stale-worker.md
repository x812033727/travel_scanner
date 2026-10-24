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

## Read-only path audit and narrow implementation plan (2026-10-24)

The three other open tickets whose **scope** includes `story.mjs` are
`2026-10-10-dictionary-merge-treats-constructor-and-tostring` (also
`story.test.mjs` and `flow.mjs`),
`2026-10-14-support-10-minute-minimax-cute-brand` (also those two paths), and
`2026-10-17-story-worker-a-rejected-pronunciation-proposal` (`story.mjs`).
`2026-10-16-align-story-writer-and-listener-guidance` separately includes
`story.test.mjs`. All currently show `status: open` and no owner. The
10-minute support ticket says PR #1499 was merged and its owner released an
obsolete claim for A01 lexicon integration; that is narrower than C09 guard
authorization. The owner's earlier five-ticket narrow release covered
`core/lint*`, `core/state*`, and shared `docs/videos/long-form/review.*`, not
these story worker paths. No other ticket scope was changed or force-claimed.

Exact risk: `advanceStory` in `story.mjs` initializes lexicon and can call
`relint`; `relint` writes `video.json`, `claims.md`, and `script.md` from the
six chapter files. `approveScript` writes `script.md` again. Existing
`pilotScriptReviewProblem` binds only two unrelated v2 pilots and expects
worker chapter files absent from this manual C09 project. `flow.mjs` calls
`advanceStory` before its shared TTS/media path. The C09 local project has
`category: explainer` for approved stats cards, whereas `composeStory` emits
`category: story`, so even a narration-only comparison would miss damage.

After normal narrow scope coordination, add a C09-only fail-closed check at
the **start** of `advanceStory`, before lexicon initialization or any write:
read the canonical approved `script.md`, `visual-plan.json`, and `video.json`
SHA-256 values, report a precise missing/drifted file if any, and return a
`STOPPED_HOLD` for the frozen manual project even when all hashes match.
That non-undefined return prevents the shared `flow.mjs` stages from running.
Do not try to make C09 pass the v2 six-chapter receipt logic, and do not
silently regenerate a new 77-scene project. A future worker resumption would
need a separate reviewed handoff proving chapter-source parity, postproduction
card-copy parity, owner approval, and C09 budget/voice/account readiness.

Focused tests should invoke the story step with matching, drifted, and missing
C09 files and assert: exact HOLD reason; original bytes preserved; no lexicon,
chapter, script or project write; no paid/provider calls. A non-C09 story
fixture must retain its previous behavior. Add host deployment/readback before
changing the paused series. This paragraph is a reviewable plan only; no
claimed worker file was edited.
