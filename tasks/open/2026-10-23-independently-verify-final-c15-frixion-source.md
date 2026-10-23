---
id: 2026-10-23-independently-verify-final-c15-frixion-source
title: Independently verify final C15 FriXion source and visual delta
status: review
priority: P1
area: docs
owner: codex-c15-final-delta
claimed_at: 2026-10-23T04:30:27Z
created_at: 2026-10-23T04:30:03Z
completed_at:
branch: codex/brand-story-frixion-c15-final-delta
depends_on: []
scope:
  - docs/videos/story-everyday-frixion-c15/reviews/independent-final-delta.md
---

# Independently verify final C15 FriXion source and visual delta

## Why

The C15 author changed H07, H08 and N05 after two narration-only blind readers held the prior draft for repeated information. The previous source/visual PASS was bound to different bytes. A separate reviewer must check the changed claims and paired images against the issuer originals before fresh blind reads.

## Definition of done

- [x] A separate receipt identifies the author head and four exact Git-blob SHA-256 values.
- [x] H07, H08 and N05 and their paired visuals have PASS/HOLD decisions from direct PILOT source reading.
- [x] The 87 script lines, visual rows and JSON items have matching order and narration, with the image preset verified.
- [x] The review remains a separate draft PR with no paid or owner-approval claim.

## Steps

- [x] Compare author head `be7bad23848f925dda3495701802bafa0f8f43c4` with previous `31e43913902cc397a4bd3e6924a01b692f63f83f`.
- [x] Read PILOT's Part 1, Part 2 and current FAQ directly; decide each changed claim and image.
- [x] Check exact Git-blob hashes, 87/87/87 parity and model/preset; write independent receipt.
- [x] Open a separate draft PR and read back its gates.

## How to verify

Run the parity/checksum script described in the receipt, `git diff --check`, and `npm run check:tasks`. Read back draft/label/auto-merge status of the review PR.

## Notes

Direct source review PASS for H07/H08/N05 and paired text visuals; full narration-only blind reads remain pending. In the Windows checkout, raw `Get-FileHash` on `visual-plan.json` differs from the Git blob SHA-256 because of line-ending conversion. All four receipt hashes are computed from Git blob bytes. No author files were changed.
