---
id: 2026-10-22-independently-review-c08-84-line-v5
title: Independently review C08 84-line v5 source and visual delta
status: review
priority: P2
area: docs
owner: codex-c08-independent-v5
claimed_at: 2026-10-22T18:26:18Z
created_at: 2026-10-22T18:26:04Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-84-delta-v5.md
---

# Independently review C08 84-line v5 source and visual delta

## Why

Two narration-only blind readers held v4's story flow, so the author revised C08's 84 spoken lines and paired visuals. Independently recheck the new factual claims, source ceilings, adjacent continuity, and visuals without editing authored material or inheriting v4 PASS.

## Definition of done

- [x] A unique exact-hash v5 receipt gives precise PASS/HOLD IDs for changed narration and paired visuals, including c080408 and c080608–609.
- [x] Only this task and its scoped receipt are committed; older untracked duplicate task copies remain untouched.

## Steps

- [x] Verify the author head and three input hashes, then compare v4 to v5 and reopen K1, GK R1/D1, MoMA M1, Ekuan E1, K4/K5/K7, K3 and J1 within their actual scopes.
- [x] Count paired IDs and card/shot structure, record the narrow factual verdict, and read back the draft PR body and head.

## How to verify

Get-FileHash of the three authored inputs; gh pr view 1681 --json headRefOid,isDraft,autoMergeRequest,labels,body; compare the 84 script and visual IDs in order; git diff --cached --check and exact staged-file list.

## Notes

Author head `5ce9f7c8b9c0f17f9e65b9cd2661a16bd8e36560`; script SHA-256 `ACCC7EB9FB001AE819119FBC0296AFD5F3CD0D1D09389740796F33342036F991`, visual SHA-256 `38C3B4CEDC6DE1CF45F18AA5EE272DB7737AF25B92885A4035DFC4434C225B68`, addendum SHA-256 `82D1147FE720B4ECB3A9222C8A19E76717BC40B4E70B56EA9A3256F5D22DEDE5`. Source HOLD C08-V5-S01 at c080512: K5 states a regional cap-rounding purpose, not a measured reduction in hand injuries or a global glass-bottle redesign. c080408 and c080608–609 pass only within the non-quantified, non-causal limits in the receipt. Duration and later media/owner gates remain held. Six pre-existing policy-blocked duplicate open-task copies must not be staged or removed.
