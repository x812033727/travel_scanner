---
id: 2026-09-28-prepare-batch041-on-page-and-image
title: Prepare Batch041 on-page and image SEO artwork
status: in-progress
priority: P2
area: docs
owner: codex-batch041-pair-b-art
claimed_at: 2026-09-28T14:24:04Z
created_at: 2026-09-28T14:23:38Z
completed_at:
branch: codex/article-localization-041-seo-b
depends_on: []
scope:
  - apps/web/public/guides/on-page-seo-workflow
  - apps/web/public/guides/image-seo-workflow
  - docs/article-localization/batch041-pair-b-evidence.md
---

# Prepare Batch041 on-page and image SEO artwork

## Why

The published zh-TW on-page and image SEO guides have text-bearing SVG covers
and diagrams. Their four missing language documents need localized artwork.
This task prepares the assets; article JSON is separately claimed.

## Definition of done

- [x] Both source SVG sets remain byte-identical while four locales receive
      localized hero SVG/JPEG and diagram SVG files.
- [x] All 16 SVGs render without text overflow, overlap, missing glyphs or
      card-boundary violations at 1600 by 900.
- [ ] Pair B article content and visual-page review complete in a later task
      after #934 corrects the image SEO source link.

## Steps

- [x] Pinned source SVG hashes and preserved Mokaair credit.
- [x] Translated title, description and every visible SVG text node.
- [x] Rendered 16 SVGs in Edge 154, exported eight JPEG covers and reviewed
      the four-locale contact sheets.
- [x] Committed artwork and evidence; the paired documents are peer-reviewed
      and a focused content PR is being prepared.

## How to verify

Run the source-hash-guarded generator at
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b-assets.py`
from this worktree, then the renderer at
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b\render-assets.cjs`.
Inspect its receipt and contact sheets, run `npm run check:tasks` and
`git diff --check`.

## Notes

The read-only production baseline is
`C:\Users\x8120\.codex\article-localization-release\batch041-seo-readonly-inventory-20260928\receipt-20260928T134834Z.json`.
Both articles are active/published, with zh-TW v4 matching the pre-correction
repository source and four target locales absent. #934 proposes a one-inline
zh-TW source-link correction for image SEO; this artwork task does not edit it.
Independent local article-page review passed 16 desktop/mobile renders with
gallery SHA-256 `336e763cdaa481cabea6ee7096539aeed9724bb3d1d39659bc94af3314d24eae`.
No deployment, import, publication or public browser verification occurred.
