---
id: 2026-10-23-independently-review-c16-bialetti-v7-script
title: Independently review C16 Bialetti v7 script and visuals
status: in-progress
priority: P1
area: docs
owner: codex-c16-v7-independent
claimed_at: 2026-10-23T07:31:59Z
created_at: 2026-10-23T07:31:51Z
completed_at:
branch: codex/c16-bialetti-v7-source-visual
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/independent-script-source-visual-v7.md
---

# Independently review C16 Bialetti v7 script and visuals

## Why

The author changed C16 from the previously reviewed 81-line v6 to a 72-line v7. The old independent PASS is not evidence for the new bytes; source claims and paired visual directions need fresh review on PR #1704 exact head `02051051742014e18de262e29819618206c6bcad`.

## Definition of done

- [x] An independent receipt gives a source verdict for all 72 oral lines, a paired-visual verdict for all 72 rows, the exact four file hashes and any production handoff HOLD.
- [x] The author script and visual plan remain unedited in this branch.

## Steps

- [x] Read the primary issuer sources, then audit every current narration line and paired visual, including M16/M17 boundaries.
- [x] Compare Markdown and JSON structurally and review every unequal prompt for meaning and forbidden-image risk.
- [x] Write `docs/videos/story-everyday-bialetti-c16/reviews/independent-script-source-visual-v7.md` with exact verdict and minimum repair.
- [ ] Open a draft review PR stacked on PR #1704 and attach it to this task.

## How to verify

Run `npm run check:tasks` and `git diff --check`. Independently extract the Markdown table and JSON `shots`: 72 unique line IDs in script/MD/JSON, same order, 63 `shot` and 9 `stats`, 9 unequal shot prompt strings only. Read the receipt against the four pinned hashes and PR #1704 exact head.

## Notes

Current verdict: 72/72 narration-source PASS; 72/72 visual-to-narration semantic PASS; overall visual file handoff HOLD because JSON c160210 omits the Markdown prohibition on drawing the filter or water path, which can spoil the mechanism reveal. Eight other prompt differences are also documented by ID and need synchronization. No paid production, owner approval, merge, upload, or publication is authorized here.
