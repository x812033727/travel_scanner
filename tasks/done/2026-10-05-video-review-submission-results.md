---
id: 2026-10-05-video-review-submission-results
title: Check review submission results before advancing video gates
status: done
priority: P2
area: tools
owner: codex-news-video-stall-fixes
claimed_at: 2026-10-05T10:48:13Z
created_at: 2026-10-05T10:19:14Z
completed_at: 2026-10-05T10:48:54Z
branch: codex/news-video-stall-fixes-20261005
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Check review submission results before advancing video gates

## Why

In flow.mjs:1385-1390, the publish-confirmation branch ignores the return code
from review-push and reports that confirmation was sent even after a rejected
submission. With no persisted review, later units can submit the same package
again. Other review gates also treat every nonzero result as later(), allowing
a deterministic input or storage failure to be retried indefinitely.

This is a source-confirmed defect found during the 2026-10-05 production
diagnosis, not evidence that it caused today's live outage. Today's observed
writer rejection has a separate format/policy-hold task.

## Definition of done

- [x] Report a successful review submission only after the command succeeds
      and the matching persisted review is reconciled.
- [x] Separate temporary transport failures, uncertain outcomes, owner gates,
      and settled validation failures. Preserve receipts for uncertain work.
- [x] A deterministic failure is visible on its project and cannot starve
      other eligible projects or cause repeated identical review submissions.
- [x] Existing success, rejected-review and hash-bound approval behavior stays
      intact without publishing or granting a new approval.

## Steps

- [x] Coordinate with active owners of flow.mjs and policy-hold/fairness tasks
      before claiming or changing this shared scope.
- [x] Audit review-push result handling in publish, final, look, storyboard and
      languages branches, then implement consistent outcome handling.
- [x] Independently review and run relevant offline regression tests.

## How to verify

Use stubbed review submission results and the real Automation. Return a settled
lint refusal and verify no success report or duplicate submission, then permit
a second project to advance. Cover transport loss with a remotely persisted
review, success, and owner rejection. Run affected automation tests and the
complete tools suite. Do not call live review or model endpoints for testing.

## Notes

- Observed in checkout/live SHA 7318edc7fe24ed1a0cd2495f6e5356d06e16c05b.
- flow.mjs:2574 defers every nonzero final-gate submission; the languages branch
  at line 2122 already distinguishes lint failures. Use current source rather
  than assuming these line numbers remain stable.
- Initial diagnosis made no live failure attribution. The owner subsequently
  authorized repair with "修"; the implementation was coordinated within the
  format/policy-hold task's flow scope. That claim is completed before this
  overlapping task is claimed and closed, rather than force taking a second lock.
- Publish now checks the actual review-push exit and reports success only after
  the official submission command succeeds. That command reconciles a saved
  review; the next unit reads the hash-bound review before advancing. A lost
  reply with a persisted review is recovered through the existing decision path.
- Shared handling parks final/look/storyboard/publish EXIT.lint refusals locally.
  Existing languages handling already parks permanent submission failures;
  service/transport/owner interruptions retain their existing deferred handling.
  No gate approval, source identity, media or YouTube publication was fabricated.
- Regression covers real review HTTP 413/422/401/429/503 responses, no false
  publish-success report, one settled rejected submission and a second eligible
  project advancing; all three other permanent gates are covered. Full
  automation passed 102 cases with two later focused cases separately passing;
  independent repair-pattern tests passed 28 cases and duration receipt checks
  passed. The PR records complete branch checks separately.
- No production submission, paid generation, upload or publication occurred.
