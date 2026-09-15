---
id: 2026-09-14-investigate-windows-task-archive-leftover-open
title: Investigate Windows task archive leftover open file
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-14T04:41:07Z
completed_at:
branch:
depends_on: []
scope:
  - tools/tasks.mjs
---

# Investigate Windows task archive leftover open file

## Why

On Windows PowerShell, `npm run tasks -- done <id>` reported success and wrote the completed task under tasks/done, but the original tasks/open file remained for both two-site-life-batch-01 and two-site-life-batch-02. The next check:tasks rejected duplicate IDs. Cause remains unconfirmed; commandDone appears to call rmSync after writing the completed file.

## Definition of done

- [ ] Diagnose why the completed task can retain its open copy and prevent duplicate IDs after successful completion.
- [ ] Verify that a failed archive cannot report success or lose the original task.

## Steps

- [ ] Reproduce with a disposable task on Windows and inspect filesystem/process behavior.
- [ ] Apply a scoped fix if confirmed and run task-tool regression checks.

## How to verify

Create, claim, and complete a disposable task; verify exactly one task file remains under tasks/done and run npm run test:tools and npm run check:tasks.

## Notes

Observed 2026-09-14 in worktree 7291. The two stale open copies were removed only after comparing them with completed copies: all checklist items were complete and differences were status/completed_at. No tool implementation changed during article production. Evidence of the initial validation failure is preserved in docs/content-research/two-site-life/batch-02-tasks-initial.log. Investigate concurrency and Windows filesystem behavior without assuming either is the cause.
