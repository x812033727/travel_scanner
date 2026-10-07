---
id: 2026-10-07-imported-language-runner-hides-native-speech
title: Imported language runner hides deferred native dub speech holds
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T03:03:54Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/imported-long-languages/runner.mjs
  - docs/videos/imported-long-languages/runner.test.mjs
---

# Imported language runner hides deferred native dub speech holds

## Why

The actual imported-language runner loses the native dub's held speech reason. The
test `actual runner and native dub keep an unknown speech POST held across invocations`
fails at `runner.test.mjs:744`: it expects `/saved result is held/`, but receives
`Dub did not produce a checked track or an explicit skip reason`.

An isolated Windows run on 2026-10-07 used bundled Node v24.19.0 with its directory
prepended to PATH. The unchanged repository test completed with actual exit 1,
1 test / 0 pass / 1 fail, in 5.888 seconds. This is an assertion failure, not a
native Node crash or a missing full-suite summary.

The source trace is platform-independent: the imported speech journal returns a
409 `video_speech_result_held`; the native speech client classifies it as a service
error and dub returns code 4. `Automation.makeDub` calls `defer`, which marks the
video skipped and saves its wait without setting `halted` or `status=blocked`.
`runner.mjs:829` checks only those two states, continues, then replaces the native
held reason with the generic missing-track error at line 837.

The no-repeat paid boundary still works. An external diagnostic copy of the same
fixture completed two invocations using only its fake fetch: POST count stayed 1,
the imported journal kept one `unknown` entry with the current final identity,
both native dub command events retained code 4 and the held detail, and neither
invocation produced checked or skipped dubs. This ticket concerns preserving the
native wait/hold outcome in the runner; it is not a duplicate-payment incident.

## Definition of done

- [ ] A deferred native dub ends the imported-language unit with its original
      wait/hold reason instead of continuing into the generic missing-track error.
- [ ] The unchanged unknown-speech integration case passes across two invocations:
      one provider POST, one retained unknown journal entry, no checked/skip receipt.
- [ ] A normal completed dub still requires its checked track or explicit skip;
      source, STOP, identity and no-repeat paid guards remain intact.

## Steps

- [ ] Trace the native dub result through `Automation.makeDub` and runner's unit
      completion check, including Automation's per-video deferral/skip outcome.
- [ ] Repair only the imported runner's handling of that outcome and add the
      smallest necessary regression in `runner.test.mjs`; preserve journal bytes.
- [ ] Run targeted offline tests and record complete logs and actual exit codes.

## How to verify

From the repository root, with dependencies installed and the verified bundled
Node directory first in PATH:

```powershell
$nodeRuntimeDir = 'C:\Users\x8120\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin'
$env:PATH = $nodeRuntimeDir + ';' + $env:PATH
& ($nodeRuntimeDir + '\node.exe') --test --test-reporter=tap --test-name-pattern 'actual runner and native dub keep' 'docs\videos\imported-long-languages\runner.test.mjs'
$LASTEXITCODE
```

This fixture supplies fake HTTP and generated test bookends; it must make no live
production/provider request. If comparing the pinned worker image, use network
none, a read-only test-source mount and no production home/credential mounts.

## Notes

- Filed unclaimed during read-only diagnosis of the incomplete Windows full run.
  No repository code, production profile, STOP/hold, provider or media state was
  changed. Production dubs remain held.
- Actual original failure evidence is preserved outside Git at
  `C:\Users\x8120\mokaair-work\handoff\renewed-finals-20261007\native-runner-r3-unknown-speech-isolated-20261007.log`
  and its adjacent `.exit.json` (exit 1).
- Two-invocation evidence is in
  `native-runner-r3-unknown-speech-diagnostic-20261007.log` and its `.exit.json`
  in that directory. The external diagnostic copied the test, rewrote only its
  import locations and printed the error/count/event assertions so execution could
  reach the second invocation. Its exit 0 means diagnostic completion, not a pass
  of the unchanged repository test. The POST-count, unknown-journal and empty
  checked/skipped assertions still ran.
- The R3 language-submission caller fix changes `submitSnapshot`'s project argument
  at line 851 and does not change this earlier dub-outcome path. Do not expand this
  ticket into shared speech-client or Automation behavior unless new evidence
  proves that necessary and its scope is explicitly updated.
- Related but different existing ticket:
  `2026-10-05-imported-language-runner-test-still-expects` addresses the saved-WAV
  consumer-interruption fixture after the native dub acquired its own journal.
  It does not cover this lost deferral reason.
