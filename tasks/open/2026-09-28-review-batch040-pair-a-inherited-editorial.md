---
id: 2026-09-28-review-batch040-pair-a-inherited-editorial
title: Review Batch040 Pair A inherited editorial intake failures
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T17:25:09Z
completed_at:
branch:
depends_on:
  - 2026-09-28-install-reviewed-batch040-affiliate-and-store
scope:
  - apps/api/app/guides/content/affiliate-marketing-basics.json
  - apps/api/app/guides/content/independent-store-marketplace.json
---

# Review Batch040 Pair A inherited editorial intake failures

## Why

Strict `intake_check.py --from-content` reports inherited source failures:
affiliate-marketing-basics starts with a paragraph instead of summary and has
three 本文/這篇 references (limit one); independent-store-marketplace starts with
a paragraph instead of summary. The localization preserves existing source text.

## Definition of done

- [ ] Review whether and how the existing published source should be corrected.
- [ ] Make any accepted correction as a distinct versioned change with review.
- [ ] Update all five editions consistently and rerun intake and source checks.
- [ ] Refresh release source/review bindings if documents change.

## How to verify

Run strict intake separately for both exact slugs and scoped pack lint; verify
source/locale hashes, complete paragraphs, attribution and unchanged facts.

## Notes

Unclaimed follow-up; do not overlap the localization claim. Internal article
targets and all SVG numeric checks passed. These failures are not hidden behind
the zero-error pack lint result. Do not silently modify the live source.
