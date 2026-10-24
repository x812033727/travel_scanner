---
id: 2026-10-24-rebind-c15-lint-correction-in-independent
title: Rebind C15 lint correction in independent duration review
status: done
priority: P1
area: docs
owner: codex-c15-rebind
claimed_at: 2026-10-24T04:55:33Z
created_at: 2026-10-24T03:50:26Z
completed_at: 2026-10-24T04:59:23Z
branch: codex/c15-frixion-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Rebind C15 lint correction in independent duration review

## Why

The C15 canonical script contains `日本文字`. The shared written-language lint used a
plain substring search for `本文`, so it falsely rejected that spoken sentence. The
C15 branch changes only this phrase match and adds five regression cases, but the
independent long-form duration registry still binds the previous bytes of those
two files. Its check correctly reports exactly two stale bindings.

## Definition of done

- [x] The current lint source and regression test have an independent DURATION_ONLY
      review increment, with only their two SHA-256 bindings refreshed.
- [x] The existing duration floor and all 106 other bindings remain valid; the
      long-form check, focused tests and task-board check pass.
- [x] The C15 PR retains its draft and `no-auto-merge` state until its gates pass.

## Steps

- [x] Verify the four merged PRs and release only the two receipt paths from their
      still-open task scopes, under the owner's 2026-10-24 narrow authorization.
- [x] Claim this ticket normally, without force, and review the exact lint diff.
- [x] Add the independent duration-only finding and rebind only the two changed
      source files; compute the report hash last.
- [x] Run the focused and broader applicable checks, then close this ticket in
      the same PR.

## How to verify

`node --test tools/video/core/lint.test.mjs tools/video/core/duration.test.mjs tools/video/long-form/review.test.mjs`;
`node tools/video/long-form/cli.mjs check`;
`npm run check:tasks`;
`npm run test:tools` and `npm run test:docs-videos` when their dependencies are
materialized in this sparse checkout. The PR checks must include `api`, `web`,
`containers` and `full-stack-smoke` before merge.

## Notes

- C15 branch source commit `6be628ab2` changes only `tools/video/core/lint.mjs`
  and `tools/video/core/lint.test.mjs` in the duration registry. The correction
  is `/(?<!日)本文/u`: `日本文字` and `日本文化` no longer flag, while standalone
  `本文` still does. It does not edit the duration floor or a frame count.
- Four older PRs #1787, #1791, #1794 and #1797 are merged. Their tasks retain
  all other scope and work. Seven other active tasks mention the review files
  in prose, but none lists them in its YAML scope; the normal claim succeeded.
- The first review check saw exactly two stale bindings once the existing
  sparse checkout was expanded for its missing read dependencies; no new
  checkout or paid-media directory was created.
- After the rebind: focused lint/duration/review tests 67/67 PASS, long-form CLI
  PASS for 473 plans, `npm run check:tasks` exit 0, and `npm run test:docs-videos`
  19/19 PASS. `npm run test:tools` was attempted but this sparse checkout lacks
  unrelated repository directories and root node packages (`@playwright/test`,
  `js-yaml`); its failures are environment/inventory errors. The PR's full
  checkout CI remains the broad gate before any merge.
