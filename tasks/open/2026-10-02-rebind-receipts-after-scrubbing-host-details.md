---
id: 2026-10-02-rebind-receipts-after-scrubbing-host-details
title: Rebind receipts after scrubbing host details from hash-bound evidence
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-02T17:16:40Z
completed_at:
branch:
depends_on:
  - 2026-09-23-scrub-host-details-from-docs
scope:
  - docs/ai-terms-series/postgresql-validation.json
  - docs/ai-terms-series/publication.json
  - docs/article-localization/releases/2026-09-22/batch010-singapore
  - docs/article-localization/releases/2026-09-22/batch011-jeju
  - docs/article-localization/releases/batch021/evidence.json
  - docs/article-localization/releases/batch022/evidence.json
  - docs/catalog-content-reviews/2026-09-09-followup.json
  - docs/catalog-content-reviews/2026-09-09-followup-result.md
  - docs/videos/so-thats-why/season2/reviews/completion/T37.md
  - docs/videos/so-thats-why/season2/reviews/completion/T37.json
  - tasks/done/2026-09-22-localize-jeju-car-rental-guide-in.md
  - tasks/done/2026-09-23-release-localized-household-purchasing-guides-batch021.md
  - tasks/done/2026-09-23-release-localized-website-planning-guides-batch022.md
  - tools/repo-hygiene.test.mjs
---

# Rebind receipts after scrubbing host details from hash-bound evidence

## Why

Ticket 2026-09-23-scrub-host-details-from-docs replaced local user paths, the PuTTY
saved-session name and a disposable database password with placeholders in about 290 tracked
files. Eleven files were left alone because another file records their SHA-256, so editing
them would silently break that receipt:

| File still carrying a host detail | Recorded by |
| --- | --- |
| `docs/ai-terms-series/postgresql-validation.json` (session name, root login, user path, the disposable password) | `docs/ai-terms-series/publication.json`, written by `export_publication.py` |
| `docs/article-localization/releases/2026-09-22/batch010-singapore/release-candidate-equivalence.json` | `release-evidence.json` in the same folder |
| `docs/article-localization/releases/2026-09-22/batch011-jeju/` — `independent-content-review.json`, `release-candidate-equivalence.json`, `source-correction-review.json`, `structural-qa.json`, `svg-independent-review.json` | each other, `release-evidence.json`, and `tasks/done/2026-09-22-localize-jeju-car-rental-guide-in.md` |
| `docs/article-localization/releases/batch021/evidence.json` | `tasks/done/2026-09-23-release-localized-household-purchasing-guides-batch021.md` |
| `docs/article-localization/releases/batch022/evidence.json` | `tasks/done/2026-09-23-release-localized-website-planning-guides-batch022.md` |
| `docs/catalog-content-reviews/2026-09-09-followup.json` (237 paths; `apps/api/tests/test_catalog_content_review_followup.py` reads it) | `docs/catalog-content-reviews/2026-09-09-followup-result.md` |
| `docs/videos/so-thats-why/season2/reviews/completion/T37.md` | `T37.json` in the same folder |

`tools/repo-hygiene.test.mjs` tolerates exactly these counts in its `KNOWN` table and fails
if they grow. The container behind the password was deleted the day it was made, so nothing
here is live; it is recon-level data in a public repository.

## Definition of done

- [ ] None of the files above contains a local user path, the saved-session name or the
      password, and every receipt that records their digest matches the new bytes.
- [ ] Their entries are gone from `KNOWN` in `tools/repo-hygiene.test.mjs`.

## Steps

- [ ] For each binder, decide: regenerate it with the tool that wrote it (for example
      `export_publication.py` for `publication.json`), or update the recorded digest by hand
      with a sentence saying the evidence was redacted on a later date and why.
- [ ] Check whether any binder is itself bound (a digest of `release-evidence.json`,
      `T37.json`, and so on, recorded somewhere else) and follow the chain; also check
      `docs/videos/long-form/review.json`, which binds about 70 files.
- [ ] Run `node --test tools/repo-hygiene.test.mjs`, `npm run test:tools`, and the API test
      that reads `2026-09-09-followup.json`.

## How to verify

```bash
node --test tools/repo-hygiene.test.mjs
npm run test:tools
cd apps/api && uv run pytest tests/test_catalog_content_review_followup.py -q
```

## Notes

- Use the placeholders the hygiene test names: `<repo>`, `<home>`, `<saved-session>`,
  `<disposable-password>`. Rotate nothing; history keeps the old bytes and rewriting it is out
  of scope.
