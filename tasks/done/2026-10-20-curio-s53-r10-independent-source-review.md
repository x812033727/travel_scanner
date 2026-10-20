---
id: 2026-10-20-curio-s53-r10-independent-source-review
title: Curio S53 R10 independent source review
status: done
priority: P2
area: docs
owner: codex-s53-r10-source-independent
claimed_at: 2026-10-20T20:39:05Z
created_at: 2026-10-20T20:38:02Z
completed_at: 2026-10-20T20:40:46Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s53/review/r10-source-independent.md
---

# Curio S53 R10 independent source review

## Why

The S53 R10 author revised eight spoken lines and claims, six visual prompts, and two chapter-link loops after the R9 narrative review. The frozen revision needs a separate source and written-visual check before it can be treated as a verified script candidate.

## Definition of done

- [x] Independent R10 exact-hash source and written-visual verdict at `docs/videos/curio-s53/review/r10-source-independent.md`.

## Steps

- [x] Check the five frozen hashes, pinned source hashes and primary text lines, and the complete R9→R10 difference.
- [x] Check all changed claims, visual prompts, loops, line IDs, script regeneration, lint and duration.

## How to verify

Use `sha256sum` on the five S53 files; compare R9 archived files at `/tmp/s53-r9-r10-author-baseline/`; run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json` and `npm run check:tasks`. The review records results and scope.

## Notes

R10 exact files match the author freeze. Pinned R and C text hashes match `research.md`; all eight changed claims and six written prompts pass source boundaries. Two revised loops have next-scene payoffs. The 124 scenes, 126 lines and claims, 16 loops, script bytes and lint pass. Fast estimated body is 8:05.37; this is not measured TTS. Independent verdict is source/visual PASS only; formal R10 blind narrative review remains separate.
