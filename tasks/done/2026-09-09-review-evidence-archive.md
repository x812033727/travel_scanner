---
id: 2026-09-09-review-evidence-archive
title: Archive completed catalog and hotel review evidence
status: done
priority: P2
area: docs
owner: codex-review-archive
claimed_at: 2026-09-09T06:23:11Z
created_at: 2026-09-09T06:23:11Z
completed_at: 2026-09-11T15:54:26Z
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
- [ ] Create a clearly scoped evidence PR and pass offline artifact tests, task checks and current-head CI.

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

## Initial PR source integration

Normally integrated final main 98f8067b3664a956e44d0b6e9f372b27a22775e6 after
the authorized #343 and #335 merges. Only the generated board conflicted.
The same root owner also closes those two narrow integration tasks here using
their actual verified-merge evidence; those metadata records are separate from
the unchanged original review artifacts. No application behavior, CI configuration
or old review evidence is edited by this archival PR. At this checkpoint, the
new PR remained unmerged pending the user's separate review of this large,
historical evidence handoff.

## Authorized merge preparation after #365

The user subsequently authorized merging #365 and #376, but not #377. The first
PR was guard-merged as 3d88373caf5c6aab99399867112ed9944b30684c at
2026-09-09T07:34:43Z after all 12 checks passed. Normally integrated that exact
main into this branch; only the generated board conflicted and it was regenerated.
The old #376 head 7b88b105 passed 12/12 checks, including one disclosed same-head
Web rerun after an unchanged Escape-dialog test failed; this is not a test fix.
The updated head requires fresh CI before the authorized guarded merge.

An independent preflight again confirmed all 213 hotel, 15 catalog and 4 content
source blobs unchanged, no runtime/CI/package/Compose changes, and no material
from the still-active fourth worktree. The original #365 integration owner
explicitly handed only its completion-record scope to root, so this PR also
closes that narrow task without closing its two operational follow-ups.

Do not execute archived operators, contact production, deploy, alter provider
configuration, or merge/fix #377. Preserve historical qualified failures and
no-replay boundaries. Verify the final head and merged-main checks separately.

## Closed after merge (site owner's instruction, not the holder)

PR #376 merged on 2026-09-09 as squash `2bd7c51`, whose tree is identical to the PR head
`4542d97`, so everything on the branch reached main; the branch has since been deleted.
Every check on that head passed: `api`, `web`, `containers`, `full-stack-smoke`,
`discovery-browser` and `planner-browser`. The task stayed in `review` and kept holding its
scope, which blocked later claims, so claude-opus-5 moved it to done on 2026-09-11.

The unticked item, the evidence PR with passing current-head CI, is PR #376 itself.

If the holder still has follow-up work that never reached the branch, file a new task rather
than reopening this one.
