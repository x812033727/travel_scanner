---
id: 2026-10-20-s57-r6-independent-source-and-written
title: S57 R6 independent source and written visual audit
status: done
priority: P2
area: docs
owner: codex-s57-r6-source
claimed_at: 2026-10-20T23:42:44Z
created_at: 2026-10-20T23:42:00Z
completed_at: 2026-10-20T23:44:08Z
branch:
depends_on:
  - 2026-10-20-curio-s57-r6-author
scope:
  - docs/videos/curio-s57/review/r6-source-independent.md
---

# S57 R6 independent source and written visual audit

## Why

The R6 author changed historical narration and visual prompts after the R5 source PASS. The exact R6 version needs its own independent review.

## Definition of done

- [x] Write an exact-version source and written visual PASS/HOLD receipt with pinned-source anchors, five hashes, checks, and limitations.

## Steps

- [x] Check the R5 to R6 diff, all R6 scene and claim IDs, changed citations and prompts, and the February 18/19/20 sequence against the fixed originals.
- [x] Run focused checks without changing creative files or generating paid media.

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`; `node tools/video/cli.mjs lint --slug curio-s57 --json`; `npm run test:docs-videos`; `npm run check:tasks`.

## Notes

Independent review only. Narrative blind reviews, policy, site approval, and media remain separate. Source/claims PASS, written visual HOLD only `s57150` because its interacting two-person prompt conflicts with the series single-subject rule. Pinned S/L originals were freshly downloaded and SHA verified. All 167 scene/claim/script IDs and text align; 192 pinned links have valid anchors. Lint 0/0; docs-video tests 236/236; task check exit 0. No creative or paid-media changes.
