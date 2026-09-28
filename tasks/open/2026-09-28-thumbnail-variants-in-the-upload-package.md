---
id: 2026-09-28-thumbnail-variants-in-the-upload-package
title: Thumbnail variants in the upload package and the review page
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-28T12:28:35Z
completed_at:
branch:
depends_on:
  - 2026-09-28-so-that-s-why-thumbnail-template
scope:
  - tools/video/package
  - tools/video/review/sync.mjs
---

# Thumbnail variants in the upload package and the review page

## Why

`render` now draws YouTube "Test & compare" variants: `thumbnail.variants` in `video.json` gives
B and C, written as `thumbnail-b.jpg` and `thumbnail-c.jpg` beside `thumbnail.jpg` (A) and listed
in `frames/manifest.json` as `thumbnail_variants` (docs/videos/so-thats-why/thumbnails.md, A/B).
The upload package and the owner's review page still carry A only, so the owner has to find B and
C in the work directory to upload them to the test in Studio. `tools/video/package` was in
another active task's scope (`2026-09-26-video-dubs-worker`) when G4 landed, so this part was split
out.

## Definition of done

- [ ] `package` copies the variants listed in `frames/manifest.json` into the upload directory,
      records them in the package manifest, and `UPLOAD.md` says to upload all three to
      "Test & compare" (thumbnail test, up to three images) and not to change the title during
      the test.
- [ ] `package/check.mjs` fails when a listed variant is missing or over 2 MB, as it does for A.
- [ ] The final gate's review push (`review/sync.mjs`) sends B and C with A so the owner sees all
      three on /admin/videos (check whether the site's review files accept more than one
      `thumbnail` kind first; if not, file the API/web part as its own task).
- [ ] A video without variants packages byte for byte as before.

## Steps

- [ ] Read `render/cli.mjs` (`thumbnail_variants`) and `render/plan.mjs` (`thumbnailVariantFile`).
- [ ] Package, check, UPLOAD.md text, tests.
- [ ] Review push.

## How to verify

`npm run test:tools`; package the explainer fixture's work directory with variants drawn.

## Notes

- 2026-09-28 filed by claude-opus when G4 of `2026-09-28-so-that-s-why-thumbnail-template` landed
  (render side only).
