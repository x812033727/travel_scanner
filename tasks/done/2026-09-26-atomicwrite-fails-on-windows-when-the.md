---
id: 2026-09-26-atomicwrite-fails-on-windows-when-the
title: atomicWrite fails on Windows when the target is briefly locked (EPERM on rename)
status: done
priority: P3
area: tools
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T08:48:36Z
created_at: 2026-09-26T02:29:02Z
completed_at: 2026-09-28T09:01:03Z
branch: codex/pr896-batch-verification
depends_on: []
scope:
  - tools/video/core/paths.mjs
  - tools/video/core/paths.test.mjs
  - tools/video/tts/batch-recovery.test.mjs
---

# atomicWrite fails on Windows when the target is briefly locked (EPERM on rename)

## Why

On 2026-09-26, one full `npm run test:tools` run on Windows failed
`check-audio flags only the line Jev doubts, writes a redo file, and reuses its work`
(`tools/video/tts/check.test.mjs:132`) with:

```
Error: EPERM: operation not permitted, rename '...\review\check.json.27168.tmp' -> '...\review\check.json'
    at atomicWrite (tools/video/core/paths.mjs:52)
    at checkAudio (tools/video/tts/check.mjs:172)
```

The same file passed four times in a row on its own. Windows refuses to rename over a file that
another process holds open for a moment, for example Defender or the indexer scanning a file
that was just written. The rename fails at once, although waiting a few milliseconds would let
it through. Linux CI never sees this. The owner's machine does, and `check-audio`, `tts`,
`approve` and `auto` all save state through `atomicWrite`: one unlucky rename ends the command.

## Definition of done

- [x] On Windows, `atomicWrite` retries a rename that fails with `EPERM`, `EACCES` or `EBUSY` for a
      short, bounded time before giving up, the way graceful-fs does. Other platforms and other
      errors behave as before.

## Steps

- [x] Add the retry in `tools/video/core/paths.mjs`, with a test that fakes a rename failing twice.

## How to verify

`node --test tools/video/core/*.test.mjs`. On Windows, `npm run test:tools` run a few times in a row.

## Notes

Seen while working on `2026-09-26-the-render-font-check-fails-slides`, which does not touch
`paths.mjs`.

2026-09-28 merge follow-up: the integrated PR #896 TTS suite reproduced the same failure
(42 passed, 1 EPERM failure). No open PR changes paths.mjs, and this existing ticket was
unclaimed. The fix also supplies the missing committed cross-scene batch recovery check:
retain the first 40 paid judgments after the next batch fails, then resume only the rest.

Implemented a maximum of six retry waits (10, 20, 40, 80, 160, 320 ms), only for the three
Windows lock errors. The complete temporary file is written once. The old destination
remains intact until rename succeeds; persistent errors are rethrown unchanged. Tests inject
transient and permanent locks and verify unchanged immediate failure on other platforms or
for unrelated errors. Existing two-argument callers use the real platform and filesystem.

Validation on Windows, Node 24.19:

- Before: integrated TTS suite 42 passed and 1 real EPERM rename failure; the eight new
  fault-injection tests also failed against the old implementation.
- After: core paths plus all TTS tests 52/52 passed, including the 90-scene interrupted-batch
  recovery test. No real API, speech, model account, or paid request was used.
- Two complete tool-suite runs with `--test-concurrency=1`: each 518 passed, 0 failed,
  1 existing skip (`pull-images.sh`: Bash cannot see the Windows temporary directory).
  Both commands exited 0. Serial execution bounds this shared host's test load without
  changing assertions, CI settings, test timeouts, or runner retries.
- Full tool runs include every `tools/video/core/*.test.mjs` test.

Logs remain in the watcher worktree's ignored `test-results/pr896-atomic-tts-after.log`
and `pr896-tools-after-{1,2}.log`. This fixes the reproduced transient rename failure;
it does not claim to identify which Windows process held the file open.
