---
id: 2026-10-24-create-held-c-series-budget-accounts
title: Create held C-series budget accounts in 0138 migration
status: done
priority: P1
area: api
owner: codex-c-series-integration
claimed_at: 2026-10-24T01:11:15Z
created_at: 2026-10-24T01:11:08Z
completed_at: 2026-10-24T01:59:14Z
branch: codex/c-series-budget-0138-migration-20261024
depends_on: []
scope:
  - apps/api/migrations/versions/0138_everyday_story_budget.py
  - apps/api/tests/test_migration_0138_everyday_story_budget.py
---

# Create held C-series budget accounts in 0138 migration

## Why

Main has the C-series USD 25-per-film policy and fail-closed paid dispatch, but
its Alembic head is still 0137. Seven already owner-authorized pilots need
separate, attributable ledger accounts before any spend can be considered.
C03–C06 have prior provider requests whose actual charges are not reconciled;
their full USD 25 caps must stay unavailable. C07/C10/C15 have approved caps
but must also remain held until pricing, attribution and voice-duration gates
are verified. This migration-only ticket does not activate paid dispatch.

## Definition of done

- [x] Revision `0138_story_everyday_budget` upgrades from
      `0137_video_manga_tier` to seven distinct USD 25 held accounts for
      C03–C07, C10 and C15; C03–C06 each carry a full-cap uncertain
      pre-ledger-history reservation using the current compatible model.
- [x] Repeated upgrade preserves existing matching data without resetting
      balances; any existing conflicting account/reservation causes a clear
      failure instead of `ON CONFLICT DO NOTHING` acceptance.
- [x] A real PostgreSQL/Compose upgrade and downgrade prove rollback removes
      only rows owned by 0138 and leaves other ledger data untouched.
- [x] Paid C-series routing and all per-film STOP conditions remain unchanged;
      this PR does not call providers or grant spending access.

## Steps

- [x] Read current 0137 schema and #1793 compatibility code; inspect the
      closed #1749 candidate only as reference, correcting its model and
      conflict behavior.
- [x] Implement only the two scoped new files: 0138 migration and focused
      migration tests. Do not change #1583's overlapping service or guard files.
- [x] Exercise idempotence, mismatched pre-existing data, and targeted
      downgrade with real PostgreSQL/Compose; record actual commands/results.

## How to verify

Run focused tests in `apps/api`, `uv run ruff check` on the two files,
`npm run check:tasks`, `git diff --check`, and a disposable PostgreSQL/Compose
upgrade/downgrade/readback. No provider request is part of verification.

## Notes

2026-10-24 read-only preflight: main/0137 already contains the held constants
and rollback compatibility from #1793. No open PR creates the 0138 file.
Draft PR #1583 overlaps broader budget service/guard files, so this ticket
claims only the two new migration/test paths. Closed #1749 used an incompatible
`pre-ledger` model and accepted conflicting existing rows; do not cherry-pick it.
Actual provider charges and TTS prices are separate unresolved gates.

2026-10-24 implementation handoff: added only the two scoped migration/test
files. The migration freezes the nine existing account limits, adds seven
separate USD 25 accounts, and records four full-cap uncertain holds with
`model=unattributed` as required by the 0137 rollback guard. A dedicated
0138 provenance table records which account and hold rows it actually created;
repeat upgrade verifies existing rows without resetting settled evidence,
while downgrade deletes only unchanged rows created by 0138 and refuses a
reconciled hold or later operation. The API and three local paid clients were
not edited, so their preproduction holds remain in place.

Local verification: `uv run --frozen alembic heads` reported the single head
`0138_story_everyday_budget`; focused pytest plus schema/dialect tests reported
13 passed, 8 PostgreSQL tests skipped; scoped Ruff and mypy passed; task check
passed with unrelated existing warnings. A deliberate
`RUN_INTEGRATION_TESTS=1` attempt failed at connection setup with
`ConnectionRefusedError [WinError 1225]` because local TCP 127.0.0.1:5432 is
closed; `docker` is not installed in this host's PATH. No PostgreSQL/Compose
upgrade, repeat, mismatch, rollback or 0137-image readback is claimed yet.
The added CI-only integration case creates a disposable local PostgreSQL
database, runs actual Alembic 0137 -> 0138 -> 0137 commands, checks the seven
accounts, four holds, nine prior accounts, and a prior operation, then drops
that database. CI or another disposable PostgreSQL environment must run all
eight PostgreSQL cases before the migration is eligible to merge or deploy.
No provider call occurred.

2026-10-24 completion readback: PR #1804 head `7ab87304c93ed3e16d6aa582748cbfdd781ae332`
passed all four required GitHub checks (`api`, `web`, `containers`,
`full-stack-smoke`); PostgreSQL `api-tests (3/4)` passed after fixing a
test-only SQLAlchemy result-materialization bug. An independent review found
no migration safety HOLD. On a disposable local WSL Docker Compose
`postgres:16-alpine` database, focused tests ran with `RUN_INTEGRATION_TESTS=1`
and reported `10 passed, 1 skipped` (the skipped case is intentionally CI-only
because it creates a separate database). Actual Alembic/readback on that
Compose database: `0137_video_manga_tier` had 9 prior accounts and 0
operations; upgrade to `0138_story_everyday_budget` had 16 accounts, exactly
7 C-series USD 25 accounts, 4 full-cap `pre-ledger-history` uncertain holds,
and 7 provenance rows; downgrade to 0137 restored 9 accounts, 0 operations,
and no 0138 provenance table. The CI-only disposable-database Alembic
up/down test also passed in the PostgreSQL job. The exact Compose project
`cseries0138verify1024` was stopped and removed with `down -v`; `compose ls
--all` returned `[]`. This verifies the migration, not deployed host state,
historical charge settlement, spending-route activation, or actual vendor
prices. All paid C-series STOP gates remain in place.
