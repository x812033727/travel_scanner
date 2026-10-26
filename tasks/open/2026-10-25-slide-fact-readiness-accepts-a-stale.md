---
id: 2026-10-25-slide-fact-readiness-accepts-a-stale
title: Slide fact readiness accepts a stale REVISE report
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-25T19:57:36Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa/facts.mjs
  - tools/video/core/state.mjs
---

# Slide fact readiness accepts a stale REVISE report

## Why

During PR1856 the current slide script changed from 112 to 105 lines while verify-1.md still described the prior source and explicitly requested a claims correction (REVISE). Status nevertheless showed fact-checked because core/state only checks that verify-1.md exists; the QA facts item only looks for still-cited NOT FOUND rows. Neither represents acceptance of the current script/claims revision.

## Definition of done

- [ ] Slide readiness distinguishes a historical or unresolved review from an accepted review covering the current spoken claims and required metadata.
- [ ] A changed spoken assertion cannot inherit checked status merely because verify-1.md exists or there are no NOT FOUND rows.
- [ ] Legitimate retained historical reports and explicitly verified corrections remain usable without deleting evidence.

## Steps

- [ ] Claim only after branch/worktree/remote/PR collision checks; inspect current review formats and existing source-bound story review handling.
- [ ] Define and validate a current accepted fact-review binding without weakening existing NOT FOUND citation checks.
- [ ] Add meaningful stale-after-rewrite and unresolved-REVISE regressions plus current accepted-review coverage.

## How to verify

Relevant native state/QA tests and docs-video suite. Reproduce current-source change with a historical hash-bound REVISE report and verify status cannot present it as accepted current facts. Confirm unchanged accepted current evidence remains valid, and all historical reports are preserved.

## Notes

Observed 2026-10-25 during claude-formal-verification-255 production. Initial source2b3db9fe/claimse0de07ac/verify1 REVISE was retained; R1a77c48e4/claims134e8e88 required genuine verify2 PASS. The coordinator deliberately waited for that independent PASS before paid narration. No shared tool code changed here; this is an unclaimed follow-up, not a blocker or an auto-approval workaround for the finished manual review.
