---
id: 2026-10-22-record-c07-owner-script-and-storyboard
title: Record C07 owner script and storyboard approval
status: done
priority: P2
area: docs
owner: codex-c07-owner-receipt
claimed_at: 2026-10-22T15:05:18Z
created_at: 2026-10-22T15:05:13Z
completed_at: 2026-10-22T15:05:41Z
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/owner-script-approval.md
---

# Record C07 owner script and storyboard approval

## Why

The owner approved C07's current script and storyboard direction after the independent source, two blind narration, and visual text checks. Record the exact approved bytes separately from the earlier Treatment decision and future paid gate.

## Definition of done

- [x] A SHA-bound owner decision receipt for the 73-line script and 73-beat visual plan.

## Steps

- [x] Confirm the owner reply and the two approved file hashes.
- [x] State paid production and remaining timed-media gates accurately.

## How to verify

`Get-FileHash` for `script.md` and `visual-plan.md`, compared with the receipt and PR #1680 head; `git diff --check` for the scoped change.

## Notes

Approval is only for this script and storyboard direction. It does not authorize paid media or publication. The C07 source and two blind reads are at the same script SHA; the complete visual preflight binds the current visual SHA.
