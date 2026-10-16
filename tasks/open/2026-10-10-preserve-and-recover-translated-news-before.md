---
id: 2026-10-10-preserve-and-recover-translated-news-before
title: Preserve and recover translated news before pack validation
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T09:39:55Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
---

# Preserve and recover translated news before pack validation

## Why

Candidate28289a1b-5b85-4cb0-8fee-92beef07250f stopped with a known
LocalizedDocument validation error: an English summary had308characters,
exceeding the300 limit. Current persisted state is failed/news_judge_approved,
retry8, no Guide article and only a zh-TW cached document. Translation runs
and locale/judge assessments succeeded, but the invalid English document is
not in the candidate cache, saved revisions or run rows. Editing a saved
English draft cannot repair this item because none exists. Repeating provider
calls would discard the useful distinctions between known malformed output,
preserved reviews and uncertain requests.

## Definition of done

- [ ] Successful raw translated outputs remain recoverable with original
  candidate/source/input hashes and genuine run identities before pack validation.
- [ ] Known malformed output can be corrected and independently rechecked
  through an audited recovery path without inventing prior saved documents,
  model approvals, responses or publication.
- [ ] The300character constraint and native content/publication checks remain
  enforced. Original cap/retry/audit history and uncertain requests are preserved.

## Steps

- [ ] Trace translation-to-pack ordering and the missing persistence boundary.
- [ ] Preserve raw responses and validation errors safely; distinguish an
  explicit new reviewed correction from resending an uncertain provider request.
- [ ] Integrate with the separate audited held-bundle ingestion task for
  no-guide/partial-cache candidates; do not write the database/cache directly.

## How to verify

Add focused API tests for a308character translated summary, validation failure
after a successful translation, source/input drift, partial-language cache and
unknown provider outcomes. Verify genuine native revision/audit joins and that
an ingestion/save operation does not fabricate assessments or publish.

## Notes

- Actual full readback: external news-review/20261010-6f71/
  newholds-diag3-0711.capture/sql.json at09:03:34Z.
- Run rows contain metadata/token usage and error fields, with no translated
  response documents. Candidate draft_bundle_json has only zh-TW.
- Existing follow-up:2026-10-10-add-audited-held-news-bundle-ingestion.
- No candidate282 recovery write or new provider request has been made.
