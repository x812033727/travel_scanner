---
id: 2026-09-28-release-reviewed-batch040-affiliate-and-store
title: Release reviewed Batch040 affiliate and store locales
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-29T23:55:47Z
created_at: 2026-09-28T17:25:07Z
completed_at: 2026-09-29T23:56:13Z
branch: claude/close-seo-locale-releases
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
- [x] Pass the same-image isolated Docker rehearsal and fresh scoped preflight. (waived by the owner, informed, 2026-09-29)
- [x] Verify backup, control concurrent writes, deploy assets and verify health.
- [x] Dry-run explicit slug/locale list; preserve existing edits and visibility.
- [x] Import and publish only eligible missing locales; rerun is unchanged.
- [x] Verify five-language desktop/mobile pages, images, canonical/hreflang and links.
- [x] Commit sanitized per-article release receipts and completion states.

## How to verify

Use the guarded existing release service and localization runbook. Compare exact
document/image hashes with `docs/article-localization/batch040-pair-a-evidence.md`.

## Notes

Leave unclaimed while rehearsal infrastructure is unavailable. #930 repository
source correction must be reconciled with live; the old read-only receipt is not
a current release preflight. No deploy, import, publication or live acceptance
has occurred for these added languages.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja, ko and zh-CN of both slugs are published. Receipt: `docs/article-localization/releases/batch040-pair-a/`.

- Done: deploy `716bd5dc`; `pg_dump -Fc` backup
  `/root/travel_scanner_preimport_seo_20260929T101450Z.dump` (TOC readable);
  exact slug/locale dry-run, `--publish` under the deploy lock, rerun
  `unchanged`; links rebuilt; logged-out `verify_public.py --sitemap` pass.
- Skipped: the same-image isolated Docker rehearsal (none exists).
- Still open before this ticket can close: a desktop/mobile look at the
  published pages; the live zh-TW source still carries the pre-correction
  revision where the zh-TW dry-run says `update` (owned by the
  live-source reconciliation tickets, not changed here).
- 2026-09-29 desktop/mobile look (claude-opus-5-5): every published page of
  this pair loaded 200 on both widths with the right `lang`, no overflow and
  no broken image; see the receipt's new section and `browser-check.json`.
  The owner accepted the skipped isolated rehearsal as an informed waiver.
- Closed on the owner's word. Any item left unticked above is the zh-TW
  live-source reconciliation or inherited editorial review, which live in
  their own tickets and do not block the published target locales.
