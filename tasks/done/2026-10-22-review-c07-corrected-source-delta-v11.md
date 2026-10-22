---
id: 2026-10-22-review-c07-corrected-source-delta-v11
title: Review C07 corrected source delta v11
status: done
priority: P2
area: docs
owner: codex-c07-v11-source-reviewer
claimed_at: 2026-10-22T14:26:45Z
created_at: 2026-10-22T14:26:30Z
completed_at: 2026-10-22T14:28:04Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v11.md
  - tasks/open/2026-10-22-review-c07-corrected-source-delta-v11.md
  - tasks/done/2026-10-22-review-c07-corrected-source-delta-v11.md
---

# Review C07 corrected source delta v11

## Why

The prior independent review held two source boundaries: a brand history page does not establish a brush or hand painting for floral customization, and the museum's 1995 date is the boot's production date. The author changed three narration and visual IDs; the corrected hashes need independent rereading before approval.

## Definition of done

- [x] Directly reread B2 and M1 and check all changed narration, visuals and source notes against them.
- [x] Bind a PASS/HOLD delta receipt to the exact three current SHA-256 values and push it to draft PR #1680.

## Steps

- [x] Compare the previous reviewed commit `7e18faece` with corrected commit `4902c0143`.
- [x] Check unique IDs, shot/card counts and maximum consecutive cards.
- [x] Save `reviews/script-source-review-v11.md` without editing author files.

## How to verify

Recompute SHA-256 for script.md, visual-plan.md and script-source-notes.md; compare all three to the v11 receipt. Run `git diff --check` and `npm run check:tasks`; read B2's 1980s passage and M1's Object details directly.

## Notes

The three repaired IDs PASS direct-source boundaries. The inherited 70 IDs were assessed in v10; full blind reads, full visual preflight, actual TTS duration and owner gates remain. Existing untracked duplicate open task files in this worktree can make `check:tasks` fail; do not remove them through alternate commands after policy blocks.
