---
id: 2026-09-09-review-evidence-archive
title: Archive completed catalog and hotel review evidence
status: in-progress
priority: P2
area: docs
owner: codex-review-archive
claimed_at: 2026-09-09T06:23:11Z
created_at: 2026-09-09T06:23:11Z
completed_at:
branch: codex/review-evidence-archive-20260909
depends_on: []
scope:
  - docs/review-evidence-archive-20260909.md
  - docs/hotel-review-all-20260908
  - docs/hotel-review-followup-20260909
  - docs/hotel-review-remaining-20260909
  - docs/hotel-review-redirects-20260909
  - docs/hotel-review-platforms-20260909
  - docs/hotel-review-evidence-20260909
  - docs/catalog-review-2026-09-08.md
  - docs/catalog-review-followup-2026-09-08.md
  - docs/hotspot-review-2026-09-08.md
  - docs/catalog-content-reviews/2026-09-09-followup-result.md
  - docs/catalog-content-reviews/2026-09-09-followup.json
  - ops/hotel_review_all_20260908.py
  - ops/hotel_review_followup_20260909.py
  - ops/hotel_review_remaining_20260909.py
  - ops/hotel_review_redirects_20260909.py
  - ops/hotel_review_platforms_20260909.py
  - ops/hotel_review_evidence_20260909.py
  - ops/catalog_review_20260908.py
  - ops/catalog_review_20260908_decisions.json
  - ops/catalog_review_20260908_styles.json
  - ops/catalog_review_followup_20260908.json
  - ops/catalog_review_followup_20260908.py
  - ops/hotspot_review_20260908.json
  - ops/hotspot_review_20260908.py
  - apps/api/tests/test_catalog_content_review_followup.py
---

# Archive completed catalog and hotel review evidence

## Why

Three completed, committed review batches still exist only in local worktrees.
Their historical decisions and verification evidence need a traceable repository
handoff, without implying a new review, production import or application release.

## Definition of done

- [ ] Preserve the three completed source groups and their dates, hashes, qualified failures and remaining work.
- [ ] Exclude the fourth still-active, dirty resolution worktree and avoid importing unrelated source changes.
- [ ] Complete a public-repository secret/privacy/scope review before any upload.
- [ ] Pass offline artifact tests, task checks and current-head CI, then create a clearly scoped evidence PR.

## Steps

- [ ] Bring over only the ten committed archive changes from the three clean source branches.
- [ ] Add an index distinguishing historical assessed/applied/approved/published outcomes.
- [ ] Validate safe offline readers and tests; never run the archived production operators.

## How to verify

Run artifact/JSON checks and the existing offline verifier/operator guard tests
against isolated API settings (no usable database, Redis, provider or production
credentials). Run the follow-up content test with related catalog tests, task
tool checks, and diff checks. Full CI is required for the final PR head.

## Notes

Initial main: a899437aaf2f60c7affe2e944d49d62216537c90. Preserve source worktrees.
Sources: hotel review through 2b307423 (six commits), catalog review through
a24472d0 (three commits), content follow-up 262c76ee (one commit). These are
already-applied historical data actions, not work to execute again. No deployment,
service activation, paid request, bulk approval, production SQL or source refresh
is authorized by this archival step. The content-review-resolution worktree is
still active and dirty and is intentionally excluded.
