---
id: 2026-10-20-s55-r10-remove-repeated-balloon-diameter
title: S55 R10 remove repeated balloon diameter
status: done
priority: P2
area: docs
owner: codex-s55-r10-author
claimed_at: 2026-10-20T21:36:21Z
created_at: 2026-10-20T21:36:18Z
completed_at: 2026-10-20T21:38:06Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/video.json
  - docs/videos/curio-s55/claims.md
  - docs/videos/curio-s55/script.md
  - docs/videos/curio-s55/review/r10-author-fix.md
---

# S55 R10 remove repeated balloon diameter

## Why

Two no-history readers jointly rejected R9 because the first balloon's twelve-foot diameter was repeated at s55018 and s55038. Preserve the eight-minute floor while removing that repetition.

## Definition of done

- [x] R10 freezes a single-line factual comparison without the repeated dimension, with synchronized claims and script.

## Steps

- [x] Verify the pinned Franklin passages for both balloon dimensions and unmanned status.
- [x] Replace only s55038, regenerate the screenplay, and record the five hashes and next gates.

## How to verify

`node tools/video/cli.mjs script --slug curio-s55`; `VIDEO_WORKDIR=/tmp/curio-s55-r10-author NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s55 --json` (0 errors/0 warnings). Inverse R10→R9 video and claims hashes reproduce the frozen R9 values in `review/r10-author-fix.md`.

## Notes

R10 author's text-only candidate. Independent source/visual check and two fresh no-history narrative readers are required. Body fastest estimate 2626 Han / 325 ≈ 8.08 minutes; no TTS or art.
