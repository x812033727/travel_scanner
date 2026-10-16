---
id: 2026-10-07-coordinate-guarded-local-installation-of-reviewed
title: Coordinate guarded local installation of reviewed wave4 article bundles
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T17:14:08Z
created_at: 2026-10-07T16:24:23Z
completed_at: 2026-10-07T17:33:47Z
branch: codex/article-locales-wave4-20261007
depends_on: []
scope:
  - .codex/localization-staging/wave4-life-reviewed
  - .codex/localization-staging/wave4-japan-reviewed
  - docs/article-localization/installations/.lock
  - docs/article-localization/installations/bundles/a175e63ec2a7ef5b
  - docs/article-localization/installations/bundles/fc048145476869d1
  - docs/article-localization/installations/japan-entry-2026-visit-japan-web.json
  - docs/article-localization/installations/css-layout-basics.json
  - docs/article-localization/installations/image-formats-compression.json
  - docs/article-localization/installations/responsive-layout-basics.json
  - docs/article-localization/installations/web-layout-hierarchy.json
  - docs/article-localization/installations/website-color-system.json
  - docs/article-localization/installations/website-information-architecture.json
  - docs/article-localization/installations/website-cache-cdn.json
  - docs/article-localization/installations/search-crawlers-explained.json
  - docs/article-localization/installations/structured-data-basics.json
  - docs/article-localization/installations/sitemap-website-submission.json
  - docs/article-localization/installations/web-design-project-workflow.json
  - docs/article-localization/installations/seo-content-cannibalization.json
---

# Coordinate guarded local installation of reviewed wave4 article bundles

## Why

The official installer requires pinned bundle, baseline and independently reviewed
jobs inside the repository, and writes a shared installation lock plus exact bundle
journals and per-article receipts. Keep private inputs ignored and claim these
coordination paths separately from the twelve life and Japan article scopes.

## Definition of done

- [x] Stage only final, hash-verified independently reviewed inputs in ignored paths.
- [x] Claim exact manifest-prefix journal directories and selected per-article
      receipts before the unchanged official installer can write them.
- [x] Install and replay with matching pack/media/journal/receipt hashes.
- [x] Preserve original external evidence; include only sanitized records in Git.

## Steps

- [x] Inspect the unchanged official installer and existing task scopes.
- [x] Claim private staging directories and the actual shared installation lock.
- [x] Assemble genuine reviewed inputs, then extend and check exact receipt scopes.
- [x] Stage with byte-for-byte verification; install and replay with durable journals.

## How to verify

Run the unchanged assembler, publisher verification and installer with exact manifest
pins; compare every selected pack and original media digest against the admitted
baseline. A replay must preserve all installed bytes and installation state. Run
task validation and the applicable content checks before the content PR.

## Notes

- The lock is `docs/article-localization/installations/.lock`; the earlier external
  plan's `.install.lock` spelling is superseded by the actual unchanged code.
- Bundle journals use the first sixteen characters of the actual manifest digest.
  Exact journal/receipt scopes will be added only after successful assembly.
- The tracked installations `.gitignore` already excludes private journals/receipts.
  Each claimed staging directory must exclude all its private contents before copying.
- This is local authoring coordination. It authorizes no deployment or publication.
- Actual official life assembly completed with all 48 authentic target reviews and
  six independently verified source-correction reviews; 12 articles and 156 assets.
  Manifest: `a175e63ec2a7ef5b845e5416bd3b6f4f0a41ca8e2b90f9428ddb5cd8d6e2594c`.
  The exact life journal directory and twelve receipts are now in this narrow scope.
- Actual official Japan assembly completed after all four genuine final reviews:
  one article, seven assets and one independently verified source correction.
  Manifest: `fc048145476869d1e7ec5fffba794908d0b58065fcb84b04477a3ea046791a3c`.
  Its exact journal directory and article receipt are now in this narrow scope.
- Both official installations and their identical replays exited0. Life final
  receipt `f9cd63964fc2da6faf6c4da836412ad75ea5bc1c3a5b24140d2bb0819df58ab1`
  verifies168 operations and the actual193-file replay capture; pack bytes are
  additionally verified by both official runs and final guards. Japan receipt
  `c83c899a2606f17aed486197dd7bc77d5a6d0d1b6d8001ce0bd6eeafcd97ca2a`
  verifies8 operations and all captured pack/asset/journal/receipt bytes unchanged.
- No baseline, job, private journal, installation receipt or staging input will be
  committed. The sanitized source-review documents record actual hashes and limits.
