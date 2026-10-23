---
id: 2026-10-23-manual-youtube-upload-offers-no-per
title: Manual YouTube upload offers no per-language thumbnails
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-10-23T14:28:00Z
created_at: 2026-10-23T14:27:39Z
completed_at:
branch: claude/manual-upload-locale-thumbnails
depends_on: []
scope:
  - apps/web/components/admin-video-manual-upload.tsx
  - apps/web/components/admin-video-manual-upload.test.tsx
---

# Manual YouTube upload offers no per-language thumbnails

## Why

The owner uploads by hand from `/admin/videos` (「手動模式：下載檔案與複製文字」). Its thumbnail
step offered only the main `thumbnail.jpg`, although the approved publish package carries a
thumbnail per language (`thumbnail_<locale>`, `thumbnails/<locale>.jpg`) for Studio's language
page. The full download list on the review card has them; the manual guide did not, so the owner
could not get the language thumbnails there (2026-10-23).

## Definition of done

- [x] The manual guide's thumbnail step lists a download per `thumbnail_<locale>` file, named
  `thumbnail.<locale>.jpg`; Test & compare variants (`thumbnail-b`) are not shown as languages.
- [x] No new strings: it reuses `admin.videoReviews.downloadLocaleThumbnail` with the guide's
  language names, so the five `admin.json` files (bound by the duration review) are untouched.
- [ ] Merged and deployed.

## How to verify

`cd apps/web && npx vitest run components/admin-video-manual-upload.test.tsx` (10 pass).
