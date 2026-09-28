---
id: 2026-09-28-prepare-batch042-search-intent-and-content
title: Prepare Batch042 search intent and content quality localized artwork
status: review
priority: P2
area: api
owner: codex-batch042-root
claimed_at: 2026-09-28T18:01:54Z
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

Both published SEO guides lack four localized editions and text-bearing artwork. JSON installation waits for source correction #942; this scope is artwork and evidence only.

## Definition of done

- [x] Freeze corrected source and eight complete external 32-block translations.
- [x] Create 24 localized assets with original credit and source art intact.
- [x] Pass independent full-text/image review at exact candidate hashes.
- [x] Validate 16 SVGs and 20 five-language local desktop/mobile previews.
- [x] Record sanitized source/content/asset/review evidence.
- [ ] Finish PR review; install via the separate JSON task after #942 merges.

## How to verify

See docs/article-localization/batch042-pair-a-evidence.md for hash-bound independent review, assets and browser receipts. Candidate lint has zero errors; strict inherited summary/self-reference findings remain explicit. Run task and diff checks before push.

## Notes

PR #946 contains localized art/evidence, not article JSON. The coordinating agent has taken over the completed author's work. Installation belongs to 2026-09-28-batch042-pair-a-install-reviewed-locales. The dry run refused pre-correction main as intended. No production operation occurred and required nonproduction rehearsal infrastructure is unavailable.
