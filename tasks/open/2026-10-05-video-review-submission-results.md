---
id: 2026-10-05-video-review-submission-results
title: Check review submission results before advancing video gates
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T10:19:14Z
completed_at:
branch:
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

- [ ] Report a successful review submission only after the command succeeds
      and the matching persisted review is reconciled.
- [ ] Separate temporary transport failures, uncertain outcomes, owner gates,
      and settled validation failures. Preserve receipts for uncertain work.
- [ ] A deterministic failure is visible on its project and cannot starve
      other eligible projects or cause repeated identical review submissions.
- [ ] Existing success, rejected-review and hash-bound approval behavior stays
      intact without publishing or granting a new approval.

## Steps

- [ ] Coordinate with active owners of flow.mjs and policy-hold/fairness tasks
      before claiming or changing this shared scope.
- [ ] Audit review-push result handling in publish, final, look, storyboard and
      languages branches, then implement consistent outcome handling.
- [ ] Independently review and run relevant offline regression tests.

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
- No implementation, production action or live failure attribution occurred.
