---
id: 2026-10-22-independently-review-patagonia-c09-treatment-sources
title: Independently review Patagonia C09 Treatment sources
status: done
priority: P2
area: docs
owner: codex-c09-independent-reviewer
claimed_at: 2026-10-22T13:05:18Z
created_at: 2026-10-22T13:04:59Z
completed_at: 2026-10-22T13:12:43Z
branch: codex/brand-story-patagonia-c09-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09-review
---

# Independently review Patagonia C09 Treatment sources

## Why

The C09 Patagonia Treatment needs a second agent to read primary and contemporaneous sources, inspect the catalog images and edition history, and bind a claim-level verdict to the exact Treatment and source-matrix bytes before owner review.

## Definition of done

- [x] Independent M01-M10 and Treatment chapter verdict is recorded with source locations and both input SHA-256 hashes in `docs/videos/story-everyday-patagonia-c09-review/independent-source-review.md`.
- [x] Material revisions are handed back without editing the author files or opening a production gate.

## Steps

- [x] Claim an exact sibling review-document scope; confirm PR #1685 and the two expected SHA-256 hashes.
- [x] Reopen S1-S4 and S6-S9 directly, inspect S8 scan images and S9 edition caveat, and read S5 Appendix I.
- [x] Judge M01-M10 and each Treatment chapter without borrowing the author's verdict.
- [x] Record and push the version-bound HOLD receipt to the draft PR.

## How to verify

`Get-FileHash docs/videos/story-everyday-patagonia-c09/{treatment,source-matrix}.md -Algorithm SHA256` (run as two PowerShell calls); `git diff --check`; `npm run check:tasks`; open each direct URL in the review receipt. The S8 p0/p48/p67 original-size images and pp2-3, 8-11, 48-53 embedded scans were viewed in the browser; their small print was not represented as fully transcribed.

## Notes

Overall HOLD on these exact bytes. The 1972 foreword asks climbers to use chocks and avoid pitons on clean routes, not to buy less. Bestseller comes only from a 2022 Patagonia retrospective. The scanned catalog has piton and chock pages, but its inner cover says One Dollar and its p67 price list is headed Great Pacific Iron Works; Karabin documents different 1972-74 printings. The Treatment's 1972 same-copy cold open therefore overstates what was verified. Its linked 20-episode plan also is absent in this branch. Root was notified for author revision; no author file was edited. Recheck affected claims against new hashes after revision.
