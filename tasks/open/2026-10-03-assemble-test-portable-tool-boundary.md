---
id: 2026-10-03-assemble-test-portable-tool-boundary
title: Make assemble auto-fit test tool boundary portable
status: review
priority: P2
area: tools
owner: codex-assemble-portable-20261003
claimed_at: 2026-10-03T13:21:44Z
created_at: 2026-10-03T13:20:47Z
completed_at:
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
---

# Make assemble auto-fit test tool boundary portable

## Why

The native auto-fit regression creates JSON stand-ins for MP4 clips and Unix
shebang stand-ins for ffmpeg/ffprobe. On Windows the resolver looks for `.exe`,
skips those fake executables, then falls back to the host PATH. A real ffprobe
tries to decode the JSON clip and fails with `moov atom not found`, before the
test reaches the natural-speed preflight assertion.

## Definition of done

- [ ] The native auto-fit regression runs without a host ffmpeg installation or
      platform-specific executable fixtures, on Windows and POSIX.
- [x] It proves every directed clip is probed, rejects the short eight-second
      action at natural speed, and starts no encoding or segment directory.
- [x] Existing CLI callers retain the exact default tool resolver, execution,
      environment, and duration behavior; the full assemble test module passes.
- [x] An independent reviewer refreshes the two existing duration bindings.

## Steps

- [x] Diagnose the recorded Windows failure and clear exact source/task scope.
- [x] Normally claim the task; add a default-preserving optional tool boundary.
- [x] Replace Unix executable stand-ins with injected tool replies and keep the
      existing natural-speed/no-encoding assertions, adding complete probe order.
- [x] Run the focused assemble module after the coordinated web typecheck.
- [ ] Obtain independent source review and duration receipt increment.
- [ ] Recheck task hygiene and record final validation before archival.

## How to verify

`node --test tools/video/assemble/assemble.test.mjs`; `git diff --check`;
`node tools/tasks.mjs check`; independent duration review followed by
`node tools/video/long-form/cli.mjs check`. Root coordinates the complete tools
suite; this ticket does not rerun it concurrently with other heavy checks.

## Notes

- Baseline: `<home>/.codex/tmp/task-continuation-20261003/test-tools-final.log`
  lines 1498-1507 records the real ffprobe decoder error; the accompanying time
  receipt and exit file record exit 1, 1442 selected tests, 1428 passed, five failed
  and nine skipped. The other four failures are separate work.
- Collision gate: `<home>/.codex/tmp/assemble-native-fixture-20261003/four-path-gate-final.json`
  SHA256 `237ffb23ca8bf32e0a24751f31532ca424b708b0c14819d6d4791ef5e18e8bdf`.
  Main `a9c8e2b7e2b0a44cea5c9766e1699785c259c96f`; 495 refs, 28 worktrees,
  32 live remote heads and both open PRs were checked. No active implementation,
  dirty scope or active claim overlaps; normal claim succeeded without force.
  Old branch deltas are either exact main-history blobs, a scoped patch identical
  to merged #1094, or stale ancestry of merged #1139.
- Both source files remain bound by `docs/videos/long-form/review.json`.
  The author does not edit or self-sign that receipt. This change neither accepts
  real media nor changes production duration rules, settings, uploads or retries.
- Windows focused validation: bundled Node `v24.21.0`,
  `node --test --test-concurrency=1 tools/video/assemble/assemble.test.mjs`,
  exit 0, 15 passed, zero failed or skipped. The actual runtime path/version,
  argv, timestamps and matching pre/post source hashes are recorded in
  `<home>/.codex/tmp/assemble-native-fixture-20261003/assemble-focused-green.json`
  with its complete `.log`; elapsed wall time was 54.316 seconds.
- `<home>/.codex/tmp/assemble-native-fixture-20261003/source-scope-proof.json`
  proves that reversing only the import aliases and optional fourth-argument
  signature restores every original CLI byte. All other test cases and the three
  original natural-speed/no-encoding assertions are unchanged. Scoped
  `git diff --check` passed.
- Frozen SHA256: `cli.mjs`
  `0a179fd43024fa0d61fe88932bca19033ef261e6dca18d84a8330ca754b43b38`;
  `assemble.test.mjs`
  `93dbe7d0ec41daaf1fb44c446cf4480784501d684efb66810572bcacc429e468`.
- POSIX execution, independent duration receipt refresh, complete tools suite and
  final task hygiene remain pending. Root coordinates these checks; the author
  does not claim cross-platform execution or whole-suite success from this
  Windows focused run.
- Independent duration increment now passed: the two assembly bindings and the
  separate anime-input fixture binding were refreshed, with the complete
  108-file registry and all earlier review history retained. Actual CUA Node
  24.21.0 passed all 473 plan checks and both receipt tests, exit 0, zero skips.
  Private `anime-input-windows-junction-20261003/duration-increment/validation-receipt.json`
  SHA256 `905c0547f41892ceb11b87331153103fc4fc74cca4f200394d00fd8fedb9e8f4`.
  POSIX/complete-tools CI and final task validation remain pending.
