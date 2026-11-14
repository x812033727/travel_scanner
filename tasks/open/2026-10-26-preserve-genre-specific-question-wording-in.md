---
id: 2026-10-26-preserve-genre-specific-question-wording-in
title: Preserve genre-specific question wording in merged narrative receipts
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-26T05:59:12Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
---

# Preserve genre-specific question wording in merged narrative receipts

## Why

`panelVerdict` receives `panelQuestions(doc)`, so each blind reader answers the current story-series wording (including at most two opening teasers). `mergePanelVerdicts` rebuilds merged answers from global `NARRATIVE_PANEL`; its stored `question` text therefore shows legacy wording, such as at least three opening moments. Actual question IDs, yes/no votes, raw reader answers and rules/input hashes remain preserved, but the merged receipt is misleading for reviewers.

## Definition of done

- [ ] Merged receipt questions preserve the actual per-reader genre wording after validating compatible IDs/order/required flags.
- [ ] Default, story-series and tutorial panels retain their own question text with unchanged voting and evidence rules.
- [ ] Meaningful regression checks compare the input questions with the merged saved receipt for these variants.

## Steps

- [ ] Reproduce using the native panel functions and the current story-series question overrides.
- [ ] Make the bounded merger change without rewriting historical receipts.
- [ ] Run the affected native narrative tests.

## How to verify

See `docs/videos/brand-story-remakes-20261025/native-receipt-question-wording.json` for the frozen Seiko R4 example and exact hashes. The task is unclaimed; no core implementation was changed in the brand-remake PR.

## Notes

The current brand-remake workflow supplies the correct genre questions to each independent reader and preserves blind-input/binding/raw files. Do not reinterpret historical votes according to the misleading merged label or resample an unchanged narration.
