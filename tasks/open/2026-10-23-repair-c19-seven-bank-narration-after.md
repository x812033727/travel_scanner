---
id: 2026-10-23-repair-c19-seven-bank-narration-after
title: Repair C19 Seven Bank narration after blind review
status: in-progress
priority: P2
area: docs
owner: codex-c19-v3-narrative
claimed_at: 2026-10-23T07:02:26Z
created_at: 2026-10-23T07:02:20Z
completed_at:
branch: codex/brand-story-seven-bank-c19-script
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/script.md
  - docs/videos/story-everyday-seven-bank-c19/script-source-notes.md
  - docs/videos/story-everyday-seven-bank-c19/visual-plan.md
  - docs/videos/story-everyday-seven-bank-c19/visual-plan.json
  - docs/videos/story-everyday-seven-bank-c19/reviews/author-script-receipt-20261023.md
---

# Repair C19 Seven Bank narration after blind review

## Why

The C19 source and paired visual review passed on the old 79-line script, but two independent narration-only blind reads held its story. The opening revealed the answer early; the 2010 fee model arrived before the 2001–07 expansion; chapters sounded like a table of contents; and a five-line closing recap replaced a final payoff. The owner approved the Treatment direction, not the script.

## Definition of done

- [x] Rewrite the 79-line narrator script as one chronological, scene-first story with delayed payoffs and a concise answer.
- [x] Keep the 79 visual rows, source notes and JSON narration/tags exactly paired to the revised script.
- [x] Preserve source time boundaries, including the 2010 fee model and later 2023–24 services, and record new source-backed claims.
- [x] Record exact staged-blob SHA-256 values, a narration-only projection hash, and explicit downstream gates in an author receipt.
- [x] Commit and push the revised author draft to PR #1742 without paid media, import, upload, merge or publication.

## Steps

- [x] Inspect blind review HOLDs and approved Treatment/source matrix.
- [x] Revise script, source notes and paired MD/JSON visuals.
- [x] Regenerate the narrator-only projection and run mechanical parity and rhythm checks.
- [x] Run repository task checks and push the author draft.

## How to verify

From the author worktree, run `python C:\Users\x8120\.codex\worktrees\b16f\travel_scanㄐ\c19-sync-and-check-v3.py`, `python C:\Users\x8120\.codex\worktrees\b16f\travel_scanㄐ\c19-hook-gaps.py`, `git diff --check`, and `npm run check:tasks`. The first check verifies all 79 IDs/order, narration/source parity, JSON visual type and count, max card streak, exact look and model, and branded image prompt exclusions. Confirm PR #1742 remains draft and points to the committed author head. Independent source/visual review, two blind readers, owner script review, actual voice duration and quote remain separate.

## Notes

The approved Treatment's paper sequence put the fee mechanism before expansion; the narrator script puts 2005–07 expansion first to eliminate an audible time jump. This is a narration-order refinement under the same approved factual direction; it is explicitly documented in the script and receipt for owner review. The old full source/visual PASS at `f45d93d` and blind HOLD receipts #1751/#1752 do not validate the new script. No paid media or product publishing was attempted. The exact author commit and hashes are in the adjacent `reviews/author-script-receipt-20261023.md` and PR #1742.
