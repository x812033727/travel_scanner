---
id: 2026-10-07-windows-video-test-imports
title: Make video automation test imports finish on Windows
status: in-progress
priority: P2
area: tools
owner: codex-windows-video-validation
claimed_at: 2026-10-08T16:47:16Z
created_at: 2026-10-07T05:37:50Z
completed_at:
branch: codex/windows-video-validation-20261009
depends_on: []
scope:
  - tools/video/automation/automation.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Make video automation test imports finish on Windows

## Why

A broad test:tools run on Windows reaches ERR_UNSUPPORTED_ESM_URL_SCHEME
(protocol c:) and leaves automation.test.mjs running with no log progress.
This prevents a complete local tools verdict during unrelated localization work.

## Definition of done

- [x] Identify the absolute-path ESM import and use portable file URLs.
- [x] Ensure failing test children and mock servers terminate on every failure.
- [ ] Run the affected test on Windows and the required Linux CI suite.

## Steps

- [x] Preserve the exact broad-run log and verify the stalled test child identity.
- [x] Stop only the verified test child/runner after prolonged no-progress state.
- [x] Reproduce the specific import and implement a narrow portable fix.
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

## 2026-10-09 repair

The owner explicitly requested reproduction and repair. Branch `codex/windows-video-validation-20261009` starts from `c6454463d`. The child script passes an absolute Windows path directly to dynamic import; its readiness promise also ignores an early exit, so the test hangs before entering cleanup. Repair is scoped to the test fixture and its lifecycle regression coverage. No global Node installation or production worker setting is changed.

The duration receipt scope is included because `automation.test.mjs` is one of its 108 bound files. An independent reviewer verified all immutable baseline bindings and will review and rebind this one-file delta after the author commit. PR #1387 also updates shared receipt files for different implementation paths; preserve both increments when integrating, and do not modify its branch.

The child script's sole absolute ESM specifier now uses `pathToFileURL(...).href`. Its test-only lifecycle helper observes errors and closure immediately, registers cleanup before readiness, retains stderr diagnostics, and bounds readiness, release, and cleanup. The existing lease, request-count, and worker-state assertions remain. The affected fixture uses in-memory mock responses, not a listening server. No production code changed.

Windows Node v24.19.0 verification:

- A builtin-only probe failed with the old native path (`exit=1`, `ERR_UNSUPPORTED_ESM_URL_SCHEME`) and succeeded with the file URL (`exit=0`).
- Temporarily restoring the old import in the repaired fixture made the actual held-project test fail and finish in 550.9 ms with the original diagnostic, instead of hanging. The portable import was restored immediately.
- The restored targeted run passed 6/6 in 1220.9 ms: startup import failure preserves its diagnostic; missing readiness and ignored release time out; both timeout cases verify that cleanup awaited child termination; the original cross-process lease behavior passes.
- `git diff --check` passed. The complete automation file finished naturally with exit 0: 216 passed, none failed, skipped, or cancelled, in 188.4 seconds. Its log is `<home>/mokaair-work/windows-video-validation-20261009/automation-test.log`. Broader tools validation and Linux CI remain to be recorded by the coordinator.
