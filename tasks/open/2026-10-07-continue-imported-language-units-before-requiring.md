---
id: 2026-10-07-continue-imported-language-units-before-requiring
title: Continue imported language units before requiring a merged locale artifact
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T02:05:34Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/imported-long-languages/runner.mjs
  - docs/videos/imported-long-languages/runner.test.mjs
---

# Continue imported language units before requiring a merged locale artifact

## Why

The shared native translation flow retains one reviewed worksheet unit per call
and returns before the locale is fully merged. The imported language runner then
hashes `i18n/<locale>.json` immediately. On the 2026-10-07 approved-final handoff,
EP01 and EP05 each completed a translator and reviewer successfully, but paused
with ENOENT because only their first units were ready. Successful answers must
remain reusable; this is not permission to repeat a model request or reset spend.

## Definition of done

- [ ] A completed unit is persisted and reported as partial progress until every
      source-bound locale unit is reviewed and actually merged.
- [ ] The runner consumes exact retained answers and continues only unanswered
      units; it never hashes a missing locale file or treats a partial unit as a
      complete translation, caption set or language package.
- [ ] Existing unknown-result, source/configuration drift, STOP and producer-lock
      guards remain intact; incomplete/rejected model output stays held.
- [ ] A caption unit is checked against its exact original lines without claiming
      that other lines in the same scene were requested or reviewed; the final
      merged locale still requires every original selected line.

## Steps

- [ ] Review the exact pinned native flow and imported-runner contract, including
      existing PR #1355 work, before selecting the narrow integration change.
- [ ] Add multi-unit regressions for restart after one reviewed unit, no repeated
      successful calls, a unit inside a longer scene, actual locale merge, rejected
      output and unknown response.
- [ ] Validate captions and emitted language manifests through the real consumer.

## How to verify

Use meaningful multi-unit fixtures and request counters. One successful chunk
must not require a merged file; restarting must keep its original result and
request count. Full completion requires the actual merged locale artifact and
source-bound metadata/CC review readback. No paid media or production operations
are authorized by this follow-up.

## Notes

- First host attempt is preserved at
  `/root/renewed-finals-20261007/translation-resume-state.json` and profile logs;
  it exited held at `2026-10-07T02:04:22.951Z` with all isolated STOPs restored.
- Fresh native journal, HTTP and database readback confirmed exactly four
  successful subscription stages and zero unresolved results for EP01/EP05;
  no language review had been submitted. Operator evidence is outside Git at
  `C:/Users/x8120/mokaair-work/handoff/renewed-finals-20261007`.
- Preserve frozen production runtime and native source receipts. Any temporary
  external operator adapter is separate from completing this native-tool ticket.
- The isolated `validateResumeSheet` call also receives native `unitVideo`, which
  retains every line in a selected scene. `mergeSheet` then requires lines outside
  the caption unit. Fix validation of the exact requested unit while retaining
  full source/completeness validation of the final merged locale; do not narrow
  or relabel the request to hide a missing answer.
