---
id: 2026-09-22-localize-taoyuan-airport-departure-guide-in
title: Localize Taoyuan airport departure guide in four missing languages
status: review
priority: P2
area: docs
owner: codex-gpt6-batch014
claimed_at: 2026-09-22T03:43:42Z
created_at: 2026-09-22T03:43:35Z
completed_at:
branch: codex/article-localization-batch-014-taoyuan
depends_on: []
scope:
  - apps/api/app/guides/content/taoyuan-airport-departure-guide.json
  - apps/web/public/guides/taoyuan-airport-departure-guide
---

# Localize Taoyuan airport departure guide in four missing languages

## Why

The published Taoyuan Airport departure guide only has a Traditional Chinese locale. Add
complete English, Japanese, Korean, and Simplified Chinese documents and matching localized
diagrams while preserving the published zh-TW source, Taiwan-departure audience, legal
eligibility conditions, citations, media credits, and article metadata.

## Definition of done

- [x] The pack contains five complete locale documents with the same 42-block and 11-source
  structure as the live zh-TW source.
- [x] Four localized SVGs carry the approved locale text, all factual numbers, and the full
  e-Gate eligibility scope: ROC nationality, Taiwan household registration, and ROC passport.
- [x] Independent editorial and desktop/mobile visual reviews pass on hash-bound artifacts.
- [x] A draft PR exposes the exact committed pack and SVG bytes for final integration review.

## Steps

- [x] Capture a read-only production source/version/topics snapshot.
- [x] Draft and independently review all four missing locale documents.
- [x] Integrate the documents and diagrams without changing zh-TW or pack metadata.
- [x] Render each diagram at desktop and at the production 1180px mobile scroll geometry.
- [x] Commit the reviewed bytes and open a draft PR.

## How to verify

- Run scoped `lint_all` for `taoyuan-airport-departure-guide`; it must report no errors.
- Run `npm run check:tasks`.
- Inspect `git diff --check`, the final pack diff, all four desktop renders, and all twelve
  production-width mobile scroll captures.
- Bind the exact Git blob IDs and SHA-256 values in the release freeze after commit.

## Notes

- Production source snapshot: `batch014/live-source.json`, captured 2026-09-22T03:44:45Z;
  published and draft normalized source SHA-256 is
  `f5fbd6565dbb94cc199fd08ae3127d30ebb04b82896a208b17654b9da295d049`.
- Fresh live topics are `packing` and `transport`; the pack intentionally preserves its existing
  topic order `[transport, packing]`.
- The final locale documents passed independent full-field editorial review. Japanese was
  independently authored by the parent agent; the other three were independently reviewed.
- The localized SVGs keep every label at the repository's 15px minimum. Browser geometry found
  no outside text, overlaps, or card overflow in any locale.
- The production `ContentBlocks` mobile layout uses a 1180px diagram in a horizontally scrollable
  390px viewport with 20px wrapper padding; left, center, and right captures cover the full image.
