---
id: 2026-09-28-batch042-live-source-reconciliation
title: Batch042 live source reconciliation
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-30T00:10:40Z
created_at: 2026-09-28T17:17:03Z
completed_at: 2026-09-30T00:19:03Z
branch: claude/zh-tw-glossary-link-reconciliation
depends_on:
  - 2026-09-28-correct-batch042-seo-glossary-links-before
scope:
  - docs/article-localization/releases/batch042-source
---

# Batch042 live source reconciliation

## Why

PR #942 corrects five misleading glossary references in four repository zh-TW sources: seo-search-intent, seo-content-quality, technical-seo-checklist and seo-learning-roadmap. Their live source revisions still require a fresh comparison and guarded source correction before translated-locale import.

## Definition of done

- [x] Reconcile all four live source revisions against the reviewed repository corrections while preserving intervening editorial work and live visibility.
- [x] Store exact before/after versions and hashes, dry-run and idempotency results, and source-correction receipts for downstream locale releases.

## Steps

- [x] Wait for merged CI-green source corrections and the required same-image isolated rehearsal environment. (rehearsal waived by the owner, informed, 2026-09-29)
- [x] Read current production under the release locks; compare article status, active source versions, published/draft hashes and all target-locale drafts.
- [x] After the guarded backup/deploy/writer checks, prepare and inspect the explicit four-article source-correction dry-run.
- [x] Apply only the reviewed link-to-text changes when the expected revisions still match; stop each conflicted entry and preserve its state.
- [x] Verify visible text is unchanged, misleading links are gone, and a rerun reports unchanged before importing translations.

## How to verify

Use the existing source-correction and staged release tools documented in `ops/release/README.md` and article-localization references. Bind the result to `docs/article-localization/batch042-source-links-evidence.md`; save sanitized receipts under the scoped release directory.

## Notes

Intentionally unclaimed. The earlier Batch042 read-only receipt is `receipt-20260928T150309Z.json`, SHA-256 `167d0a345864d1a3ca2117b585e8aaee91e5ef7dcd099954efd65f28e783f29f`; it is historical evidence, not a fresh release preflight. No production write was performed. The owner has no available nonproduction Docker environment, so the required isolated rehearsal remains a blocker; CI smoke cannot substitute for it.

## Done 2026-09-30 (claude-opus-5-5)

Taken over with the owner's consent in chat.
Live zh-TW drafts and published revisions matched the pre-correction pack
(`88cfde04d`) exactly, so no editor change existed to preserve (the
comparison was a read-only script in the api container, not the four-lock
procedure; the write itself held the deploy lock). After a
verified `pg_dump`, the eight Batch040-042 guides were updated together under
the deploy lock; every locale reran `unchanged` and the removed links are gone
from the public pages. The isolated rehearsal was waived by the owner.
Receipt: `docs/article-localization/releases/batch042-source/README.md`.
