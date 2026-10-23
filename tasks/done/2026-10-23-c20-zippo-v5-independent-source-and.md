---
id: 2026-10-23-c20-zippo-v5-independent-source-and
title: C20 Zippo v5 independent source and visual audit
status: done
priority: P2
area: docs
owner: codex-c20-v5-source-review
claimed_at: 2026-10-23T07:37:27Z
created_at: 2026-10-23T07:37:10Z
completed_at: 2026-10-23T07:43:04Z
branch: codex/c20-zippo-v5-full-source-visual-review
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/independent-v5-source-visual.md
---

# C20 Zippo v5 independent source and visual audit

## Why

Independently check the 60-line v5 script and 60 paired visual directions in author draft PR #1728, binding the verdict to exact author bytes.

## Definition of done

- [x] All 60 spoken claims and all 60 paired directions have explicit PASS/HOLD rows in an independent receipt.
- [x] Every HOLD has an exact line ID, primary-source or series-rule basis, and a narrow repair direction.

## Steps

- [x] Reopen the patent, company history and date-code record, UK repairs, US warranty/hinge/finish, and Double Arc first-party pages.
- [x] Verify script, source notes, visual Markdown and JSON pairings and hashes.
- [x] Commit the receipt and open a stacked draft PR without editing author files: [#1766](https://github.com/x812033727/travel_scanner/pull/1766).

## How to verify

Read the source URLs linked in the receipt. Recalculate SHA-256 of the four author files, run the Node parity check described in the receipt, `npm run check:tasks`, and `git diff --check`.

## Notes

Current result: spoken 59 PASS / 1 HOLD (`c200608`); paired visuals 56 PASS / 4 HOLD (`c200201`, `c200406`, `c200601`, `c200609`). Full receipt records the reasoning. No paid calls.
