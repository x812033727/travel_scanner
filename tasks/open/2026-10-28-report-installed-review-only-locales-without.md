---
id: 2026-10-28-report-installed-review-only-locales-without
title: Report installed review-only locales without false source drift
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-28T03:41:47Z
completed_at:
branch:
depends_on: []
scope:
  - docs/article-localization/report_progress.py
  - docs/article-localization/test_report_progress.py
---

# Report installed review-only locales without false source drift

## Why

After a reviewed localization bundle is installed and published, the progress
report can reject its existing-language review-only jobs as source-pack drift.
The wave6 report on 2026-10-28 exited 0 with no batch errors and recorded all
81 publications/browser verifications, but twenty review-only jobs reported
`source pack changed after baseline`. Its stage counters therefore report only
the 48 newly rendered jobs as reviewed, although the unchanged official bundle
publisher independently validated all 68 approved target documents.

## Definition of done

- [ ] Reproduce the report's twenty review-only source-drift issues using a small fixture.
- [ ] Admit only a valid hash-bound installation for report-only source comparisons.
- [ ] Preserve refusals for actual source/artifact/review drift, unrelated installations,
      altered receipts and paths outside the pinned repository.
- [ ] Distinguish newly translated work from independently reviewed existing text;
      never inflate publication or review counts from file existence.

## Steps

- [ ] Inspect report_progress.staged_locale and pipeline.assert_no_drift/admitted_installation.
- [ ] Confirm why review-only jobs do not receive the same installation admission
      as the 48 full jobs; preserve original jobs and receipts while diagnosing.
- [ ] Implement the narrow report fix and meaningful positive/negative tests.
- [ ] Run the report tests and rerun a hash-pinned report without rewriting history.

## How to verify

Run the report-progress test module with the API Python environment. Exercise a
review-only locale whose containing pack changed solely through the exact
approved bundle installation, and negative cases changing source prose, review
hashes, installation bindings and unrelated locales. A subprocess exit 0 is not
enough: inspect errors, per-locale issues and all stage counters.

## Notes

The release itself is separately evidenced by manifest
`94239e012d0bf4a858c47b7e94f767c9aebf6ea51d481981fa0f7ae37894629a`,
native 81 draft/81 publication operations, all 85 current public documents,
independent preservation auditing and 170 actual desktop/mobile screenshot
reviews. Do not rerun a production publication or change old approvals to make
this report green. The new report is a current-cohort observation against its
original pinned baseline, not a reconstruction or advancement of the missing
historical program ledger. No implementation has been attempted on this ticket.
