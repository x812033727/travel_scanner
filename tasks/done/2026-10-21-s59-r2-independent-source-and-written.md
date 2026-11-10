---
id: 2026-10-21-s59-r2-independent-source-and-written
title: S59 R2 independent source and written visual review
status: done
priority: P2
area: docs
owner: codex-s59-r2-source-review
claimed_at: 2026-10-21T00:08:00Z
created_at: 2026-10-21T00:08:00Z
completed_at: 2026-10-21T00:12:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s59/review/r2-source-independent.md
---

# S59 R2 independent source and written visual review

## Why

R2 revises four source blockers in the 1878 du Moncel and 1910 Edison account. A separate reviewer needs to check the frozen text, its source tier, and whether its written images can be made under the series rules before media production.

## Definition of done

- [x] Record exact five-file hashes, direct checks against pinned original sources, claim alignment, and source/written visual PASS or HOLD with narrow repair boundaries.

## Steps

- [x] Independently fetch the fixed 1878 French, 1910 English, and auxiliary 1892 translated texts, and verify raw SHA-256 values.
- [x] Check all 109 claim, scene, and script IDs and narration lines; inspect all 121 source ranges and review original witness attribution.
- [x] Revisit R1 blockers s59018, s59019, s59057, and s59069; review each written image prompt and run episode lint.
- [x] File [R2 independent review](../../docs/videos/curio-s59/review/r2-source-independent.md) without changing creative files or paid media.

## How to verify

`sha256sum docs/videos/curio-s59/{research.md,brief.md,claims.md,video.json,script.md}`; `VIDEO_WORKDIR=/workspace/.video-work NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s59 --json`; `npm run test:docs-videos`; `npm run check:tasks`. Read the pinned source lines in the review.

## Notes

Source and claim PASS: the four R1 source blockers are repaired, 109/109 lines align, and the 121 pinned source ranges exist. Written visual HOLD: s59004, s59009, s59070, and s59071 require a second visible human despite their one-person prompts; s59017 uses a paper strip in the Edison quoted disk sequence; s59097 combines two simultaneous actions. The frozen R2 cannot start paid image production. Thumbnail literal asterisks and outdated quota wording are nonblocking editorial cleanups. No creative or site approval changes.
