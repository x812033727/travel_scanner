---
id: 2026-09-28-guard-story-starts-and-repair-merged
title: Guard story starts and repair merged migration chain
status: done
priority: P1
area: api
owner: codex-pr910-followup
claimed_at: 2026-09-28T11:53:27Z
created_at: 2026-09-28T11:52:26Z
completed_at: 2026-09-28T12:14:44Z
branch: codex/pr910-start-quota-followup
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_story.py
  - apps/api/migrations/versions/0111_video_story_series.py
---

# Guard story starts and repair merged migration chain

## Why

After a story job is advertised, an owner may pause its series or lower a quota before the
worker starts it. The start endpoint currently commits a new request despite those holds.
Main also acquired two Alembic heads when #898 and #910 merged from the same 0108 parent.

## Definition of done

- [x] A fresh story start respects current active state and quotas under the existing series lock.
- [x] Allowed starts, same-episode refusal, and other series kinds keep their behavior.
- [x] The merged Shorts and story migrations form one chain without changing their SQL behavior.
- [x] Focused local tests and lint pass; remaining CI verification is explicitly documented.

## Steps

- [x] Verify current main and ownership, reproduce stale-start holds, and inspect migration heads.
- [x] Apply the story-only quota guard and regression cases; point 0111 at 0109_video_shorts.
- [x] Run scoped Python, schema/migration, type, lint, and task checks (type-check limit below).
- [x] Recheck remote ownership/main and prepare exact paths for the follow-up PR.

## How to verify

Use the existing watcher Python environment with this worktree's apps/api as cwd/PYTHONPATH.
Run pytest for test_video_story.py, test_schema.py, test_migration_sql_dialect.py, and
test_migration_0111_video_story_series.py; run Alembic heads, scoped Ruff/mypy, and tasks check.
PostgreSQL integration is available only in CI; no production operations are part of this task.

## Notes

- Base: main 3156370b831a24246c33d01104050e5d3969b018. PR #898 merged as
  63bd9c4670eafb97e56d17cdc96f5ff4e516c12f at 2026-09-28T11:48:00Z; #910 merged as
  3156370b831a24246c33d01104050e5d3969b018 at 11:49:04Z. Both revisions originally
  descended from 0108_video_drama_messages; `alembic heads` confirmed two heads before repair.
- Claim override rationale: the five overlapping #870 tasks and the #910 task remain owned
  in tasks/open after their feature PRs merged. Current main contains their work, the #910
  remote branch is gone, and no open PR or active branch implements this narrow quota repair.
  The user authorized PR/CI repairs; the coordinator assigned this isolated follow-up. Only
  this task is claimed/edited; the other owners' tasks and branches remain unchanged.
- Reused the idle managed pr905-schedule-guard worktree after confirming clean bb60b961 and
  no process using it. Its original branch remains at that commit; work is on the new
  codex/pr910-start-quota-followup branch.
- Immutable #910 scratch reproduction: four stale holds (paused, daily, in-flight, monthly)
  failed before the guard; three preservation tests passed. With the guard, all nine focused
  tests passed. The existing series lock already prevents two starts of the same episode;
  this repair addresses stale/direct fresh starts, not a claimed duplicate-worker race.
- Actual-worktree verification: 36 passed, 1 skipped in the four scoped pytest files; the
  skipped test requires PostgreSQL. Scoped Ruff check and format check pass for all three
  changed Python files. The schema tests confirm 0111 is the single highest-numbered head.
- Local scoped mypy (`--follow-imports=silent --platform linux` on series.py and the story
  tests) was stopped after approximately ten minutes without a result under severe host
  memory pressure. It is incomplete, not passed; CI's type checks remain required.
- Read main API job 108913425506: three schema failures explicitly name the two original
  heads. Discovery job 108915637975 also fails `alembic upgrade head` with exit 255 for that
  reason. No checks/audit were disabled or bypassed.
- Updated this branch from main 3156370b to c54594e488f48e3655566cc8a86d45e9dc2e004e before
  pushing. The incoming changes are content, web, and tasks; none change the guarded service,
  its tests, or migrations. Existing #904 remains an independent flat-explainer feature;
  it does not implement this quota repair and its branch is untouched.
