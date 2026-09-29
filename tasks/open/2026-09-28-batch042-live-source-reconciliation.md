---
id: 2026-09-28-batch042-live-source-reconciliation
title: Batch042 live source reconciliation
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T17:17:03Z
completed_at:
branch:
depends_on:
  - 2026-09-28-correct-batch042-seo-glossary-links-before
scope:
  - docs/article-localization/releases/batch042-source
---

# Batch042 live source reconciliation

## Why

PR #942 corrects five misleading glossary references in four repository zh-TW sources: seo-search-intent, seo-content-quality, technical-seo-checklist and seo-learning-roadmap. Their live source revisions still require a fresh comparison and guarded source correction before translated-locale import.

## Definition of done

- [ ] Reconcile all four live source revisions against the reviewed repository corrections while preserving intervening editorial work and live visibility.
- [ ] Store exact before/after versions and hashes, dry-run and idempotency results, and source-correction receipts for downstream locale releases.

## Steps

- [ ] Wait for merged CI-green source corrections and the required same-image isolated rehearsal environment.
- [ ] Read current production under the release locks; compare article status, active source versions, published/draft hashes and all target-locale drafts.
- [ ] After the guarded backup/deploy/writer checks, prepare and inspect the explicit four-article source-correction dry-run.
- [ ] Apply only the reviewed link-to-text changes when the expected revisions still match; stop each conflicted entry and preserve its state.
- [ ] Verify visible text is unchanged, misleading links are gone, and a rerun reports unchanged before importing translations.

## How to verify

Use the existing source-correction and staged release tools documented in `ops/release/README.md` and article-localization references. Bind the result to `docs/article-localization/batch042-source-links-evidence.md`; save sanitized receipts under the scoped release directory.

## Notes

Intentionally unclaimed. The earlier Batch042 read-only receipt is `receipt-20260928T150309Z.json`, SHA-256 `167d0a345864d1a3ca2117b585e8aaee91e5ef7dcd099954efd65f28e783f29f`; it is historical evidence, not a fresh release preflight. No production write was performed. The owner has no available nonproduction Docker environment, so the required isolated rehearsal remains a blocker; CI smoke cannot substitute for it.
