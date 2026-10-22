---
id: 2026-10-22-independently-verify-c08-v5-1-cap
title: Independently verify C08 v5.1 cap-purpose correction
status: review
priority: P2
area: docs
owner: codex-c08-independent-v5-1
claimed_at: 2026-10-22T18:32:44Z
created_at: 2026-10-22T18:31:54Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-84-delta-v5-1.md
---

# Independently verify C08 v5.1 cap-purpose correction

## Why

The v5 independent source review held c080512 because K5 stated a European cap-rounding safety purpose, while the narration had claimed an achieved injury reduction and ambiguously broadened the changed part. Review the author's one-line v5.1 repair against K5 and the neighboring K7 product transition without editing author files.

## Definition of done

- [x] A unique exact-hash receipt states whether C08-V5-S01 is resolved and confirms all other narration/visual input bytes are unchanged.
- [x] Only this ticket and its scoped receipt enter the review commit; six older untracked duplicate C08 task copies remain untouched.

## Steps

- [x] Verify PR author head, three SHA-256 hashes, and the exact one-line diff.
- [x] Reopen K5 and K7, check c080510–513 and paired visual rows, then publish PASS/HOLD with remaining gates.

## How to verify

Get-FileHash for the three authored files; git diff 75c9db46e..b3c4985ee of the authored inputs; gh pr view 1681 --json headRefOid,isDraft,autoMergeRequest,labels,body; git diff --cached --check and exact staged-file list.

## Notes

V5.1 author input head `b3c4985ee4bce10b53a520b3b9238199b53e1e92`; script SHA-256 `53D82301F053189718BC2BD883A44A030A2F8694D4C25EA8645931829C8DBEA8`, visual SHA-256 `38C3B4CEDC6DE1CF45F18AA5EE272DB7737AF25B92885A4035DFC4434C225B68`, addendum SHA-256 `82D1147FE720B4ECB3A9222C8A19E76717BC40B4E70B56EA9A3256F5D22DEDE5`. C08-V5-S01 is resolved: c080512 now states K5's design purpose and only the cap change. Receipt: `docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-84-delta-v5-1.md`. Production and owner gates remain held; no author file was edited in this review.
