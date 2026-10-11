---
id: 2026-10-11-translate-held-news-ingestion-error-messages
title: Translate held-news ingestion error messages
status: in-progress
priority: P2
area: api
owner: codex-news-held-error-copy
claimed_at: 2026-10-11T07:38:39Z
created_at: 2026-10-11T07:38:38Z
completed_at:
branch: codex/news-held-bundle-ingestion
depends_on: []
scope:
  - apps/api/app/i18n.py
---

# Translate held-news ingestion error messages

## Why

The held-news ingestion service introduced 15 AppError codes outside an
operator-only module. Their reader-facing translations were missing from the
existing API error catalog, so a non-default locale would receive a generic
sentence. The complete API run found this with the existing error-coverage
test: 7118 passed, 458 skipped and this one failure.

## Definition of done

- [x] All 15 new codes describe the actual refusal in every existing locale.
- [x] Existing codes and sentences remain unchanged, and normal coverage passes.

## Steps

- [x] Add precise sentences to the existing news error catalog in i18n.py.
- [x] Run the existing localization and error-response tests and review all copy.

## How to verify

Run the existing test_error_localization.py and relevant existing i18n/error
response tests. Run Ruff and mypy on the changed catalog. Independently compare
the resulting tables to the prior catalog and actual service refusals, including
safe handling of an already-used operation and an expired snapshot.

## Notes

- Root checked current branches, remote heads, open PRs and landed history for
  apps/api/app/i18n.py before claiming. No active task or open PR touches it.
- This ticket owns only the catalog. The four previously reviewed ingestion
  implementation/test files remain frozen. No test or exemption is changed.
- Complete API log: external evidence file held-ingestion-full-api-pytest-v2.log.
  Its exit code is 1. The sole failure is
  test_every_public_error_code_has_a_sentence_in_every_locale; this is a real
  omission in PR1439 rather than a baseline failure or permission decision.
- The initial two CI documentation failures had the same eight personal-path
  cause. Root replaced those with home placeholders; the amended head's
  web-checks already passed. Further required checks remain pending.
- The catalog is frozen at SHA256
  d0c8d74c364546f63fe89e2aa79a8b013b125026c4bf18de457dd13eedf7c697:
  15 codes in five existing locales, 75 new sentences, 123 additions and no
  deletion. Removing only those additions restores the original catalog bytes.
- The existing localization/i18n tests pass: author 13 passed in 0.74s,
  Root 13 passed in 0.71s. Full API Ruff and mypy app471 pass afterward.
  The four ingestion implementation/test files retain their reviewed hashes.
- The shared event-date error uses date-rule wording rather than claiming
  every source date must be equal. An already-used operation tells the
  operator to inspect the saved record, rather than invent a replacement retry.
- PostgreSQL CI on the prior documentation-only head executed all 179 news
  cases without a skip, including all three new lock/version cases. This
  demonstrates those tests ran, but required CI must pass at the final PR head.
- This is a correction to the existing catalog and coverage contract; no
  production save, provider call, content approval or publication is performed.
- Nonauthor final review held-news-ingestion-error-localization-independent-review-v1.json,
  SHA256 7bca0ffef2bee63050a1d1a2123d8a3cc9dc6f2fbd71804f14bd110c2f77d2a9,
  passes all 75 sentences, exact prior whole-module bytes/AST and all original
  four frozen hashes. Corrected final-head CI is still required before merge.
