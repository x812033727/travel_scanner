---
id: 2026-09-28-release-reviewed-batch041-on-page-and
title: Release reviewed Batch041 on-page and image locales
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T17:34:17Z
completed_at:
branch:
depends_on:
  - 2026-09-28-install-reviewed-batch041-image-seo-language
  - 2026-09-28-localize-on-page-seo-workflow-article
scope:
  - docs/article-localization/releases/batch041-pair-b
---

# Release reviewed Batch041 on-page and image locales

## Why

The two five-language repository packs do not publish database locale rows.
Release only on-page-seo-workflow and image-seo-workflow in zh-CN/en/ja/ko.

## Definition of done

- [ ] Resolve editorial acceptance, merge the content PR and reconcile live image source.
- [ ] Pass the same-image nonproduction Docker rehearsal and fresh version/hash checks.
- [ ] Verify backup, control concurrent writers, deploy and check service health.
- [ ] Dry-run the explicit slug/locale list and stop any conflicting record.
- [ ] Publish only eligible missing languages, preserving existing edits and visibility.
- [ ] Rerun unchanged and verify five-language desktop/mobile public pages and images.
- [ ] Verify canonical/hreflang, actual published-locale links and draft protection.
- [ ] Save per-article release receipts and final statuses.

## How to verify

Use the existing guarded localization release workflow and the exact final hashes
in docs/article-localization/batch041-pair-b-evidence.md.

## Notes

Leave unclaimed: no isolated rehearsal environment is available. The historical
image source predates #934. Reconcile currently plain-text related-reading labels
against actual target-language publication before enabling public links.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja, ko and zh-CN of both slugs are published. Receipt: `docs/article-localization/releases/batch041-pair-b/`.

- Done: deploy `716bd5dc`; `pg_dump -Fc` backup
  `/root/travel_scanner_preimport_seo_20260929T101450Z.dump` (TOC readable);
  exact slug/locale dry-run, `--publish` under the deploy lock, rerun
  `unchanged`; links rebuilt; logged-out `verify_public.py --sitemap` pass.
- Skipped: the same-image isolated Docker rehearsal (none exists).
- Still open before this ticket can close: a desktop/mobile look at the
  published pages; the live zh-TW source still carries the pre-correction
  revision where the zh-TW dry-run says `update` (owned by the
  live-source reconciliation tickets, not changed here).
