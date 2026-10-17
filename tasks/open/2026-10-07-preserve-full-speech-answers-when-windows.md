---
id: 2026-10-07-preserve-full-speech-answers-when-windows
title: Preserve full speech answers when Windows blocks journal promotion
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-07T04:46:57Z
completed_at:
branch:
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
`C:\Users\x8120\mokaair-work\llm-language-completion-20261007\journal-recovery`.

## Definition of done

- [ ] A valid complete provider answer survives confirmed-receipt rename failure
  and is reused after restart, with full byte/request provenance retained.
- [ ] Missing, changed, partial or uncertain answers still hold; never automatically
  clear/forget a request or call a provider again to repair local journal I/O.
- [ ] Cover injected promotion failures and interrupted/repeated local recovery.

## Steps

- [ ] Inspect current journal ownership and existing generic rename retries first.
- [ ] Implement a narrowly guarded journal recovery/promotion path and tests.

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
