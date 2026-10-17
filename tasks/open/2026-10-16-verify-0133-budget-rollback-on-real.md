---
id: 2026-10-16-verify-0133-budget-rollback-on-real
title: Verify 0133 budget rollback on real PostgreSQL
status: in-progress
priority: P1
area: api
owner: codex-gpt6-rollback-pg
claimed_at: 2026-10-16T02:50:09Z
created_at: 2026-10-16T02:49:32Z
completed_at:
branch: codex/a01-pilot-deploy-evidence-20261015
depends_on: []
scope:
  - apps/api/tests/test_story_budget_rollback_integration.py
  - tasks/open/2026-10-16-verify-0133-budget-rollback-on-real.md
---

# Verify 0133 budget rollback on real PostgreSQL

## Why

The production `migrate` service runs `alembic upgrade head` before the API starts. After #1510 applies `0133_story_followon_budget`, a rollback to an API image whose local head is 0132 fails because Alembic cannot locate the database's 0133 revision. API compatibility checks alone do not make rollback bootable. Draft #1521 is adding an exact 0133-on-0132 guard; its safety must be demonstrated against real PostgreSQL and the actual compose migration command before #1510 can deploy.

## Definition of done

- [ ] A real PostgreSQL test starts from migration 0132 with the original B18 v2 US$25 account and preserved operation rows, applies the exact #1510 migration 0133, then runs the #1521 image's **actual compose migrate command** without database downgrade or stamp.
- [ ] The rollback image starts API `/ready` and read-only budget status, retains the old B18 operations, reads B18 v2 and five exact follow-on accounts at US$5, and refuses paid calls that would exceed each film's own limit.
- [ ] Unknown 0134, multiple revisions, incomplete 0133 schema/account rows and unavailable database all make the rollback migration guard fail closed. Tests do not create a fake PASS by stubbing out the command, database or paid-route boundary.
- [ ] CI runs the test with PostgreSQL and records the exact #1521/#1510 SHAs and results; no formal host write or paid call occurs.

## Steps

- [ ] Wait for #1521's guarded migrate implementation and its independent review; coordinate with the owner of the overlapping #1510 migration test without editing that active task's files.
- [ ] Add one isolated integration test in this ticket's new file, using the repository's existing PostgreSQL fixture conventions and the exact 0133 migration.
- [ ] Run the focused test in CI with `RUN_INTEGRATION_TESTS=1` and inspect its logs for migrate exit status, API health, account/operation readback and refusal cases.
- [ ] Record any release limitation in the pilot and migration tickets before asking for #1510 deployment approval.

## How to verify

Run the new pytest file with a real PostgreSQL service and `RUN_INTEGRATION_TESTS=1`; inspect the test's command/exit evidence and DB readback. The existing 0133 migration unit test or a mocked `schema_is_current` assertion alone does not close this ticket. This is a prerequisite for the #1510 migration release, not approval to deploy it.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
