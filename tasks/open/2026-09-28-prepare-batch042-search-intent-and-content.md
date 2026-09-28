---
id: 2026-09-28-prepare-batch042-search-intent-and-content
title: Prepare Batch042 search intent and content quality localized artwork
status: in-progress
priority: P2
area: api
owner: codex-batch042-pair-a
claimed_at: 2026-09-28T15:06:40Z
created_at: 2026-09-28T15:06:35Z
completed_at:
branch: codex/article-localization-042-seo-a
depends_on: []
scope:
  - apps/web/public/guides/seo-search-intent
  - apps/web/public/guides/seo-content-quality
  - docs/article-localization/batch042-pair-a-evidence.md
---

# Prepare Batch042 search intent and content quality localized artwork

## Why

Both published SEO guides have only zh-TW. Their covers and diagrams contain Traditional Chinese text. The four missing language documents must be based on the corrected source version, while source-link PR #942 currently owns the article JSON files.

## Definition of done

- [x] Corrected zh-TW source frozen with SHA-256 and eight complete repo-external 32-block locale candidates.
- [x] Four locale versions of both text-bearing covers and diagrams generated with source attribution.
- [x] Structural, image-dimension, asset-reference and Edge SVG overflow checks pass.
- [x] Independent language and desktop/mobile image review passes.
- [x] Assets and evidence are committed, pushed and reviewable without touching the article JSON.
- [x] Follow-up article pack installation is documented for after #942 merges and source scope releases.

## Steps

- [x] Check read-only production and repo inventories; verify source correction.
- [x] Draft and audit zh-CN, English, Japanese and Korean article candidates outside the repository.
- [x] Localize SVG text and raster covers; verify source image provenance.
- [x] Incorporate independent review findings and finalize evidence.
- [ ] Open scoped artwork PR and record pack-install handoff.

## How to verify

Run `python C:\Users\x8120\.codex\article-localization-release\batch042-pair-a\build_candidates.py`, `python C:\Users\x8120\.codex\article-localization-release\batch042-pair-a\audit.py`, and `node C:\Users\x8120\.codex\article-localization-release\batch042-pair-a\svg_browser_bbox.cjs`. In the branch, run `npm run check:tasks` and `git diff --check`. See `docs/article-localization/batch042-pair-a-evidence.md` for source and candidate hashes.

## Notes

- Source-link correction [PR #942](https://github.com/x812033727/travel_scanner/pull/942) removes two misleading AI glossary links from the zh-TW source. It has not been merged at initial staging. Do not edit or claim either JSON pack until that task releases its scope.
- Independent peer QA PASS: report `C:\Users\x8120\.codex\article-localization-release\batch042-pair-a\peer-qa\review.md` SHA-256 `2a859bac89181a8b2aa0fe60d923a30f8f07d689f952ab16d8224e99aad3f12d`; 16 local desktop/mobile preview receipt SHA-256 `1c19a91e0187fbb40257ad12c535c617a7baefd0bb9f8e9ebd5ba60a20ee247b`.
- Combined candidates live under `C:\Users\x8120\.codex\article-localization-release\batch042-pair-a`; neither pack is imported or published.
- Related-reading labels are plain text in new locales until their corresponding article routes are confirmed publicly available in those languages.
- Production release is held because no non-production Docker rehearsal environment is available.
