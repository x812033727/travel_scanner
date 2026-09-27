---
id: 2026-09-27-localize-wordpress-performance-plugins-and-safe
title: Localize WordPress performance plugins and safe reset Batch032 Pair B
status: done
priority: P2
area: api
owner: codex-batch032-pair-b
claimed_at: 2026-09-27T14:20:18Z
created_at: 2026-09-27T14:19:56Z
completed_at: 2026-09-27T14:33:47Z
branch: codex/article-localization-032-pair-b
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-performance-plugins.json
  - apps/api/app/guides/content/wordpress-reset-safely.json
  - apps/web/public/guides/wordpress-performance-plugins
  - apps/web/public/guides/wordpress-reset-safely
---

# Localize WordPress performance plugins and safe reset Batch032 Pair B

## Why

Both currently published zh-TW v4 articles lack en, ja, ko and zh-CN. The
source-link correction commit `a4d3cc5070f43cf6d6133dbd3f464727dfbc22da`
replaces unrelated AI glossary links with ordinary text in these two zh-TW
documents. Those corrected revisions are provisional until published.

## Definition of done

- [x] Eight complete locale documents preserve source structure, audience,
      product qualifications, numbers, source URLs/dates and conditional links.
- [x] Twenty-four localized assets render without clipping or missing glyphs;
      the six originals and two zh-TW source documents remain unchanged.
- [x] Pack lint, targeted API tests, source/asset hashes, link policy and
      visual QA pass; commit locally without push, PR or production write.

## Steps

- [x] Translate both complete guides into en, ja, ko and zh-CN.
- [x] Localize hero SVG/JPG and diagram SVG for each language.
- [x] Record source-correction publication prerequisite and exact hashes.

## How to verify

Run scoped pack lint and guide pack/link/ingest API tests from `apps/api`,
plus `npm run check:tasks`, image renders, and hash/structure/source checks.

## Notes

Inventory SHA-256 `fa3262b33c0948c125f4a46b93caeade730723d1428ffed0ee8d5d6ccd3a4d73`;
source correction receipt SHA-256
`848c102856ec4094270d0e074e2ed465820543d81ac8e7cd10905455ed975553`.
Published source models at the inventory: performance v4
`b51710d0eaf7b53708f29399103471c22573264b6d68a5e997883b4188922f39`,
reset v4 `0e35950667a9c14985c34c0c9e30db67c93c100a8b48bb741f4ed5daa87ebfa6`.
Provisional corrected models: performance
`cf547f499451f30ddebd951f5edd3442a5cb2606d52aba29d417744611b6c65a`,
reset `631ed336116212e02260fd628999f0ffd421ec34c155c3614c7c777af3d25514`.
Publish these zh-TW source fixes and rebind by new published versions/hashes
before the locale additions can be published. Performance links to
`website-cache-cdn` and `pagespeed-performance-review` (inventory zh-TW only)
and `wordpress-website-backup` (five-language); reset links to
`wordpress-website-backup` and `wordpress-local-development` (five-language)
and `wordpress-theme-selection` (inventory zh-TW only). Unpublished
same-language targets must render as plain text.

Local validation receipt:
`C:\Users\x8120\.codex\article-localization-release\batch032-pair-b\validation.json`,
SHA-256 `23272cc4d94c5cb1163f58d6d61c58946227c3baa506ce451769126e170b28b1`.
It verifies eight 33-block documents, 24 new assets, six original image hashes,
the unchanged corrected zh-TW source models and root metadata, translated
source titles with unchanged URLs/check dates, code literals, and link targets.
All six four-locale contact sheets were visually reviewed at full resolution;
no clipping, overlaps, or missing glyphs were observed. Pack lint returned
zero errors; no-summary and two English length warnings are advisory. The
Targeted pack/link/ingest API tests: 67 passed, 5 skipped in 114.46 seconds.
Task check: 929 files validated, with pre-existing stale-claim warnings.
The tests and lint ran from this worktree with `PYTHONPATH=.` using the already
initialized Batch031 API venv because creating a new venv in Pair A had failed
on a Windows PE resource access-denied error. `git diff --check` passed.
