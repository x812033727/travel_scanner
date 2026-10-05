---
id: 2026-10-05-windows-stage-receipt-rename
title: Handle a transient Windows rename denial while preserving stage receipt durability
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-stage-receipt-rename
claimed_at: 2026-10-05T12:26:28Z
created_at: 2026-10-05T11:22:44Z
completed_at:
branch: claude/stage-receipt-rename
depends_on:
  - 2026-10-05-video-slides-prompt-repair-format
scope:
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
---

# Handle a transient Windows rename denial while preserving stage receipt durability

## Why

The Windows full tools run at stall-fix source 6aeb21ccc had one EPERM while
renaming a stage receipt's temporary file over its journal. It occurred in
run-receipts.test.mjs:17 during receive(), before the policy authority assertions.
The existing save() uses an exclusive mode-0600 temporary file, fsync, close and
a single rename; this low-level save implementation was unchanged by PR #1274.

The exact case subsequently passed 1/1 and the receipt suite passed 11/11.
The same source's Linux CI tools run passed 1,687/1,690 with three skips and
zero failures. The error has not been reproduced; a scanner, file lock or other
specific cause has not been established. Preserve the observed failure and
investigate bounded handling of transient Windows rename denials.

## Definition of done

- [x] A temporary Windows rename denial can settle the same receipt without
      losing its original request/result identity or exposing partial bytes.
- [x] Preserve mode 0600, fsync and exclusive temporary-file creation; an earlier
      receipt remains intact if saving cannot complete.
- [x] Permanent filesystem errors still fail clearly; no paid operation is
      reissued because saving its reply failed.
- [x] Linux error behavior and policy/pending/uncertain receipt contracts remain
      unchanged, with deterministic tests of the error boundaries.

## Steps

- [x] Recheck current source and overlapping native-language/policy-hold work
      before claiming this narrow scope.
- [x] Compare existing Windows rename handling in core/paths.mjs without
      replacing the receipt store's stronger mode/fsync contract.
- [x] Add a bounded, injectable error test and validate preservation on failure
      before choosing a repair; do not claim the original OS cause is known.

## How to verify

Run the receipt suite and client suite with the bundled compatible Node, then
the relevant tools checks. Verify the same test on Linux; test a transient
denial, a permanent denial and unchanged saved identities/bytes explicitly.

## Notes

- Observed Windows full run: 1,682 tests reached, 1,672 passed, one failed,
  nine skips, exit 1. Log SHA-256:
  dd801603c1b1f24e5bac705c5739dc5bf624ad5bf58c8ce2d4773393e6135c0d.
- Independent reproduction: exact test 1/1 passed (393.53ms), complete receipt
  suite 11/11 passed (580.22ms), both exit 0. No assertion or timeout changed.
- Linux CI run 37301485119, web-checks job 111734994754, binds source
  6aeb21cccbc54938f8e38b03fccf4432009719db; full tools zero failures.
- The production host runs Linux. This local observation is separate from the
  diagnosed slides/drama route mismatch, policy hold loop and producer handoff.
- 2026-10-05 (claude-opus-5-5-stage-receipt-rename): rechecked origin/main c12e159d0.
  `save()` still did one `renameSync`, and a refused rename left its `.tmp` file
  behind. who-is-on-it showed no active task on this scope. No open PR touches
  `run-receipts.*` or `core/paths.mjs`, including the policy-hold PR #1275 and #1254.
- Mechanism probe (Windows 11, Node 24.13.0, ad-hoc script, not committed): another
  process opened the journal with `FileShare.Read` (readers allowed, delete denied).
  Before the repair, `receive()` threw `EPERM` from `rename '<hash>.json.<uuid>.tmp' ->
  '<hash>.json'`, which is the error class of the original failure. The journal bytes
  and the in-memory record stayed intact, and one `.tmp` file was left. With
  `FileShare.None`, the read before the save fails instead. This shows that one
  mechanism produces the same error. It does **not** establish the original cause
  (scanner, indexer or other handle); that remains unknown.
- Repair, kept inside run-receipts.mjs: `renameJournal()` retries only the rename. It
  retries only on win32, only for EPERM/EACCES/EBUSY, and only on the same schedule as
  core/paths.mjs `atomicWrite` (10..320 ms, at most 630 ms of waiting, 7 attempts). Then
  it rethrows the original error. The exclusive `wx` 0600 temporary file, its
  write+fsync+close, and the single journal file are unchanged. On any failure after the
  temporary file exists, `save()` unlinks only that temporary file (ignoring its own
  error) and rethrows, so the destination journal is never touched. The archive's
  final journal move uses the same helper. `ctx.receiptIo` ({ platform, rename, wait })
  is the test seam. The schedule is duplicated rather than exported from core/paths.mjs
  to keep this ticket's scope; a shared helper there would need its own scope.
- Tests added (run-receipts.test.mjs, deterministic, injected platform/rename/wait):
  - transient EPERM×2 settles on the 3rd attempt, from the one complete temporary file,
    with waits [10, 20];
  - permanent EPERM fails after 7 attempts with waits [10..320]; the earlier journal's
    SHA-256, its request_key and receipt id are unchanged, and no `.tmp` is left;
  - linux EPERM/EBUSY, darwin EACCES, win32 ENOSPC/EXDEV each fail on attempt 1 with no
    wait;
  - `hold()` retries EACCES/EBUSY on win32;
  - the archive move survives one EBUSY;
  - the temporary file is 0600 before its rename. This last test is POSIX only and
    skipped on win32, so the PR's Linux CI tools job is its first real run.
- After the repair the same real-lock probe gave these results. When the lock was
  released inside the window, the save succeeded with the same receipt id and
  request_key and left no `.tmp` (e.g. EPERM×5 then ok, 395 ms). A 1,500 ms lock gave
  `EPERM` after 7 attempts (726 ms), with the journal unchanged and no `.tmp`.
  PowerShell's release timing is imprecise, so one nominal 150 ms hold also overran
  the window and failed cleanly the same way.
- Client check (ad-hoc, client.test.mjs is outside this scope) for a durable writer
  whose reply cannot be saved:
  - with no receipt yet, it re-POSTs only the identical body with the one saved
    request_key (the existing same-key reconnect), then stops with
    `video_ai_run_pending`;
  - with a running receipt saved, it only GETs the job by id (1 POST in total);
  - a restart settles the same key. One request_key was used overall, and no new
    paid operation was dispatched.
