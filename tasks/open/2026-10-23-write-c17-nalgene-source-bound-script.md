---
id: 2026-10-23-write-c17-nalgene-source-bound-script
title: Write C17 Nalgene source-bound script and visual plan
status: review
priority: P1
area: docs
owner: codex-c17-script
claimed_at: 2026-10-23T03:23:57Z
created_at: 2026-10-23T03:23:52Z
completed_at:
branch: codex/brand-story-nalgene-c17-script
depends_on: []
scope:
  - docs/videos/story-everyday-nalgene-c17/script.md
  - docs/videos/story-everyday-nalgene-c17/script-source-notes.md
  - docs/videos/story-everyday-nalgene-c17/visual-plan.md
  - docs/videos/story-everyday-nalgene-c17/visual-plan.json
  - docs/videos/story-everyday-nalgene-c17/reviews/author-script-receipt.md
---

# Write C17 Nalgene source-bound script and visual plan

## Why

C17 Treatment and M01–M12 were independently checked and adopted on PR #1699. The episode still needs spoken Traditional Chinese narration and a scene-by-scene plan before an independent script review or owner script approval can occur. The 1949 brand origin, 1960s outdoor use, mid-1970s consumer business, 2008 scoped material announcement, and 2020 mass-balance product must remain distinct.

## Definition of done

- [x] Six chronological chapters have a concrete cold open, open loops, source-bound spoken lines, a one-to-one cute-mystery visual plan, and a clear closing answer/comment/subscription sequence.
- [x] Every factual line has a reviewable source mapping; illustration prompts contain no brand names, logos, readable text, real-person likenesses, or false documentary evidence.
- [x] Mechanical author checks and unresolved duration/source/visual/blind-reader gates are recorded. This task does not claim independent PASS, actual TTS duration, or production approval.

## Steps

- [x] Draft narration and per-line source notes from the adopted matrix.
- [x] Draft one-to-one visual cues and machine-readable plan with the fixed look preset.
- [x] Check IDs, chapter order, coverage, card runs, prompt restrictions, and task-board status; open a draft PR without auto-merge.

## How to verify

Use `git diff --check`, a local ID/source/visual consistency check, and `npm run check:tasks`. Record exact file hashes in the author receipt. A separate reviewer must reopen S1–S7 and check each line/visual delta; two readers must see narration only. Real body TTS must be at least 480 seconds before paid images.

## Notes

Base: adopted C17 PR #1699 head `2410b0976b22b57215069a4fe06e924d12bf6741`. Existing PR body has a stale HOLD after an automatic `blocked by policy` on editing; do not retry that action by another route. This script branch contains no paid or release work. Managed worktree attachment failed, so the Git worktree was created from the original C17 checkout and remains functional but unmanaged by the app.

Author draft PR: https://github.com/x812033727/travel_scanner/pull/1703 (draft, no-auto-merge). 69/69 line/source/visual IDs match; 60 illustration cues, 9 cards, max card run 1; `npm run check:tasks` and staged diff check passed. Next: another agent's independent line-and-visual review, two narration-only blind readers, then owner script approval. Body TTS, illustrated time share, and paid budget remain unmeasured/unapproved.
