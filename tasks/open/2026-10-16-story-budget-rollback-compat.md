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
  - apps/api/app/admin/operations_service.py
  - apps/api/app/database_admin/service.py
  - apps/api/app/schema.py
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/tests/test_admin_operations.py
  - apps/api/tests/test_database_admin.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_video_story_policy.py
  - tasks/open/2026-10-16-story-budget-rollback-compat.md
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
- [x] Five later story slugs are already fail-closed in the 0132 application; status skips absent follow-on accounts only while the database is exactly at 0132, and exposes each USD 5 account after 0133.
- [x] Rollback health displays use the same exact schema compatibility as `/ready`.

## Steps

- [x] Add exact-revision compatibility and tests.
- [x] Add B18 v2 read/settlement compatibility, paid gate and tests.
- [x] Add five follow-on fail-closed routing, missing-account status handling, and rollback dashboard tests.
- [ ] Run focused API checks and CI; deploy this release before 0133.

## How to verify

`cd apps/api && uv run ruff check app/admin/operations_service.py app/database_admin/service.py app/schema.py app/video_budget app/video_media/admin_api.py tests/test_admin_operations.py tests/test_database_admin.py tests/test_schema.py tests/test_video_media_api.py tests/test_video_pilot_budget.py tests/test_video_story_policy.py && uv run pytest tests/test_admin_operations.py tests/test_database_admin.py tests/test_schema.py tests/test_video_media_api.py tests/test_video_pilot_budget.py tests/test_video_story_policy.py -q`; then verify `/ready` and pilot budget status after the compatibility deployment, before 0133.

## Notes

The prior USD 25 task is still in-progress under an old owner from 2026-10-15,
although its PR was merged. Its broad scope overlaps this exact repair, so the
claim used `--force`; this work touches only the listed files and is isolated in
its own branch. Do not deploy 0133 in the same release as this compatibility code.

2026-10-16 local: 20 focused API tests passed, 2 PostgreSQL-only tests skipped;
targeted mypy and ruff passed. CI and production deployment are pending. The
follow-on migration remains in a separate draft PR and must not ship first.

Independent review found that the first candidate recognized only the original four pilot slugs. A rollback after follow-on jobs were queued could therefore bypass their USD 5 reservations. The compatibility application now recognizes the exact five follow-on slugs even before 0133 creates their accounts: paid calls fail closed; media status skips genuinely absent rows only when the database revision is still exactly 0132. After 0133, a missing follow-on row or a present row with the wrong limit remains a 503 error. The admin overview and database revision view now apply the same exact 0133-on-0132 acceptance as `/ready`. B18 v2 can settle and release old operations while its stored row is still USD 25, but new paid reservations wait for USD 5. This is code and test preparation only; no deployment or paid work has started.

2026-10-16 expanded local check: the initial focused API suite had 95 passed, 3 skipped. After independent review tightened the status omission to exact database revision 0132, the media API suite passed again with 12 tests. Targeted ruff, `npm run check:tasks`, and `git diff --check` passed. Full app/tests mypy and PR CI remain pending at this note.

After rebase onto main `0b6844a4a`, the focused suite exposed one test fixture missing the `alembic_version` table that the new status guard reads; its other 95 tests passed and 3 skipped. The SQLite fixture now explicitly represents 0132, and that status regression passed in isolation. This is test setup only; paid routing remains fail-closed and the PR remains draft.
