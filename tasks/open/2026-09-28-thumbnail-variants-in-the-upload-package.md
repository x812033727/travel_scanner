---
id: 2026-09-28-thumbnail-variants-in-the-upload-package
title: Thumbnail variants in the upload package and the review page
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-thumb-variants
claimed_at: 2026-10-02T06:11:56Z
created_at: 2026-09-28T12:28:35Z
completed_at:
branch: claude/thumbnail-variants-package
depends_on:
  - 2026-09-28-so-that-s-why-thumbnail-template
scope:
  - tools/video/package
  - tools/video/review/sync.mjs
  - docs/videos/so-thats-why/thumbnails.md
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

- [x] `package` copies the variants listed in `frames/manifest.json` into the upload directory,
      records them in the package manifest, and `UPLOAD.md` says to upload all three to
      "Test & compare" (thumbnail test, up to three images) and not to change the title during
      the test.
- [x] `package/check.mjs` fails when a listed variant is missing or over 2 MB, as it does for A.
- [x] The final gate's review push (`review/sync.mjs`) sends B and C with A so the owner sees all
      three on /admin/videos (check whether the site's review files accept more than one
      `thumbnail` kind first; if not, file the API/web part as its own task).
- [x] A video without variants packages byte for byte as before.

## Steps

- [x] Read `render/cli.mjs` (`thumbnail_variants`) and `render/plan.mjs` (`thumbnailVariantFile`).
- [x] Package, check, UPLOAD.md text, tests.
- [x] Review push.

## How to verify

`npm run test:tools`; package the explainer fixture's work directory with variants drawn.

## Notes

- 2026-09-28 filed by claude-opus when G4 of `2026-09-28-so-that-s-why-thumbnail-template` landed
  (render side only).
- 2026-10-02 claude-opus-5-5-thumb-variants: claimed with `--force` because the only blocking
  claim was `2026-09-28-drama-listener-stale-check` (codex-ten-drama, branch
  `codex/ten-drama-audit-fixes`), whose PR #978 is merged; that stale claim overlapped on
  `tools/video/review/sync.mjs`.
- What was done:
  - `package/check.mjs`: `thumbnailVariants(framesManifest)` keeps only `thumbnail-<letter>.jpg`
    names from render's `thumbnail_variants`; `packageFiles` gives such a file the role
    `thumbnail-b` / `thumbnail-c`; `filesItem` fails a listed variant that is missing and any
    thumbnail (A, the variants, the language ones) over `THUMBNAIL_MAX_BYTES` (2 MB). The package
    check never checked A's size before (render and qa did), so that is new for A too; a package
    within the limit reads the same.
  - `package/cli.mjs`: with a `thumbnail.jpg`, copies each listed variant that exists into
    `upload/` and records all listed ones as `metadata.json` `thumbnail_variants` (only when there
    are any), so a variant gone by package time fails the check by name.
  - `package/metadata.mjs`: `thumbnailStep` writes step 1.4 of `UPLOAD.md`: with variants, upload
    A, B and C to 「測試與比較」 (up to three), do not change the title during the test, and record
    the winner in `brief.md`; without variants the old line, unchanged.
  - `review/sync.mjs`: the final review uploads B and C after `thumbnail`, with roles
    `thumbnail-b` / `thumbnail-c`. The publish review already sends every `packageFiles` entry.
- Role names: `thumbnail_b` would be read as a language by the publish card's `localeOf`
  (`apps/web/components/admin-video-review-card.tsx`, every `thumbnail_<x>` is a locale), so the
  roles keep the file's hyphen, which the card ignores for now. The API accepts them as they are
  (`ReviewFile.role` pattern `^[a-z][A-Za-z0-9_-]{0,39}$`, image/jpeg allowed, at most 48 files;
  images stay after the mp4 retirement; YouTube sync reads only `thumbnail`). The web shows only
  `thumbnail` (as the final card's poster) and offers no download for the new roles, so the
  display part is filed as `2026-10-02-show-thumbnail-variants-b-and-c` (web).
- Byte for byte: packaged the minimal fixture (cut, checked, captioned, approved) with origin/main's
  tools and with this branch's, with and without variants: without variants `upload/` is identical
  file by file and so is the package output; with variants only `metadata.json` (the new key),
  step 1.4 of `UPLOAD.md` and the two new images differ. `package/variants.test.mjs` keeps that
  in a test (no new key, file, line or output).
- Added `docs/videos/so-thats-why/thumbnails.md` to the scope: its A/B section and gap table said
  the package carried A only.
- Not bound by `docs/videos/long-form/review.json`: none of the changed files are (sync.test.mjs
  is bound and was left alone; the review-push tests are in `package/variants.test.mjs`).
