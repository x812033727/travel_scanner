---
id: 2026-10-07-keep-renewed-final-evidence-notes-portable
title: Keep renewed-final evidence notes portable
status: done
priority: P2
area: tools
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:03:40Z
created_at: 2026-10-07T04:05:55Z
completed_at: 2026-10-24T13:03:58Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - tasks/open/2026-10-01-hand-off-owner-approved-renewed-finals.md
  - tasks/open/2026-10-07-continue-imported-language-units-before-requiring.md
  - tasks/open/2026-10-07-handle-a-no-cut-range-in.md
  - tasks/open/2026-10-07-imported-language-runner-hides-native-speech.md
  - tasks/open/2026-10-07-support-proven-thumbnail-encoding-in-renewal.md
---

# Keep renewed-final evidence notes portable

## Why

The renewed-final evidence notes include operator-specific home paths. The full
tools check correctly rejects those new tracked paths. Keep durable artifact
names and hashes while expressing the operator root as `<home>`.

## Definition of done

- [x] Tracked handoff notes pass the repository host-detail policy without
      changing their evidence names, hashes or operational meaning.

## Steps

- [x] Replace the five affected notes' local home roots with `<home>`.
- [x] Run the repository hygiene test and task validation.

## How to verify

`node --test tools/repo-hygiene.test.mjs` and `node tools/tasks.mjs check`.

## Notes

The full Windows tools run completed with exit 1: 1,948 passes, 11 failures and
13 platform skips. Its new host-detail failure is fixed here; the other failures
are Windows FFmpeg/filter-path, path-separator and speech-journal rename issues
outside this documentation scope. The successful focused native-unit tests and
exact production-image isolation are separate evidence from that full-suite exit.
The focused hygiene test passed 3/3, exit 0; task validation and diff checks
passed. Only portable note paths changed, with no production operation.


### 2026-10-24 owner-directed open-task reconciliation

The owner requested evaluating all open tasks, closing unnecessary or completed work, and executing needed work. This metadata-only takeover archives this ticket; it does not claim another live producer or change product files.

Disposition: close_completed.

- Task status=review; unresolved checklist rows=0
- All done and Steps boxes checked, task records 3/3 hygiene validation; rerun tools/repo-hygiene.test.mjs before archiving

依已合併實作及驗收記錄結案；結案只涵蓋本票，沒有啟動正式站或付費工作。
