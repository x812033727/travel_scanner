---
id: 2026-10-22-independently-review-c12-condensed-ending-source
title: Independently review C12 condensed ending source visual delta
status: done
priority: P2
area: docs
owner: codex-c12-source-delta
claimed_at: 2026-10-22T17:02:17Z
created_at: 2026-10-22T17:02:12Z
completed_at: 2026-10-22T17:03:23Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v6.md
---

# Independently review C12 condensed ending source visual delta

## Why

Two blind readers held the C12 draft for repeated beats. The author deleted four paired narration/visual rows and changed the ending transition; the new hashes require an independent source and visual delta review.

## Definition of done

- [x] Save a SHA-bound PASS/HOLD receipt for each changed or deleted narration/visual ID and adjacent T-to-N factual scope.
- [x] Verify 76 unique narration and visual IDs in matching order.

## Steps

- [x] Reopen direct Corning Museum, Corning Inc., and European brand originals at the product boundaries.
- [x] Compare changed rows against the prior reviewed head and save the delta receipt.
- [x] Run final targeted checks and close the ticket.

## How to verify

`Get-FileHash` on the two inputs, `git diff --unified=1 2c378383e 5912fac...`, per-ID row count/order check, `git diff --cached --check`, and `npm run check:tasks`.

## Notes

Receipt: `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v6.md`. Source/visual delta PASS; the museum Pyrex FAQ live page timed out again, so no claim of a direct read of that specific page. Preserve the two unrelated pre-existing ghost tasks.

`npm run check:tasks` exits 1 solely for the two pre-existing duplicate ghost IDs; all 76 script/visual IDs are unique and aligned, with 63 illustrations and 13 cards. Final staged whitespace check is performed before commit.
