---
id: 2026-10-23-prepare-held-c-series-ledger-compatibility
title: Prepare held C-series ledger compatibility before 0138
status: in-progress
priority: P1
area: api
owner: codex-c-series-integration
claimed_at: 2026-10-23T16:53:35Z
created_at: 2026-10-23T16:53:29Z
completed_at:
branch: codex/c-series-budget-0138-compat-20261024
depends_on:
  - 2026-10-23-consolidate-c-series-budget-holds-and
scope:
  - apps/api/app/migration_guard.py
  - apps/api/app/schema.py
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/recovery.py
  - apps/api/app/video_budget/service.py
  - apps/api/tests/test_migration_guard.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_video_pilot_budget.py
---

# Prepare held C-series ledger compatibility before 0138

## Why

Seven owner-approved C-series pilots have USD 25 ceilings, but the current 0137
database has no per-film accounts. Four of them (C03–C06) made paid requests
before ledger protection and their provider charges are not yet reconciled.
Production migrates the database before switching application images. A later
0138 migration must therefore be readable by the previous 0137 app during a
rollback, without opening any new paid route. The current app rejects unknown
0138 revisions and hides even read-only budget summaries for these films.

## Definition of done

- [x] The 0137 compatibility image accepts only the reviewed 0138 schema and
      exact seven account limits, including four durable historical holds.
- [x] C-series budget summaries are readable once their exact accounts exist,
      and reconciliation output states the admission hold explicitly, while
      every `story-everyday-*` paid reservation remains held.
- [x] The existing 0132→0133 rollback exception and nine-account contract stay intact.
- [x] Focused schema, migration-guard and budget tests pass; 0138 is not yet
      migrated, activated or deployed in this phase.

## Steps

- [x] Add explicit 0137→0138 rollback classification and exact readback.
- [x] Add read-only known C-series summary without lifting spend holds.
- [x] Test tampered revisions, accounts, operations and schema constraints.

## How to verify

From `apps/api`: `uv run --frozen pytest tests/test_schema.py tests/test_migration_guard.py tests/test_video_pilot_budget.py -q` (43 passed, 2 PostgreSQL-only skips); `uv run --frozen ruff check` on edited Python files (PASS). From repository root: `npm run check:tasks` (PASS with unrelated existing warnings); `git diff --check` (PASS).

## Notes

The broad P1 reconciliation ticket overlaps another active task on `tools/video/tts`,
so this ticket owns only the compatibility files above. Do not force a claim or
change the old worker route here. The 0138 migration and live deployment require
separate guarded stages. Historical C03–C06 billing and `hostinger2` access remain
unverified; do not infer authorization to spend from a numeric remaining balance.
The 0138 readback requires each original `pre-ledger-history` hold and exact
immutable identity, while allowing later evidence-bound settlement or release.
Additional operation rows are permitted because legitimate later production
activity must remain readable on app rollback; 0137 still blocks all C-series
paid admissions. A real PostgreSQL/Compose 0138 upgrade and rollback test is
required in the subsequent migration stage; `/ready` alone does not prove it.
