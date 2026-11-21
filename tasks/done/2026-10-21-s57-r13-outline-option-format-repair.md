---
id: 2026-10-21-s57-r13-outline-option-format-repair
title: S57 R13 outline option format repair
status: done
priority: P1
area: docs
owner: codex-s57-outline-author
claimed_at: 2026-10-21T01:42:38Z
created_at: 2026-10-21T01:42:35Z
completed_at: 2026-10-22T00:34:37Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s57/brief.md
  - docs/videos/curio-s57/review/r13-author-outline-format.md
---

# S57 R13 outline option format repair

## Why

S57 R12's `brief.md` A/B table is invisible to `outlineOptions`, so `review-push --gate outline` created a zero-option owner card. That card cannot validate the A/B choice even though a delegated local A continuation is recorded. Repair only the outline's Markdown shape after the R12 technical audio artifacts and checks are frozen.

## Definition of done

- [x] Replace the A/B table with parser-valid A and B headings, summaries, and hooks while preserving its decision and source limits.
- [x] Verify exactly two parsed options, five before/after hashes, unchanged narration/script, and a same-body policy request SHA where applicable.
- [x] Obtain [independent delta/source check](../../docs/videos/curio-s57/review/r13-independent-outline-format.md), then accurately rebind delegated local outline decision and site card; do not claim personal owner review.

## Steps

- [x] Diagnose current zero-option card and draft a minimal repair proposal in `review/r12-media-readiness/outline-format-repair-proposal.md` (outside this task's creative scope).
- [x] Wait for the R12 `check-audio` execution to finish and capture audio card status: check exits 1, audio HOLD, no audio card submitted.
- [x] Apply the exact narrow `brief.md` format edit and write the [R13 author receipt](../../docs/videos/curio-s57/review/r13-author-outline-format.md).
- [x] Independent reviewer PASS; rebind local recommended A to current `brief.md` SHA and re-push an A/B outline card. New website card is pending the owner.

## How to verify

Run the repository `outlineOptions` on the edited brief; compare exact creative-file SHA-256 values, `policyRequest` JSON SHA, and `script.md` narration hash against R12; `node tools/video/cli.mjs lint --slug curio-s57 --json`; `npm run check:tasks`.

## Notes

R12 audio's first machine check is complete and HOLD: 159/159 transcript records, 43 flags; its site audio card was not submitted. R13 changes only the A/B section of `brief.md` (`0c8284f9…` → `6b0cd778…`). The [author receipt](../../docs/videos/curio-s57/review/r13-author-outline-format.md) records an exact reversible diff, parser output, unchanged policy body and creative hashes, lint, and task check. A separate [independent reviewer](../../docs/videos/curio-s57/review/r13-independent-outline-format.md) confirmed PASS for the narrow format/source delta. Local recommended A was rebound to the new brief SHA under the user's delegated-choice instruction; the new website outline card contains A/B and is **pending** the owner. The old site's prior approval belongs to the stale zero-option SHA and does not approve the new card. Jev recommended A at 0.99, but no automatic approval applied. No paid art or music was created by this repair.
