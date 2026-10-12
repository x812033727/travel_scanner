---
id: 2026-10-12-reconcile-passing-storyboard-verdicts-with-nonempty
title: Reconcile passing storyboard verdicts with nonempty minor remarks
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-12T03:01:10Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
---

# Reconcile passing storyboard verdicts with nonempty minor remarks

## Why

An illustrated-slides storyboard can finish native keyframes with every ordinary
shot marked `judge.passed: true`, yet remain pending after submission. In H03,
81 selected file hashes and expected-shot coverage match, the lowest ordinary score
is 7.18 against the configured threshold 7, and no shot needs review. However,
48 of 76 ordinary shots retain 49 judge remarks. `storyboardSubmission` carries
those remarks in each shot's `judge.problems`, while `storyboard_check_passed`
requires every ordinary shot's problems to be empty. The first 9.29-score shot
therefore fails the backend predicate. Five explicitly accepted shots are skipped
correctly and are not the cause.

Keep all source remarks and the existing owner gate. Reconcile the meaning of a
passing verdict with actionable problems, or make the pending reason explicit,
without converting an unreviewed/problematic image into an approval.

## Definition of done

- [ ] The native producer and backend use a documented, consistent rule for a passing verdict with remarks.
- [ ] Pending reviews identify the actual blocking reason; score, coverage and kept-shot issues remain distinguishable.
- [ ] Original judge remarks, selected-file hashes and owner decisions remain intact.
- [ ] Regression coverage exercises passing-with-remarks, failed verdicts, low scores, incomplete coverage and explicitly kept pictures.

## Steps

- [ ] Reproduce with the H03 review and determine which remarks are advisory versus blocking under the existing policy.
- [ ] Implement the narrow producer/backend contract fix and tests; do not auto-approve existing pending reviews by rewriting their evidence.

## How to verify

Run `node --test tools/video/review/sync.test.mjs` and the relevant
`apps/api/tests/test_video_automation_settings.py` tests. Replay the unmodified
H03 payload against the original and revised predicate, documenting any changed
decision. Production resubmission requires a normal source-bound review, not a
hand-edited local approval.

## Notes

- H03 storyboard review `da0651b4-5904-4232-81ec-d71928e3e551`, submitted
  2026-10-12T02:50:35.295903Z; content SHA
  `3557df3d544adaaeb4f8ad5a073d23d4c60ace5ea8f909ab1c1ffff95ce44af8`.
- Read-only diagnosis and exact-payload predicate replay are preserved outside git
  at `C:/Users/x8120/mokaair-work/videos/curio-h03/_audit/storyboard-pending-diagnosis.md`
  and `.json`. No payload, score or approval was modified.
- Similar pending evidence appears in the LLM production task
  `2026-10-04-ai-term-large-language-model`; the existing cute-explainer keep-best
  and ILLUSTRATED documentation tasks address different behavior.
