---
id: 2026-10-23-independently-recheck-c16-bialetti-v7-visual
title: Independently recheck C16 Bialetti v7 visual handoff delta
status: in-progress
priority: P1
area: docs
owner: codex-c16-v7-visual-delta
claimed_at: 2026-10-23T07:51:53Z
created_at: 2026-10-23T07:51:34Z
completed_at:
branch: codex/c16-bialetti-v7-visual-delta
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/independent-visual-handoff-v7-delta.md
---

# Independently recheck C16 Bialetti v7 visual handoff delta

## Why

PR #1704 changed the nine prompts that had blocked the earlier independent C16 v7 visual handoff review. The new bytes must be checked against the old exact head and the spoken lines before that HOLD can be lifted.

## Definition of done

- [x] Independent delta receipt states PASS/HOLD for all nine changed scenes on new head `f064752a557617d591cd1841996956eba2c07a52` and pins all four hashes.
- [x] No edits to author script or visual plans in this branch.

## Steps

- [x] Compare all author changes from old head `02051051742014e18de262e29819618206c6bcad` to new head.
- [x] Recheck each of the nine changed visuals against its narration and forbidden-depiction constraints.
- [x] Independently verify MD/JSON field equality and 72/72 ID pairing.
- [ ] Open a draft receipt PR stacked on the new exact author head.

## How to verify

Run the structural Python readback against both Git heads, `npm run check:tasks`, and `git diff --check`; inspect the exact four SHA-256 values and nine-row verdict table in the receipt.

## Notes

Verdict: PASS, no remaining blocking shot. New JSON `c160210` explicitly keeps the shell closed and bars filter/water-path depiction; all 63 prompts now match Markdown exactly. Source notes and script bytes are unchanged. This does not imply blind reads, owner approval, measured TTS, paid media, upload, or publication.
