---
id: 2026-09-07-gemini-catalog-review
title: Gemini catalog review and 100-item expansion
status: review
priority: P1
area: api
owner: codex-gemini-catalog
claimed_at: 2026-09-07T03:41:45Z
created_at: 2026-09-07T01:22:51Z
completed_at:
branch: codex/catalog-review-missing-assessments
depends_on: []
scope:
  - apps/api/app/catalog_review
  - apps/api/tests/test_catalog_review.py
  - apps/api/tests/test_catalog_review_integration.py
  - apps/api/tests/test_catalog_review_provider.py
  - apps/api/tests/test_catalog_review_jobs.py
  - apps/web/components/admin-catalog-review-panel.tsx
  - apps/web/components/admin-catalog-review-panel.test.tsx
  - apps/web/messages/en/catalogReview.json
  - apps/web/messages/ja/catalogReview.json
  - apps/web/messages/ko/catalogReview.json
  - apps/web/messages/zh-CN/catalogReview.json
  - apps/web/messages/zh-TW/catalogReview.json
  - docs/catalog-review.md
---

# Gemini catalog review and 100-item expansion

## Why

The user has a working backend Gemini key and requests review of the entire pending
catalog, followed by 100 new candidates (40 hotspots, 20 dishes, 40 merchants) and
review before publication. There is currently no catalog assessment HTTP workflow.

## Definition of done

- [x] Administrator can snapshot all pending catalog rows and obtain persisted Gemini assessments.
- [x] Completed assessment unlocks bounded discovery of 100 candidates, with deduplication and review.
- [x] Approval requires independent trusted evidence and existing verified durable POI identity.
- [x] Per-call budgets, idempotency, stale-row checks, resumability and audit are enforced.
- [x] Seed reruns preserve reviewer decisions and corrected location evidence.
- [ ] API, frontend, migration and CI checks pass; production execution is reported separately.

## Steps

- [x] Backend persisted jobs, evidence, Gemini adapters and APIs.
- [x] Five-locale administration and tests.
- [x] Seed ownership regression guards.
- [x] Validate PR #315, merge after authorization, and deploy over SSH with migration 0054.
- [x] Fix live batch reliability and safe diagnostics, pass CI, merge and deploy the verified fix.
- [ ] Reject omitted model assessments and safely resume only legacy synthetic placeholders.
- [ ] Resume only failed/unprocessed rows and apply eligible evidence-backed decisions.
- [ ] Discover and independently review the requested 100 candidates; report actual public totals.

## How to verify

Run API pytest/ruff/mypy, web lint/i18n/typecheck/Vitest/build, tools/task checks,
PostgreSQL migration and full-stack CI. After deployment: review pending snapshot,
check evidence and apply eligible decisions, discover 40/20/40, review and confirm
actual database/publication outcomes; do not equate pending import with publication.

## Notes

Base 46eeb84; isolated worktree outside shared dirty checkout. Prior live audit left
101 hotspots and 206 merchants pending. Gemini test succeeded but does not prove
response content quality. Never clear backlog by approving missing POI/source data.
Gemini calls must consume the existing configured daily Gemini budget; no member
credits are charged. Missing Korean Naver identities remain explicit review gaps.

Implementation validation is in progress. No new production Gemini review, candidate
import or batch publication has been run for this feature. Live pending counts above
are the previous manual-audit snapshot, not a promise that current production is unchanged.
Migration is renumbered 0054 because main now owns 0053_ui_text_overrides.

Rebased onto 4839412. Local Ruff and mypy (220 modules), five-locale parity,
web typecheck and focused administration tests (23) pass. Provider/evidence tests
(73), imports/worker tests (46), seed guards and task tooling pass. A real public
Wikidata Q615183 fetch succeeded with canonical evidence and no Gemini request.
The full Windows API rerun excludes the existing UnixStreamServer deployment test;
PostgreSQL integration runs in Linux CI. Full local Vitest was stopped after failing
to finish under machine load; no full-suite success is claimed. C: has about 1.9 GB
free, so production/container builds and full web/stack validation run in CI.

Merge/deployment and the live pending-review/100-candidate import are still required.
This change deliberately does not auto-publish generated coordinates or map IDs.

PR: https://github.com/x812033727/travel_scanner/pull/315. Rebased Windows API
result: 1402 passed, 73 skipped (plus the Unix-only module excluded as above).
Final cross-review added hotspot translated names/aliases to the immutable snapshot;
concurrent localization edits now invalidate the old approval. Its focused regression
set is 79 passed. Initial CI already passed fresh PostgreSQL migration; final-head
complete CI results must still be verified before merge.

Head 83e16bc completed all CI checks: API 1491 passed/1 skipped, Web 617 tests,
94 browser UI tests and 4 full-stack journeys; containers/builds passed. Main then
advanced to 8553097 (UI text loader), so this branch was rebased again and the new
catalogReview namespace added to both new editable-namespace registries. Final
rebased-head CI must pass too; the original result is not claimed for a new SHA.

