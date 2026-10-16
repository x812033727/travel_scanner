---
id: 2026-10-12-independently-bind-pr-1475-private-studio
title: Independently bind PR 1475 private Studio link duration receipt
status: done
priority: P2
area: docs
owner: codex-pr-review-1475-duration
claimed_at: 2026-10-12T18:03:15Z
created_at: 2026-10-12T18:03:10Z
completed_at: 2026-10-12T18:12:14Z
branch: codex/curio-five-recuts-20261012
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Independently bind PR 1475 private Studio link duration receipt

## Why

PR #1475 changes nine files bound by the long-form duration receipt while adding a
guarded way to record private Studio videos for pending imported final cuts. The
receipt must be updated by a reviewer other than the API/UI author, after checking
the old hashes and reading the final diff for duration-rule changes.

## Definition of done

- [x] The nine prior bindings match the branch's merge-base bytes, and the
      final author commit has been independently reviewed for duration rules.
- [x] `review.md` records the increment and `review.json` binds the final bytes
      with a distinct reviewer identity; both duration checks pass.

## Steps

- [x] Check task/PR collisions and claim this exact two-file receipt scope.
- [x] Baseline-check the nine protected files against the current merge base.
- [x] Re-read the final author commit after the API/UI author hands it off.
- [x] Update only the two receipt files and run checks; the exact receipt
      commit follows task closure.

## How to verify

`node tools/video/long-form/cli.mjs check` and
`node --test tools/video/long-form/review.test.mjs`.

## Notes

At `c43d975c88b5862fc7956e7e3105c04866d550f7`, all nine protected-file
hashes at merge base `a933427269e55365c3f3eed4769ca70ce9a8e692` matched the
existing receipt. The root agent asked to wait for an API/UI edge-case follow-up
commit before rebinding. Other open PRs also touch the receipt: #1454, #1391,
and #1387; none has an active task claim on this exact scope in this checkout.

The final author commit is `2d5552fe8d7edec44b09c698fff592b3ca35a5fd`.
The nine existing hashes still match the merge base; their new bytes were read
and rebound. The new positive YouTube duration check confirms a processed,
playable upload and does not modify long-form episode targets or measured floors.
`node tools/video/long-form/cli.mjs check` passed all 473 plans; the independent
review test passed 2/2. `npm run check:tasks` and `git diff --check` also passed.
