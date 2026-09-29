---
id: 2026-09-28-release-reviewed-batch041-keyword-and-title
title: Release reviewed Batch041 keyword and title locales
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T17:30:47Z
completed_at:
branch:
depends_on:
  - 2026-09-28-localize-seo-keyword-and-title-guides
scope:
  - docs/article-localization/releases/batch041-pair-a
---

# Release reviewed Batch041 keyword and title locales

## Why

Repository localization and artwork do not create published database editions.
Only seo-keyword-research and seo-title-writing in zh-CN/en/ja/ko are in scope.

## Definition of done

- [ ] Resolve source editorial acceptance and merge the reviewed content PR.
- [ ] Pass same-image nonproduction Docker rehearsal and fresh version/hash preflight.
- [ ] Verify backup and health; deploy the reviewed code/assets with controlled writes.
- [ ] Dry-run only the exact slug/locale list and stop any conflicting record.
- [ ] Publish only eligible missing languages, preserving edits and visibility.
- [ ] Re-run import unchanged and verify five-locale desktop/mobile public pages.
- [ ] Save per-article image, body, canonical/hreflang, link and draft-protection results.

## How to verify

Follow the existing guarded localization release workflow and exact hashes in
docs/article-localization/batch041-pair-a-evidence.md.

## Notes

Unclaimed: the required rehearsal environment is unavailable. The historical
read-only receipt and local standalone previews are not current live acceptance.
The two plain-text related-reading labels in each new locale must be reconciled
with actual published target locales before enabling public links.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja, ko and zh-CN of both slugs are published. Receipt: `docs/article-localization/releases/batch041-pair-a/`.

- Done: deploy `716bd5dc`; `pg_dump -Fc` backup
  `/root/travel_scanner_preimport_seo_20260929T101450Z.dump` (TOC readable);
  exact slug/locale dry-run, `--publish` under the deploy lock, rerun
  `unchanged`; links rebuilt; logged-out `verify_public.py --sitemap` pass.
- Skipped: the same-image isolated Docker rehearsal (none exists).
- Still open before this ticket can close: a desktop/mobile look at the
  published pages; the live zh-TW source still carries the pre-correction
  revision where the zh-TW dry-run says `update` (owned by the
  live-source reconciliation tickets, not changed here).
