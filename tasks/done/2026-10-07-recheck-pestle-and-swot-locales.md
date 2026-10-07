---
id: 2026-10-07-recheck-pestle-and-swot-locales
title: Recheck PESTLE and SWOT locales
status: done
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T06:23:49Z
created_at: 2026-10-07T06:23:46Z
completed_at: 2026-10-07T06:37:48Z
branch: codex/refund-source-correction-v2-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/pestle-business-scan.json
  - apps/api/app/guides/content/swot-tows-action-plan.json
  - apps/web/public/guides/pestle-business-scan
  - apps/web/public/guides/swot-tows-action-plan
  - docs/article-localization/pestle-swot-review-20261007.md
---

# Recheck PESTLE and SWOT locales

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

Selected slugs: `pestle-business-scan`, `swot-tows-action-plan`.
Fresh next-cohort safety plan SHA
`50fd8c5c08558acb95ecc2fe10d66b4e36d2217e84db2c1472ff91980d71fe9a`.
The original authoring tickets are done. The current repository, published source
and protected source-asset hashes match the pinned baseline. No new provider call,
production write or publication approval is implied. This pair is outside PR #1365.

Final independent eight-target PASS review SHA
`c6402686d5f3fc348d05ef10235bffec78b5207f2ceee7f7ab7a83b55076448b`;
complete evidence SHA
`6237ecc37c25c43da3611793d2f04f777b930dc6d317b88cdb37944c096eb151`.
Both full source documents and all eight targets, twenty SVG/hero variants and
twenty offline desktop/mobile body renders were reviewed. Minimum actual SVG
font is 18px. No content or asset correction was needed; original source, all
root metadata, credits, dates, numerical values and image hashes are preserved.
Official Route B review-schema validation accepted all eight genuine rows with
the actual original translator and distinct current reviewer.

Five next-cohort packs passed scoped lint with exit 0 and no errors; inherited
summary/English-length warnings remain. The public evidence is in
`docs/article-localization/pestle-swot-review-20261007.md`.
Local review work closes in the content PR. Merge/deploy/CI and all production
publication/browser checks are handed to
`2026-10-07-release-business-analysis-missing-locales`; no target has been published.
