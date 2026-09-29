---
id: 2026-09-28-batch040-pair-a-artwork-evidence
title: Batch040 Pair A localized artwork and source evidence
status: done
priority: P2
area: docs
owner: codex-batch040-root
claimed_at: 2026-09-28T17:18:29Z
created_at: 2026-09-28T13:38:54Z
completed_at: 2026-09-28T17:27:07Z
branch: codex/article-localization-040-affiliate-a
depends_on: []
scope:
  - apps/web/public/guides/affiliate-marketing-basics
  - apps/web/public/guides/independent-store-marketplace
  - docs/article-localization/batch040-pair-a-evidence.md
  - tasks/open/2026-09-28-batch040-pair-a-artwork-evidence.md
---

# Batch040 Pair A localized artwork and source evidence

## Why

The two source articles contain text-bearing hero images and diagrams that need
matching zh-CN, en, ja and ko versions.

## Definition of done

- [x] Pin corrected source and unchanged original image hashes.
- [x] Create 24 localized SVG/JPG assets with original credit retained.
- [x] Render all 16 localized SVGs and independently inspect all eight diagrams.
- [x] Record exact review hashes and final five-locale local preview results.

## Steps

- [x] Translate graphic labels and generate eight 1600×900 hero JPGs.
- [x] Validate text bounds, margins and image hashes.
- [x] Reconcile #930/#948 and integrate evidence with the separate two-pack task.

## How to verify

See `docs/article-localization/batch040-pair-a-evidence.md`: six originals remain
unchanged; all 24 new image bytes match their tracked Git blobs and reviewed
receipts. Twenty final local desktop/mobile previews passed.

## Notes

Source PR #930 and its task closure #948 are merged. The historical live affiliate
source is still pre-correction in the available receipt. A fresh reconciliation
and isolated release rehearsal are required before import; no release occurred.
