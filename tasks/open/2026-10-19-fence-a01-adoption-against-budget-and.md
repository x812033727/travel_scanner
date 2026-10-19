---
id: 2026-10-19-fence-a01-adoption-against-budget-and
title: Fence A01 adoption against budget and text dispatch
status: in-progress
priority: P1
area: api
owner: codex-gpt6-a01-db-fence
claimed_at: 2026-10-19T03:08:55Z
created_at: 2026-10-19T03:08:49Z
completed_at:
branch: codex/a01-db-admission-fence-20261019
depends_on: []
scope:
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/run_jobs.py
  - apps/api/app/video_media/jobs.py
  - apps/api/migrations/versions/0134_a01_admission_fence.py
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/api/tests/test_video_stage_jobs.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_migration_0134_a01_admission_fence.py
---

# Fence A01 adoption against budget and text dispatch

## Why

A01 is already imported. The proposed 104→105 source adoption must hold a durable,
self-owned database token while its nine exact files are staged. A global worker STOP
cannot by itself keep an A01 text-stage dispatch or paid media reservation from racing
with adoption. Current `video_pilot_budgets` has no admission token; `reserve()` and
`video_automation/ai.py` do not check one. The offline transaction in draft #1580
therefore correctly remains on HOLD.

## Definition of done

- [ ] A schema change adds a nullable A01 admission token to the existing budget row,
      preserves all prior accounts and operations, and allows the prior application
      to run after a database-first deploy or application rollback.
- [ ] A token holder can be created and read back only through a row-locked operation;
      releasing requires the same token and cannot clear another holder's fence.
- [ ] While the token is held, A01 vendor reservations and durable A01 text-stage
      dispatch reject before provider contact, under the same budget-row lock.
- [ ] Other slugs and normal A01 requests without a token keep their existing behavior;
      unfinished or uncertain work cannot be made safe by this patch alone.

## Steps

- [ ] Implement the row and migration after #1510's 0133, with focused migration
      tests including existing-row preservation and rollback compatibility.
- [ ] Implement acquire/readback/release and both dispatch refusals with concurrency
      and exact-token mismatch tests. Do not add a production CLI or arm the host here.
- [ ] Independently review the exact diff and retain a draft/no-auto-merge PR for
      the separately approved merge and deployment chain.

## How to verify

Run focused budget, automation-AI and 0134 migration tests, `uv run ruff check .`,
`uv run mypy app`, `uv run mypy tests`, `uv run alembic heads`, and `npm run check:tasks`.
CI must prove the PostgreSQL migration branch. There is no production readback or
adoption permission from a green local test.

## Notes

2026-10-19 owner authorized a narrow transfer of `models.py`, `service.py`, and
`test_video_pilot_budget.py` from #1510's in-progress budget ticket; the removal
and handoff note are commit 379b3a80e on #1510. Its 0133 migration, clients,
recovery, other tests and original branch remain untouched. This task is stacked
on that exact #1510 commit and claims only the paths listed above. #1510 stays
draft/no-auto-merge. #1580's transaction library explicitly has no host wrapper
and blocks the old r23 manifest; this patch does not start production.

2026-10-19 deployment HOLD: 0134 requires #1510's 0133 migration to land
first. The current 0133 image's schema and migration guards reject a 0134
database, and its budget/text dispatch code would ignore a held token on
rollback. An independently reviewed, fence-aware 0133 pre-compatibility image
must be deployed before the nullable-column migration; the pre-compatibility
path must allow a normal 0133 database and refuse A01 dispatches under a held
0134 token. A rollback while adoption is active must stay stopped. Do not mark
the rollback-compatibility definition of done complete from local 0134 tests.

2026-10-19 race review: acquire now takes the A01 budget row `FOR UPDATE`
and, before inserting its token in that same transaction, refuses any
`reserved`/`uncertain` A01 budget operation or `queued`/`running`/`uncertain`
A01 text-stage job. This closes preflight-to-acquire races against service
reservations and committed stage dispatches. The first review found that
`submit_job` only locked its tool token, so a new queued job could still enter
after acquire. The Phase 1 queue-admission follow-up below closes that path.
The host adoption wrapper remains HOLD until it can STOP and drain workers,
acquire, immediately recheck live work, and retain and verify this token until
its write has finished. Migration 0134 never performs an automatic downgrade,
even when token is NULL, to avoid a check/drop race.

2026-10-19 phase split: this uncommitted worktree now holds the 0133/0134
dual-schema A01 dispatch interception. Its ORM model does not map the optional
token column, and `alembic heads` remains 0133. The 0134 model, migration,
acquire/readback/release and related tests are preserved as a separate local
draft for rebasing after pre-compatibility code. The acquire/downgrade notes
above describe that parked Phase 2 draft, not code present in this worktree.
Phase 1 still needs separately scoped schema and migration-guard compatibility
changes plus PostgreSQL CI evidence before deployment.

2026-10-19 narrow queue-admission expansion: the task owner added
`run_jobs.py` and `test_video_stage_jobs.py` to this claim after an independent
review found a new A01 queued job could enter while the token was held. Both
pre-existing open tickets that mention these paths have blank owners; the
historical `codex/video-stage-deploy-race` branch has no open PR from that head.
Only A01 queue admission and idempotent queued recovery are changed here. The
scope does not transfer ownership of either old ticket's other work.

Phase 1 now locks the A01 budget row and reads the optional 0134 token before
`submit_job` commits a new queued receipt. A held token rejects the new row;
an existing queued receipt remains readable without Redis re-enqueue on POST,
poll or worker startup. Terminal results remain readable, and other slugs do
not use the A01 account lock. Focused SQLite tests cover the 0133 no-column
path, 0134 held-token refusal, idempotent recovery, unrelated slug and startup
recovery. A PostgreSQL two-order interleave test was added but remains a CI
gate: local `RUN_INTEGRATION_TESTS` is off. Focused API suite 80 passed, 6
skipped; Ruff, mypy app/tests, task check and diff check passed. Phase 2's
actual acquire race tests remain in the parked draft. The queue gate and
schema/guard pre-compatibility changes must be brought together and reviewed
before any deployment or A01 source adoption.

In the combined precompatibility branch, Phase 1 runs against the current 0132
image and a reviewed 0133 successor without an additional migration. The
separate Phase 2 migration and acquire/release feature still depend on #1510's
0133 migration; this ticket cannot name that not-yet-merged task as a
`depends_on` in a branch based on main because task validation would reject it.

2026-10-19 media scope handoff: the owner authorized transferring only
`video_media/jobs.py` and `test_video_media_jobs.py` from the #1510 budget
ticket and #1556 media-cutover ticket. Their task-scope handoff commits are
0dfd0b59e and 5bc1bf984; both original PRs remain draft/no-auto-merge with
their code and other scopes untouched. The older ownerless MiniMax H3 ticket
also lists these paths but has no active claim. This A01 task now claims only
the narrow media-admission change in those two files, to close the queued-row
race independently found in the combined Phase 1 / Phase 2 review. No merge,
deployment, host action or paid work follows from the handoff.
