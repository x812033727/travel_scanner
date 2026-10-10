---
id: 2026-10-10-windows-automation-fixture-import
title: Bound Windows automation test fixture startup and use file URL imports
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-10T17:46:18Z
completed_at:
branch:
depends_on:
  - 2026-10-10-photo-paste-card
scope:
  - tools/video/automation/automation.test.mjs
---

# Bound Windows automation test fixture startup and use file URL imports

## Why

On Windows Node 24.19, the broad tools suite starts a fixture child which imports an absolute C: path as an ESM URL. The child reports ERR_UNSUPPORTED_ESM_URL_SCHEME and the parent remains waiting without a bounded startup failure. The suite was stopped after no new output for several minutes; this prevents a reliable complete tools check.

## Definition of done

- [ ] Fixture imports work on Windows with file URL conversion.
- [ ] Fixture startup failure terminates promptly with useful diagnostics and cleans up its child.
- [ ] The targeted automation tests and full tools suite complete without this hang.

## Steps

- [ ] Reproduce the fixture child error and identify its startup wait.
- [ ] Convert filesystem paths to file URLs and bound child startup.
- [ ] Verify both normal startup and early child failure, then run relevant checks.

## How to verify

Use the bundled Node 24.19 on Windows to run tools/video/automation/automation.test.mjs, then the repository tools suite. Preserve complete exit status and confirm no fixture child remains after a failed startup.

## Notes

2026-10-10: Filed during Codex course validation. Logs: C:/Users/x8120/mokaair-work/codex-practical-series/runs/test-tools.log. The owned test process tree was stopped; the broad suite is incomplete, not green. tools/video/automation/automation.test.mjs is in the active photo-paste-card task scope, so no implementation change or overlapping claim was made. This ticket remains open until that ownership is released.
