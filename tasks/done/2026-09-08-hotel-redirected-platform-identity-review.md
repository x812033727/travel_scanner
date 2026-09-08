---
id: 2026-09-08-hotel-redirected-platform-identity-review
title: Hotel redirected platform identity review
status: done
priority: P1
area: ops
owner: codex-hotel-redirect-review
claimed_at: 2026-09-08T23:08:06Z
created_at: 2026-09-08T23:07:36Z
completed_at: 2026-09-08T23:32:22Z
branch: codex/hotel-redirect-review-20260909
depends_on: []
scope:
  - docs/hotel-review-redirects-20260909
  - ops/hotel_review_redirects_20260909.py
---

# Hotel redirected platform identity review

## Why

Continue the requested hotel review with fresh built-in-browser evidence. Three
previously failed empty Agoda slots now have directly observed localized landing
URLs. This is a new bounded batch, not a rewrite of the previous 27 receipts.

## Definition of done

- [x] Review exactly the three newly evidenced Busan Agoda identities through the
  normal URL-safety and admin edit/review services; retain any guard failure as a hold.
- [x] Preserve all 60 products, the 316 already approved rows, all out-of-scope
  options, configuration, provider quote state, prior receipts and historical audits.
- [x] Verify full-row results, normal audit pairing, replay and unchanged public catalog.

## Steps

- [x] Capture the new 420-row baseline and freshly reload all three actual IAB destinations.
- [x] Compile the exact UUID/URL manifest; verify pinned operator and offline guards.
- [x] Back up production; dry-run, normal review, read-only independent verification and replay.
- [x] Record actual approvals/holds and remaining unresolved items without claiming full publication.

## How to verify

Use the existing API Python runtime with PYTHONPATH=apps/api; run the new and
previous operator guard tests, scoped Ruff, new read-only SQL and three anonymous
six-city/five-locale public matrices. Preserve before/after/replay evidence in
docs/hotel-review-redirects-20260909. No deployment, provider API quota increase,
booking, affiliate clickout or quote activation is in scope.

## Notes

Fresh baseline: 2026-09-08 23:08:17.381350+00:00, semantic SHA256
14978ec20e1b05f7f5991194c9568f56bb6da93486c91105ebc5391dc4fad56d.
Counts: 40 approved / 20 pending products; 276 approved / 84 pending options.
All three parents remain pending; approving their independent booking identities
must not publish those hotels. Browser locale redirects are observations, not proof
that the server-side guard will accept the final URL.

Result: all three exact final URLs passed the unchanged normal guard; 3 approvals,
0 holds, versions 1 to 3, normal edit/review audits 3 each. Replay returned the same
receipts without writes. SQL protected all 417 other full rows, 316 prior approved
rows, 384 old receipts and 9,330 historical audits. No parents/configs/quotes changed.
All 90 anonymous public checks retain the same 40 products / 192 options and body
fingerprints. Remaining 20 products / 81 options are explicitly carried forward
with prior evidence dates in the new remaining-items.json, not claimed re-reviewed.
172 offline tests and complete local evidence verification passed. This narrow data
batch is complete and live; the broader hotel-readiness task remains open.
