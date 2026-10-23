---
id: 2026-10-23-independently-audit-c19-seven-bank-script
title: Independently audit C19 Seven Bank script and paired visuals
status: review
priority: P2
area: docs
owner: codex-c19-independent-source-visual
claimed_at: 2026-10-23T06:18:05Z
created_at: 2026-10-23T06:17:55Z
completed_at:
branch: codex/c19-seven-bank-source-visual-review-20261023
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/reviews/independent-script-visual-source-review-20261023.md
---

# Independently audit C19 Seven Bank script and paired visuals

## Why

The owner approved C19's revised Treatment, then PR #1742 submitted an author script and visual plan at a33b270152cf67b883a1ab11480fa4eb71234f80. The author's source notes and parity receipt are not an independent pass. Review all 79 lines and paired visuals against issuer originals without altering author files.

## Definition of done

- [x] All 79 narration and visual IDs have an explicit PASS or HOLD tied to direct official source locators.
- [x] The review receipt binds the four author files by independently computed SHA-256 and verifies four-way structure.
- [x] A separate draft, no-auto-merge PR contains only the review receipt and this task handoff.

## Steps

- [x] Create isolated worktree at the exact author head and confirm the adopted Treatment/source-matrix hashes.
- [x] Reopen official Seven Bank S1–S7 pages/PDFs, including S3 P14 and S4 P17–P18.
- [x] Compare each script row, notes row, MD visual row, and JSON shot row; classify 74 PASS and 5 HOLD.
- [x] Run task and diff checks, push branch, and open draft review PR.

## How to verify

Recompute the four SHA-256 values listed in docs/videos/story-everyday-seven-bank-c19/reviews/independent-script-visual-source-review-20261023.md; parse the four files to confirm 79 same-order unique IDs, identical narration/source tags and visual text, 67 shots, 12 cards, max card run 2. Run npm run check:tasks and git diff --check. Compare the new PR against the author branch to ensure it changes only this review receipt and task file.

## Notes

- Hold IDs: c190313 (fictional partner hesitation in image), c190409 (S3 says maintenance/funding costs, not physical cash replenishment or each partner's site decision), c190410 (prompt asks for a readable fixed amount symbol), c190501 (image shows the initial Tokyo corner rather than narrated expansion), c190607 (S4 describes document-reading services already offered, while line/image call them only future/unactivated).
- S3's partner text is PDF zero-index P14, printed page 13. S4 P17–P18 clarifies document reading. S7 separates July achieved >1,000 from future November 11 figures. S6 P12 shows an allied bank as early as May 2001; no need to invent all-first-day connectivity.
- Independent reader, owner, TTS, paid-media, import and publication gates remain distinct and pending.
- Draft PR #1745: https://github.com/x812033727/travel_scanner/pull/1745; base is exact author head a33b270, head 16b99ee0cf8d453854433132b1c89f0af023394c at creation; draft and no-auto-merge label applied. Do not mark this task done until that PR is merged or owner otherwise closes the review.
