---
id: 2026-10-16-pr1517-narrative-duration-receipt
title: Bind PR 1517 narrative panel changes in long-form duration receipt
status: in-progress
priority: P2
area: docs
owner: codex-pr-review-1517
claimed_at: 2026-10-16T04:18:56Z
created_at: 2026-10-16T04:18:37Z
completed_at:
branch: codex/clarify-narrative-adjacent-20261016
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - tasks/open/2026-10-16-pr1517-narrative-duration-receipt.md
  - tasks/done/2026-10-16-pr1517-narrative-duration-receipt.md
---

# Bind PR 1517 narrative panel changes in long-form duration receipt

## Why

PR #1517 changes four files bound by the long-form duration receipt. The narrative-panel
rules and saved-verdict matching change, so the prior SHA-256 bindings no longer describe
the branch tree. An independent reviewer must inspect their exact diff for duration effects
before rebinding; a stale receipt makes the video tooling checks fail.

## Definition of done

- [x] The four changed bound files are independently reviewed against the prior receipt
  and their duration effects are recorded.
- [x] The report and all 108 SHA-256 bindings match the branch tree, with a passing
  duration receipt check and focused tests.
- [ ] Close this ticket when the interrupted `tasks done` copy can be cleaned up by
  an authorized operation and `npm run check:tasks` passes on the worktree.

## Steps

- [x] Verify that the merge-base versions of all four files match the prior receipt.
- [x] Inspect the exact four-file diff and the duration gates it calls.
- [x] Add the independent DURATION_ONLY report increment and update the receipt hashes.
- [x] Run focused checks and submit the scoped receipt and open task files.

## How to verify

`node tools/video/long-form/cli.mjs check` passed all 473 plans;
`node --test tools/video/long-form/review.test.mjs` passed 2/2;
`node --test tools/video/core/narrative.test.mjs` passed 14/14.
Bundled Node v24.19.0 passed the focused state, automation panel, and story pilot
recheck tests (1/1 each). The final local `npm run check:tasks` exits 1 because
the interrupted close left two physical copies of this task. CI on the submitted
tree must check the single committed open copy.

After integration with main #1391 at `99f0651eecb6454873b57dc9775c967d868014fd`,
the independent duration reviewer verified all 108 file and report bindings, finding
only the combined `automation.test.mjs` SHA stale (`ef1b881cea4230b6db1b2cad4f8386f446b54f274b72352a3284681e664e8310`).
The integrated report and receipt now bind that SHA; report SHA is
`e7b5d2134e4a0d27bb37d04ad0d87c353dd1503fc527d8bcdb0f9017f20f1b1b`.
Post-rebind, `node tools/video/long-form/cli.mjs check` passed all 473 plans and
`node --test tools/video/long-form/review.test.mjs` passed 2/2. Bundled Node
v24.19.0 passed the combined narrative-panel and cross-process lease tests 7/7,
the narrative core suite 14/14, and the focused stale-PASS status test 1/1.
The review applies only to duration compatibility of the integrated source bytes.

## Notes

The baseline is `697e197ee180d22f632b7f3c7624cc30927b2136` (also `origin/main`
at claim time). Its raw bytes match all four existing bindings. Only those four of 108
are stale on PR head `9ebd387b8a3b39ebf80e6bf80906f45c14573b55`.
This isolated branch was handed over by `codex-a01-gate`; overlapping older board
claims include merged #1520, so this narrow receipt task was claimed with `--force`
after checking live branch ownership. This ticket does not modify implementation.
The installed Node v24.13.0 crashed with Windows exit `3221226505` when loading
fixture-heavy state, automation and story test files, so the focused checks used
the bundled Node v24.19.0 runtime. One broad state and one broad story test run
were interrupted after they proved slower than the focused receipt checks;
those full suites are not claimed as passing. The scoped tests above exited 0.
`npm run tasks -- done` wrote a done copy but failed to remove the open copy because
Windows held it. The exact-path manual removal was blocked by automatic policy;
do not retry it through another route. The done copy remains untracked and
physically untouched in this worktree. This open ticket stays `in-progress` for
later authorized cleanup. Only `review.md`, `review.json`, and this open ticket
are submitted; the duplicate done copy is not staged or committed.
