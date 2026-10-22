---
id: 2026-10-22-repair-c12-pyrex-blind-narration-a
title: Repair C12 Pyrex blind narration A findings
status: in-progress
priority: P1
area: docs
owner: codex-c12-script-repair
claimed_at: 2026-10-22T15:36:13Z
created_at: 2026-10-22T15:36:03Z
completed_at:
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/script.md
  - docs/videos/story-everyday-pyrex-c12-script/visual-plan.md
  - docs/videos/story-everyday-pyrex-c12-script/author-blind-a-repair.md
---

# Repair C12 Pyrex blind narration A findings

## Why

Independent blind narration read A placed the 80-line C12 draft at HOLD (script SHA-256 `491AEE730835B0FFC6AC034E544AF25BB257C0CAD354BF0FC845DB8376411036`). It found an early final-chapter reveal, repeated obstacles, a weak run of modern examples, process language, and a next-video mention. The source and visual receipts covered the old bytes, so the author needs a narrow revision with a new hash and an explicit handoff.

## Definition of done

- [x] Revise only the needed script and visual-plan rows, keeping 80 ordered IDs and 67 illustration / 13 card direction with a maximum run of 2 cards.
- [x] Leave an author-only SHA and changed-ID receipt that routes the new bytes to independent review without self-approval.
- [ ] Run local structure and repository checks; push this narrow revision to draft PR #1692.

## Steps

- [x] Read AGENTS, brand-story, youtube-video story and script-writing rules, the source matrix, and the blind A HOLD.
- [x] Reopen applicable primary pages and revise the repeated beats, final comparison, oral clarity, and ending.
- [x] Adjust only visual rows whose scene or card meaning moved.
- [ ] Verify hashes, IDs, scene types, diff, task format, and video-doc checks.
- [ ] Commit and push only `script.md`, `visual-plan.md`, `author-blind-a-repair.md`, and this task file.

## How to verify

Compare `git show HEAD:<file>` with working files by ID; compute `Get-FileHash` SHA-256 for both; parse 80 unique ordered IDs and visual `I`/`C` types; run `git diff --check`, `npm run check:tasks`, and `npm run test:docs-videos`. Confirm the draft PR's new head after push. Old review receipts may be used as routing evidence only.

## Notes

Author revision changes 34 narration IDs and 8 visual IDs, listed in `docs/videos/story-everyday-pyrex-c12-script/author-blind-a-repair.md`. S3 live FAQ timed out in this pass; N01 did not expand the historical claim. Independent source/visual recheck, two new-hash blind reads, pronunciation, owner script review, measured audio duration, images, cost, and publication stay as separate gates. Other agents' untracked review-task files in this shared worktree are outside this task and must not be staged. `npm run check:tasks` currently fails because those two open copies duplicate tracked done tasks; the coordinator was notified, and this task must not delete them.
