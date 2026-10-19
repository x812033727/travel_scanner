---
id: 2026-10-19-prepare-0133-image-for-guarded-0134
title: Prepare 0133 image for guarded 0134 A01 schema
status: in-progress
priority: P1
area: api
owner: codex-gpt6-a01-precompat
claimed_at: 2026-10-19T03:26:18Z
created_at: 2026-10-19T03:26:08Z
completed_at:
branch: codex/a01-0134-precompat-20261019
depends_on: []
scope:
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
  - apps/api/app/schema.py
  - apps/api/app/migration_guard.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_migration_guard.py
  - apps/api/tests/test_story_budget_rollback_integration.py
---

# Prepare 0133 image for guarded 0134 A01 schema

## Why

The A01 source-adoption design adds a nullable admission token in revision 0134.
Production migrates before switching application containers, and a rollback does
not downgrade the database. The present 0132-compatible application recognizes
only the reviewed 0133 story-budget revision. A deployment of 0134 would make
that rollback image reject `/ready` and the migrate guard; an image that ignores
a held token could also dispatch A01 work during source adoption.

## Definition of done

- [ ] A pre-migration application image recognizes only the exact reviewed 0134
      successor of 0133 when the additive admission column and existing budget
      schema match; unknown future revisions or changed schemas still fail closed.
- [ ] The image works against its own 0132/0133 schema and can serve `/ready`
      against 0134 without applying or downgrading any migration.
- [ ] The release includes the A01 reserve and text-stage dispatch checks from
      the separately claimed DB-fence task, written to tolerate 0133 without the
      column and to reject a held token under the same budget row lock on 0134.
- [ ] Exact tests show both DB states, held-token refusal, unknown-revision
      refusal, and a real rollback guard rather than a mocked success.

## Steps

- [ ] Implement and test only the schema/guard paths in this ticket's scope.
- [ ] Coordinate the overlapping reserve/dispatch code with the A01 DB-fence
      task; do not modify those files under this claim or deploy schema-only code.
- [ ] Independently review the combined exact diff and deploy this precompat
      release before the 0134 migration, under a separately approved release.

## How to verify

Run focused `tests/test_schema.py`, `tests/test_migration_guard.py`, and
`tests/test_story_budget_rollback_integration.py`; run Ruff, mypy, Alembic
single-head/schema checks, and `npm run check:tasks`. The existing 0133
PostgreSQL fixture must exercise the 0134 column as well. A local PASS is not
deployment or production permission.

## Notes

2026-10-19: #1510's unmerged 0133 migration is still in a draft PR. The A01
DB-fence draft is stacked on #1510 and has scope over `service.py`, `ai.py`,
their focused tests, the 0134 migration and token model. This ticket claims
only schema/migration-guard files to avoid overlapping an active task. The two
sets must be combined into a **single precompat application release before
0134**; until then, neither is deployable. A01's last read-only `-03` capture
also contains one uncertain stage job and a global active-work HOLD.

2026-10-19: The schema/guard-only draft now accepts the exact 0133→0134
revision pair after checking the existing 0133 budget ledger and an additive
nullable UUID admission column; the 0132→0133 exception remains scoped to the
old image. A held A01 token prevents the precompat rollback image from starting.
Focused local results: 11 passed, 2 PostgreSQL cases skipped without a local
server; Ruff, mypy and task-board checks passed. This is not yet an installable
release: the separate Phase1 A01 reserve/text-dispatch checks must join it,
followed by real PostgreSQL CI and independent review.

2026-10-19 independent review: P1 release integration blockers remain. The
production `.agents/skills/deploy/scripts/host-verify.sh` allowlist accepts only
0132→0133, so it must explicitly accept 0133→0134 with a focused test and be
installed with the precompat release. The owner approved the narrow transfer
of that script and its test from the older monthly-cap ticket. The migration
guard is only a startup check; Phase1 reserve, submit and text-dispatch checks
are required in the same image.

2026-10-19: The verifier draft now admits only the additional exact pair
0133 image→0134 database when its migrate guard passes, the image has one
head, and the reported expected head matches. Local `bash -n` passed; the
shell-executed decision test passed when Git Bash was on PATH. The older
monthly-cap log tests remain unchanged. This draft is pending independent
review and the combined precompat release; no host script was installed.

2026-10-19 independent verifier review: no P0/P1. The review caught an
existing broken `awk` availability probe in the focused test: `BEGIN{}` is
rejected by Git awk and had silently skipped the monthly-cap cases. It is now
`BEGIN { exit 0 }`; with Git Bash on PATH all five focused tests pass without
skips, and the cap-classification script itself has no changed lines.
