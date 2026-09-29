---
id: 2026-09-28-review-batch041-keyword-and-title-summary
title: Review Batch041 keyword and title summary blocks
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T17:31:06Z
completed_at:
branch:
depends_on:
  - 2026-09-28-localize-seo-keyword-and-title-guides
scope:
  - apps/api/app/guides/content/seo-keyword-research.json
  - apps/api/app/guides/content/seo-title-writing.json
---

# Review Batch041 keyword and title summary blocks

## Why

Strict intake reports one inherited source failure in each of seo-keyword-research
and seo-title-writing: their first block is paragraph instead of summary.
Localization preserves the published source and has not silently rewritten it.

## Definition of done

- [ ] Review the source correction and make a separate versioned change if accepted.
- [ ] Keep all five editions consistent without deleting details or altering facts.
- [ ] Re-run strict intake, locale checks and exact review/source hash binding.

## How to verify

Run intake_check.py --from-content for each slug and scoped pack lint. Internal
article targets, self-reference counts and SVG numeric checks already passed.

## Notes

Leave unclaimed until localization scope is released. Any source change requires
the guarded reconciliation path before production import.
