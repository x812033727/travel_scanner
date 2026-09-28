---
id: 2026-09-28-investigate-windows-native-crash-in-video
title: Investigate Windows native crash in video test fixtures
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T01:56:16Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/fixtures/load.mjs
---

# Investigate Windows native crash in video test fixtures

## Why

On Windows, the existing video test processes terminate before reporting individual assertions. This blocks the complete local tools suite even when the unrelated drama document checks pass. The failure reproduces while constructing the shared sandbox, without any media requests. The root cause is not yet established.

## Definition of done

- [ ] Identify the smallest native-crash reproduction and record the relevant runtime/platform conditions.
- [ ] The shared sandbox and affected video tests complete on a supported Windows runtime, or document a verified environment remedy if repository changes are unnecessary.
- [ ] Preserve the real test assertions and retain Linux CI coverage.

## Steps

- [ ] Reproduce sandbox() without the test runner, then isolate its filesystem operations.
- [ ] Compare the observed Windows runtimes and a clean Linux CI run; do not assume this is the separate atomicWrite rename/EPERM issue.
- [ ] Apply and verify the smallest justified fix; expand scope only after the cause is known.

## How to verify

- node --test --test-reporter=tap tools/video/automation/series.test.mjs
- node --test --test-reporter=tap tools/video/core/state.test.mjs
- node --input-type=module -e "import {sandbox} from './tools/video/core/fixtures/load.mjs'; console.log('before sandbox'); sandbox(); console.log('after sandbox');"
- npm run test:tools

## Notes

- Observed while preparing five drama planning documents on main baseline 152e47ba. No tools/video source files were modified by that work.
- Node 24.13.0 full suite: 286 reported tests, 265 pass, 20 test-file failures, 1 skip. TAP for series.test.mjs reports child exitCode 3221226505, ERR_TEST_FAILURE, before per-test output.
- The series test also fails under temporary npx Node 22.22.2; state.test.mjs fails under temporary npx Node 22.23.2 with the same native exit code. Changing Node alone has not been shown to fix it. No global runtime was changed.
- The direct sandbox reproduction prints before sandbox and exits before after sandbox. sandbox currently creates temp directories and copies fixture files; the crashing sub-operation has not been isolated.
- Similar pre-assertion failures were already recorded in tasks/open/2026-09-27-localize-wordpress-contact-forms-and-smtp.md. The separate task 2026-09-26-atomicwrite-fails-on-windows-when-the covers a reported JavaScript EPERM rename, not this native exit.
- Five-drama source/review validation and its 17 regression tests pass independently. This ticket remains open rather than claiming the full Windows suite passed.
