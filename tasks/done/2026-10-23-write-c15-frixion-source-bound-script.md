---
id: 2026-10-23-write-c15-frixion-source-bound-script
title: Write C15 FriXion source-bound script and visual plan
status: done
priority: P1
area: docs
owner: codex-c15-script
claimed_at: 2026-10-23T03:21:30Z
created_at: 2026-10-23T03:21:24Z
completed_at: 2026-10-23T03:26:49Z
branch: codex/brand-story-frixion-c15-script
depends_on:
  - 2026-10-22-c15-frixion-treatment
scope:
  - docs/videos/story-everyday-frixion-c15/script.md
  - docs/videos/story-everyday-frixion-c15/script-source-notes.md
  - docs/videos/story-everyday-frixion-c15/visual-plan.md
  - docs/videos/story-everyday-frixion-c15/visual-plan.json
  - docs/videos/story-everyday-frixion-c15/reviews/author-script-receipt.md
---

# Write C15 FriXion source-bound script and visual plan

## Why

The owner adopted C15's revised six-chapter treatment, but the episode still needs a source-bound spoken script and a one-to-one visual proposal before independent checks and any media purchase. The C15 treatment, matrix and their approval hashes must remain intact.

## Definition of done

- [x] Produce a chronological, hook-led author script with each spoken sentence mapped to the adopted source matrix.
- [x] Produce one-to-one visual prompts and postproduction cards with explicit limits on historical and technical implications.
- [x] Leave a reproducible author receipt with counts, hashes and the pending independent and owner gates.

## Steps

- [x] Verify the exact old tasks/open treatment file was absent and the completed copy preserved; commit only that user-completed move on the treatment branch.
- [x] Branch from the adopted treatment commit and claim a narrow script scope without force.
- [x] Reopen the primary sources, write the six-chapter narration, then map every line to one visual and source notes.
- [x] Run mechanical author checks and open a draft, no-auto-merge PR based on the treatment branch.

## How to verify

`npm run check:tasks`; `git diff --check`; compare IDs and counts across `script.md`, `visual-plan.md` and `visual-plan.json`; inspect `reviews/author-script-receipt.md`. Paper duration and picture share are estimates, not actual TTS or assembled-video checks.

## Notes

Source treatment is draft PR #1696, commit `7031cd928ba5f43856bf96af58732004d3a627bd`, adopted treatment SHA-256 `D84494C81E2034B116C0322EF416E17C3DDE860B58626D12DE2E73501980D9C0`, matrix SHA-256 `6E030F4399F6FD2AE99550DE89B5B46658D708CF870910199804069A784C4C09`. This task covers **authoring only**. A different reviewer must still do line-by-line source and paired-visual review, and two independent readers must assess narration without research notes. The owner has not approved this script or paid production. No TTS, images, music, import, upload or publication was performed. An app-managed worktree lookup failed; the script branch is a valid native Git worktree and remains separate from the treatment checkout.
