---
id: 2026-10-23-archive-retained-c04-app-worktree
title: Archive retained C04 app worktree after primary checkout repair
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-23T11:32:48Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-23-archive-retained-c04-app-worktree.md
---

# Archive retained C04 app worktree after primary checkout repair

## Why

The app-managed C04 Bubble Wrap review checkout remains after its source PR
#1668 closed. Its exact root is
`C:\Users\x8120\.codex\worktrees\brand-story-bubble-wrap-c04\travel_scanㄐ`.
The 2026-10-23 closeout audit found it clean, pushed and idle. It contains a
`node_modules` junction. App `archive_worktree` returned queued repeatedly;
a later attempt said `Could not verify the task's primary checkout`. The
original `b16f` checkout currently lacks `.git`, so manual removal would
skip the app's ownership and attachment check. Retain this checkout until
the primary checkout binding is repaired and the app can archive it.

## Definition of done

- [ ] Restore and verify the task's primary checkout binding, then archive
      exactly this C04 worktree through the app.
- [ ] Read back that the app detached it and the exact root is absent, without
      disturbing its junction target or any other checkout.

## Steps

- [ ] Recheck PR #1668 is CLOSED, the exact worktree path and resolved
      ancestors, clean Git status including untracked files, pushed HEAD,
      junction target, running process/CWD and chat attachment.
- [ ] Repair the app's primary checkout reference using its supported flow;
      repeat `archive_worktree` for this worktree only after verification.
- [ ] Record the archive result and independent absence/registry readback.

## How to verify

Use the app's worktree inventory and archive result, then inspect the exact
root and `git worktree list --porcelain` from the repaired primary checkout.
Re-run the conservative clean/pushed/idle checks immediately before archive.
Run `npm run check:tasks` after editing this ticket.

## Notes

Do not delete the root with a manual filesystem command, and do not recurse
through the `node_modules` junction. The failed archive is an app verification
problem, not evidence the worktree was removed. This ticket records cleanup
only; it does not reopen C04 production or authorize paid work.
