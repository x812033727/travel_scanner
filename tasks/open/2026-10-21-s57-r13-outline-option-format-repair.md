---
id: 2026-10-21-s57-r13-outline-option-format-repair
title: S57 R13 outline option format repair
status: in-progress
priority: P1
area: docs
owner: codex-s57-outline-author
claimed_at: 2026-10-21T01:42:38Z
created_at: 2026-10-21T01:42:35Z
completed_at:
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

- [ ] Replace the A/B table with parser-valid A and B headings, summaries, and hooks while preserving its decision and source limits.
- [ ] Verify exactly two parsed options, five before/after hashes, unchanged narration/script, and a same-body policy request SHA where applicable.
- [ ] Obtain independent delta/source check, then accurately rebind delegated local outline decision and site card; do not claim personal owner review.

## Steps

- [x] Diagnose current zero-option card and draft a minimal repair proposal in `review/r12-media-readiness/outline-format-repair-proposal.md` (outside this task's creative scope).
- [ ] Wait for the R12 check-audio pass and audio card status to be captured.
- [ ] Apply the exact narrow `brief.md` format edit and write the R13 author receipt.
- [ ] Request a reviewer who did not author the edit; rebind and re-push only after review.

## How to verify

Run the repository `outlineOptions` on the edited brief; compare exact creative-file SHA-256 values, `policyRequest` JSON SHA, and `script.md` narration hash against R12; `node tools/video/cli.mjs lint --slug curio-s57 --json`; `npm run check:tasks`.

## Notes

Task claimed while the separate R12 audio check is active. No `brief.md` edit has been made yet. Root requested this narrow author repair only after R12 audio results are frozen, followed by an independent check. No paid art or music is in scope.
