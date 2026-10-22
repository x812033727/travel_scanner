---
id: 2026-10-22-independently-verify-c08-v5-2-visual
title: Independently verify C08 v5.2 visual count summary
status: review
priority: P2
area: docs
owner: codex-c08-independent-v5-2
claimed_at: 2026-10-22T18:36:58Z
created_at: 2026-10-22T18:36:51Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/visual-count-review-20261023-v5-2.md
---

# Independently verify C08 v5.2 visual count summary

## Why

After v5.1 source PASS, the author found that visual-plan.md's chapter 4, chapter 6 and total count summary still described the older 71-shot/13-card layout, while its 84 actual rows were 73-shot/11-card. Independently verify the count-only v5.2 correction without changing authored files.

## Definition of done

- [x] A unique exact-hash receipt compares every chapter summary with actual rows and gives PASS/HOLD for this mechanical delta.
- [x] Only this ticket and its scoped receipt enter the review commit; older untracked duplicate task copies remain untouched.

## Steps

- [x] Verify the final author PR head, three SHA-256 hashes and diff from v5.1 review commit.
- [x] Recount shots/cards per chapter, ratio and longest consecutive card run; confirm 84 row texts and the two other authored inputs are unchanged.

## How to verify

Get-FileHash for the three authored inputs; git diff 93d191987..8b00c5dfa for visual-plan.md; row parser counts per c0801xx–c0806xx and maximum card run; git diff --cached --check; gh pr view 1681 --json headRefOid,isDraft,autoMergeRequest,labels,body.

## Notes

V5.2 author input head `8b00c5dfa981918fed4c1f3ebb60f217b8f90482`; script SHA-256 `53D82301F053189718BC2BD883A44A030A2F8694D4C25EA8645931829C8DBEA8`, visual SHA-256 `8562D6C5BFA224B4416268809C44B1FE575E6AE9AA9C75353622C4B78C46BA12`, addendum SHA-256 `82D1147FE720B4ECB3A9222C8A19E76717BC40B4E70B56EA9A3256F5D22DEDE5`. Correct count: 84 rows, 73 shots, 11 cards, 86.9% by count, max one card in sequence. Receipt: `docs/videos/story-everyday-kikkoman-c08/reviews/visual-count-review-20261023-v5-2.md`. Screen-time share remains unmeasured; no author files edited in this review.
