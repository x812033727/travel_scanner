---
id: 2026-10-24-task-inventory-archive-race
title: Tolerate concurrent task archival while loading the shared queue
status: done
priority: P2
area: tools
owner: codex-open-tasks-board
claimed_at: 2026-10-24T14:42:23Z
created_at: 2026-10-24T13:27:57Z
completed_at: 2026-10-24T14:46:49Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tools/tasks.mjs
  - tools/tasks.test.mjs
---

# Tolerate concurrent task archival while loading the shared queue

## Why

Reproduced2026-10-24: loadTasks enumerates all task names, then another disjoint done operation moves a named file; readFileSync throws ENOENT. A claim failed on someone else's task, and a done operation reported failure while its archive had actually succeeded. Parent serialized all mutations as a workaround.

## Definition of done

- [x] A deterministic archival-race fixture reproduces the failure and passes after a narrow fix.
- [x] True duplicate records, malformed tasks and genuine permission errors remain visible; no task is lost or overwritten.

## Steps

- [x] Claim exact tool/test scope after collision checks.
- [x] Test a file moved between directory enumeration and read; retry or consistently select its done record without hiding real duplicates.

## How to verify

Run tools/tasks.test.mjs, full tools checks, check:tasks and diff check; include negative duplicate/parse/error fixtures.

## Notes

Filed from the533-task owner-requested reconciliation. No current production/paid changes are needed.


### 2026-10-24 coordinated execution

Parent verified current open-task scopes and open-PR ownership before taking the listed narrow paths. This is a local implementation task; no production, paid or media approval is implied. Existing unrelated producers and evidence remain intact.


### 2026-10-24 coordinator acceptance

Deterministic fixture reproduced original readFileSync ENOENT after a separate archival move (red1fail/4pass). Loader now retries one full snapshot only for file-readENOENT and requires the vanished filename to survive in that snapshot. EACCES, malformed frontmatter, true duplicates, unarchived disappearance and repeatedENOENT remain visible. Complete task suite24/24actualexit0. Independent peer review by codex-independent-gemini2k-review-20261024 found no blocker; existing filename/id validation remains. These two tool files need no duration binding. Full Linux CI follows the final PR head.

Implementation is local on `codex/open-tasks-reconcile-20261024`; merge/deployment and any paid media actions remain separate. No vendor POST, media deletion, upload or approval was performed by this fix.
