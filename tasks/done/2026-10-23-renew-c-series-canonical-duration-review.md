---
id: 2026-10-23-renew-c-series-canonical-duration-review
title: Renew canonical duration receipt for C-series video safety port
status: done
priority: P1
area: docs
owner: codex-duration-review-c-series
claimed_at: 2026-10-23T12:20:43Z
created_at: 2026-10-23T12:16:05Z
completed_at: 2026-10-23T12:25:52Z
branch: codex/c-series-video-safety-port-20261023
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Renew canonical duration receipt for C-series video safety port

## Why

The C-series port of #1610, #1667 and #1669 changes eight files bound by the
long-form duration receipt. `review.mjs` reads the canonical `review.md` and
`review.json`; a new supplemental receipt cannot replace their raw-byte and
report-hash bindings. The old unmerged #1669 task
`2026-10-22-renew-long-form-duration-review-music` was blocked by overlapping
claims. The owner-directed 2026-10-23 board handoff released only these two
canonical paths for an independent reviewer, preserving that unfinished review
here before #1669 closes.

## Definition of done

- [x] A reviewer independent of the port author checks the final eight-file diff
      against merged main, including unchanged 480-second unwrapped-body logic.
- [x] Canonical `review.md` records the actual compatibility increment and keeps
      earlier review sections; `review.json` binds the current report and every
      registered file, not just the changed eight.
- [x] Long-form review tests and CLI `check` pass on the final PR commit without
      any stale source or report binding.

## Steps

- [x] Wait for #1782 to merge and for the safety port author to rebase the same
      checkout and freeze the final commit and eight file SHA-256 values.
- [x] Claim this ticket under the independent reviewer identity before editing
      `review.md/json`; inspect the eight changed files and existing 108-file
      registry/report scope. Coordinate other canonical receipt increments.
- [x] Rebind the final bytes once, run the long-form tests and CLI check, and
      record exact evidence in the task and PR.

## How to verify

Run `node --test tools/video/long-form/review.test.mjs` and
`node tools/video/long-form/cli.mjs check`, then verify PR CI `video-tests`,
`web-checks` and `smoke`. No media provider call is needed.

## Notes

The bound changed paths are `tools/video/core/branding.mjs`,
`branding.test.mjs`, `lint.mjs`, `lint.test.mjs`, `state.mjs`,
`state.test.mjs`, `tools/video/assemble/cli.mjs` and
`tools/video/media/clips.test.mjs`. The #1669 old receipt task covered only the
last two at its earlier head; its recorded SHA values are historical and must
not be reused. The source author must not self-approve this receipt.

2026-10-23 independent review: source HEAD `4ba043f573059be8c9c50eac1a4b5e7dfc1aec52` on merged-main base `efbb3012f0778f79327394b079a52070d0f12d94`. All eight base blobs matched the old table/JSON hashes, and the other 100 of 108 worktree files remained bound. Pre-rebind CLI named exactly eight stale paths. Reviewed the 174-addition/17-deletion bound diff: caption intro rounding, everyday-story visual lint and generated-music measurement/integrity guards do not relax the unwrapped 480-second body floor. Rebound only those eight rows plus reviewer metadata/report hash; preserved historical sections and other 100 rows. Report SHA-256 `c157b986ad8fdbc547da0b1038e3e20269312534b5578edcebf7f97925420550`.

Validation: bundled Node v24.19.0 four affected test files 52/52 PASS, 0 skipped; `node tools/video/long-form/cli.mjs check` PASS all 473 plans; `node --test tools/video/long-form/review.test.mjs` 2/2 PASS; `npm run check:tasks` PASS 2116 files; `git diff --check` PASS. The shell default Node v24.13.0 produced two file-level failures for state/clips tests without diagnostics, so the passing affected suite was rerun with the repository bundled Node v24.19.0. PR CI remains the integration gate after the combined PR is opened. No provider or production mutation was performed.
