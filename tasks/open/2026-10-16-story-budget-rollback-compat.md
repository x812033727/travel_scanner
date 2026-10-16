---
id: 2026-10-16-story-budget-rollback-compat
title: Stage rollback compatibility before USD 5 story migration
status: in-progress
priority: P1
area: api
owner: codex-gpt6-story-budget-compat
claimed_at: 2026-10-16T01:08:45Z
created_at: 2026-10-16T01:08:20Z
completed_at:
branch: codex/story-budget-rollback-compat-20261016
depends_on: []
scope:
  - apps/api/app/schema.py
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_video_pilot_budget.py
---

# Stage rollback compatibility before USD 5 story migration

## Why

The planned 0133 migration lowers B18 v2 from USD 25 to USD 5 and seeds five more
accounts. Production runs the migration before switching the API; a failed release
rolls back application code without downgrading the database. The currently deployed
API rejects B18 v2 at USD 5 and rejects revision 0133 at `/ready`, which would make
the rollback unusable. This compatibility release must deploy before 0133.

## Definition of done

- [x] The 0132 API can serve `/ready` against exactly reviewed revision 0133.
- [x] Existing B18 v2 ledger/status and reconciliation work at both stored limits.
- [x] No fresh B18 v2 paid dispatch while the stored limit remains USD 25.

## Steps

- [x] Add exact-revision compatibility and tests.
- [x] Add B18 v2 read/settlement compatibility, paid gate and tests.
- [ ] Run focused API checks and CI; deploy this release before 0133.

## How to verify

`cd apps/api && uv run ruff check app/schema.py app/video_budget tests/test_schema.py tests/test_video_pilot_budget.py && uv run pytest tests/test_schema.py tests/test_video_pilot_budget.py -q`; then verify `/ready` and pilot budget status after the compatibility deployment, before 0133.

## Notes

The prior USD 25 task is still in-progress under an old owner from 2026-10-15,
although its PR was merged. Its broad scope overlaps this exact repair, so the
claim used `--force`; this work touches only the listed files and is isolated in
its own branch. Do not deploy 0133 in the same release as this compatibility code.

2026-10-16 local: 20 focused API tests passed, 2 PostgreSQL-only tests skipped;
targeted mypy and ruff passed. CI and production deployment are pending. The
follow-on migration remains in a separate draft PR and must not ship first.
