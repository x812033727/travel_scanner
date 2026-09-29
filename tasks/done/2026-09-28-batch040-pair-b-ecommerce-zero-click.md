---
id: 2026-09-28-batch040-pair-b-ecommerce-zero-click
title: Localize ecommerce product SEO and zero-click guides in five languages (Batch040 B)
status: done
priority: P1
area: docs
owner: codex-batch040-root
claimed_at: 2026-09-28T17:38:12Z
created_at: 2026-09-28T13:37:49Z
completed_at: 2026-09-28T17:44:07Z
branch: codex/article-localization-040-seo-b
depends_on: []
scope:
  - apps/web/public/guides/ecommerce-product-seo
  - apps/web/public/guides/zero-click-search-strategy
  - docs/article-localization/batch040-pair-b-evidence.md
  - tasks/open/2026-09-28-batch040-pair-b-ecommerce-zero-click.md
---

# Localize ecommerce product SEO and zero-click guides in five languages (Batch040 B)

## Why

The two published source articles lacked four complete language editions and localized artwork. This repository source task preserves the current corrected source and adds reviewable five-language content; live release is tracked separately.

## Definition of done

- [x] Install eight complete 33-block translations with frozen-source and staged-byte checks.
- [x] Preserve zh-TW, article metadata, source URLs/dates, image credits and remaining publication-aware targets.
- [x] Produce 24 localized assets and inspect all final SVGs and five-language cover previews.
- [x] Independently read all source/target text and validate 20 desktop/mobile local previews.
- [x] Pass scoped pack lint and focused API tests; disclose inherited strict-intake failures.
- [x] Record reproducible evidence and separate editorial/release tasks.

## How to verify

See `docs/article-localization/batch040-pair-b-evidence.md` for exact reviewed pack/asset/report hashes. Scoped pack lint: zero errors. Focused content-pack/link tests: 15 passed, 11 database-dependent skipped. Local article previews: 20/20; SVG geometry: 16/16. Repository CI and task validation accompany the PR.

## Notes

#930 and #948 have merged and released the JSON scopes. Existing source summary/self-reference failures remain visible in `2026-09-28-review-batch040-pair-b-inherited-editorial`; these were not silently corrected in a translation change. Release lives in `2026-09-28-release-reviewed-batch040-product-seo-and`. Standalone previews are not Next.js or live acceptance; production remains NO-GO without the required isolated rehearsal and fresh preflight.
