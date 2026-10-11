---
id: 2026-10-10-track-ledger-duplicate-coverage-gap
title: Track Ledger duplicate coverage gap
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T05:15:23Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/duplicates.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_automation.py
---

# Track Ledger duplicate coverage gap

## Why

The news duplicate filter includes titles from candidates that are still drafting or verifying. A same-event candidate can therefore become `duplicate` even when the matching story never publishes. The duplicate assessment currently stores neither a matched article ID nor a snapshot of the compared titles, so a duplicate verdict alone does not prove retained public coverage.

In the original208 recovery, Ledger candidate `c318db49-235f-46c9-b108-f9e0209ec569` received native duplicate assessment `d90182b0-27f0-4a52-aa3b-c63cf5c0cc3c` at 2026-10-10T04:47:52Z (confidence 0.91). Independent comparison of its bound CoinDesk source and the Decrypt source for `efc90b90-7f0d-41f9-b4a3-2b4f7d59b4b0` identifies the same October 9 Ledger/CryptoBilis event. The latter was verifying at that time, then was captured as `needs_redraft`, retry_count 6, with no guide at 04:51:31Z. An in-flight title explaining the duplicate is an inference; the historical matched parent is not recorded. Another published same-event article has not yet been ruled out.

## Definition of done

- [ ] Establish whether an actual published same-event Ledger article exists, using published revision and source bodies rather than a pending title.
- [ ] Record a bounded recovery decision for the exact Ledger pair, preserving the original208 membership, native assessment, capped rewrites, and uncertain requests.
- [ ] Prevent future duplicate classification from silently implying retained public coverage; retain sufficient matched-record evidence for review.
- [ ] Verify the chosen behavior with meaningful pending-title, failed-peer, published-peer, and concurrent-state cases.

## Steps

- [ ] Inspect a fresh read-only published Guide search and the exact pair's full SQL/RQ history after the currently eligible recovery cohort finishes.
- [ ] Read the actual same-event source and five locale publication evidence, if any, and choose one canonical continuation using independent factual reviews.
- [ ] Prepare any necessary recovery in a new bounded namespace with fresh CAS and native audit evidence; do not replay a completed owner90 job or reset caps.
- [ ] Implement and test a narrowly scoped duplicate coverage remedy if the investigation confirms the gap.

## How to verify

Run focused news automation tests for a pending match that later fails, a genuinely published match, and concurrent state changes. For the exact Ledger pair, retain the full candidate/run/audit readback and verify actual published revisions and five public locale responses after a remedy. A queued job, duplicate assessment, or unpublished draft does not satisfy publication verification.

## Notes

- Original runtime evidence is outside the checkout at `<home>\.codex\news-review\20261010-6f71\`.
- `owner90-batch02-terminal-0457.capture/sql.json` SHA256 `bcefe068d6b392be50b949d588be2cd74ede5b327b6fe93973d254e766288844` captured the exact terminal state at 04:51:31Z.
- Independent bound-source comparison `owner90-native-duplicate2-source-comparison-independent.json` SHA256 `4b36b2d612885a6845ff7d61b61bcb0f7066ce03cab914e0ebf466920e3fd45f` supports the same-event finding; it does not establish the historical JEV parent.
- `owner90-native-duplicate2-published-guide-discovery-readonly.sql` SHA256 `c3b02aefcb371e7503a9117b5e0bb66f9bf9c33f224bf73d6d711e7cf24a9572` is a prepared bounded read-only search, not yet executed.
- That exact query was subsequently executed read-only at 05:31:02Z. Actual receipt `native-duplicate2-published-discovery-0542.json` SHA256 `db04f7344bf404e8385afd0cf5b8f2531f5d16a5b76129fa851ddfb54dee7302` found one published DWF guide and no Ledger match under the specified source/title/30-day filters. This is a bounded negative result, not proof that no Ledger coverage exists anywhere, and does not reconstruct the historical JEV parent.
- At filing, no duplicate restoration, retry, rejection, cap reset, approval, or publication was performed for this pair. Existing user authorization for news processing persists; this ticket itself is not a new authorization or a reason to request it again.
