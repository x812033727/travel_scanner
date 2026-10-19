---
id: 2026-10-19-a01-0133-story-budget-migration
title: Isolate reviewed 0133 story budget migration
status: review
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

- [x] A draft PR from main contains the exact transferred migration and its
  test, with no #1510 implementation or other production-code changes.
- [x] Alembic has one head, 0133 follows 0132, focused checks and PostgreSQL CI
  pass, and the release dependency on the 0132 compatibility image is explicit.
- [x] Independent migration review is recorded before this draft is considered
  for a separately authorized merge or deployment.

## Steps

- [x] Confirm #1510 is a draft at its exact remote head, release only these
  two claims there, and preserve its other code and task scope.
- [x] Copy the two files byte-for-byte to this current-main branch.
- [x] Run focused migration, schema, SQL dialect, Ruff, mypy, and task checks.
- [x] Open draft PR #1585 with `no-auto-merge` and inspect PostgreSQL CI.

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
PostgreSQL upgrade case was left to CI, which provisions PostgreSQL and sets
`RUN_INTEGRATION_TESTS=1` in the API test shards.

Draft PR #1585 at `b01ca052991e74f7307c2007aaf981806b7c6858` completed
22/22 CI checks successfully on 2026-10-19, including all four PostgreSQL API
test shards, `api-checks`, `containers`, and `full-stack-smoke`. The PR remains
draft with `no-auto-merge`; independent migration review and explicit owner
authorization remain separate gates. No merge, deployment, or paid work ran.

Independent migration review of the unchanged migration and PostgreSQL test at
PR head `6f2e2e1adeedf402c4e0cbff2a232f8107f922f4` found no blocking
findings. It verified the 0132 down revision, widened budget constraint,
conditional B18 v2 USD 25-to-5 adjustment, five separate USD 5 follow-on
accounts, preservation of existing operation rows, and downgrade refusal.
Before any separately authorized production deployment, preflight must prove
the five new accounts are absent or already exactly USD 5 with reviewed
operations; `ON CONFLICT DO NOTHING` would otherwise preserve a mismatched
existing account. After migration, read back the exact nine account limits,
constraint, Alembic head, and rollback readiness. The 0132 compatibility
image's live state and #1510's duplicate 0133 must also be reconciled.
