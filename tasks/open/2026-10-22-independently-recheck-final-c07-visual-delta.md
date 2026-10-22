---
id: 2026-10-22-independently-recheck-final-c07-visual-delta
title: Independently recheck final C07 visual delta
status: review
priority: P2
area: docs
owner: codex-c07-visual-delta-review
claimed_at: 2026-10-22T12:25:48Z
created_at: 2026-10-22T12:25:41Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/visual-delta-review.md
---

# Independently recheck final C07 visual delta

## Why

The prior visual source review is bound to an older visual-plan SHA. The author
then changed four C07 rows to answer a focused visual HOLD. A separate reviewer
must check the changed plan against the frozen narration and direct sources
before its visual direction can be called reviewed.

## Definition of done

- [x] A new independent review receipt binds the exact script and visual-plan
      SHA-256 values and records a bounded PASS/HOLD with direct sources.
- [x] The draft C07 PR carries the receipt while retaining no-auto-merge and
      all later owner, time, image, and paid gates.

## Steps

- [x] Recount every ID, shot/card type and longest card run.
- [x] Review the four changed rows, the shared image contract, the unchanged
      adjacent shots, and the brand archive, museum object, and Crucq article.
- [x] Preserve the script and visual plan unchanged, and record the final-cut
      ambiguity to check at c070607–608.

## How to verify

Compare SHA-256 values with the receipt; recount the 77 unique matching IDs,
64 shots, 13 cards, and two-card maximum. Run git diff --check and
npm run check:tasks. Verify PR #1680 remains draft with no-auto-merge.

## Notes

2026-10-22: Independent plan-level PASS, 77/77, is in
docs/videos/story-everyday-dr-martens-c07/reviews/visual-delta-review.md.
The 1995 museum object is purple/yellow tartan; c070608 is a distinct
blue/green illustrative fashion boot. Final editing should mark or visibly
separate it from the preceding museum card. Neither rendered images nor
time-weighted illustration share or TTS duration has been checked.

Verification: git diff --check passed, and the script/visual SHA-256 values
still match the receipt. npm run check:tasks exited 1 on four pre-existing C07
open/done duplicate IDs: c07-revised-script-source-review, c07-source-delta-v3,
recheck-c07-hook-source-delta, and recheck-c07-narrative-source-delta. Those
untracked open copies were not created or edited by this task; their prior
deletion attempts were policy-blocked. Do not report this check as green.
