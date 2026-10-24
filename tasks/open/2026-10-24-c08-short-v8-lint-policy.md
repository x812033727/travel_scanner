---
id: 2026-10-24-c08-short-v8-lint-policy
title: Allow exact approved C08 short-v8 lint target
status: in-progress
priority: P2
area: tools
owner: codex-c08-short-backend
claimed_at: 2026-10-24T05:22:22Z
created_at: 2026-10-24T05:22:10Z
completed_at:
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Allow exact approved C08 short-v8 lint target

## Why

The exact owner-approved C08 short-v8 is a 4–5-minute exception, while ordinary story lint expects the longer series target. Keep the exception bound to its slug, series and episode; leave the other 19 rows and all global duration rules intact.

## Definition of done

- [x] C08 short-v8 local lint accepts the approved 36-line source with no errors and the 4-minute floor.
- [x] Nearby slugs and ordinary stories retain their existing lint requirements.
- [ ] Independent long-form duration/lint review binding remains required before green production checks.

## Steps

- [x] Add exact C08 lint identity predicate and focused near-miss tests.
- [x] Check the top-level project via the video CLI without synthesis or media spend.

## How to verify

`node --test tools/video/core/lint.test.mjs tools/video/core/duration.test.mjs`; `node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08-short-v8`. Current lint: zero errors, seven warnings. `checkDurationReview` is stale until an independent incremental review rebinds four changed files.

## Notes

Precise completed-claim takeover: `2026-10-24-avoid-false-written-language-lint-hit` had the same previous owner, all DoD/steps checked, and PR #1810 merged at 05:20Z with both lint paths. The owner explicitly authorized `claim --force` on only `tools/video/core/lint.mjs` and `tools/video/core/lint.test.mjs`; the old ticket and its other state were not changed. C08 work began only after C15 merged and this branch incorporated main commit `a8e97528072bdce0b726c151cee9c4e98431f56c`. No global lint floor was relaxed.
