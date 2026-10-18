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

The final complete Windows run at `14bbdb59d9f5f27ae167623edf9d6152d30bfc8b` finished with exit 1: 2,173 passes, one failure and 13 skips out of 2,187 tests, in 683.7 seconds. `dubs/freshness.test.mjs:196` still exhausted nine atomic-rename attempts over 2,637.55 ms. This is a remaining failure, not a passing Windows validation or a completed repair. The exact case subsequently passed 32 bounded runs at concurrency four; this intermittent non-reproduction does not close the issue. The same source passed Windows docs 199/199 and exact-head Linux web, video and all five smoke routes. Evidence: `repaired-tools-result.json`, `repaired-tools-test.log`, `repaired-persistent-journal-eperm-pid36216.json`, `freshness-contention-stress-result.json`, and `ci-watch-98wwy1/pr1391-14bbdb59d-SUMMARY.md` under the external evidence directory.

Read-only Windows Restart Manager diagnostics have a verified positive control: they identify an independent PowerShell FileStream holder. A real transient probe arrived after the fixture was removed, so its empty owner list is inconclusive; a preloaded resident probe avoids that startup delay. Official Node v24.19 sources close ordinary UTF-8 read handles synchronously, and a 2,000-rename experiment reproduced transient EPERM without reading the destination at all. Do not attribute the unresolved conflict to GC, antivirus, or a named external process without further evidence. No security settings, runtime installation, provider calls, or another task's journal recovery files were changed.

Further bounded fake-provider journal diagnostics reproduced a persistent condition: eight replacements still failed after an additional 15 seconds each; one remained Win32 error 5 at least 156.9 seconds after the first failure and after its writer exited naturally. The warm Restart Manager probe queried while files still existed and found no holder. Both files have matching normal owner/DACL access, DELETE access succeeds, exclusive read succeeds, no reparse point or delete-pending state exists, and names contain only expected ASCII. Same-byte fresh copies replace successfully. After separately verified backups, both original identities could be renamed to unused sibling names and restored without changing hashes. This narrows the failure to replacing the original destination under its file/OS state; it does not establish a particular mapped-section owner or security product. Increasing retries again is not a justified fix. Trace-open EBUSY from the diagnostic logger was excluded as instrumentation, not product failure.

The original evidence and all complete replacement bytes remain preserved. No provider request was repeated and no real provider/network call was made. Every diagnostic process ended. See `persistent-rename-diagnosis.md`, `journal-release-stress-summary.json`, `preserved-rename-writer-alive.json`, `preserved-rename-writer-exited.json`, `preserved-native-delete-access.json` and `preserved-reversible-identity-moves.json` under the external evidence directory. This task stays unfinished: the current PR fixes the proven path/ffmpeg issues and handles the controlled temporary sharing lock, but does not resolve the persistent Windows replacement failure. Continue from this preserved case rather than repeatedly running until a green suite or changing security settings without a diagnosed cause.

Follow-up native diagnostics retained fresh backups before each synthetic-file operation. The older preserved pair eventually accepted normal MoveFileEx after roughly 35 minutes; that bounds a long-lived transient condition but does not identify its cause. Three new failing pairs still rejected MoveFileEx with Win32 error 5 and native classic rename with STATUS_ACCESS_DENIED, then accepted ReplaceFileW with flags 0. New target bytes and prior backup bytes were verified by SHA-256. However, Microsoft documents ReplaceFileW failures 1176/1177 that can leave the requested target absent. The current journal treats a missing entry as permission to create a new request; restoring a backup after the native call does not protect a concurrent reader or interruption. Independent review rejected a transparent ReplaceFileW fallback, even though its successful samples would make the tests greener.

FileRenameInformationEx with REPLACE_IF_EXISTS and POSIX_SEMANTICS also failed with STATUS_ACCESS_DENIED on two original failing pairs. The same operation succeeded on a same-byte copied-file control, ruling out a simple unsupported API/buffer explanation. No helper was added, no bypass/ignore-ACL/read-only flags were used, and security settings were unchanged. The bounded probe made 317 mock calls and zero external or paid calls; its child processes ended. The current core still preserves the old target, complete temporary bytes and native error on exhausted retries.

No validated core-only fix is established. A ReplaceFile-based design would require coordinated durable per-request recovery and exclusion across journal reads, initial creation, waiting claims and updates before any target can disappear. Unknown recovery state must prevent dispatch, and recovery must never overwrite a newer entry. That changes another active task's journal protocol and is outside this claim's narrow scope. Preserve this unfinished status for coordinated follow-up; do not merge a native fallback based solely on the successful replacement samples.

Final external evidence: `native-diagnostic-final-receipt.json` indexes nine hashed diagnostic artifacts and preserved byte backups; `native-replacement-research-and-design.md` has SHA-256 `abc1389c439df78fa164f01c12d975434fc4c019228dc44257ad1a1fe3056404`; `independent-native-replacement-review-20261009.md` has SHA-256 `ec67b5d87fa282d9038eaa6b5cd3478ef7114218d8560a13f1fbb2df73fecb69`. See the [Microsoft ReplaceFileW failure contract](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew) and [rename information flags](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_rename_information). Exact-head Linux CI at `a8ed0405e87b92de531d37e4f9050a1d49c2308e` is green, including tools 2,202 passes / 2 skips, docs 199 passes, web 2,179 passes / 14 skips and all five smoke flows; this does not close the remaining native Windows failure. The aggregate receipt is `ci-watch-98wwy1/latest-4514d8059-a8ed0405e-summary.json`.
