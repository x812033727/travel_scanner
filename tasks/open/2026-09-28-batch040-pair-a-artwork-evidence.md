---
id: 2026-09-28-batch040-pair-a-artwork-evidence
title: Batch040 Pair A localized artwork and source evidence
status: in-progress
priority: P2
area: docs
owner: codex-batch040-pair-a
claimed_at: 2026-09-28T13:39:24Z
created_at: 2026-09-28T13:38:54Z
completed_at:
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

The published zh-TW affiliate and store-channel guides have Chinese text in their hero
covers and diagrams. The four target locales need matching artwork and source evidence.
PR #930 currently owns the affiliate source JSON in a separate review task, so this
task intentionally excludes both content packs until that scope is released.

## Definition of done

- [x] Pin the #930 corrected repository source and original art hashes, plus the
  independent four-lock, read-only production snapshot and its pre-correction limit.
- [x] Create localized hero SVG/JPG and diagram SVG for zh-CN, en, ja, and ko for both
  guides, preserving original art provenance and browser-verified layout.
- [x] Record exact art hashes, editorial caveats, image previews, and publication
  boundary in the scoped evidence document.

## Steps

- [x] Inventory corrected source art, labels, citations, and links.
- [x] Translate graphic text and generate eight matching covers.
- [x] Browser-render all 16 SVGs, inspect previews, and audit new asset hashes.

## How to verify

Render each localized SVG at 1600x900 in Edge/Chromium; check text bounds, card
margins, overlap, and JPG output. Compare exact hashes of original art and source
packs to the pinned #930 head. Run the scoped pack linter only after the separate
content task owns the packs. Run `npm run check:tasks` before pushing.

## Notes

Checkout: `C:\Users\x8120\.codex\worktrees\batch040-affiliate-a\travel_scanㄐ`, branch
`codex/article-localization-040-affiliate-a`, starting at #930 correction head
`128c3f3cd877da4aec1e1c5ad3a4cb8310449793`. #930's task is in `review` and
holds `apps/api/app/guides/content/affiliate-marketing-basics.json`; do not force
claim or edit either Pair A content pack yet. The shared production read-only receipt
is outside the repository at `C:\Users\x8120\.codex\article-localization-release\batch040-commerce-search-readonly-inventory-20260928\receipt-20260928T133638Z.json`,
SHA-256 `676b67043693c188020e6adf9d5b16bd1e25a4b0a44f8660ed6034fb970dcd0d`.
It confirms published zh-TW v4 matched the pre-correction main; the corrected #930
pack intentionally differs. No production write, import, or publication is authorized.
All 16 SVG browser-layout cases and the exact 24-new-asset audit passed; both
four-language contact sheets also passed independent visual inspection. Details and
receipt hashes are in the scoped evidence document. Article text remains outside the
repository while #930's overlapping JSON task is active.
