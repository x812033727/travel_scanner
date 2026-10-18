---
id: 2026-10-10-add-audited-source-extension-for-held
title: Add audited source extension for held news
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T01:47:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/router.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/validation.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_validation.py
---

# Add audited source extension for held news

## Why

Two held articles need an additional official source: GitHub/SB1000 candidate
a540117f-7e42-4709-af6f-1ac7366b257d needs the governor's later signing notice;
Microsoft Orchard candidate77a835d1-5f8e-4f53-a75d-d657dccbd537 needs the
versioned author paper to distinguish its model/method scores from the dataset
card. The existing refresh service only handles news_evidence_changed and
re-fetches already stored URLs. There is no audited source-addition service for
these editorial holds. Do not fake an evidence-change hold or modify evidence
rows directly to force that route. Microsoft physical-AI candidate
63cb5134-d2fa-47d3-92bd-f18a3bfaecf8 also needs an audited completion of its
existing official source excerpt: the saved excerpt ends before the cited
framework claim, while the complete source page supports that wording.

## Definition of done

- [ ] An authorized content manager can extend a held article's evidence through
      a guarded audited service while retaining original sources and histories.
- [ ] Fetching respects configured enabled hosts, source roles, robots, safe
      redirects and rate limits; absent source policy remains an explicit hold.
- [ ] Any changed evidence invalidates prior verification eligibility and sends
      the actual saved locales through normal independent review gates.
- [ ] Commit/enqueue uncertainty is reconciled from durable audits and jobs.

## Steps

- [ ] Review the two exact official-source proposals, the truncated existing
      source excerpt and active ownership.
- [ ] Design the narrow service/schema/route and source-policy handling.
- [ ] Test invalid hosts, changed evidence, preserved history and single dispatch.
- [ ] Obtain production readiness and apply only the three exact guarded candidates.

## How to verify

Meaningful service/validation tests must exercise real saved drafts and review
fingerprints, not fabricated approval markers. Run API Ruff/mypy and the affected
news suites. For production, preserve full before/after evidence and draft seals,
real audit IDs and public-locale readback separately from queue success.

## Notes

- Proposals are stored at <home>/.codex/news-review/20261010-6f71/
  source-extension-proposals-primary2.json (SHA256
  ebeed614072f472b06bdf0c312fccad969cca9ac61e8551837d13fc6deb99ff2).
  Recheck the proposal's actual bytes and current source pages before use.
- The governor notice supports the signing outcome; it does not establish every
  legal effect or effective date. Orchard's paper and card identify distinct
  backbones/methods; do not infer that the card is obsolete.
- Original 208-ID operation: 2026-10-10-news-held-cohort-recovery.
  This follow-up does not authorize broad source-setting or queue changes.
- Physical-AI's existing five saved documents, including the Chinese wording,
  already contain the historical corrections. Keep them unchanged; refresh or
  extend the actual evidence through an audited service before re-verification.
