---
id: 2026-10-07-recheck-business-models-and-five-forces
title: Recheck business models and five forces locales
status: done
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T06:23:44Z
created_at: 2026-10-07T06:23:37Z
completed_at: 2026-10-07T06:37:48Z
branch: codex/refund-source-correction-v2-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/business-models-b2b-d2c.json
  - apps/api/app/guides/content/porter-five-forces.json
  - apps/web/public/guides/business-models-b2b-d2c
  - apps/web/public/guides/porter-five-forces
  - docs/article-localization/business-five-forces-review-20261007.md
---

# Recheck business models and five forces locales

## Why

Two public life articles already have complete four-language repository drafts,
but the live snapshot exposes only Traditional Chinese. Recheck the actual text
and artwork before admitting these eight documents to a guarded release.

## Definition of done

- [x] Independently read all four target documents for each article and their original source/artwork.
- [x] Correct only exact reviewer findings, preserving public source, metadata, original images and credits.
- [x] Bind final document/image/source hashes to genuine review evidence and a content PR.
- [x] Hand deployment, database publication and public validation to a separate release ticket.

## Steps

- [x] Verify original baseline, current pack pins, fresh public source/asset responses and absence of competing claims/PR paths.
- [x] Complete independent whole-document, visual, glyph, route and related-title review.
- [x] Apply exact findings under this claim, recheck final bytes and prepare the next content candidate.

## How to verify

Run targeted pack lint and route/document/image guards. Independent review must
name its actual reviewer and original translator, bind all final hashes, and
record unresolved findings without granting PASS. A fresh database baseline is
required before publication; a public GET cannot prove absence of private drafts.

## Notes

Selected slugs: `business-models-b2b-d2c`, `porter-five-forces`.
Fresh next-cohort safety plan SHA
`50fd8c5c08558acb95ecc2fe10d66b4e36d2217e84db2c1472ff91980d71fe9a`.
The original authoring tickets are done. The current repository, published source
and protected source-asset hashes match the pinned baseline. No new provider call,
production write or publication approval is implied. This pair is outside PR #1365.

Final independent eight-target PASS review SHA
`46dc2bb0461d3f01b2796ee30100a921217ad78c64be63bc29e4a6f72da4c0a4`;
evidence SHA `82c0b13341ae430f72c11391053c52bb6aadf13e06f5b501c80f03678a90f9d6`.
All ten source/target documents, twenty SVGs and ten hero rasters were actually
read/viewed. Three EN/JA diagram-text findings were proposed independently,
applied by the root, then independently rendered and checked again; minimum
actual font remains 22px. Source packs, metadata, original diagrams and hero
masters/raster bytes are unchanged. The initial root verification misclassified
translated SVGs as unchanged source assets; its failure and subsequent exact-byte
inspection were preserved rather than replaying writes or inventing exit 0.

Five next-cohort packs passed scoped lint with exit 0 and no errors; inherited
summary/English-length warnings remain. The public evidence is in
`docs/article-localization/business-five-forces-review-20261007.md`.
Local review work closes in the content PR. Merge/deploy/CI and all production
publication/browser checks are handed to
`2026-10-07-release-business-analysis-missing-locales`; no target has been published.
