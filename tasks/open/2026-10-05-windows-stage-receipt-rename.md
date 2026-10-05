---
id: 2026-10-05-windows-stage-receipt-rename
title: Handle a transient Windows rename denial while preserving stage receipt durability
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T11:22:44Z
completed_at:
branch:
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

- [ ] A temporary Windows rename denial can settle the same receipt without
      losing its original request/result identity or exposing partial bytes.
- [ ] Preserve mode 0600, fsync and exclusive temporary-file creation; an earlier
      receipt remains intact if saving cannot complete.
- [ ] Permanent filesystem errors still fail clearly; no paid operation is
      reissued because saving its reply failed.
- [ ] Linux error behavior and policy/pending/uncertain receipt contracts remain
      unchanged, with deterministic tests of the error boundaries.

## Steps

- [ ] Recheck current source and overlapping native-language/policy-hold work
      before claiming this narrow scope.
- [ ] Compare existing Windows rename handling in core/paths.mjs without
      replacing the receipt store's stronger mode/fsync contract.
- [ ] Add a bounded, injectable error test and validate preservation on failure
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
