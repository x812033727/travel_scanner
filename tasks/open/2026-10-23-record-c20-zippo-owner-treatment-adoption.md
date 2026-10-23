---
id: 2026-10-23-record-c20-zippo-owner-treatment-adoption
title: Record C20 Zippo owner Treatment adoption
status: review
priority: P1
area: docs
owner: codex-root-c20
claimed_at: 2026-10-23T04:31:09Z
created_at: 2026-10-23T04:30:45Z
completed_at:
branch: codex/brand-story-zippo-c20
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/owner-treatment-adoption.md
---

# Record C20 Zippo owner Treatment adoption

## Why

The owner adopted the exact C20 Treatment in this chat after independent source review. Persist that decision with content hashes before script authors treat the direction as approved.

## Definition of done

- [x] Record the owner's exact adoption, the Treatment and matrix hashes, and the independent review PR.
- [x] State the regional warranty limits and which downstream gates remain separate.
- [ ] Keep the adoption receipt in a draft PR for review; no merge or paid production implied.

## Steps

- [x] Match the current PR #1708 author head and recompute the two content hashes.
- [x] Write `docs/videos/story-everyday-zippo-c20/reviews/owner-treatment-adoption.md`.
- [ ] Run task/diff checks, push the existing draft PR, and read back its status.

## How to verify

Use `Get-FileHash` on Treatment and matrix, `npm run check:tasks`, `git diff --check`, and `gh pr view 1708` to verify draft/no-auto-merge and the exact author head.

## Notes

2026-10-23: The owner replied `採用 C20 企劃方向` to the question naming PR #1708, review PR #1710, the UK/US service boundaries and the no-paid/no-upload scope. This receipt is a new narrow file; it does not edit historical Treatment or matrix assertions.
