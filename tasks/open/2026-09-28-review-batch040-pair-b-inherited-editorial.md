---
id: 2026-09-28-review-batch040-pair-b-inherited-editorial
title: Review Batch040 Pair B inherited editorial intake failures
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T17:43:02Z
completed_at:
branch:
depends_on:
  - 2026-09-28-install-batch040-product-seo-and-zero
scope:
  - apps/api/app/guides/content/ecommerce-product-seo.json
  - apps/api/app/guides/content/zero-click-search-strategy.json
---

# Review Batch040 Pair B inherited editorial intake failures

## Why

Strict intake reports four inherited source failures: both packs begin with a paragraph rather than summary, ecommerce-product-seo has three source self-references and zero-click-search-strategy has two (limit one). Localization preserved the published source structure and wording.

## Definition of done

- [ ] Review whether and how the existing source should be corrected.
- [ ] Make an accepted correction as a separate versioned and reviewed change.
- [ ] Keep all five editions consistent and rerun strict intake, scoped pack lint and source checks.
- [ ] Refresh release document hashes and source/review bindings after any change.

## How to verify

Run strict intake separately for the two exact slugs, preserve complete paragraphs/facts/attribution, and compare five-language document and image hashes.

## Notes

Unclaimed follow-up. Internal article targets and SVG numeric checks already passed. Zero-error pack lint does not conceal strict editorial failures. Do not silently change the live source.
