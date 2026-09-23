---
id: 2026-09-23-localize-four-hosting-setup-guides-batch024
title: Localize four hosting setup guides batch024
status: in-progress
priority: P2
area: api
owner: codex-batch024
claimed_at: 2026-09-23T15:06:24Z
created_at: 2026-09-23T15:06:13Z
completed_at:
branch: codex/article-localization-batch024-hosting-setup
depends_on: []
scope:
  - apps/api/app/guides/content/bluehost-wordpress-setup.json
  - apps/web/public/guides/bluehost-wordpress-setup
  - apps/api/app/guides/content/hosting-com-wordpress-setup.json
  - apps/web/public/guides/hosting-com-wordpress-setup
  - apps/api/app/guides/content/hostinger-wordpress-setup.json
  - apps/web/public/guides/hostinger-wordpress-setup
  - apps/api/app/guides/content/managed-hosting-comparison.json
  - apps/web/public/guides/managed-hosting-comparison
---

# Localize four hosting setup guides batch024

## Why

Four published hosting guides currently provide Traditional Chinese only. Add complete English, Japanese, Korean and Simplified Chinese documents and localized text-bearing images while preserving the published source, metadata and existing assets.

## Definition of done

- [ ] All four articles have complete reviewed five-language packs; the existing Traditional Chinese models and 12 original assets remain unchanged.
- [ ] Sixteen new documents and 48 localized images pass independent editorial, numeric, provenance, layout and glyph review.
- [ ] Scoped repository checks and actual PR CI pass; deployment, import/publication and browser acceptance remain separately recorded.

## Steps

- [x] Compare fresh read-only published, draft and latest revisions with main; verify all 16 source files and check shared task/worktree/PR scope.
- [x] Create this isolated worktree and claim only the four pack paths and four asset directories.
- [ ] Author and independently review Bluehost and hosting.com full translations and images outside the repository.
- [ ] Author and independently review Hostinger and hosting-comparison full translations and images outside the repository.
- [ ] Assemble exactly four packs and 48 new assets from approved hashes, preserving source models and metadata.
- [ ] Run scoped checks, review the complete diff and open the batch PR.
- [ ] Complete authorized guarded deployment, target-only import/publication and five-language desktop/mobile browser acceptance.

## How to verify

Use the article-localization pipeline strict fields, GuideDocument validation, pack lint, artifact binding and desktop/mobile renders. Run relevant pipeline, assembly, render, article-pack, frontend and task checks, plus lint, type checks, i18n and build. Bind release phases to explicit slugs/locales and actual source versions; verify public bodies, images, canonical, hreflang, links and complete sitemap separately.

## Notes

Source main: `32f032b161534328f95366010fda1722397ae10c`. Fresh read-only capture: `2026-09-23T14:54:05Z`, source SHA-256 `98f78118e062f7dcc8778252df69cfb0d35213f6ae8ac2a5534b7e34d8fd8c19`. All four articles are active and published at article version 2; Traditional Chinese draft, published and latest models equal the repository at locale version 4. No other locale rows exist.

Outside evidence is under `C:/Users/x8120/.codex/article-localization-release/batch024-candidate-inventory`; ready manifest SHA-256 `edf0b58254ea1b1ba3dfe5eee3068cc2f13a8dd0d47212d6dbad9dce504f2623`, source review `dd4ab0c222d2aeec9b806e1d7e79dc9609c4ac7ea7ab6c631cae151a37c39ff7`.

Bluehost, hosting.com and Hostinger each have 27 blocks and image-description pointer `/blocks/22/description`; managed-hosting-comparison has 29 blocks and `/blocks/24/description`. Each has four sources checked on `2026-09-14`; preserve those dates, Taiwan-reader audience, currency conditions, product labels, source URLs, structured article identities and Mokaair copyright. Record the 16 target-only canonical empty-description backfills explicitly. The AI glossary links and shortened related-article labels are semantically valid. Related-language publication must be verified before release.

All four original 1600×900 JPEG covers contain text and have native SVG originals. Each target needs a localized hero SVG, 1600×900 hero JPEG and diagram SVG. Preserve original drawings and the 12 source files. No translation, publication or visual acceptance is implied by this claim.

Fresh setup scan found no competing active claim, translation, recent scoped commit or open PR. The strict historical `P:` worktree HOLD is preserved and resolved by read-only metadata/index inspection: four task-only/incomplete checkouts contain no selected files; no ownership override, index repair or old-worktree modification was performed. Resolution SHA-256 `91de3378dd8b0f1db032324d99e28b2971df404e19d3755262fd9df43bac664f`.
