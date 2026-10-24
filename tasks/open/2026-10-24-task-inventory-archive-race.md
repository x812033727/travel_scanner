---
id: 2026-10-24-task-inventory-archive-race
title: Tolerate concurrent task archival while loading the shared queue
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-24T13:27:57Z
completed_at:
branch:
depends_on: []
scope:
  - tools/tasks.mjs
  - tools/tasks.test.mjs
---

# Tolerate concurrent task archival while loading the shared queue

## Why

Reproduced2026-10-24: loadTasks enumerates all task names, then another disjoint done operation moves a named file; readFileSync throws ENOENT. A claim failed on someone else's task, and a done operation reported failure while its archive had actually succeeded. Parent serialized all mutations as a workaround.

## Definition of done

- [ ] A deterministic archival-race fixture reproduces the failure and passes after a narrow fix.
- [ ] True duplicate records, malformed tasks and genuine permission errors remain visible; no task is lost or overwritten.

## Steps

- [ ] Claim exact tool/test scope after collision checks.
- [ ] Test a file moved between directory enumeration and read; retry or consistently select its done record without hiding real duplicates.

## How to verify

Run tools/tasks.test.mjs, full tools checks, check:tasks and diff check; include negative duplicate/parse/error fixtures.

## Notes

Filed from the533-task owner-requested reconciliation. No current production/paid changes are needed.
