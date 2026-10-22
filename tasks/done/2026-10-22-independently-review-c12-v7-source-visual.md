---
id: 2026-10-22-independently-review-c12-v7-source-visual
title: Independently review C12 v7 source visual delta
status: done
priority: P2
area: docs
owner: codex-c12-source-delta
claimed_at: 2026-10-22T17:23:55Z
created_at: 2026-10-22T17:23:42Z
completed_at: 2026-10-22T17:28:21Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v7.md
---

# Independently review C12 v7 source visual delta

## Why

The C12 author condensed seven paired narration/visual rows and rewrote 22 narration lines after the v6 blind review. The new hashes need an independent source and visual delta audit, plus an exact 69-ID and picture/card check.

## Definition of done

- [x] Save a SHA-bound independent PASS/HOLD receipt for changed/deleted rows and adjacent source/visual boundaries.
- [x] Verify the exact 69-ID correspondence and picture/card/cue rules.
- [x] Identify any adopted Treatment contradiction seen while reading the changed ending.

## Steps

- [x] Reopen the original Corning Museum, Corning Inc., and product-owner sources.
- [x] Compare all changed/deleted narration and visual rows with v6 and read adjacent rows.
- [x] Run final targeted checks and close the narrow task.

## How to verify

`Get-FileHash` for script and visual; per-ID comparison with `b925c6b1c`; unique/order/type/cue checks; `git diff --cached --check`; `npm run check:tasks`.

## Notes

Receipt: `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v7.md`. Source/visual delta PASS; overall adopted C12 Treatment ending alignment HOLD at missing story-linked comment prompt and unchanged spoken N16 subscription invitation. The Museum Pyrex FAQ live page timed out; its unchanged historical material line is not re-certified by this delta. Preserve the two pre-existing ghost tasks.

Rechecked exact input SHA-256 and Git head. `npm run check:tasks` exits 1 only for those two pre-existing duplicate IDs; 69 script/visual IDs align, 56 illustrations plus 13 cards, longest card run two, all 23 written cue IDs exist. Final staged whitespace check runs before commit.
