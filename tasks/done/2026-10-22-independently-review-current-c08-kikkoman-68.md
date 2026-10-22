---
id: 2026-10-22-independently-review-current-c08-kikkoman-68
title: Independently review current C08 Kikkoman 68-line script and visuals
status: done
priority: P2
area: docs
owner: codex-c08-independent-68
claimed_at: 2026-10-22T17:44:01Z
created_at: 2026-10-22T17:43:56Z
completed_at: 2026-10-22T17:49:22Z
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-68-current.md
---

# Independently review current C08 Kikkoman 68-line script and visuals

## Why

PR #1681 has a new 68-line script and paired visual draft. Earlier independent reviews bind older hashes. The author needs a separate primary-source and image-boundary verdict on this exact version before any narrative or production gate.

## Definition of done

- [x] Reopen the primary company, design-team, museum, and Ekuan first-person sources, keeping retrospective claims and source scopes separate.
- [x] Audit all 68 narration IDs and 68 paired visual rows, including the 1961 150 mL product, spout and prototype claims, 2018 Japanese mark, and cumulative shipments.
- [x] Record exact correction IDs, structural estimates, remaining gates, current hashes, and author PR head in a review receipt.
- [x] Commit and push only this review receipt and task file; update and read back PR body with HOLD and the receipt link.

## Steps

- [x] Inspect worktree, PR, task ownership, and five pre-existing untracked duplicate task copies; claim only a unique review receipt path.
- [x] Directly reread K1/K2a/K3/D1/M1/R1/E1/K4, with M+ used only for its limited scope.
- [x] Review each pair; write the independent HOLD receipt without touching author text or visual.
- [x] Run focused validation, commit/push receipt and task, update PR description, and verify remote readback.

## How to verify

Compare receipt's three current author-file SHA-256 hashes and PR input head with `Get-FileHash` and `gh pr view 1681 --json headRefOid` at review time. Recount IDs and types from the two Markdown tables. Run `git diff --cached --check` and `npm run check:tasks`, reporting the five pre-existing untracked duplicate open/done task copies separately. Confirm the final commit touches only this task and its unique receipt, then read back PR #1681 body and labels.

## Notes

The independent review receipt is `docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-68-current.md`. It gives source and visual HOLD at `c080405` and `c080410` for unsourced angle/length qualifiers, plus visual HOLD at `c080215` and `c080414` because achieved factory-filled product is shown before the narrative's 1961 reveal. The duration STOP persists: 1,652 body manuscript characters are only about 396.5 seconds at the repository's 250 characters/minute proxy, not actual TTS. Two fresh blind narration readers, actual audio timing, independent art check, owner approvals, and payment gates remain outside this review. Five older untracked C08 task copies were not altered.

Validation checkpoint: receipt table has 68 distinct IDs; author file hashes and PR author head still match. `npm run check:tasks` before `done` exited 1 on five pre-existing untracked duplicate open/done C08 task copies. The `done` command wrote this task to `tasks/done` but left its own open copy at `tasks/open/2026-10-22-independently-review-current-c08-kikkoman-68.md`; a single exact, non-recursive deletion attempt was rejected as `blocked by policy`. That sixth local duplicate remains untracked and will not be committed. Existing stale-claim and overlapping-scope warnings are unrelated. The exact staged files get `git diff --cached --check` before commit.