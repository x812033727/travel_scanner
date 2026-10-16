---
id: 2026-10-11-add-audited-correction-for-obsolete-held
title: Add audited correction for obsolete held news claim ledgers
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T10:51:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/tests/test_news_automation.py
---


# Add audited correction for obsolete held news claim ledgers

## Why

Genuine Guide draft editing preserves the candidate's historical claim ledger.
Sanders0c72c4f4-500d-45f6-9bc4-d08f7c531bea claim12 still asserts20 countries
using only Verge policy/AI listings; glassesddf85a1f-84b9-4eec-8481-5eb0a94e0157
claim14 cites tech for unsupported Muse Charm. Independently reviewed Guide
corrections remove those assertions, but do not change the native claims.
Audited navigation repair correctly refuses any historical ledger citation.
Neither dropping evidence nor treating historical multi-source citations as
implicitly obsolete is acceptable; these stories remain unpublished.

## Definition of done

- [ ] Provide an independently reviewed, dry-run-first exact held-candidate
  correction through an active content actor, fresh whole12 CAS/NOWAIT and
  no active DB/RQ work; refuse published candidates or uncertain old intents.
- [ ] Bind all five genuinely saved Guides, their revision/audit provenance,
  complete original ledger and retained current-source bodies. Replace only
  explicitly justified obsolete/unsupported claims with a fully source-bound
  ledger; archive every old claim and complete before/after actor provenance.
- [ ] Preserve Source roles/configuration, Evidence bodies/hashes, all old
  assessments/runs/revisions/audits, assets, retries and judge caps. Invalidate
  stale verification eligibility without manufacturing a pass or a source.
- [ ] Keep ledger correction separate from evidence removal, verification,
  enqueue and publication. Durable single-CID intent survives unknown outcomes.
- [ ] Test CAS drift, active editor/worker, malformed or unsupported replacement,
  unchanged old history/caps, atomic rollback, lost commit ack and fresh gates.

## Steps

- [ ] Inspect the full stored/current source bodies and all old claims, plus
  the actual current five Guide drafts; do not use claim indexes alone as proof.
- [ ] Implement and independently review the narrow service/CLI and tests.

## How to verify

Run API Ruff, mypy app/tests and focused news tests including PostgreSQL
NOWAIT. A later authorized native operation must retain actual full12 before/
after and genuine audit readback before separate ordinary fact/locale/final
source review; correction is not publication.

## Notes

Unclaimed capability gap; no native ledger/evidence mutation has occurred.
Read R/audited-legacy-navigation-repair-readonly-design-v1.json SHA17ae4b0c
and owner-resolution5c3d6964; the exact historical source URLs and excerpts
are in held-defect-0c72c4f4 and held-defect-ddf85a1f native-content-state-v1.
Six Guide corrections and three model-card source diffs do not authorize
claim deletion or reset the original caps. Preserve each unknown intent.
