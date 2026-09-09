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

- [x] Preserve the three completed source groups and their dates, hashes, qualified failures and remaining work.
- [x] Exclude the fourth still-active, dirty resolution worktree and avoid importing unrelated source changes.
- [x] Complete a public-repository secret/privacy/scope review before any upload.
- [ ] Pass offline artifact tests, task checks and current-head CI, then create a clearly scoped evidence PR.

## Steps

- [x] Bring over only the ten committed archive changes from the three clean source branches.
- [x] Add an index distinguishing historical assessed/applied/approved/published outcomes.
- [x] Validate safe offline readers and tests; never run the archived production operators.

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

## Offline preparation checkpoint

- The repository is public. An independent, bounded inspection of the original
  214 hotel, 16 catalog and 5 content source paths found no specific credential,
  login, personal-account, private backup or binary-image content requiring
  redaction. This is not a blanket copyright or provider-usage authorization.
- Git blob comparison against each original source HEAD, excluding the generated
  board, confirmed all 213 hotel, 15 catalog and 4 content files are unchanged.
  Only generated board merges, this new integration task and the new index differ.
- Nine archived ops modules retain explicit apply/write capabilities. No automatic
  runtime, CI, tools or Compose invocation was added. The index forbids replay
  from merge/deployment and explicitly retains the qualified provider-config
  verification failure and unresolved publication gates.
- Six operator-guard modules and three verifier-test modules: **502 passed**,
  with two existing Python dependency deprecation warnings. The standalone content
  manifest test passed **11 tests**. A separate related API run of
  `test_catalog_content_review_followup.py`, `test_hotspot_guides.py` and
  `test_catalog_review_scope.py` passed **60 tests**, including those 11; counts
  are not additive. No standalone operator or strict verifier was executed.
- Tests used a task-local complete Python environment, this worktree's API import
  path, `RUN_INTEGRATION_TESTS=0`, and unusable database/Redis loopback endpoints
  on port 1. No production, provider or real database service was contacted.
- Full API Ruff and scoped Ruff over all nine ops modules and six evidence
  directories passed. Locked task-local npm dependencies were installed with
  scripts disabled; tool tests passed **27**, i18n passed five locales and
  25 namespaces, and task checks passed **214 files**. Existing unrelated
  stale-claim/scope warnings remain unchanged. Diff checks passed.
- Root will update to the final integration main before opening the evidence PR.
  New-head CI remains required. This checkpoint is not production revalidation,
  a new deployment, or approval to merge the newly created archival PR.
