---
id: 2026-09-28-release-reviewed-batch040-affiliate-and-store
title: Release reviewed Batch040 affiliate and store locales
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T17:25:07Z
completed_at:
branch:
depends_on:
  - 2026-09-28-install-reviewed-batch040-affiliate-and-store
scope:
  - docs/article-localization/releases/batch040-pair-a
---

# Release reviewed Batch040 affiliate and store locales

## Why

Repository translations and localized media do not publish database locale rows.
Release only `affiliate-marketing-basics` and `independent-store-marketplace`
in zh-CN, en, ja and ko after the documented gates pass.

## Definition of done

- [ ] Resolve editorial acceptance and Batch040 live-source reconciliation.
- [ ] Pass the same-image isolated Docker rehearsal and fresh scoped preflight.
- [ ] Verify backup, control concurrent writes, deploy assets and verify health.
- [ ] Dry-run explicit slug/locale list; preserve existing edits and visibility.
- [ ] Import and publish only eligible missing locales; rerun is unchanged.
- [ ] Verify five-language desktop/mobile pages, images, canonical/hreflang and links.
- [ ] Commit sanitized per-article release receipts and completion states.

## How to verify

Use the guarded existing release service and localization runbook. Compare exact
document/image hashes with `docs/article-localization/batch040-pair-a-evidence.md`.

## Notes

Leave unclaimed while rehearsal infrastructure is unavailable. #930 repository
source correction must be reconciled with live; the old read-only receipt is not
a current release preflight. No deploy, import, publication or live acceptance
has occurred for these added languages.
