---
id: 2026-10-24-stage-exact-c20-0139-rollback-compatibility
title: Stage exact C20 0139 rollback compatibility
status: blocked
priority: P1
area: api
owner: codex-c20-budget-compat
claimed_at: 2026-10-24T05:36:14Z
created_at: 2026-10-24T05:36:10Z
completed_at:
branch: codex/c20-budget-0139-compat-20261024
depends_on: []
scope:
  - apps/api/app/schema.py
  - apps/api/app/migration_guard.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_migration_guard.py
  - apps/api/tests/test_c20_budget_rollback_integration.py
  - .github/workflows/ci.yml
  - tasks/open/2026-10-24-stage-exact-c20-0139-rollback-compatibility.md
---

# Stage exact C20 0139 rollback compatibility

## Why

C20 Zippo short v8 has an approved USD 25 local-pilot ceiling, but no durable
per-film budget account. A later additive 0139 migration must run before a new
application image. If that image is rolled back to the current 0138 image, the
existing migrate service and `/ready` reject an unknown 0139 database. Stage
only an exact, read-verified rollback exception before any account migration.

## Definition of done

- [ ] The 0138 image accepts only the exact future C20 0139 revision after
      reading back 17 exact budget accounts, the four historical C03–C06 holds,
      and the C20 account ownership record.
- [ ] Real PostgreSQL and the production Compose migrate command prove a
      simulated additive 0139 database can be served by the 0138 image; malformed
      account, provenance, revision and unavailable database states are rejected.
- [ ] The application still refuses all C-series paid requests; no 0139
      production migration or paid activation is introduced.

## Steps

- [x] Verify current main, a clean and pushed C20 content branch, and no active
      task-board scope collision; normal claim succeeded without force.
- [x] Add exact 0139 classification and schema/readback checks.
- [x] Add unit and isolated PostgreSQL/Compose rollback tests and CI gate.
- [x] Run focused checks, push a draft no-auto-merge PR, and record handoff.

## How to verify

`cd apps/api && uv run pytest tests/test_schema.py tests/test_migration_guard.py
tests/test_c20_budget_rollback_integration.py -q`; in CI,
`RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_c20_budget_rollback_integration.py -q`
uses PostgreSQL. Also run `uv run ruff check` and `uv run mypy app tests`,
`npm run check:tasks`, and `git diff --check`.

## Notes

Main was `a8e97528072bdce0b726c151cee9c4e98431f56c` at claim time. C20
content PR #1808 was clean at `1b22d8dd6181106145883a2e3b5dca566638a33b`;
this work uses the existing sparse checkout on a new main-based branch and
does not edit that content PR. Old overlapping budget tickets dated 2026-10-16
and 2026-10-23 are open and unowned. Future exact revision:
`0139_c20_zippo_pilot_budget`; only account slug:
`story-everyday-zippo-c20-short-v8`; USD 25. The 0138 image remains a
preproduction paid hold for every `story-everyday-*` slug. Future migration
must match the source-bound test fixture before it can ship.

2026-10-24 local verification: focused schema/guard suite 14 passed, one
PostgreSQL integration skipped; no Docker command, PostgreSQL service or
`psql`/`pg_isready` is installed on this host. Full `ruff check .`, `mypy app
tests` (899 files), `npm run check:tasks`, and `git diff --check` passed after
expanding this same sparse checkout for CI/deploy sources and existing local
Python packages. `check:tasks` emitted existing stale/overlap warnings but
validated 2135 files. CI's PostgreSQL test is the actual rollback release
gate; do not describe the local skip as a pass. Synthetic future migration
source is pinned to SHA256
`209f225ca2c38b25d7e962cd0c6fd4e44f379daf953f3248128d2ba1e9a452a5`.
It does not exist in the release migration tree. The later migration must
match this source or redo the exact compatibility review and test. Deploy this
0138 compatibility application and verify its production readback before
installing 0139. Neither step is authorized by this code-only ticket.

Draft PR #1816 is labeled `no-auto-merge` and targets current main. Task is
blocked while the explicit CI PostgreSQL result, host verifier path release,
and independent release review are pending. This is not a completed deployment
or paid activation.

Independent read-only review confirmed the C20 HOLD, 17-account/4-hold guard,
and fixture source digest. It also found two important limits. `/ready` checks
the exact revision but not budget row contents, so later ledger corruption
could leave `/ready` at 200; production acceptance must run
`python -m app.migration_guard --status` for full ledger readback and host
verification `TOTAL fail=0`. The integration test reads Compose's migrate
command and runs the same Python command against real PostgreSQL; it does not
boot a Compose container. Its CI run is still pending.

Host verifier `alembic-head` currently accepts only 0132→0133 in the
`rollback-compatible` branch; 0137→0138 and the staged 0138→0139 require an
exact predicate/test change. The occupied paths have their own blocked narrow
ticket `2026-10-24-guard-reviewed-c20-rollback-pairs-in`; normal claim was
rejected because 2026-10-14's in-progress ticket still owns them. No force
claim or edit was made. The parent is coordinating a narrow release with the
site owner. PR #1816 remains draft and not merge/deployment ready.
