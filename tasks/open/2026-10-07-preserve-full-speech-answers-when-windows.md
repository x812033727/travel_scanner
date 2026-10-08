---
id: 2026-10-07-preserve-full-speech-answers-when-windows
title: Preserve full speech answers when Windows blocks journal promotion
status: in-progress
priority: P1
area: tools
owner: codex-windows-journal-recovery
claimed_at: 2026-10-08T01:09:19Z
created_at: 2026-10-07T04:46:57Z
completed_at:
branch: codex/windows-atomic-write-retry-20261008
depends_on: []
scope:
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
---

# Preserve full speech answers when Windows blocks journal promotion

## Why

On Windows, native selected-language synthesis twice received a complete valid
provider WAV, wrote the confirmed JSON temporary file, then failed with EPERM
renaming it over the earlier `sent` receipt. The command exits 1 and the next
native run would see `sent`, although the full answer exists locally. Increasing
ordinary rename waits did not resolve the two inspected files.

Observed during `ai-term-large-language-model` language completion:

- ja request `24c123dd59fe4d934bcf7cfeebe3a0939d16f574dcf6fdd0144c669732d5ad6a`
- en request `a754e4d8e59cfcdf2881fec517f76d8b505db91a69dada39c7e4e9732e8c48ba`

The operation independently archived the original sent receipt, actual confirmed
temporary receipt and full WAV, checked exact request/sent identity, actual full
WAV SHA/bytes/PCM and dead producer PIDs, then completed only the local receipt
promotion. Native synthesis subsequently reused the answer without calling the
provider again. Private evidence is under
`<home>/mokaair-work/llm-language-completion-20261007/journal-recovery`.

## Definition of done

- [x] A valid complete provider answer survives confirmed-receipt rename failure
  and is reused after restart, with full byte/request provenance retained.
- [x] Missing, changed, partial or uncertain answers still hold; never automatically
  clear/forget a request or call a provider again to repair local journal I/O.
- [x] Cover injected promotion failures and interrupted/repeated local recovery.

## Steps

- [x] Inspect current journal ownership and existing generic rename retries first.
- [x] Implement a narrowly guarded journal recovery/promotion path and tests.

## How to verify

Use the existing speech-journal unit suite with injected EPERM during confirmed
receipt promotion. Assert that a restart uses the exact saved response without a
second provider request, while changed/missing/partial response cases still hold.
Exercise both full WAV answers and inline ASR/Jev answers, exclusive ownership,
interrupted recovery, full hashes/bytes, and preservation of evidence on failure.

## Notes

Two further English requests needed the same guarded local promotion during the
operation. Their full sent/confirmed receipts, WAVs and recovery receipts are in
`runtime-journal-recovery`, while the two initial recoveries are in
`journal-recovery`. The private workaround leaves orphan confirmed temporary
files as evidence; an offline transfer accepts them only when complete recovery
proof, exact bytes, dead producer and native release all match.

This is an open native-tool defect. The one-time recovery and runtime shim do not
constitute a repository or production fix. Do not blindly clear journal entries,
force an entire language, or re-buy an answer to repair local file promotion.

2026-10-08 native repair (`codex-windows-journal-recovery`):

- Reused this existing ID and its original text from the pending
  `codex/llm-selected-language-completion-20261007` branch. It was not present in
  origin/main `af596412c8f433b184c1e544d432f44145f666a8`; no second ticket was
  invented. Integration of that branch must retain this task's completed record
  rather than reintroduce its earlier open copy.
- Fresh ownership audit examined 33 worktrees and 12 open PRs: neither scoped
  journal file was dirty, claimed, or in an open PR. Normal claim succeeded;
  no force, other-owner release, or production/media/journal modification occurred.
- Generic `atomicWrite` already retries Windows EPERM/EACCES/EBUSY seven times
  with 630 ms total waiting. Exhaustion is the failure condition; this repair
  does not change that helper or retry a provider request.
- New sent receipts carry a unique generation and producer PID. A complete,
  fsynced write-once `request.answer.json` is staged before canonical confirmation.
  A failed canonical promotion still reports the real filesystem failure.
- A later native run reuses only a complete confirmation bound to exact sent
  bytes, the incoming request/route, and a definitively closed producer. Legacy
  `request.json.PID.tmp` receipts additionally must reconstruct the exact original
  sent JSON. Unknown/live producer, changed generation, conflicting answers,
  missing/corrupt WAV, bad inline schema/hash, held or unreadable canonical all hold.
- Recovery leaves canonical sent untouched and first preserves exact sent,
  confirmation, source files and full WAV in immutable content-addressed evidence
  with an exclusive proof. Archive directories reject symlinks/junctions; archives
  never authorize another request. Reuse has zero new billable characters and is
  not voice/language approval. Caller release is bound to the consumed generation,
  preventing an older reader from deleting a newer intentional retake.
- Independent protocol review reproduced and then verified the junction guard
  and ordinary-reuse snapshot guards. The three extra guard suites passed 5/5;
  a real closed-child producer test passed 1/1 using the default PID probe and
  zero parent sender calls. New three-route and corruption/recovery cases passed.
- Negative regression used a private archive of unchanged origin/main tooling:
  the new three-route suite failed 4/4 as expected. No live endpoint or paid request.
- Own bundled Node 24.19.0 `npm ci`: 547 packages, exit 0. Task check validated
  1,634 files, exit 0; syntax and whitespace checks passed. Windows complete journal
  runs initially passed 55/56 twice, with different existing normal consumers
  hitting actual 630 ms canonical rename exhaustion; this is not claimed green.
  Final focused journal suite passed 62/62, exit 0, including the actual closed
  child/default-PID restart test. Full tools and CI results are recorded below
  when complete.
- Private ownership/check/negative-regression evidence is retained under
  `<home>/mokaair-work/windows-journal-recovery-20261008`.
