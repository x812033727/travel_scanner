---
id: 2026-09-14-investigate-windows-task-archive-leftover-open
title: Investigate Windows task archive leftover open file
status: done
priority: P2
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:12:30Z
created_at: 2026-09-14T04:41:07Z
completed_at: 2026-09-19T11:12:30Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - tools/tasks.mjs
---

# Investigate Windows task archive leftover open file

## Why

On Windows PowerShell, `npm run tasks -- done <id>` reported success and wrote the completed task under tasks/done, but the original tasks/open file remained for both two-site-life-batch-01 and two-site-life-batch-02. The next check:tasks rejected duplicate IDs. Cause remains unconfirmed; commandDone appears to call rmSync after writing the completed file.

## Definition of done

- [x] Diagnose why the completed task can retain its open copy and prevent duplicate IDs after successful completion.
- [x] Verify that a failed archive cannot report success or lose the original task.

## Steps

- [ ] Reproduce with a disposable task on Windows and inspect filesystem/process behavior.
- [x] Apply a scoped fix if confirmed and run task-tool regression checks.

## How to verify

Create, claim, and complete a disposable task; verify exactly one task file remains under tasks/done and run npm run test:tools and npm run check:tasks.

## Notes

Observed 2026-09-14 in worktree 7291. The two stale open copies were removed only after comparing them with completed copies: all checklist items were complete and differences were status/completed_at. No tool implementation changed during article production. Evidence of the initial validation failure is preserved in docs/content-research/two-site-life/batch-02-tasks-initial.log. Investigate concurrency and Windows filesystem behavior without assuming either is the cause.

### 2026-09-19 folded into 2026-09-14-tasks-done-retains-open-copy (claude-fable-5-1)

Same defect, same file. The fix and its tests live with that ticket: `done` now deletes the file it
actually read, verifies the open copy is gone (with brief retries), and exits non-zero with a
diagnosis instead of reporting "moved" while both copies exist; `check` names a leftover open copy
for what it is. The one step left — reproducing with a disposable task on Windows — is written in
that ticket for the owner; nothing else remains here.
