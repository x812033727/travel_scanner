---
id: 2026-09-07-gemini-catalog-review
title: Gemini catalog review and 100-item expansion
status: review
priority: P1
area: api
owner: codex-gemini-catalog
claimed_at: 2026-09-07T01:22:51Z
created_at: 2026-09-07T01:22:51Z
completed_at:
branch: codex/gemini-catalog-review
depends_on: []
scope:
  - apps/api/app/catalog_review
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/i18n.py
  - apps/api/app/worker.py
  - apps/api/app/config.py
  - apps/api/app/cli.py
  - apps/api/app/hotspots/service.py
  - apps/api/app/foods/service.py
  - apps/api/app/foods/merchant_service.py
  - apps/api/migrations/versions/0054_catalog_review.py
  - apps/api/tests/test_catalog_review.py
  - apps/api/tests/test_catalog_review_integration.py
  - apps/api/tests/test_catalog_review_provider.py
  - apps/api/tests/test_catalog_review_jobs.py
  - apps/api/tests/test_catalog_review_imports.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_hotspot_seed_ownership.py
  - apps/api/tests/test_hotspot_seed_reconciliation.py
  - apps/api/tests/test_food_seed_ownership.py
  - apps/api/tests/test_merchant_seed_ownership.py
  - apps/web/app/[locale]/admin/catalog-review
  - apps/web/components/admin-catalog-review-panel.tsx
  - apps/web/components/admin-catalog-review-panel.test.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/messages/en/catalogReview.json
  - apps/web/messages/ja/catalogReview.json
  - apps/web/messages/ko/catalogReview.json
  - apps/web/messages/zh-CN/catalogReview.json
  - apps/web/messages/zh-TW/catalogReview.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/i18n
  - apps/web/vitest.setup.tsx
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
- [ ] Validate and open PR; deployment and live run remain explicitly recorded.

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
