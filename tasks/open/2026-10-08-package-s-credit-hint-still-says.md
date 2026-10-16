---
id: 2026-10-08-package-s-credit-hint-still-says
title: Package's credit hint still says lint does not count the picture credits
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-08T05:54:56Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package/metadata.mjs
  - tools/video/package/metadata.test.mjs
---

# Package's credit hint still says lint does not count the picture credits

## Why

Since #1382, `tools/video/core/lint.mjs` composes the YouTube description with `assets` (lines
471 and 503), exactly as `package` does, so `lint` already refuses a description that the
「圖片來源」 credits push past 5,000 bytes. `tools/video/package/metadata.mjs` `withCreditHint`
still says the opposite, in its comment ("Lint composes the description without the picture
credits (lint.mjs reads no assets)") and in the problem it adds ("the 圖片來源 credits of
assets[] add N bytes that lint does not count"), and `metadata.test.mjs` pins that sentence.
Found while merging #1382 into #1361; #1361 corrected the same claim in `ILLUSTRATED.md` and
`visuals.md` but `package/metadata.mjs` is outside its tickets.

## Definition of done

- [ ] `package`'s over-limit problem no longer says lint does not count the credits (it may still
      say how many bytes the credits take), and its comment says what lint does now.

## Steps

- [ ] Reword or drop `withCreditHint` in `tools/video/package/metadata.mjs`.
- [ ] Update the pinned message in `tools/video/package/metadata.test.mjs`.

## How to verify

`node --test tools/video/package/metadata.test.mjs`, then `npm run test:tools`.

## Notes

A description over the limit should now fail at `lint` first, so this hint is reached only by a
package run without a lint run before it.
