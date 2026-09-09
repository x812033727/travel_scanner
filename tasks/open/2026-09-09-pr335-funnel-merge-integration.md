---
id: 2026-09-09-pr335-funnel-merge-integration
title: Prepare PR 335 funnel integration against current main
status: in-progress
priority: P1
area: api
owner: codex-pr335-merge-ready
claimed_at: 2026-09-09T06:13:49Z
created_at: 2026-09-09T06:13:49Z
completed_at:
branch: codex/pr335-merge-ready-20260909
depends_on: []
scope:
  - apps/api/tests/test_analytics_events.py
  - apps/api/tests/test_integration_postgres_redis.py
  - docs/user-flow-plan.md
---

# Prepare PR 335 funnel integration against current main

## Why

PR #335 adds the missing flight `offer_attached` funnel event. Its old successful
checks do not validate integration with current main. Prepare an isolated, normally
merged and tested head without reopening the completed observe-the-funnel task.

## Definition of done

- [ ] Current main behavior and historical completed task state are preserved.
- [ ] Only successful flight attachment emits the expected enum-only event, while
  invalid requests, stale versions and rolled-back writes add no persisted event.
- [ ] Relevant regression, Ruff, mypy and task checks pass with explicit local gaps.
- [ ] Deliver a clean local head for root's fresh remote CI and guarded merge.

## Steps

- [x] Pin PR head `1a83d64efbaed5db45656ea2ff58e347c6d59371` and current main
  `a899437aaf2f60c7affe2e944d49d62216537c90`; create a narrow integration claim.
- [ ] Normally merge current main and resolve only relevant overlaps.
- [ ] Independently inspect transaction, privacy and repeat-request semantics.
- [ ] Validate and hand back; root owns push, final CI and merge after #343.

## How to verify

From `apps/api`, set PYTHONPATH to this worktree's `apps/api`, then run focused
analytics, flight-attachment and PostgreSQL integration regressions with the matching
test environment. Run Ruff, mypy and repository task checks. Regenerate conflicting
`tasks/BOARD.md` only with `npm run tasks:board`.

## Notes

No production data, provider calls, deployment, push or remote PR mutation is in this
subtask. The old branch still marks planner-calm as review and claims the trip router;
current main has already completed that task. Initial integration scope excludes the
router to avoid an overlapping claim until the normal main merge imports that state.
The existing `tasks/done/2026-09-07-observe-the-funnel.md` remains completed.
