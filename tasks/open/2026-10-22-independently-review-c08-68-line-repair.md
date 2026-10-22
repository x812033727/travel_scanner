---
id: 2026-10-22-independently-review-c08-68-line-repair
title: Independently review C08 68-line repair delta v2
status: review
priority: P2
area: docs
owner: codex-c08-independent-v2
claimed_at: 2026-10-22T17:56:22Z
created_at: 2026-10-22T17:56:17Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-68-delta-v2.md
---

# Independently review C08 68-line repair delta v2

## Why

PR #1681 author head `20c8b8f1c` repairs four specific HOLD IDs from an independent 68/68 review. The repair needs a new hash-bound independent verdict; adjacent language and a contradictory evidence note also need checking.

## Definition of done

- [x] Independently compare four narration/visual repair IDs to v1 and reopen their primary sources.
- [x] Audit adjacent sentences, shots and the visual-plan evidence note for remaining contradictions.
- [x] Write a narrow review receipt tied to current script, visual, addendum hashes and author PR head.
- [x] Commit/push only this review receipt and task ticket; update and read back draft PR body.

## Steps

- [x] Inspect head, files, branch, existing tasks and six pre-existing untracked duplicate open task copies; claim a unique exact review-receipt path.
- [x] Reopen MoMA, Kikkoman K3, GK and K4; re-read Ekuan's first-person article and the earlier rendered official GK Report.
- [x] Confirm four specified paired deltas PASS; identify remaining HOLD IDs and the separate evidence-note consistency failure.
- [ ] Run focused checks, place ticket in review for the still-open PR, commit/push two exact files, and read back PR body.

## How to verify

Read `docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-68-delta-v2.md` against the three full SHA-256 hashes and PR author head. Compare `git diff 8c7a9585..20c8b8f1`, inspect `c080406`, `c080415`, `c080604–605` and visual-plan line 133, then use `git diff --cached --check`. Run `npm run check:tasks`; any failure from the six untracked duplicate open/done copies is local existing state, not a reason to touch them. Verify final commit contains only this task and unique receipt. Read PR #1681 body, head, draft state and no-auto-merge label after update.

## Notes

The four requested repair IDs `c080215`, `c080405`, `c080410`, `c080414` now pass their narrow delta check. Overall remains HOLD: `c080605` still says unsupported 「小斜角」; `c080406` says 「改動很小」 and needs to be localized to the tip rather than suggesting unmeasured magnitude; `c080415` shot shows a filled product while its paired narration asks whether launch item would be empty or prefilled. Independently, visual-plan line 133 falsely says 2018 cumulative shipments are absent; `c080604` narration/card and the addendum include K3's correctly qualified >500 million global cumulative shipments through March 2018. The duration STOP and all owner/paid gates remain. Do not edit author inputs or the six untracked policy-blocked copies.
