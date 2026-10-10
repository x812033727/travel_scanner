---
id: 2026-10-09-windows-speech-journal-rename-failures
title: Investigate Windows speech journal rename failures under tool tests
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T17:24:33Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/paths.mjs
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/shorts/check-journal.test.mjs
---

# Investigate Windows speech journal rename failures under tool tests

## Why

The concurrent full tools run on Windows returned EPERM while atomically renaming
mock speech-journal files in three tests. The actual stacks reach atomicWrite,
durableWrite and sendOnce. This records an observed failure, without claiming a
common writer defect or guessing which process held the files.

## Definition of done

- [ ] Exact serial and concurrent reproductions distinguish platform/contention causes.
- [ ] Any repair preserves durable provider receipts and never resubmits uncertain paid work.
- [ ] Targeted tests and relevant journal/retention suites pass on Windows and Linux.

## Steps

- [ ] Claim exact scopes; inspect existing atomic-write and journal fixes first.
- [ ] Run the three observed tests serially with fresh mock fixtures and capture complete logs.
- [ ] Reproduce concurrent failure before changing retries, receipt writes or cleanup behavior.
- [ ] Implement only the demonstrated correction and retain uncertainty/retention guards.

## How to verify

Use only the existing mock-provider tests in speech-journal.test.mjs:88,
tts.test.mjs:929 and shorts/check-journal.test.mjs:115. Capture real exit codes
and the source/destination/holder state during a failed rename. Never test a paid
provider or delete an unfinished production journal to reproduce this local issue.

## Notes

Observed actual full tools exit1 with Node24.19.0 on Windows. All three errors
were EPERM rename from a temporary journal file to its final JSON; stacks name
core/paths.mjs:60, tts/speech-journal.mjs:77 and :318. No targeted rerun or cause
determination was made in the localization task. Earlier atomic-write fixes are
already done, but these new failures remain unverified follow-up work.
