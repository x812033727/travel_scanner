---
id: 2026-09-28-release-reviewed-batch043-google-ranking-and
title: Release reviewed Batch043 Google ranking and Trends locales
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T17:14:35Z
completed_at:
branch:
depends_on:
  - 2026-09-28-localize-batch043-google-ranking-and-trends
scope:
  - docs/article-localization/releases/batch043-pair-a
---

# Release reviewed Batch043 Google ranking and Trends locales

## Why

The reviewed Google ranking-history and Trends-research packs add zh-CN, en, ja and ko documents and localized images. These eight article/locale targets remain absent from production and need the existing guarded publication workflow.

## Definition of done

- [ ] Publish the eight reviewed target documents after successful isolation, source and target-draft checks; preserve any withdrawal, expiry or conflict.
- [ ] Record per-article import, publication and public five-language desktop/mobile acceptance separately.

## Steps

- [ ] Complete the required same-image nonproduction Docker rehearsal; the owner currently has no available environment.
- [ ] Verify merged CI-green content, deployed assets, fresh live hashes/versions/visibility, a restorable backup and writer coordination before any guarded write.
- [ ] Use the explicit two-slug/four-locale dry-run and reviewed manifest, then verify an idempotent rerun.
- [ ] Check public body, images, canonical, reciprocal hreflang and same-language article links in all five locales on desktop and mobile.

## How to verify

Follow `ops/release/README.md` and the article-localization release workflow. Bind the release to the exact candidates in `docs/article-localization/batch043-pair-a-evidence.md`; save sanitized receipts under this task's release directory.

## Notes

Intentionally unclaimed. No production import or publication occurred. Local standalone previews and CI smoke do not replace the required isolated rehearsal or public acceptance. Preserve the source and reconcile any later source editorial revision through its own guarded version/hash workflow.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja and ko of both slugs are published. **zh-CN is not**: it waits for `2026-09-28-batch043-pair-a-final-independent-review`; after acceptance, dry-run and `--publish` only these two slugs with `--locale zh-CN`. Receipt: `docs/article-localization/releases/batch043-pair-a/`.

- Done: deploy `716bd5dc`; `pg_dump -Fc` backup
  `/root/travel_scanner_preimport_seo_20260929T101450Z.dump` (TOC readable);
  exact slug/locale dry-run, `--publish` under the deploy lock, rerun
  `unchanged`; links rebuilt; logged-out `verify_public.py --sitemap` pass.
- Skipped: the same-image isolated Docker rehearsal (none exists).
- Still open before this ticket can close: a desktop/mobile look at the
  published pages; the live zh-TW source still carries the pre-correction
  revision where the zh-TW dry-run says `update` (owned by the
  live-source reconciliation tickets, not changed here).
