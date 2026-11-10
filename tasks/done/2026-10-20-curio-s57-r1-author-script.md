---
id: 2026-10-20-curio-s57-r1-author-script
title: Draft source-bound S57 Livingstone full episode
status: done
priority: P2
area: docs
owner: codex-s57-author
claimed_at: 2026-10-20T22:32:19Z
created_at: 2026-10-20T22:32:18Z
completed_at: 2026-10-20T22:45:43Z
branch:
depends_on:
  - 2026-10-20-curio-s57-independent-source-feasibility
scope:
  - docs/videos/curio-s57/research.md
  - docs/videos/curio-s57/brief.md
  - docs/videos/curio-s57/claims.md
  - docs/videos/curio-s57/video.json
  - docs/videos/curio-s57/script.md
  - docs/videos/curio-s57/review/r1-author-fix.md
---

# Draft source-bound S57 Livingstone full episode

## Why

S57's source feasibility review conditionally passed a narrow Stanley/Livingstone question, but corrected the source hierarchy and left the exact meeting day unresolved. The episode needs a complete, source-bound author draft before independent full-script and narrative review.

## Definition of done

- [x] R1 research, brief, 189-row claims, 189-scene video JSON and screenplay are frozen as an author candidate, with five SHA-256 values in `review/r1-author-fix.md`.
- [x] Opening condensation is 44 seconds; planned 5-second channel intro follows it. Body exceeds eight minutes at 325 Han characters per minute; shared 21-second endscreen plan and source/channel links are written.
- [x] Video lint is 0 errors and 0 warnings; 236 documentation video tests pass.
- [x] Hand off for independent full source/visual review and two fresh context-free narrative readers. No paid media or author self-approval.

## Steps

- [x] Apply source-feasibility corrections: S abridged notice, two-source return persuasion, L medicine lines, italic round meeting date and exact-day hold.
- [x] Write single-question story in eight event chapters; account for Susi, Chuma, local workers and limits of both published texts.
- [x] Generate screenplay, line claims and art/card directions; check date conflicts and audience hooks.
- [x] Freeze five file hashes and hand off to parent for independent gates.

## How to verify

`node tools/video/cli.mjs lint --slug curio-s57`; `npm run test:docs-videos`; `npm run check:tasks`; compare five SHA-256 values in `docs/videos/curio-s57/review/r1-author-fix.md`.

## Notes

The dated source-feasibility review is `docs/videos/curio-s57/source-feasibility-1.md`. S and L give conflicting exact meeting days; narration says only 1871 late autumn. L itself writes Dec 27 departure and Dec 26 march start; narration says late December. The source and two narrative reviews must be independent of this author round. TTS, image and music services were not called.
