---
id: 2026-10-23-c20-zippo-script-source-visual-delta
title: C20 Zippo script source visual delta review
status: in-progress
priority: P1
area: docs
owner: codex-c20-source-visual-delta-review
claimed_at: 2026-10-23T05:39:41Z
created_at: 2026-10-23T05:39:36Z
completed_at:
branch: codex/brand-story-zippo-c20-script-source-delta-review
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/independent-script-source-visual-delta-review.md
---

# C20 Zippo script source visual delta review

## Why

Independent source/visual review PR #1732 judged the author's C20 script at head `4b51defa16c8a8ca19f5504d67d1428c56227b4f` 65 PASS / 3 HOLD. The author repaired those three IDs in PR #1728 and moved its head to `856b6b24564d7de3a4b1804ccf1f7fc6f10232f2`. A reviewer must bind the new bytes and recheck the changed claims and cards before anyone treats the earlier review as approval.

## Definition of done

- [x] A standalone receipt locks the new author head and four blob SHA-256 values, tests 68/68 alignment, and states a precise PASS/HOLD verdict for the three changed IDs.
- [x] The receipt reopens relevant primary sources and carries forward the prior 65 PASS only after confirming those rows have no unrelated drift.
- [ ] A separate draft, no-auto-merge review PR targets the author branch, with metadata read back.

## Steps

- [x] Reopen Zippo history, museum and original patent; compare `c200207`, `c200310`, `c200410` voice and paired visuals in context.
- [x] Recompute four new hashes, inspect the old/new four-file diff, and assert identical order/content across all 68 IDs and 58 shot / 10 card entries.
- [x] Write the exact delta receipt without editing the author's worktree or paid media.
- [ ] Commit, push, open draft review PR, apply `no-auto-merge` and read back exact base/head.

## How to verify

Use `git diff 4b51defa16c8a8ca19f5504d67d1428c56227b4f 856b6b24564d7de3a4b1804ccf1f7fc6f10232f2 -- docs/videos/story-everyday-zippo-c20/{script.md,script-source-notes.md,visual-plan.md,visual-plan.json}` to inspect the three row edits and general source note. Recompute SHA-256 over each author file from `git show <head>:<path>`; parse the four new files to assert 68 identical IDs and exact narration/source/visual fields. Run `npm run check:tasks` and `git diff --check`. On GitHub read back PR `isDraft=true`, `autoMergeRequest=null`, `no-auto-merge` label and target author branch.

## Notes

2026-10-23: Reopened official primary sources. New `c200207` now labels the 1933 price/guarantee as company recollection in voice and card; `c200310` separates that recollection from the 1934 patent filing and removes the invented sales-card image; `c200410` dates only the museum opening to 1997 and makes the Repair Clinic current, while the next image is explicitly fictional. All three PASS. The other 65 rows are unchanged from the old 68-row independent review. New four files align 68/68, with 58 shots and 10 cards. No author files or media were changed.

The earlier PR #1732 task file and its locally untracked duplicate remain untouched after the exact cleanup attempt was blocked by policy. This separate task uses its own isolated sparse worktree and new receipt path.
