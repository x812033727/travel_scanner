---
id: 2026-10-12-derive-video-upload-guide-category-and
title: Derive video upload guide category and disclosure text from actual package
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-12T04:05:55Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package
---

# Derive video upload guide category and disclosure text from actual package

## Why

H03's native package sets category_id=27 (Education), but UPLOAD.md says 科學與技術（27） because uploadSteps hard-codes the category name. Its generic illustrated-video disclosure reason also claims a licensed music bed when the episode has no music. The generated guide turns default audience and synthetic-content values into instructions, even though the publishing skill leaves those Studio fields to the owner.

## Definition of done

- [ ] The generated category name matches category_id, including 27 Education and 28 Science & Technology.
- [ ] Handoff text describes only assets present in the package and distinguishes automated defaults from owner-controlled Studio decisions.
- [ ] Existing package consumers and source-bound approvals remain valid; episode-specific media or source files are not rewritten.

## Steps

- [ ] Trace category and disclosure wording to the generating functions; narrow the implementation scope if needed.
- [ ] Correct template wording and add targeted tests for category 27 and an illustrated episode without music.

## How to verify

Run the relevant tools/video/package tests and generate a temporary fixture package for both categories. Inspect UPLOAD.md alongside metadata.json, including the owner-controlled disclosure, audience and publication fields.

## Notes

Observed at tools/video/package/metadata.mjs:207 during H03 delivery on 2026-10-12. H03's generated external UPLOAD.md and disclosure_reason were narrowly corrected with before/after SHA receipts; category_id, contains_synthetic_media, source and all media stayed unchanged. This task covers the shared generator, which was not edited in the H03 production branch. Reproduce from a fixture rather than regenerating the owner-approved H03 package.
