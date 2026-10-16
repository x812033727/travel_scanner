---
id: 2026-10-07-make-project-lease-test-children-use
title: Make project lease test children use portable Windows imports
status: done
priority: P3
area: tools
owner: codex-windows-video-validation
claimed_at: 2026-10-08T17:08:02Z
created_at: 2026-10-07T10:24:13Z
completed_at: 2026-10-08T17:26:04Z
branch: codex/windows-video-validation-20261009
depends_on: []
scope:
  - tools/video/core/project-lease.test.mjs
---

# Make project lease test children use portable Windows imports

## Why

On Windows with Node24.19, both cross-process lease tests fail because the holder
exits1 before reporting held. The generated ESM child imports a native absolute
path produced by fileURLToPath; Node rejects the c: URL scheme. This was observed
in the full tools run during article-localization validation.

## Definition of done

- [x] Both cross-process holder tests complete on Windows.
- [x] Both cross-process holder tests complete in exact-head Linux CI.
- [x] Real live/dead-holder and retained-byte assertions remain meaningful.
- [x] Test children terminate on failures without touching unrelated processes.

## Steps

- [x] Pin the actual holder import and observed two failing tests.
- [x] Use a portable file URL in the generated ESM test script.
- [x] Run the complete affected file on Windows and prove the old import fails.
- [x] Verify cleanup when an assertion fails after the child has acquired its lease.
- [x] Verify the required Linux CI suite on the new branch head.

## How to verify

Run node --test tools/video/core/project-lease.test.mjs with the supported bundled
Node on Windows, then the exact-head Linux tools CI. No project-lease production
behavior has been changed or diagnosed as broken by these platform test failures.

## Notes

Full local tools run exited1. The separate existing automation test import,
reference-analysis range and from-drama brightness tickets remain unchanged.

2026-10-09 repair and local evidence (bundled Node v24.19.0, Windows ARM64):

- The child imports the existing module URL via `new URL(..., import.meta.url).href`; production `project-lease.mjs` is unchanged.
- Cleanup is registered before readiness is awaited. The test captures child diagnostics, bounds readiness at 10 seconds and exit/release/cleanup at 5 seconds, destroys its own pipes, and awaits its own child termination on assertion failures. Graceful releases must exit with code 0; live-holder refusal, unchanged lease bytes, exit-hook removal, killed-holder retention and dead-record takeover assertions remain.
- Complete `tools/video/core/project-lease.test.mjs`: 6/6 passed, exit 0. An isolated copy in a path containing spaces, `#` and Chinese characters also passed 6/6.
- Restoring only the old native-path import in that isolated copy failed both cross-process tests with `ERR_UNSUPPORTED_ESM_URL_SCHEME`, exit 1 in 598 ms.
- Forcing an assertion failure immediately after the holder became ready exited 1 in 540 ms; the recorded child PID no longer existed after test cleanup. No unrelated process was stopped.
- Raw output and a source-bound receipt are outside the repository at `<home>/mokaair-work/windows-video-validation-20261009/project-lease-proof-1VXWtP/`. Reviewed test SHA-256: `ecbc4566de7d365fa8934e90d808d37b713669a3ed2172ac96707d9acbf85ecc`.

Linux CI remains pending. This file is not in the long-form duration receipt registry, and no shared receipt was changed for this test repair.
### Cross-platform closeout

PR #1391 at `ea02610af9742b3893261564ab7433cf7ae67648` passed Ubuntu video-tests and web-checks. The media-equipped tools job completed 2,202 tests: 2,201 passed, zero failed/cancelled, one existing API-runtime skip; docs-video passed 199/199. Web-checks completed 2,178 passes with 13 environment skips and no failures. This validates the same committed test changes as the Windows focused runs above. The independent sync-test duration increment is `3acd739f4`; all 473 plans and both receipt tests pass. Remaining intermittent journal rename contention is handled separately and does not change this fixture/assertion fix. This implementation closure does not authorize merge or deployment.
