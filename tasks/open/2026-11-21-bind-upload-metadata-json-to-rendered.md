---
id: 2026-11-21-bind-upload-metadata-json-to-rendered
title: Bind upload/metadata.json to rendered thumbnail SHA-256s so thumbnail-only updates create new publish reviews
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-21T08:04:54Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package/cli.mjs
  - tools/video/package/package.test.mjs
---

# Bind upload/metadata.json to rendered thumbnail SHA-256s so thumbnail-only updates create new publish reviews

## Why

`publishSubmission` (`tools/video/review/sync.mjs`) uses `sha256File("upload/metadata.json")` as `content_sha256` for the `publish` gate, while `tools/video/package/cli.mjs` records only `"thumbnail": "thumbnail.jpg"` and `"thumbnails": { "en": "thumbnails/en.jpg", ... }` (file paths, without image SHA-256s). When an episode already has an `approved` `publish` review for the current `final.mp4` and only its thumbnail (`thumbnail.data` + `thumbnail.replaces` + `i18n/*.json` `thumbnail`) is updated, `package` writes byte-identical `upload/metadata.json`. `POST /api/video/reviews` (`apps/api/app/video_reviews/admin_service.py` line 1870) then matches `same.content_sha256` with `same.status == "approved"` and returns the old approved `publish` review unchanged, leaving the old `thumbnail` file attached on `/admin/videos`.

## Definition of done

- [ ] When `package` writes `upload/metadata.json` for a video with a thumbnail, `upload/metadata.json` includes `thumbnail_sha256` (and `thumbnails_sha256` for any rendered localized thumbnails, plus `thumbnail_variants_sha256` when variants exist) so changing `thumbnail.jpg` or any `thumbnails/<locale>.jpg` produces a distinct `metadata.json` SHA-256 and a fresh `(pending)` `publish` review on `review-push --gate publish`.
- [ ] `readPackageReport` (`tools/video/package/check.mjs`) verifies that recorded thumbnail hashes (when present) match the bytes in `upload/`, while older `metadata.json` files without those keys remain valid.
- [ ] Covered by unit tests in `tools/video/package/package.test.mjs`.

## Steps

- [ ] Record `thumbnail_sha256` (and `thumbnails_sha256` / `thumbnail_variants_sha256` when present) in `tools/video/package/cli.mjs`.
- [ ] Validate optional `thumbnail_sha256` / `thumbnails_sha256` in `tools/video/package/check.mjs` if needed, keeping backwards compatibility for legacy packages.
- [ ] Add unit tests in `tools/video/package/package.test.mjs` proving a thumbnail-only redraw changes `upload/metadata.json` SHA-256 without invalidating `final.mp4` or `qa` disclosure keys.

## How to verify

```bash
node --test tools/video/package/*.test.mjs tools/video/review/*.test.mjs
```

## Notes

- Observed during the 2026-11-21 9-episode Heimao emblem thumbnail rollout (`curio-s13-v2`, whose `2026-11-20` `publish` review `3965ef64` already listed all 8 localized thumbnail paths for `final` `87a597004816`). Both the `2026-11-18` rollout (`deb146d1`) and `2026-11-21` rollout worked around this by stamping `thumbnail_sha256` (and `thumbnails_sha256`) into `upload/metadata.json` immediately after `package`; `apps/api/app/video_youtube/sync.py` and `language_package.py` already accept extra keys on `metadata.json`.
- Keep `contains_synthetic_media` and `disclosure_reason` at the end of `record` (or preserve `qa` compatibility in `tools/video/qa/cli.mjs`) so running `qa` after `package` still leaves `upload/metadata.json` byte-for-byte identical.
