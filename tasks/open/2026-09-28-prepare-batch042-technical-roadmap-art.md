---
id: 2026-09-28-prepare-batch042-technical-roadmap-art
title: Prepare Batch042 technical SEO and learning roadmap localized art
status: review
priority: P2
area: web
owner: codex-batch042-root
claimed_at: 2026-09-28T17:57:29Z
created_at: 2026-09-28T15:06:00Z
completed_at:
branch: codex/article-localization-042-seo-b
depends_on: []
scope:
  - apps/web/public/guides/technical-seo-checklist
  - apps/web/public/guides/seo-learning-roadmap
  - docs/article-localization/batch042-pair-b-evidence.md
---

# Prepare Batch042 technical SEO and learning roadmap localized art

## Why

The published Traditional Chinese guides lack four localized editions and text-bearing artwork. This art/evidence task preserves both source JSON packs until #942 merges and releases them.

## Definition of done

- [x] Produce 24 localized hero/diagram assets with unchanged original art and attribution.
- [x] Freeze eight complete external 32-block translations against corrected source hashes.
- [x] Independently review both originals and every target text/table/image/source field.
- [x] Validate 16 SVGs and 20 five-language desktop/mobile standalone previews.
- [x] Record exact candidate, asset, review and browser hashes in sanitized evidence.
- [ ] Complete PR review; install packs via the separate narrowly scoped task after #942 merges.

## How to verify

Read docs/article-localization/batch042-pair-b-evidence.md. Candidate lint has zero errors. All 24 assets match their historical render bindings; all 16 SVG geometry checks and 20 standalone local article cases pass. Strict source intake still reports the documented summary/self-reference findings. Run task and diff checks before push.

## Notes

The coordinating agent took over after the original author's work completed. No other agent is editing these scopes. Installation belongs to 2026-09-28-batch042-pair-b-install-reviewed-locales. Source and final candidate hashes are bound in the evidence. The safe dry run currently refuses the pre-#942 main source as intended. No production operation occurred; isolated rehearsal infrastructure remains unavailable.
