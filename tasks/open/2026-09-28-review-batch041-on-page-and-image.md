---
id: 2026-09-28-review-batch041-on-page-and-image
title: Review Batch041 on-page and image source summary blocks
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T17:34:18Z
completed_at:
branch:
depends_on:
  - 2026-09-28-install-reviewed-batch041-image-seo-language
  - 2026-09-28-localize-on-page-seo-workflow-article
scope:
  - apps/api/app/guides/content/on-page-seo-workflow.json
  - apps/api/app/guides/content/image-seo-workflow.json
---

# Review Batch041 on-page and image source summary blocks

## Why

Strict intake reports one inherited source failure in each of on-page-seo-workflow
and image-seo-workflow: first block is paragraph instead of summary. Localization
preserves existing source text and does not silently rewrite published content.

## Definition of done

- [ ] Review any source correction as a distinct versioned change.
- [ ] Keep all five editions consistent without dropping details or changing facts.
- [ ] Re-run strict intake, locale checks and exact source/review hash binding.

## How to verify

Run intake_check.py --from-content separately for both slugs, then scoped pack lint.
Internal targets, self-reference counts and SVG numeric checks already pass.

## Notes

Leave unclaimed until localization scope is released. Source changes require
fresh review and guarded live reconciliation before production import.
