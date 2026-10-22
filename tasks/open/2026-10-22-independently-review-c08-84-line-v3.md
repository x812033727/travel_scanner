---
id: 2026-10-22-independently-review-c08-84-line-v3
title: Independently review C08 84-line v3 sources and visuals
status: review
priority: P2
area: docs
owner: codex-c08-independent-v3
claimed_at: 2026-10-22T18:07:38Z
created_at: 2026-10-22T18:07:34Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-84-v3.md
---

# Independently review C08 84-line v3 sources and visuals

## Why

PR #1681 author head 3c6408aa1 expands C08 from 68 to 84 narration/visual pairs with 2007–2018 source material. Another reviewer must check source scope, story fit, every paired visual, old HOLD repairs and documentation notes without changing the author's files.

## Definition of done

- [x] Reopen K5, K6, K7 and J1 primary materials and old sources relevant to changed claims.
- [x] Audit all 84 narration and 84 paired visual rows, including 13 postproduction cards.
- [x] Write a precise independent PASS/HOLD receipt tied to the three current SHA-256 hashes and author head.
- [x] Commit and push only this review ticket and unique receipt; update/read back draft PR body.

## Steps

- [x] Inspect worktree, PR, adopted Treatment, source addendum, skills and active task scopes; claim only a unique receipt path.
- [x] Independently inspect K5 printed p45, K6 release, K7 manager interview and J1 slide 15, plus K1/K2a/K3/MoMA/GK/K4 as needed.
- [x] Pair every current script ID with its visual row, inspect source attribution, product chronology, drawing claims, hook and duration proxies.
- [x] Validate staged diff, commit/push, update PR body and read back head/draft/label and body.

## How to verify

Compare this receipt with author input head 3c6408aa1e410fcfc3f721f28b40d90ef3834e9c and script/visual/addendum hashes. A focused parser must find 84 unique same-order IDs in both files, 71 shot/13 card, and a one-card maximum streak. Run git diff --cached --check; confirm staged and committed names are only this ticket and its receipt. Read back PR #1681 head, draft state, no-auto-merge label and body. npm run check:tasks is expected to fail locally on six pre-existing untracked duplicate C08 open task files; preserve them after an earlier policy-blocked removal.

## Notes

K5/K6/K7/J1 support the attributed 2007 cap, separate 2011 sealed product and trademark survey claims within their stated scope. Old v2 HOLD wording and filled-shot contradictions are repaired. Current overall HOLD is narrative/process line c080605 (and its visual c080605), paired visual c080513, source-addendum R1 ID misindex (c080213–214 instead of c080215), and the visual-plan header's incorrect 奇聞檔案局 series label. Preserve the full questionnaire caveat in notes, not voice-over. No paid media, author edits, merging or publication.

The 84/84 receipt and this narrow ticket were committed/pushed in ee46ea1350c0ce3bcf0c5fecfc0bd2793ee83bf4. The draft PR #1681 body was updated and read back with an exact text match, the no-auto-merge label and that remote head. The focused staged diff check passed. npm run check:tasks remains red on the same six untouched, pre-existing untracked duplicate C08 task files; the policy-blocked removal was not retried.
