---
id: 2026-10-07-preserve-speech-journal-writes-through-windows
title: Preserve speech journal writes through Windows rename contention
status: in-progress
priority: P2
area: tools
owner: codex-windows-video-validation
claimed_at: 2026-10-08T17:10:18Z
created_at: 2026-10-07T04:08:54Z
completed_at:
branch: codex/windows-video-validation-20261009
depends_on: []
scope:
  - tools/video/core/paths.mjs
  - tools/video/core/paths.test.mjs
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

Adopted the existing unclaimed ticket from PR #1359 after five fresh caller failures in the complete Windows run on 2026-10-09. Scope is narrowed to core atomic-file handling and its tests: another active branch owns retained-answer recovery in `speech-journal.mjs`, and that branch remains untouched. Diagnose the real filesystem cause before selecting a repair; do not assume that a longer retry is sufficient. If these PRs are later integrated together, retain this task's final status rather than reintroducing its earlier open copy.

The initial 137-file Windows validation recorded five EPERM replacements after fake-provider responses (among ten total failures). These are real failed tests, not accepted results. Paths were in distinct temporary directories and below 260 characters; fixture cleanup removed the original files, so their attributes and external handle owners could not be established afterward. The same five cases passed both serially and at concurrency four; all five complete affected files then passed 74/74 at concurrency four. A diagnostic native-fs wrapper recorded no rename error or known leaked journal descriptor in those runs. This does not prove an antivirus cause or justify increasing the existing 630 ms retry budget. No core file or provider behavior has been changed. A coordinated full rerun with the external diagnostic preload will preserve any observed attempts and timings; see `<home>/mokaair-work/windows-video-validation-20261009/speech-journal-eperm-diagnosis.json` and the final-run receipt.
