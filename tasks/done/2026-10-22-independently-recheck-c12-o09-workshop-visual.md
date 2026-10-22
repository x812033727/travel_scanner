---
id: 2026-10-22-independently-recheck-c12-o09-workshop-visual
title: Independently recheck C12 O09 workshop visual
status: done
priority: P1
area: docs
owner: codex-c12-o09-recheck
claimed_at: 2026-10-22T16:14:16Z
created_at: 2026-10-22T16:13:53Z
completed_at: 2026-10-22T16:16:42Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-o09-visual-recheck-v3.md
---

# Independently recheck C12 O09 workshop visual

## Why

The independent C12 delta receipt held visual O09 because it placed a complete battery jar in a home kitchen before the museum account says Jesse brought home two cut bottoms. The author changed O09 on a new visual-plan hash; an independent reviewer must verify that exact delta.

## Definition of done

- [x] A fresh receipt binds the new script and visual hashes and gives O09 a source-based PASS/HOLD verdict.
- [x] The receipt checks O09 against adjacent scenes and explicitly limits what the verdict authorizes.

## Steps

- [x] Confirm current Git head and both file hashes.
- [x] Compare all 80 rows to the prior reviewed head and reopen the museum source.
- [x] Write the O09 receipt and run targeted checks.

## How to verify

`Get-FileHash` for both inputs; per-ID Git row diff against `99ea2632c`; `git diff --check`; `npm run check:tasks`.

## Notes

Receipt: `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-o09-visual-recheck-v3.md`. At `ae113851f`, script SHA remains `87D9B4BB...` and visual SHA is `EA563A3E...`; only O09 changed among 80 visual rows. Direct museum source recheck and O08–I02 continuity yield PASS: the complete jar remains alone on an industrial workshop shelf. `npm run check:tasks` exits 1 only for the two pre-existing unrelated duplicate open/done ghost IDs (blind-narration-review-a-for-c12 and independently-audit-c12-pyrex-script-and). They were preserved. Hash and row-ID checks passed; full media tests are not relevant to this one Markdown visual prompt.
