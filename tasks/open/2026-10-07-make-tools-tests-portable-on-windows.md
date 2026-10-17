---
id: 2026-10-07-make-tools-tests-portable-on-windows
title: Make tools tests portable on Windows without hanging
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T11:22:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/automation.test.mjs
  - tools/claude-code-series.test.mjs
  - tools/reference-analysis.test.mjs
---

# Make tools tests portable on Windows without hanging

## Why

The full tools suite cannot finish cleanly on the operator's Windows ARM64 machine using the bundled Node 24.19.0. An automation test child stays active after ERR_UNSUPPORTED_ESM_URL_SCHEME reports a drive-letter import. The same suite succeeds in Linux CI at the exact observed commit. Two earlier local failures also need isolated reproduction before assigning their cause.

## Definition of done

- [ ] On Windows, the automation test child uses valid module URLs and closes all processes/servers even when a child fails.
- [ ] Reproduce the syntax-checking and reference-analysis failures in isolation; fix only confirmed portability defects, or record the measured environment cause.
- [ ] Relevant Windows tests and Linux tools checks pass without relaxing assertions or treating a killed suite as success.

## Steps

- [ ] Inspect the child-launch path and cleanup around the observed failing automation case.
- [ ] Run the three scoped tests separately and compare with Linux before changing them.

## How to verify

Use bundled Node 24.19.0: `node --test --test-concurrency=1 tools/video/automation/automation.test.mjs tools/claude-code-series.test.mjs tools/reference-analysis.test.mjs`. Capture actual exit and closed child processes. Run the Linux full tools suite on the proposed fix.

## Notes

Observed against `8cd839e58763edc9c20cbf672025b238a270b5e6` plus a public-evidence path repair; the three scoped test implementations were unchanged. Outside-Git logs: `<home>/mokaair-work/ai-teaching-continuation-20261007/logs/20261007-hygiene-test-tools-bounded.stdout.log` and its start/exit receipts. With concurrency 2, the log stops after an automation child emits `ERR_UNSUPPORTED_ESM_URL_SCHEME` for protocol `c:`; a fresh CIM observation identified `tools/video/automation/automation.test.mjs` as the surviving child. The coordinator stopped only that verified test process tree at 11:16:22Z; exit 1 is NOT_PASS, and no full test count is asserted. Earlier cases named `published JSON examples parse and JavaScript examples pass native syntax checking` and `--compare matches the measured cuts against a study record's lists` fail in this same run, but their causes are not yet isolated. Linux GitHub job `112761333902` passes the complete tools step on `decd3bf69c001ab58795dd26a61d6977f03197f4`. This task does not cover the separate Windows speech journal's confirmed-answer persistence ticket.
