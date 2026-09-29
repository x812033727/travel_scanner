---
id: 2026-09-28-release-reviewed-batch040-product-seo-and
title: Release reviewed Batch040 product SEO and zero-click locales
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T17:43:01Z
completed_at:
branch:
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
- [ ] Pass same-image isolated Docker rehearsal and fresh scoped preflight.
- [ ] Verify backup, control concurrent writes, deploy necessary assets and check health.
- [ ] Dry-run explicit slug/locale list with exact reviewed hashes and version conflict protection.
- [ ] Import/publish eligible missing locales without changing visibility or overwriting later edits; prove rerun unchanged.
- [ ] Verify real five-language desktop/mobile routes, canonical, hreflang, images and links.
- [ ] Record sanitized per-article import, publication and browser acceptance results.

## How to verify

Use the existing guarded publishing service and localization runbook; compare exact content/image hashes with docs/article-localization/batch040-pair-b-evidence.md.

## Notes

Leave unclaimed while the required nonproduction rehearsal environment is unavailable. The historical read-only inventory predates source correction and is not current release evidence. No live write has occurred for these new languages.
