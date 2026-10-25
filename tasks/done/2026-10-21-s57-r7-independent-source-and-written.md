---
id: 2026-10-21-s57-r7-independent-source-and-written
title: S57 R7 independent source and written visual audit
status: done
priority: P2
area: docs
owner: codex-s57-r7-source
claimed_at: 2026-10-21T00:08:00Z
created_at: 2026-10-21T00:08:00Z
completed_at: 2026-10-21T00:13:42Z
branch:
depends_on:
  - 2026-10-21-s57-r7-narrow-author-repair-after
scope:
  - docs/videos/curio-s57/review/r7-source-independent.md
---

# S57 R7 independent source and written visual audit

## Why

The R7 author changed historical narration and repaired the R6 `s57150` two-person written visual HOLD. The exact R7 five-file freeze needs a separate source and visual review.

## Definition of done

- [x] Write an independent exact-hash PASS/HOLD receipt for source, claims, written prompts, chronology, and source limits.

## Steps

- [x] Verify all five frozen SHA-256 values and the R6→R7 author diff.
- [x] Align all 163 scene, claims, and script IDs and narration strings; validate all 186 S/L fixed-commit line anchors.
- [x] Recheck the changed claims and the February 18 aid → 19 medicine → 20 hidden cloth order against pinned original texts.
- [x] Check all changed prompts for one subject and one main action, including repaired `s57150`; run focused lint.

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`; `node tools/video/cli.mjs lint --slug curio-s57 --json`; `npm run check:tasks`.

## Notes

Independent receipt: [R7 source and written visual](../../docs/videos/curio-s57/review/r7-source-independent.md). Source/claims PASS and written visual PASS for the exact five hashes. Lint returned 0 errors and 0 warnings. Minor nonblocking citation label precision: `s57189` calls L10–44 the Waller/1874 title source, while editor/year appear at L49–60; spoken claim remains supported. No creative, paid-media, site, or approval changes.
