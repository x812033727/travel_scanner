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

### 2026-10-16 additional docs-video reproduction

While validating the five brand-story document package in worktree `8a78`, the
bundled Windows Node runtime returned exit 1 from `test:docs-videos`: 215 tests,
214 passed, one failed. The failing test was
`docs/videos/curio-five-recuts-20261012/speech.test.mjs:101`,
`audio check uses cached transcripts/Jev and binds the aligned outputs without claiming owner approval`.
Its mock `zh-TW/audio/speech-journal/<hash>.json.<pid>.tmp` rename to `<hash>.json`
failed with `EPERM` (`errno -4048`). The stack was `core/paths.mjs:60 atomicWrite`,
`tts/speech-journal.mjs:77 durableWrite`, and `:318 sendOnce`.

A single isolated rerun using `node --test --test-name-pattern
"audio check uses cached transcripts/Jev"
docs/videos/curio-five-recuts-20261012/speech.test.mjs` also exited 1 with the same
stack, this time under the mock `ko/audio/speech-journal` directory. This is a
second observed failure, not a passing retry; the lock holder and root cause
remain unknown. No production provider or journal was used, and no implementation
change was made. Add this exact test path to scope before a repair touches it.

Evidence retained locally under
`%TEMP%/a01-switchable-cc-20261015-1421/five-next/`:
`docs-videos-check.log` and `docs-videos-failed-case-rerun.log`.
The follow-up stays open; this note only adds reproduction evidence.
