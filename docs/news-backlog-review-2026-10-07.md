# Current news backlog review — 2026-10-07

The owner requested publication or rejection of currently held news candidates, and
rewriting of the redraft queue. They explicitly selected existing AI review after
rewriting, with publication when qualified.

## Baseline

Captured at 2026-10-07 13:04 UTC (21:04 Taipei): 411 `manual_review`, 105
`needs_redraft`, four `failed`. The judge is enabled (Claude Opus 5.5), automation is in
automatic mode and all three verticals permit publication. No settings changes are needed.

The initial dry run found 389 eligible review holds. The other holds require source
refreshes, article edits, saved-bundle recovery or failure diagnosis.

## Evidence

Persistent operational artifacts live at
`<home>/.codex/news-review/20261007-fe41/`:

- `baseline.json`: all 520 candidates, their stored drafts, evidence, assessments and runs.
- `technical-holds.json`: the candidates excluded from straightforward AI review.

## Execution

All actions preserve evidence and use existing publication gates. No global settings,
retry caps or previous review hashes were changed.

- Twenty-five review holds and five redrafts entered the existing AI judge flow.
- Twenty-three complete saved bundles passed current hard checks and resumed without
  rewriting. Nine other complete bundles were materialized as unpublished drafts,
  had only CJK punctuation repaired, and entered the normal edited-draft review flow.
- Eight candidates refreshed changed evidence while preserving their five-language text.
- Thirteen existing drafts were saved/reverified: eleven had precise locale corrections
  and two already contained the requested correction. One of the eleven was subsequently
  rejected because a later official release supersedes its preview.
- Eleven AI/technology candidates wrongly classified as crypto were corrected with
  row guards and audit records.
- Two failed candidates entered normal retry. The duplicate Project Suncatcher candidate
  and an old Bitget market recap were rejected; the existing Suncatcher article was kept.

At 2026-10-07 13:27 UTC (21:27 Taipei), the immutable 520-candidate baseline had these
persisted states. These are a progress snapshot, not a final publication receipt:

| State | Count |
| --- | ---: |
| Published | 3 |
| Rejected | 4 |
| Duplicate | 2 |
| Discovered / queued | 69 |
| Locale review | 1 |
| Verifying | 1 |
| Manual review | 369 |
| Needs redraft | 71 |

## Continuing review

A one-shot supervisor began on the host at 13:29 UTC, PID 154702, operation directory
`/root/news-review-20261007-fe41/queue-driver/run`. It submits at most twenty original
manual-review candidates per batch using existing judge eligibility and enqueue helpers.
The next batch waits for persisted judge decisions or candidate status changes. Existing
active jobs are observed; failed or ambiguous provider calls are not replayed. The scope
is the original 411 manual-review IDs, with a fixed baseline-derived job tag. Current
status and receipts are in `STATUS.json`, `state.json`, `receipts.jsonl` and `driver.log`.
Its completion does not imply the other baseline redrafts or technical holds are resolved.

## Remaining repair

Japanese/Korean translations with an existing disclaimer were getting a second site
notice, which locale review removed before the helper inserted it again. A separate
code repair recognizes explicit existing warnings and generates source-neutral notices.
All 262 affected policy/pipeline/saved-bundle tests, full API lint and both API type checks
pass locally. Production rollout is still outstanding. Known disclaimer-loop redrafts
are held until that repair is live; source selection and remaining editorial holds need
their own guarded corrections.
