---
id: 2026-10-22-independently-review-c08-v5-3-spout
title: Independently review C08 v5.3 spout clarity delta
status: review
priority: P2
area: docs
owner: codex-c08-independent-v5-3
claimed_at: 2026-10-22T18:41:41Z
created_at: 2026-10-22T18:41:35Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/spout-clarity-review-20261023-v5-3.md
---

# Independently review C08 v5.3 spout clarity delta

## Why

C08 v5.3 changed two spout narration rows and their paired card after a narration-only reader found the previous geometry hard to follow aloud. An independent source and visual delta receipt is needed before a new blind read.

## Definition of done

- [x] Bind a narrow PASS/HOLD verdict to the v5.3 author head and three input hashes.
- [x] Check changed narration/card plus adjacent mechanism against E1, K4, M1 and D1.
- [x] Commit only this task and its unique review receipt to draft PR #1681; read back draft and no-auto-merge state.

## Steps

- [x] Reopen direct sources and compare v5.2-to-v5.3 changed rows.
- [x] Write exact-hash review receipt in the claimed scope.
- [x] Push review-only commit and read back PR body/state.

## How to verify

`Get-FileHash -Algorithm SHA256` on the three author files; `git diff f43f6242c 6d8f14af7 -- docs/videos/story-everyday-kikkoman-c08`; count the `| c08xxxx |` table rows; `gh pr view 1681 --json headRefOid,isDraft,autoMergeRequest,labels,body` after push.

## Notes

E1 and K4 support lower-shorter/upper-forward relative geometry; M1 supports less spout pooling. No measured flow rate or zero-drip guarantee is inferred. The six older untracked duplicate task copies remain untouched because prior deletion attempts were policy-blocked. This is a source/paired-visual delta review only; new blind readers and owner gate remain separate.
