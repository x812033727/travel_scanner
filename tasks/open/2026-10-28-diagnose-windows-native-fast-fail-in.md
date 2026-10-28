---
id: 2026-10-28-diagnose-windows-native-fast-fail-in
title: Diagnose Windows native fast-fail in full tools test run
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-28T02:37:41Z
completed_at:
branch:
depends_on: []
scope:
  - package.json
---

# Diagnose Windows native fast-fail in full tools test run

## Why

The full tools suite on Windows ARM64 / Node v24.13.0 reports 1,487 passes,
64 failures and 23 skips (actual exit 1). Several failures terminate entire test
files without a JavaScript error. A focused two-file rerun also fails, and running
`tools/animation-camera.test.mjs` directly ends with native exit -1073740791
(`0xC0000409`) and no diagnostic output. Localization geometry/artifact tests
pass 25; these full-suite failures remain unresolved.

## Definition of done

- [ ] Identify the native failure with a bounded reproducer and supported-runtime comparison.
- [ ] Retain actual process exits and resolve the cause without hiding failed checks.

## Steps

- [x] Retain full-suite, focused two-file and direct native-exit evidence.
- [ ] Minimize the unchanged camera/video import and compare supported Node runtimes.

## How to verify

Run the reproducer and complete suite on the corrected supported Windows runtime
and compare with protected CI. Scope initially covers the runtime/test entry in
package.json; narrow any implementation after identifying the cause.

## Notes

The failing camera/package sources were not changed by localization. Exact logs
remain in private retained work. Dependency engine warnings require Node >=24.15.0
or the supported 22.x range; that is a lead, not proof of the crash's cause.
Existing Windows test tickets retain their separate obligations. No video code
was modified and no broad tools PASS is claimed.
