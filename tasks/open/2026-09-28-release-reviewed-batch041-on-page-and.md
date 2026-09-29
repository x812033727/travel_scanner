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
