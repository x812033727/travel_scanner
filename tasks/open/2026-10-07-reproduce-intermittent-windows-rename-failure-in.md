---
id: 2026-10-07-reproduce-intermittent-windows-rename-failure-in
title: Reproduce intermittent Windows rename failure in TTS STOP test
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T10:25:21Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/tts.test.mjs
---

# Reproduce intermittent Windows rename failure in TTS STOP test

## Why

The TTS STOP test failed once in the full Windows Node24.19 tools run with EPERM
renaming a temporary speech-journal file to its final JSON path. It then passed
alone (1 pass,0 failures, exit0). This is an observed intermittent test/runtime
failure, without an established production cause.

## Definition of done

- [ ] Reproduce or bound the full-suite-only rename failure on Windows.
- [ ] STOP preserves actual completed takes and buys only remaining mock work.
- [ ] Record whether test cleanup/concurrency or a separately scoped implementation
      change is needed without waiving durable-journal assertions.

## Steps

- [x] Retain the full-run EPERM and exact isolated passing verdict.
- [ ] Check handles and concurrency around the atomic journal rename.
- [ ] Run affected Windows and Linux checks after any scoped correction.

## How to verify

Run node --test --test-name-pattern "a STOP file ends tts as incomplete"
tools/video/tts/tts.test.mjs and compare with the complete tools suite. Keep mock
provider boundaries; no real narration or paid runtime request should be retried.

## Notes

The isolated rerun took about2 seconds and passed. It does not convert the failed
full-suite result to a passing verdict. Production behavior remains undetermined.
