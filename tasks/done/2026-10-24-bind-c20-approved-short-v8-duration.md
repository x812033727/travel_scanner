---
id: 2026-10-24-bind-c20-approved-short-v8-duration
title: Bind C20 approved short-v8 duration in lint and QA
status: done
priority: P1
area: tools
owner: codex-c20-short-duration
claimed_at: 2026-10-24T07:23:41Z
created_at: 2026-10-24T07:23:05Z
completed_at: 2026-10-24T07:31:54Z
branch: codex/c20-zippo-v5r2-20261024
depends_on: []
scope:
  - tools/video/core/duration.mjs
  - tools/video/core/duration.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/duration.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Bind C20 approved short-v8 duration in lint and QA

## Why

The owner approved C20 Zippo v8 as an approximately six-minute 36-line, 36-scene
episode in draft PR #1808. The current generic eight-minute lint and QA floor
rejects its [5, 7] target and estimated 333.167-second body. C08 has a narrowly
bound short-v8 precedent. C20 needs its own identity- and narration-bound rule,
using measured audio and final frames before media can pass QA.

## Definition of done

- [x] Only the approved C20 short-v8 document can use a five-minute narration-body
      floor and seven-minute presented-cut cap; old C20 and all other knowledge
      stories retain their 480-second floor.
- [x] The ordinary C20 lint and QA paths apply the same exact identity gate,
      preserve actual narration and final-frame proof, and test one-frame bounds.
- [x] An independent reviewer checks the code delta and renews the long-form
      duration receipt. No paid media, import, upload, or deployment occurs.

## Steps

- [x] Bind the exact C20 slug, episode, look, [5, 7] target, ordered visible
      narration and spoken-override hashes in the duration policy.
- [x] Thread the C20 exception through draft lint and final QA CLI.
- [x] Add positive, changed-input, stale-timeline and measured-frame tests.
- [x] Run focused tests, independent review, guarded duration check, and task check.

## How to verify

`node --test tools/video/core/duration.test.mjs tools/video/core/lint.test.mjs tools/video/qa/duration.test.mjs`;
`node tools/video/cli.mjs lint --file docs/videos/story-everyday-zippo-c20-short-v8/video.json`;
`node tools/video/long-form/cli.mjs check`; `npm run check:tasks`.

## Notes

Existing `2026-10-24-prepare-c20-zippo-v8-canonical-video` owns the whole C20
short-v8 directory through draft PR #1808. This ticket excludes that directory
and does not edit its source or README. The old README/preflight expectation
of two lint errors will need a narrow handoff before this PR is finalized.

The independent reviewer `codex-c20-duration-independent-review` recomputed the
36-line visible/spoken hashes and approved-source hashes, inspected all six
source/test changes, and found no blocking defect. Bundled Node v24.19 focused
tests passed 77/77. C20 lint is 0 errors/15 warnings; its existing nonpaid
preflight now reports PASS with 36 scenes, 33 shots and three cards. The guarded
long-form CLI and review-binding tests pass after updating exactly six SHA-256
bindings. `npm run check:tasks` and `git diff --check` pass. The check uses a
current audio timeline and assembly frame receipt; actual voice/final media,
spending, backend import, upload and publication are still pending.
