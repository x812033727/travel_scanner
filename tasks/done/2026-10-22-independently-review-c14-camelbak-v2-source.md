---
id: 2026-10-22-independently-review-c14-camelbak-v2-source
title: Independently review C14 CamelBak v2 source and visuals
status: done
priority: P2
area: docs
owner: codex-c14-v2-independent-review
claimed_at: 2026-10-22T17:45:46Z
created_at: 2026-10-22T17:45:43Z
completed_at: 2026-10-22T17:48:41Z
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/reviews/independent-v2-source-visual-delta-review.md
---

# Independently review C14 CamelBak v2 source and visuals

## Why

C14 CamelBak v2 changes the narrated chronology and many visual prompts after v1 narration HOLD. The old source/visual PASS is hash-bound to v1 and cannot be transferred. A separate reviewer must reopen the primary sources and record a version-bound verdict without changing author files.

## Definition of done

- [x] A new review receipt binds its source and visual verdicts to the current six source-file hashes and PR author HEAD, with exact line/shot IDs and a correction for any HOLD.

## Steps

- [x] Reopen the brand, SEC, patent, and official trademark material; check the 61 v2 sentences and their source notes.
- [x] Check all 61 shots, exact look, prompt exclusions, bookends, and paper arithmetic; preserve measured-duration and media gates.
- [x] Push only this receipt and task to draft PR #1695 and read back the PR body.

## How to verify

Recalculate SHA-256 for the Treatment, matrix, script, notes, visual MD and JSON; parse script IDs and JSON shots for same sequence; inspect `git diff --check`, `npm run check:tasks`, `git status --short`, and `gh pr view 1695 --json headRefOid,isDraft,body,labels` after pushing.

## Notes

Receipt: `docs/videos/story-everyday-camelbak-c14/reviews/independent-v2-source-visual-delta-review.md`. Source PASS for all 61 lines, visual HOLD for I01 `post_text`: its phrase “不是原型比賽日期” can deny O10’s attributed 1989 race year. Correct to “成立年份不證比賽日期” or drop the second clause, then rehash and recheck I01/O10. The USPTO PDF timed out on direct web open; official search index supplied the first-use excerpts, and v2 uses neither date in speech/cards. Planned 505.4 seconds is not measured narration; do not mark the 480-second gate PASS. No blind review was read or signed.
