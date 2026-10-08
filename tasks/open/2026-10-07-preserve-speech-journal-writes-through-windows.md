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

- [x] Reproduce the observed EPERM with a bounded Windows-only journal fixture
      and distinguish transient file sharing from a real permission failure.
- [x] Select a bounded atomic-write recovery without deleting prior evidence.
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

The initial 137-file Windows validation recorded five EPERM replacements after fake-provider responses (among ten total failures). These are real failed tests, not accepted results. Paths were in distinct temporary directories and below 260 characters; fixture cleanup removed the original files, so their attributes and external handle owners could not be established afterward. The same five cases passed both serially and at concurrency four; all five complete affected files then passed 74/74 at concurrency four. A diagnostic native-fs wrapper recorded no rename error or known leaked journal descriptor in those isolated runs. That initial evidence did not justify a retry change; the later complete run supplied the missing evidence below.

The complete instrumented Windows run at source head `3acd739f4725c9e5eaeaf12371ba16cd5857aab5` finished with 2,185 tests: 2,170 passes, two EPERM failures, and 13 environment skips. Native rename tracing captured seven consecutive failures over 702.94 ms in a Shorts lab journal and 698.20 ms in a drama speech journal. Both complete source and destination files existed, were writable (`100666`), had single links, and had short paths (161–175 characters). No tracked journal descriptor was open in the affected process. Other conflicts recovered in 15–26 ms. This establishes a real conflict that outlasts the old retry budget; it does not identify an antivirus product or the external handle owner.

A controlled Windows proof used a hidden, separate PowerShell process and a .NET `FileStream` opened with `FileShare.ReadWrite`, excluding delete sharing. It held the target for one second. The unchanged 630 ms policy failed with EPERM after 770.44 ms while retaining the old destination and complete replacement bytes; an external copy with a 2,550 ms scheduled wait budget succeeded after 1,365.49 ms. Both holder processes exited normally. Evidence is retained outside Git in `<home>/mokaair-work/windows-video-validation-20261009/real-windows-rename-proof.json` and `persistent-journal-eperm-pid35816.json`.

The core change adds only the next two bounded rename delays, bringing scheduled waits to 2,550 ms. It still retries only Windows EPERM/EACCES/EBUSY, never deletes the old destination, and leaves the complete temporary bytes plus the native error when the budget is exhausted. Non-Windows and other error codes remain immediate failures. No journal/provider dispatch code changed. Regression coverage includes an injected one-second conflict, a real Windows reader released by another process after the first denied rename, persistent failure preserving both versions and error identity, and non-retryable failures. A bounded wait handles temporary sharing conflicts; it is not a fix for permanent permissions.

Windows author validation after the change: the full core paths test plus the five complete affected caller files passed 84/84 at concurrency four in 19.64 seconds, with existing fake-provider call-count assertions unchanged. Temporarily restoring the old delay array made both the injected and real sharing-lock regressions fail with EPERM (`exit=1`, 1.33 seconds); the real test's failure path verified that both old destination and complete new temporary bytes survived. Restoring the change passed all ten core tests (`exit=0`, 2.24 seconds). Logs: `core-paths-and-speech-callers-fixed.log`, `core-paths-old-policy-red.log`, and `core-paths-restored-green.log` in the same external evidence directory. Full-suite rerun, independent review, receipt update, and exact-head Linux CI remain the coordinator's completion gates.
