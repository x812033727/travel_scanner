---
id: 2026-10-24-c08-0140-rollback-compat
title: Stage exact C08 0140 rollback compatibility
status: done
priority: P2
area: api
owner: codex-c08-budget-compat
claimed_at: 2026-10-24T07:45:15Z
created_at: 2026-10-24T07:45:04Z
completed_at: 2026-10-24T08:46:23Z
branch: codex/c08-0140-compat-20261024
depends_on:
  - 2026-10-24-c20-0139-held-account
scope:
  - apps/api/app/schema.py
  - apps/api/app/migration_guard.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_migration_guard.py
  - apps/api/tests/test_c08_budget_rollback_integration.py
  - .github/workflows/ci.yml
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
---

# Stage exact C08 0140 rollback compatibility

## Why

After C20's held 0139 account is installed, an older 0139 application image must
survive a future additive C08 short-v8 0140 account migration. Compose runs that
older image's migrate command before API startup, so it needs an exact,
read-back-verified 0139-to-0140 exception. The C08 account, production migration,
and paid route are separate later work.

## Definition of done

- [x] An 0139 image recognizes only the pinned C08 0140 revision after reading
      back the exact 18 accounts, four historical holds, C20 ownership, C08
      ownership, and shared budget schema; unrelated revisions fail closed.
- [x] The old Compose migrate command, `/ready`, and host verifier admit that
      one reviewed rollback state while every everyday-story paid reservation
      remains held.
- [x] Disposable PostgreSQL integration applies a SHA-pinned synthetic 0140
      migration, tests rollback and damaged contracts, and CI runs it.
- [x] No actual 0140 migration/account, paid dispatch, or production change.

## Steps

- [x] Check branch, PR and active task scope; claim normally without force.
- [x] Add exact application and host verifier recognition with negative tests.
- [x] Add pinned future 0140 fixture and disposable PostgreSQL rollback test.
- [x] Run focused local checks and hand off after C20 0139 merges; exact-head
      CI with real PostgreSQL remains the PR gate.

## How to verify

`cd apps/api && uv run pytest -q tests/test_schema.py tests/test_migration_guard.py
tests/test_c08_budget_rollback_integration.py && uv run ruff check . && uv run
mypy app && uv run mypy tests`; `node --test tools/deploy-host-verify.test.mjs`;
`bash -n .agents/skills/deploy/scripts/host-verify.sh`; `npm run check:tasks`.
The PostgreSQL test requires `RUN_INTEGRATION_TESTS=1` and a disposable local
database, so CI must prove it when local PostgreSQL is unavailable.

## Notes

Originally stacked locally on C20 PR #1817 head. That HOLD migration merged as
`d2bd45b2e3952cd7f7b06fda2f261159f6fa19b5`; the compatibility commit was
then transplanted alone onto this main, without replaying C20's old commits.
Expected C08 slug is `story-everyday-kikkoman-c08-short-v8`, with a USD 25
owner-approved local pilot ceiling. That approval does not authorize a supplier
call until per-episode costs and a bounded paid route are verified separately.
The existing C08 production ticket covers visual receipts only. Seven older
unclaimed open scopes overlapped these exact paths, but no in-progress/review
holder did; the ordinary task-board claim succeeded on 2026-10-24.
The `/ready` endpoint checks the revision pair only. Deployment acceptance
must run `python -m app.migration_guard --status` to validate accounts,
historical holds, shared schema, and both ownership rows. Local focused tests
passed 17 with one PostgreSQL-only skip; Ruff, mypy app/tests, host verifier
tests, Bash syntax, and `check:tasks` passed. The future fixture is SHA-pinned
as `8d6fd7f52d6bee1fe232fe559dda95cfa7c6c4d3351596bde6b46aadd6e8a8de`.
No local Docker/PostgreSQL service is available. After the transplant, focused
pytest again passed 17 with one PostgreSQL-only skip, Ruff, mypy app (486
files), mypy tests (415 files), host verifier tests (3 passed, two local
awk-dependent skips), Bash syntax and `check:tasks` (2155 files) passed.
Independent read-only review found no blocker and reconfirmed the fixture SHA,
old-image rollback boundary and absence of an actual 0140 account. C20 duration
PR #1808 merged as `0f166b266f46da55464a27ed8a83d6d7d43f2db2`; this
branch was rebased onto that exact main before PR #1820. Its API check on
head `737c10f95365ad1f4f3d11633e6db548b0c0ec60` ran the disposable
PostgreSQL and Compose-command rollback test successfully; `api`, `web`, and
`containers` also passed. `full-stack-smoke` was still running when this task
was closed. PR #1820 remains draft with `no-auto-merge`; merge requires all
four checks on the final task-close head and a CLEAN main-base readback.
