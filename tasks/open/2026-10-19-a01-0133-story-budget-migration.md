---
id: 2026-10-19-a01-0133-story-budget-migration
title: Isolate reviewed 0133 story budget migration
status: in-progress
priority: P1
area: api
owner: codex-gpt6-a01-0133
claimed_at: 2026-10-19T04:21:50Z
created_at: 2026-10-19T04:21:42Z
completed_at:
branch: codex/a01-0133-budget-migration-20261019
depends_on: []
scope:
  - apps/api/migrations/versions/0133_story_followon_budget.py
  - apps/api/tests/test_migration_0133_story_followon_budget.py
  - tasks/open/2026-10-19-a01-0133-story-budget-migration.md
---

# Isolate reviewed 0133 story budget migration

## Why

The guarded A01 admission path needs revision 0133 before a later 0134 migration.
The only 0133 migration and its PostgreSQL test currently live inside draft
#1510, whose unrelated work is still in progress. Isolate these exact files so
their SQL and release order can be reviewed and tested independently. The owner
authorized transferring these two file claims on 2026-10-19. This task does
not authorize merging, deployment, or paid video work.

## Definition of done

- [ ] A draft PR from current main contains the exact reviewed migration and
  its test, with no #1510 implementation or other file changes.
- [ ] Alembic has one head, 0133 follows 0132, focused checks and PostgreSQL CI
  pass, and the release dependency on the 0132 compatibility image is explicit.

## Steps

- [x] Confirm #1510 is a draft at its exact remote head, release only these
  two claims there, and preserve its other code and task scope.
- [x] Copy the two files byte-for-byte to this current-main branch.
- [x] Run focused migration, schema, SQL dialect, Ruff, mypy, and task checks.
- [ ] Open a draft PR with `no-auto-merge`, then inspect PostgreSQL CI.

## How to verify

`cd apps/api && uv run alembic heads && uv run pytest
tests/test_migration_0133_story_followon_budget.py tests/test_schema.py
tests/test_migration_sql_dialect.py -q && uv run ruff check
migrations/versions/0133_story_followon_budget.py
tests/test_migration_0133_story_followon_budget.py && uv run mypy app && uv run
mypy tests`; from the root run `npm run check:tasks`. The real upgrade test uses
`RUN_INTEGRATION_TESTS=1` with PostgreSQL in CI or an available local instance.

## Notes

#1510 transferred the claims at `b850ae37ef1987a6e6926a073dcd4425ac5c89d5`.
The source file Git blobs are `ff509c86e289bd28468df8b2ad79615ea445f088`
and `1e63fb7d440faf5c483bd1f19dcca02df3f0e0ae`; this branch copied both
without editing them. The 0133 migration lowers only B18 v2's existing USD 25
account to USD 5 when it still has the old limit, seeds five independent USD 5
accounts, preserves operation rows, and refuses automatic downgrade. The 0132
compatibility image and host verifier must be live and read back before 0133 is
deployed; a merged migration PR alone is not permission to run it.

Local 2026-10-19: `alembic heads` returned exactly
`0132_video_pilot_budget (head)` before adding this file. Focused pytest:
11 passed, 1 PostgreSQL-only skipped. Targeted Ruff, `mypy app` (479 files),
`mypy tests` (403 files), and `npm run check:tasks` passed. This Windows host
has neither `pg_isready` nor Docker, so the actual
PostgreSQL upgrade case awaits CI, which provisions PostgreSQL and sets
`RUN_INTEGRATION_TESTS=1` in the API test shards.
