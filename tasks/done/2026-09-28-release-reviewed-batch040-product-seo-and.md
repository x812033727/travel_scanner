---
id: 2026-09-28-release-reviewed-batch040-product-seo-and
title: Release reviewed Batch040 product SEO and zero-click locales
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-29T23:55:50Z
created_at: 2026-09-28T17:43:01Z
completed_at: 2026-09-29T23:56:16Z
branch: claude/close-seo-locale-releases
depends_on:
  - 2026-09-28-install-batch040-product-seo-and-zero
scope:
  - docs/article-localization/releases/batch040-pair-b
---

# Release reviewed Batch040 product SEO and zero-click locales

## Why

Repository content does not create database locales. Release only ecommerce-product-seo and zero-click-search-strategy in zh-CN, en, ja and ko after the documented gates pass.

## Definition of done

- [ ] Resolve inherited editorial issues and Batch040 live-source reconciliation.
- [x] Pass same-image isolated Docker rehearsal and fresh scoped preflight. (waived by the owner, informed, 2026-09-29)
- [x] Verify backup, control concurrent writes, deploy necessary assets and check health.
- [x] Dry-run explicit slug/locale list with exact reviewed hashes and version conflict protection.
- [x] Import/publish eligible missing locales without changing visibility or overwriting later edits; prove rerun unchanged.
- [x] Verify real five-language desktop/mobile routes, canonical, hreflang, images and links.
- [x] Record sanitized per-article import, publication and browser acceptance results.

## How to verify

Use the existing guarded publishing service and localization runbook; compare exact content/image hashes with docs/article-localization/batch040-pair-b-evidence.md.

## Notes

Leave unclaimed while the required nonproduction rehearsal environment is unavailable. The historical read-only inventory predates source correction and is not current release evidence. No live write has occurred for these new languages.

## Released 2026-09-29 (claude-opus-5-5)

This supersedes any earlier note above saying no import or publication occurred.

The owner chose, in chat, to publish the missing locales without the isolated
rehearsal: back up first, create only the new locales, leave zh-TW untouched.
en, ja, ko and zh-CN of both slugs are published. Receipt: `docs/article-localization/releases/batch040-pair-b/`.

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
