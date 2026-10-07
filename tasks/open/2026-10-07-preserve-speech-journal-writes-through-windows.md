---
id: 2026-10-07-preserve-speech-journal-writes-through-windows
title: Preserve speech journal writes through Windows rename contention
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T04:08:54Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/paths.mjs
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
---

# Preserve speech journal writes through Windows rename contention

## Why

The complete Windows tools run on 2026-10-07 failed seven otherwise unrelated
TTS/dub/Shorts cases while atomically replacing a speech-journal JSON file.
The common stack is `atomicWrite` (core/paths.mjs:60), `durableWrite`
(tts/speech-journal.mjs:68), and `sendOnce` (line 253): Windows returns EPERM
renaming a sibling temporary JSON to the existing journal path. Source files in
that stack were unchanged by the renewed-final native-unit repair.

## Definition of done

- [ ] Contended Windows journal replacement preserves every prior paid receipt
      and either completes safely or leaves an actionable held state.
- [ ] A filesystem retry never redispatches a provider request; successful and
      unknown results remain protected across restart.

## Steps

- [ ] Reproduce the observed EPERM with a bounded Windows-only journal fixture
      and distinguish transient file sharing from a real permission failure.
- [ ] Select a bounded atomic-write recovery without deleting prior evidence.
- [ ] Verify the seven affected cases and Linux journal/crash regressions.

## How to verify

Use the existing speech-journal tests with explicit mock-provider counters and
retain the before/after receipt bytes. A failed replacement cannot authorize a
second provider POST.

## Notes

Observed cases: dubs.test.mjs:227; shorts/lab.test.mjs:339;
shorts/pipeline.test.mjs:195; tts/check-journal.test.mjs:336;
tts/check.test.mjs:354; tts/tts.test.mjs:757 and :816.
Complete raw evidence is retained outside Git at
`<home>/mokaair-work/handoff/renewed-finals-20261007/native-unit-full-tools-check-20261007.log`
and `.exit` (actual exit 1, 1,948 passes / 11 failures / 13 skips).
This ticket does not authorize any production media/provider operation.
