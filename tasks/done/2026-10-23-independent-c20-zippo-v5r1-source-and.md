---
id: 2026-10-23-independent-c20-zippo-v5r1-source-and
title: Independent C20 Zippo v5r1 source and visual delta review
status: done
priority: P2
area: docs
owner: codex-c20-v5r1-delta
claimed_at: 2026-10-23T07:51:25Z
created_at: 2026-10-23T07:51:15Z
completed_at: 2026-10-23T07:54:24Z
branch: codex/c20-zippo-v5r1-source-delta
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/independent-v5r1-source-visual-delta.md
---

# Independent C20 Zippo v5r1 source and visual delta review

## Why

The full v5 independent audit held one spoken line and four paired visuals. The author repaired those exact rows. The revised bytes need a separate source and image-rule decision before owner script review.

## Definition of done

- [x] Verify the author diff against old and new exact commits and lock four input hashes.
- [x] Reopen primary UK and US Zippo warranty pages and the Curio image rule; decide every repaired row.
- [x] Verify all four current row lists and Markdown/JSON text mirror; record remaining gates.
- [x] Save the independent receipt and open a draft, no-auto-merge PR stacked on the author branch.

## Steps

- [x] Review five changed IDs without editing author files.
- [x] Run targeted mechanical and task checks.
- [x] Commit review receipt and task record; create draft PR.

## How to verify

`git diff 836e2c8c1bf2d0f72e320892a2ddd50638d4088b 7eac4c6b9689532f7246c00d6fd1408992d0cf27 -- docs/videos/story-everyday-zippo-c20`; compare the five changed IDs. Reopen the primary URLs in the receipt. Parse the four current files and compare ID order, narration, source tags, prompts/card text; run `npm run check:tasks` and `git diff --check`.

## Notes

The delta passes 1/1 oral source row and 4/4 paired visual rows. Combined with the unchanged 59 oral and 56 visual PASS rows from full review PR #1766, the exact v5r1 inputs have 60/60 source and 60/60 visual PASS. The receipt is `docs/videos/story-everyday-zippo-c20/reviews/independent-v5r1-source-visual-delta.md`. Two fresh narrator-only blind reads and owner approval remain; no paid calls occurred.