## Current production follow-up (2026-09-07)

PR #315 merged as a817003 after all checks passed; main CI 34076706328 also passed.
User explicitly authorized SSH deployment, then authorized independently merging
necessary follow-up fixes once verified. No new merge authorization is needed for
this catalog task, but exact-head green CI and post-deployment checks remain required.

SSH deployment completed: backup verified, 0054 migration succeeded, API/Web/worker
healthy, authenticated catalog page reads the configured Gemini model and 307 pending
rows. See docs/catalog-review.md for operational evidence and the private archive
build requirement: the original checkout source permissions were not relaxed after
safety review rejected a broad chmod. Do not directly rebuild that checkout.

Live run 1eb2d91f-9d7c-49a4-86fd-6c8aa8a97456 finished partial: 187 needs_review,
120 errors, 17 calls, no approvals/publication, no new-100 discovery yet. Production
output limit 8000 tokens/timeout45s; existing ValueError-only logs do not identify the
exact provider cause. This branch adds smaller batches, bounded model inputs,
allowlisted error diagnostics, a failure circuit breaker, thinking-token visibility
and explicit resume preserving prior assessments. Do not reset usage or weaken
publication/source/map gates. Remaining original data task is not complete.

Final follow-up validation: Windows API 1442 passed / 73 skipped (the existing
Unix-only deployment module excluded); Ruff and mypy (221 modules) pass. Web lint,
typecheck, five-locale parity, 35 focused panel tests, task checks and 27 tooling
tests pass. Full single-worker Vitest reports all 117 files / 655 tests passed but
exits with code 1 locally, so clean full-suite/build/PostgreSQL/container/browser
validation is still required in Linux CI. Independent cross-review fixed an
incomplete five-language context approval risk: truncated/omitted review context
now forces needs_review even if Gemini proposes approval or rejection. Unknown
local exceptions remain neutral rather than being mislabeled invalid model JSON.

PR #317 merged after both complete CI runs passed; main CI also passed. CI reports
1529 API tests passed/1 skipped, 655 Web tests, 96 browser UI tests and 4 full-stack
journeys, with production builds, containers and PostgreSQL migrations passing.
Follow-up verification found legacy synthetic omitted-candidate assessments counted
as completed. This isolated follow-up rejects missing response IDs and enables
explicit same-run retries of only strict legacy placeholders while preserving real
assessments and accumulated usage. New discovery remains blocked until genuine
snapshot assessment is complete. Production outcomes are recorded in the private
deployment artifact; the original data expansion/publication task is not complete.

Missing-assessment fix local verification: 1476 Windows API tests passed/78 skipped
(PostgreSQL tests await Linux CI; the existing Unix-only module remains excluded),
Ruff, mypy 221 modules, Web typecheck/i18n and 37 panel tests pass. Independent
review confirms edited/approved/deleted legacy snapshots are skipped before any
paid retry. Five new PostgreSQL scenarios cover exact resume, discovery/apply
gates, original budgets/global concurrency and obsolete snapshots. Final head CI
must pass before this follow-up is merged or deployed.

Production run `1eb2d91f-9d7c-49a4-86fd-6c8aa8a97456` was explicitly resumed after
the missing-assessment fix and completed all 307 assessments: 101 hotspots and 206
merchants. All 307 remain `needs_review`; none passes the independent publication
gates. The overlapping gaps are 307 unverified map matches, 215 missing/unverified
durable coordinates, 214 missing verified source citations, 179 missing exact map
identities, 147 low-confidence assessments and 32 missing direct merchant sources.

The first bounded discovery run `2cb84b1a-f180-4b6b-9bbf-4b167e954259` created zero
rows and stopped safely after nine calls. Its production prompt included 33
destinations and 3,758 cross-catalog avoid values (about 77k JSON characters), causing
one truncated response and three consecutive merchant timeouts. This follow-up rotates
four destinations per request, scopes model-visible duplicate hints to the requested
kind/destinations, caps them at 8,000 characters, and preserves global database-level
deduplication. The failed run must not be blindly resumed until this fix is deployed.

After the bounded-prompt deployment, the same run completed partial with zero new
rows after 19 run calls. A separately budgeted production diagnostic proved why:
the JSON-oriented discovery response contained one plausible draft but zero Google
Search grounding chunks, so the strict source gate correctly discarded it. The same
model returned two chunks and three attributed supports when explicitly asked for a
short prose search result. This follow-up therefore separates discovery into a
grounded prose search and a second JSON structuring call that may copy only the
trusted publisher URLs resolved from that search. It also records aggregate discard
diagnostics without persisting raw provider output or weakening trusted-source,
dedupe, map or publication gates. Focused catalog tests pass (226, 18 skipped), as
do Ruff and mypy for the catalog package. CI, merge, deployment and a same-run resume
are still required before any new candidate count can be claimed.
