---
id: 2026-11-08-thumbnail-layout-and-focus-stay-out
title: Thumbnail layout and focus stay out of the visual hash
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-curio-redo-20
claimed_at: 2026-11-08T06:17:55Z
created_at: 2026-11-08T06:16:57Z
completed_at:
branch: claude/curio-redo-20-episodes-ldnrq0
depends_on: []
scope:
  - tools/video/core/timeline.mjs
  - tools/video/core/timeline.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Thumbnail layout and focus stay out of the visual hash

## Why

`visualHash` (tools/video/core/timeline.mjs) folds `thumbnail` into the hash the keyframes, clips
and assembly of a drama are bound to. Writing the split layout (`layout: "e"`, #2044) and its
`focus` into curio-h24's thumbnail after the owner approved its storyboard made the storyboard
stale, although the two fields change thumbnail.jpg alone. A brand story's `brand` is already
left out for the same reason.

## Definition of done

- [x] `focus`, and `layout` when it is "e", are left out of visualHash like `brand`.
- [x] Any other layout ("ai", "d", ...) and the headline still move the hash, so no video already
      shot changes hash.

## How to verify

`node --test tools/video/core/timeline.test.mjs`; `node tools/video/long-form/cli.mjs check` after
the independent duration increment.

## Notes
