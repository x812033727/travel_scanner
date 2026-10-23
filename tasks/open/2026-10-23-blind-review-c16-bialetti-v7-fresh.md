---
id: 2026-10-23-blind-review-c16-bialetti-v7-fresh
title: Blind review C16 Bialetti v7 fresh reader one
status: in-progress
priority: P1
area: docs
owner: codex-c16-v7-fresh-reader-1
claimed_at: 2026-10-23T08:03:27Z
created_at: 2026-10-23T08:03:19Z
completed_at:
branch: codex/c16-bialetti-v7-blind-fresh-1-20261023
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/blind-v7-fresh-reader-1-lock.md
  - docs/videos/story-everyday-bialetti-c16/reviews/blind-v7-fresh-reader-1-receipt.md
---

# Blind review C16 Bialetti v7 fresh reader one

## Why

Draft PR #1704 has a new C16 Bialetti v7 narrator text. It needs a fresh reader's story verdict before source, visual, or prior-review context can influence that verdict, followed by a byte-bound comparison against the author's exact PR head.

## Definition of done

- [x] Lock 12 narrator-only story verdicts against the supplied 72-line input, with line IDs and listener effects for every HOLD, before reading repository context.
- [x] Compare all projected spoken IDs, order, and text with PR #1704 head `f064752a557617d591cd1841996956eba2c07a52` and publish a separate receipt.
- [ ] Open a draft PR stacked on the author's PR head and attach it to the review task.

## Steps

- [x] Read only the narrator projection, verify its SHA-256, and save the dated lock outside the repository.
- [x] Read repository instructions and relevant skills only after lock, then compare with the exact author Git blob.
- [x] Copy the unchanged lock and independent receipt to the narrow review scope.
- [ ] Run checks, commit, push, and open the stacked draft PR.

## How to verify

`Get-FileHash docs/videos/story-everyday-bialetti-c16/reviews/blind-v7-fresh-reader-1-lock.md -Algorithm SHA256` must equal `89BC700F3829741CE31EE8EE80621ACE7972A6625B73463A5D967ECF8D12B21C`. Compare the 72 `[c160...]` lines of the supplied projection to the `ID` and `旁白` cells in `git show f064752a557617d591cd1841996956eba2c07a52:docs/videos/story-everyday-bialetti-c16/script.md`: same unique IDs, same order, exact same strings. `npm run check:tasks` and `git diff --check` should pass.

## Notes

Independent verdict: 6 PASS, 6 HOLD. The projection has 72 unique spoken IDs and matches the author head's 72 unique IDs/texts exactly. The author script raw SHA-256 is `E8C7CE3F426CAB6AB6EA37756CC6A73BF34AF09E3C6D0CB088288D928982A918`. The PR description still cites 81 lines and old script SHA `726D...`; use the exact Git blob. This task makes no author-script changes or historical-source/visual verdict and gives no media, owner, merge, upload, or publication approval.
