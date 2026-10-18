---
id: 2026-10-09-video-translator-owned-control-fields
title: Preserve request-owned translator control fields before genuine review
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T13:25:27Z
completed_at:
branch: codex/stalled-video-reviewed-fixes-20261008
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Preserve request-owned translator control fields before genuine review

## Why

Genuine, successful translator results can stall before their required reviewer
because the model omits the empty `lines` array in a metadata-only worksheet or
changes the echoed source text. During the October 9 recovery, Travel's Japanese
and Korean metadata returned complete draft/critique/final envelopes without
`final.lines`; a later Japanese caption echoed one Chinese source without `那`.
Embedding's last Japanese caption unit changed twelve Chinese full-width commas
to ASCII commas. The translated text and original requests remained retained,
but the strict unit guard correctly stopped before the genuine reviewer.

Private, exact-receipt recovery views handled those known cases. The normal
workflow needs a conservative rule for request-owned worksheet fields so future
runs can use a paid result without rewriting its raw receipt or bypassing review.

## Definition of done

- [ ] A metadata-only result may recover omitted `lines: []` only when its
      request has zero caption lines and all required metadata is present.
- [ ] Reviewer input retains the original request's source identity, IDs,
      order, scenes and budgets, while preserving genuine translated text and
      critique; substantive or ambiguous drift remains rejected.
- [ ] Every recovered translator result still receives a real independent
      reviewer before its unit is merged. Raw results and receipts stay intact.

## Steps

- [ ] Reproduce the actual omitted-empty-array and source-echo cases with
      sanitized fixtures, keeping draft/critique/final distinctions.
- [ ] Define which fields are request-owned and when a derived reviewer view
      is safe; record the original and derived hashes without editing receipts.
- [ ] Verify non-empty missing lines, altered IDs/budgets/order, unrelated
      punctuation, substantive source changes and changed translations reject.

## How to verify

Run `node --test tools/video/automation/automation.test.mjs` and the applicable
tools checks. Use a local mock reviewer to prove an actual reviewer request is
required, the original model receipt stays byte-exact, and the merged result is
bound to the original source. No live or paid model request is needed.

## Notes

- Travel evidence under `<home>/mokaair-work/stalled-video-audit-20261008/`
  `overnight-20261009/dubs-selected`: `Travel-JA-known-paid-empty-lines-derived-proof.json`,
  `Travel-KO-known-paid-empty-lines-derived-proof.json`, and
  `Travel-JA-second24-real-outgoing-payload-and-independent-review.json`.
- Travel exact source-echo recovery restored only the outgoing reviewer's owned
  Chinese source field for line `6kvd`; its Japanese text, translator raw result
  and unreviewed cache stayed unchanged. It did not count a manual inspection as
  the formal reviewer.
- Embedding evidence under `<home>/mokaair-work/stalled-video-completion-20261008/`
  `embedding-audio/listener-round2/selected-languages-20261009`:
  `owned-source-view.literal-comparison.actual.json` SHA
  `fd42e71f56259c8de145f40a06f3e9d5e0c76489c5ec505d7e15ec435a3836e7`;
  original paid receipt SHA
  `9943bf1a8f70d5b73cc8eca7228566b58c22c163d98b04741ca1517057507ec2`.
- Current `keptWorksheet` preserves the model's echoed source. The recovery
  wrappers deliberately stop on drift; do not weaken those guards or retry the
  original translator. A permanent rule needs the negative cases above.
- This is a separate follow-up from the existing malformed-outer-brace parser
  task. Only the evidence handoff is authored here; production tools are frozen.
