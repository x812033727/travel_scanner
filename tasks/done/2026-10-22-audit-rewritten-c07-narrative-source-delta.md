---
id: 2026-10-22-audit-rewritten-c07-narrative-source-delta
title: Audit rewritten C07 narrative source delta
status: done
priority: P2
area: docs
owner: codex-c07-rewritten-source-review
claimed_at: 2026-10-22T13:20:28Z
created_at: 2026-10-22T13:20:15Z
completed_at: 2026-10-22T13:26:01Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v7.md
  - tasks/open/2026-10-22-audit-rewritten-c07-narrative-source-delta.md
  - tasks/done/2026-10-22-audit-rewritten-c07-narrative-source-delta.md
---

# Audit rewritten C07 narrative source delta

## Why

The C07 author rewrote 49 narration rows and 38 visual rows after the v6 source review. Its PASS applies only to prior file hashes. The draft PR needs an independent, current, hash-bound source and visual-delta receipt before any later review can rely on these rows.

## Definition of done

- [x] Review every changed narration and visual row against directly readable B2/B3/M1/A1 and relevant B1/B4/B5/V2, recording source strength and limits.
- [x] Verify 77 unique script and visual IDs in matching order, 64 shots and 13 cards, and bind the review to all three current SHA-256 hashes.
- [x] Save the independent PASS/HOLD receipt on draft PR #1680 without changing script or visual plan.

## Steps

- [x] Compare the current rows with the preceding reviewed commit and inspect adjacent unchanged context.
- [x] Read the primary source pages, distinguish retrospective brand claims from museum objects and scholarly interpretation, and write the receipt.
- [x] Run applicable local checks and push the receipt.

## How to verify

`Get-FileHash docs/videos/story-everyday-dr-martens-c07/{script.md,visual-plan.md,script-source-notes.md} -Algorithm SHA256`; compare row IDs and row text with `git show 24edad7d6:<path>`; `npm run test:docs-videos`; `npm run check:tasks`; inspect PR #1680 head after push.

## Notes

Review result: 49/49 changed narration rows and 38/38 changed visual rows PASS for source boundaries. B3 gives first production date and later trade show, not first retail sale. M1's 1995 tartan object is a separate product, not evidence that 1980s user customization caused it. A1's HTML was directly read earlier in this session but the fresh reload timed out; its same-source indexed full text remained readable. V2 supplies political context, not evidence that photographed people wore the boots. No paid generation, owner script approval, upload, or merge is implied. Four unrelated pre-existing untracked duplicate task files make `npm run check:tasks` fail. The `done` command copied this ticket to `tasks/done/` but left its own open copy; removing that exact open copy was rejected by automatic policy. It remains untracked locally and is not staged for the PR; do not work around that rejection.
