---
id: 2026-09-27-localize-two-wordpress-migration-guides-batch030
title: Localize two WordPress migration guides batch030 pair A
status: done
priority: P1
area: docs
owner: codex-batch030-pair-a
claimed_at: 2026-09-27T10:34:33Z
created_at: 2026-09-27T10:34:19Z
completed_at: 2026-09-27T11:04:02Z
branch: codex/article-localization-030-pair-a
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-com-migration.json
  - apps/api/app/guides/content/wordpress-domain-migration.json
  - apps/web/public/guides/wordpress-com-migration
  - apps/web/public/guides/wordpress-domain-migration
---

# Localize two WordPress migration guides batch030 pair A

## Why

These two published WordPress migration articles exist only in zh-TW. Batch030 pair A
adds complete en, ja, ko and zh-CN documents and text-bearing artwork while retaining
the exact published zh-TW source and conditional same-language links.

## Definition of done

- [x] Both article packs have complete five-language documents, including source titles,
      image descriptions, image credits and internal-link labels.
- [x] Four-language hero SVG/JPG and diagram SVG assets render without missing text,
      overflow or mismatched facts; the three original assets per article stay intact.
- [x] Source versions, links, pack lint and image/browser QA are recorded in an
      external hash-bound receipt; the content commit is ready for review without PR
      creation or production writes.

## Steps

- [x] Verify the current published zh-TW document and original images against
      origin/main and the production read-only snapshot; claim only these two scopes.
- [x] Translate each document and all text-bearing image labels into four languages.
- [x] Render JPG variants from SVG, lint both packs, inspect all new images, and
      review source conditions plus same-language link behavior.
- [x] Commit the scoped content and close this task only after validation.

## How to verify

Run focused `guides-pack lint --slug` / `pack_cli lint --slug` (whichever this checkout
provides), the article-pack tests, SVG bounds/render checks, and `npm run check:tasks`.
Compare full normalized documents to the pinned source and inspect every image variant.

## Notes

- Base: origin/main `227aae75cc3d6ac0461117d529881f059b176433`. Its change after
  the inventory baseline touches only unrelated news-task records.
- Read-only production capture: `<home>\.codex\article-localization-release\batch030-inventory\migration-source-20260927T102207Z.json`
  SHA-256 `852cd843ce534a62851fde9e57b980992a2cc08d6043e60e03f8aff808f7834c`.
- `wordpress-com-migration`: article v2; zh-TW published locale v4, normalized SHA-256
  `7d868b9dec1857627e5aa0ff48ecfb1920a3f076b3140ba06845b20ef0f6805e`.
- `wordpress-domain-migration`: article v2; zh-TW published locale v4, normalized SHA-256
  `9ca0e1b53ab4286637b6bd784664ab8384e504758eda06222cb9a119c5c1b8bc`.
- Full live source equals repository source and current draft in both cases. The six
  original image bytes for these slugs match origin/main, host and public URLs.
- `dns-records-troubleshooting` and `https-certificate-setup` are published only in
  zh-TW. New-language references to them must remain non-clickable until published.

## Completion evidence

- Five-language packs: `wordpress-com-migration` (32 blocks each), `wordpress-domain-migration` (31 blocks each). Four new locales translate every block, table, callout, caption, alt, source title and article label. The zh-TW documents and six original images match origin/main byte-for-byte / structurally.
- Added 24 language-suffixed assets: for each of two articles and four locales, `hero.svg`, derived `hero.jpg` (1600×900), and `diagram-1.svg`. All 16 SVGs rendered at 1600×900 and inspected in contact sheets. Geometry audit found no clipping or missing glyphs and at least 22.4 px inside every diagram card.
- The 2026-09-27 10:22 UTC production read-only snapshot pins article v2 and zh-TW published locale v4 for both articles. The full source, links and original images were verified against the repository before drafting. Exact snapshot, comparison and asset hashes are in the external receipt.
- Validation: focused pack lint exit 0 (only baseline no-summary and full English-length advisories); API content-pack/import/link tests 67 passed, 5 skipped; front-end content-blocks test 65 passed; `check:i18n` passed 5 locales/25 namespaces; `check:tasks` exit 0 with unrelated stale-task warnings; `git diff --check` passed.
- The API exposes only currently published same-locale article references; the web renderer displays unresolved references as plain text. `wordpress-host-migration`, `dns-records-troubleshooting`, and `https-certificate-setup` were zh-TW-only at the pinned snapshot; no new-language public URL was inserted for them.
- External QA: `<home>\.codex\article-localization-release\batch030-pair-a\pair-a-validation.json` and `renders\image-qa.json`; these records bind all ten document hashes and all 30 image hashes (six unchanged, 24 new). No PR or production write was made.
