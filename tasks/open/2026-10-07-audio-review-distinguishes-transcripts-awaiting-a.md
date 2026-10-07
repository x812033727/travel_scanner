---
id: 2026-10-07-audio-review-distinguishes-transcripts-awaiting-a
title: Audio review distinguishes transcripts awaiting a judge
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T09:32:26Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# Audio review distinguishes transcripts awaiting a judge

## Why

`audioCheck()` counts every unmatched, unflagged transcript without a second opinion as `judged_fine`, even when `noul` is null and the native audio check has not reached its judge loop. A partial audio review can therefore describe an unfinished judgement as accepted.

The citation tutorial's actual interrupted check on 2026-10-07 had 68 current transcript rows for 143 lines: 60 exact, 3 alike and 5 unmatched rows with `noul:null` and no second opinion. The native payload reported `judged_fine:5`, although none of those five had a Jev verdict. This payload was audited locally and was not submitted as an audio review.

## Definition of done

- [ ] Unmatched rows awaiting a real judge verdict are distinguishable from rows the judge accepted; null or absent `noul` never establishes `judged_fine`.
- [ ] A partial check accurately reports checked, matched, judged, flagged and unjudged coverage without implying that all narration was accepted.
- [ ] Existing accepted judge results and bound second opinions retain their intended classification.

## Steps

- [ ] Review `audioCheck` and audio summaries together; keep existing server payload compatibility or document any necessary follow-up.
- [ ] Add a meaningful regression for interrupted primary transcription with unjudged mismatches, and run the existing review sync tests.

## How to verify

`node --test tools/video/review/sync.test.mjs`; inspect a source-bound partial payload with 68 checked / 143 total and five unmatched rows whose judge score is null. It must not count those rows as judged fine. No provider request is needed to reproduce this calculation.

## Notes

Independent read-only duplication check on 2026-10-07: open PR #1361 at bb29bc8cfd694fba02d9d188ece39cee6c120ddf and the subsequently refreshed #1364 at f2f82943bbfec2d0f9f34a91f0cb78188d035d7a retain the same residual-count audioCheck formula. Neither exact-head changed-file list includes sync.mjs or sync.test.mjs, and neither adds an unjudged/null-score classification. Their paid-answer/stage fixes and existing retained-storyboard/approved-language tickets do not resolve this defect. Keep this ticket open; scope overlap is not a duplicate implementation.

Actual read-only audit: `<home>\mokaair-work\ai-teaching-continuation-20261007\partial-audio-payload-audit.json`, checked at `2026-10-07T09:31:53.606Z`. Input check JSON SHA-256 `63560b283fe060b31eb1c8cc2dd09a621ed6103d4abe28e5a7bfecba976bfa88`; awaiting rows `ci006`, `ci027`, `ci029`, `ci091`, `ci035`. This is a payload-classification defect, separate from the preserved unknown ASR request for `ci037` and the Windows full-answer journal ticket. No paid request, approval, review payload or canonical check file was changed by the audit.
