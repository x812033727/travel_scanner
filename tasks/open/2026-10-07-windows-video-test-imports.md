---
id: 2026-10-07-windows-video-test-imports
title: Make video automation test imports finish on Windows
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T05:37:50Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/automation.test.mjs
---

# Make video automation test imports finish on Windows

## Why

A broad test:tools run on Windows reaches ERR_UNSUPPORTED_ESM_URL_SCHEME
(protocol c:) and leaves automation.test.mjs running with no log progress.
This prevents a complete local tools verdict during unrelated localization work.

## Definition of done

- [ ] Identify the absolute-path ESM import and use portable file URLs.
- [ ] Ensure failing test children and mock servers terminate on every failure.
- [ ] Run the affected test on Windows and the required Linux CI suite.

## Steps

- [x] Preserve the exact broad-run log and verify the stalled test child identity.
- [x] Stop only the verified test child/runner after prolonged no-progress state.
- [ ] Reproduce the specific import and implement a narrow portable fix.
- [ ] Check failure cleanup and complete both platform runs.

## How to verify

Run tools/video/automation/automation.test.mjs with the bundled Node on Windows;
assert a final test summary and no surviving mock server/child. Run test:tools
in CI. Do not terminate unrelated video or browser processes.

## Notes

- Node v24.19.0 reports unsupported ESM URL scheme c: for a Windows absolute path.
- Broad localization validation was incomplete/failed, not a passing tools suite.
- Exact raw log is preserved privately; localization-specific Node tests pass.
- No source change was made to the automation test during this run.
