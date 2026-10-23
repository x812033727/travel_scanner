---
id: 2026-10-23-renew-c-series-canonical-duration-review
title: Renew canonical duration receipt for C-series video safety port
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-23T12:16:05Z
completed_at:
branch:
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

- [ ] A reviewer independent of the port author checks the final eight-file diff
      against merged main, including unchanged 480-second unwrapped-body logic.
- [ ] Canonical `review.md` records the actual compatibility increment and keeps
      earlier review sections; `review.json` binds the current report and every
      registered file, not just the changed eight.
- [ ] Long-form review tests and CLI `check` pass on the final PR commit without
      any stale source or report binding.

## Steps

- [ ] Wait for #1782 to merge and for the safety port author to rebase the same
      checkout and freeze the final commit and eight file SHA-256 values.
- [ ] Claim this ticket under the independent reviewer identity before editing
      `review.md/json`; inspect the eight changed files and existing 108-file
      registry/report scope. Coordinate other canonical receipt increments.
- [ ] Rebind the final bytes once, run the long-form tests and CLI check, and
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
