---
id: 2026-10-11-render-upload-checklist-category-labels-from
title: Render upload checklist category labels from metadata
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T22:41:27Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package/metadata.mjs
  - tools/video/package/metadata.test.mjs
---

# Render upload checklist category labels from metadata

## Why

The long-video upload checklist always labels `metadata.category_id` as 科學與技術. H02's approved metadata uses category 27 (Education), so its generated `UPLOAD.md` says 科學與技術（27） and can lead the owner to choose category 28 in Studio. The metadata itself is correct; the human instructions are inconsistent.

## Definition of done

- [ ] Checklist category names match their actual IDs, including 27 Education, 28 Science & Technology and 24 Entertainment.
- [ ] Unknown IDs are displayed without an invented category name.

## Steps

- [ ] Replace the fixed category label in `uploadChecklist` with a source-bound label or a neutral numeric instruction.
- [ ] Cover multiple category IDs and the unknown-ID fallback in the existing metadata tests.

## How to verify

Run `node --test tools/video/package/metadata.test.mjs`; generate or inspect checklists with category IDs 27, 28 and 24 and verify the label and numeric metadata agree.

## Notes

- Found while packaging `curio-h02` on 2026-10-12 Asia/Taipei. `tools/video/core/schema.mjs` identifies 28 Science & Technology and 27 Education; `tools/video/package/metadata.mjs` currently hardcodes the former label.
- This ticket changes the shared template only. Do not regenerate, repurchase or alter H02's approved media/metadata. Any local reading-instruction correction must preserve the original generated file and record before/after hashes.
