---
id: 2026-10-03-anime-input-test-windows-junction
title: Anime input test Windows junction
status: done
priority: P3
area: tools
owner: codex-anime-input-windows-20261003
claimed_at: 2026-10-03T13:24:11Z
created_at: 2026-10-03T13:09:36Z
completed_at: 2026-10-03T13:39:48Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - tools/video/production/anime-input.test.mjs
---

# Anime input test Windows junction

## Why

The complete local tools run captured three `EPERM` failures when the anime
production-input tests created directory/file symbolic links on Windows without
symbolic-link privileges. These fixtures must still exercise real filesystem
aliases and reject linked source entries before opening them. Changing operating
system permissions or skipping the security assertions is unnecessary.

## Definition of done

- [x] All existing anime input cases pass on Windows with real junction metadata;
      non-Windows fixtures keep their original symbolic links.
- [x] Linked source routes/entries and output through a repository alias are still
      rejected, and the canonical source pack remains unchanged.
- [x] An independent reviewer updates the affected duration binding without
      removing any of the 108 entries or prior review history.

## Steps

- [x] Preserve the original full tools log: 1,442 cases, 1,428 passed, 5 failed,
      9 skipped. Three failures are this ticket's exact link-creation `EPERM`s;
      task-note hygiene and the separate assembly fixture failure have other fixes.
- [x] Verify current ownership and claim only this test-file scope.
- [x] Use actual Windows junctions for link fixtures, with explicit real symbolic
      link metadata; keep all original refusal and offline/write assertions.
- [x] Run the complete focused module and independent duration/task validation.

## How to verify

```bash
node --test tools/video/production/anime-input.test.mjs
node tools/video/long-form/cli.mjs check
node --test tools/video/long-form/review.test.mjs
npm run check:tasks
```

No provider, import, activation, media generation or production operation is
required. Complete tools CI must be evaluated at the actual final PR head.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- Fresh independent gate inspected 495 refs, 981 immutable task blobs, 28
  worktrees and 32 live remote heads, then refreshed main/open PRs. No active
  collision; normal claim succeeded without force. Gate SHA256
  `a094bbdf5061742a93f6804a3800bc37dfeec39e573333189c25787957770fd2`.
- Three original fixtures now use real directory junctions on Windows and keep
  their original directory/file symbolic links on other platforms. Each fixture
  explicitly verifies `lstatSync(alias).isSymbolicLink()`; the canonical-entry
  fixture still substitutes only actual link metadata and restores the original
  function in `finally`. No production adapter or operating-system setting changed.
- Complete focused module: 15/15 passed, zero failures/skips, actual primary
  Node 24.19.0, 12.129 seconds. All 35 tracked source-pack hashes are identical
  before and after the run. Private receipt:
  `<home>/.codex/tmp/anime-input-windows-junction-20261003/implementation-final.json`;
  final test SHA256 `76b4082fd9245ea331c04d430f82aa5e4afa742d4f830c0794531cc4bbe80d02`.
- Independent duration binding and final Linux tools CI remain pending. The
  original complete Windows run's three link-creation failures are retained;
  focused green is not represented as a complete tools-suite pass.
- The independent reviewer subsequently refreshed exactly three affected
  bindings, including this file, while preserving all 108 entries, the previous
  eight-binding increment and every historical paragraph. Actual CUA Node
  24.21.0: all 473 plan checks and both receipt tests passed, zero skips, exit 0.
  Private `anime-input-windows-junction-20261003/duration-increment/validation-receipt.json`,
  SHA256 `905c0547f41892ceb11b87331153103fc4fc74cca4f200394d00fd8fedb9e8f4`.
  This supersedes only the pending independent-binding note; complete Linux CI
  and final task validation are still required before archive.

### 2026-10-03 verified tools acceptance and archive

At exact PR head `641e2576a2212550db384cfe5b9d3a3dc98b0b8f`, the complete
Linux `npm run test:tools` selected 1,454 cases: 1,453 passed, zero failed,
one optional browser-render case skipped, exit 0 (49.423 seconds). No existing
test or security policy was weakened. The same web-checks job passed lint,
five-language i18n, typecheck and all 1,352 task records. The original Windows
failure receipt is preserved; this separate Linux receipt supersedes only the
earlier pending whole-tools/task/POSIX notes.

Immutable [web-checks job](https://github.com/x812033727/travel_scanner/actions/runs/37126555983/job/111212893771).
Scoped source bytes and independent duration bindings match the tested commit.
This completes this local implementation ticket; other PR/API/service checks
are evaluated separately and no media, publication, deployment or owner
acceptance is inferred. The wider PR remains draft.
