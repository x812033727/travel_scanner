---
id: 2026-09-28-investigate-windows-native-crash-in-video
title: Investigate Windows native crash in video test fixtures
status: done
priority: P2
area: tools
owner: codex-gpt6-windows-runtime
claimed_at: 2026-09-30T03:29:49Z
created_at: 2026-09-28T01:56:16Z
completed_at: 2026-09-30T03:32:24Z
branch: codex/windows-video-test-runtime
depends_on: []
scope:
  - .agents/skills/dev-and-ci/references/local-env.md
---

# Investigate Windows native crash in video test fixtures

## Why

On Windows, the existing video test processes terminate before reporting individual assertions. This blocks the complete local tools suite even when the unrelated drama document checks pass. The failure reproduces while constructing the shared sandbox, without any media requests. The root cause is not yet established.

## Definition of done

- [x] Identify the smallest native-crash reproduction and record the relevant runtime/platform conditions.
- [x] The shared sandbox and affected video tests complete on a supported Windows runtime, or document a verified environment remedy if repository changes are unnecessary.
- [x] Preserve the real test assertions and retain Linux CI coverage.

## Steps

- [x] Reproduce sandbox() without the test runner, then isolate its filesystem operations.
- [x] Compare the observed Windows runtimes and a clean Linux CI run; do not assume this is the separate atomicWrite rename/EPERM issue.
- [x] Apply and verify the smallest justified fix; expand scope only after the cause is known.

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

### 2026-09-30 resolution

- Rechecked on Windows 11 build 10.0.26200, win32/arm64, main 64f132e1.
  The system Node is 24.13.0; the bundled runtime is 24.19.0, also arm64.
  The original observations above are historical; the newer runtime now supplies
  a verified remedy without changing the shared fixture or weakening tests.
- Smallest reproduction: one ordinary file in a Unicode source directory,
  copied recursively. It does not import repository code or use the test runner:

  ```js
  import { mkdtempSync, mkdirSync, writeFileSync, cpSync } from 'node:fs';
  import { tmpdir } from 'node:os';
  import path from 'node:path';
  const base = mkdtempSync(path.join(tmpdir(), 'cp-dir-unicode-'));
  const source = path.join(base, 'source\u3110');
  mkdirSync(source);
  writeFileSync(path.join(source, 'one.txt'), 'one');
  console.log('before recursive copy');
  cpSync(source, path.join(base, 'destination'), { recursive: true });
  console.log('after recursive copy');
  ```

  Run this scratch `.mjs` with each explicit Node executable. Under 24.13.0 it
  prints only the first line and exits 3221226505, with empty stderr. Changing
  only `source\u3110` to `source` passes. Both variants pass under 24.19.0.
  Directory creation and non-recursive single-file copies pass under 24.13.0.
  Direct `sandbox()` likewise crashes under 24.13.0 and passes under 24.19.0.
  This isolates the observed trigger, not an upstream fix version or cause inside
  Node; no claim is made for intermediate releases, Node 22 or other architectures.
- Bundled Node 24.19.0: series/state tests 50 passed, no skips. The full tools
  run on the same main code passed 917 of 919 tests with 2 existing platform
  skips. That full run also included the separate ops-only docs-refresh branch;
  its changed ops files are outside the `test:tools` glob. No fixture or tool
  implementation was changed between that run and this documentation branch.
- Linux comparison: the successful [PR #1003 web job](https://github.com/x812033727/travel_scanner/actions/runs/36662407253/job/109719810981),
  head eb9541cbfc57ed36cf7a7521068fe3b7cd492885, ran Node 24.21.0 x64 on Ubuntu
  24.04 and passed all 931 tools tests, no skips. Linux coverage remains unchanged.
- Scope changed from fixture code to the shared development-environment reference.
  Documented explicit Node + npm CLI invocation because Windows npm.ps1 prefers
  its adjacent node.exe even when PATH points to the newer runtime. No global
  Node installation or environment setting was changed. Only SKILL.md has a
  Claude mirror; references are shared from `.agents/`.
- Preclaim audit: ticket unowned/open on main, 18 open PRs, 50 remote heads and
  177 accessible worktrees; no competing change or active scope on this reference.
