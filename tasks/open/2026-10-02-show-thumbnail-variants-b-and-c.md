---
id: 2026-10-02-show-thumbnail-variants-b-and-c
title: Show thumbnail variants B and C on the final and publish review cards
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-02T06:23:06Z
completed_at:
branch:
depends_on:
  - 2026-09-28-thumbnail-variants-in-the-upload-package
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - apps/web/messages
---

# Show thumbnail variants B and C on the final and publish review cards

## Why

A so-that's-why video can carry YouTube "Test & compare" thumbnail variants: render draws
`thumbnail-b.jpg` and `thumbnail-c.jpg` beside `thumbnail.jpg` (A)
(docs/videos/so-thats-why/thumbnails.md §A/B 測試). Since ticket
`2026-09-28-thumbnail-variants-in-the-upload-package`, the tools send them to the site:

- the final review (`review-push --gate final`) attaches them as files with roles `thumbnail-b`
  and `thumbnail-c` (image/jpeg), after `thumbnail`;
- the publish review attaches every package file, so `thumbnail-b` / `thumbnail-c` come with
  the package, and `upload/metadata.json` lists them under `thumbnail_variants`.

The API stores them as they are (`ReviewFile.role` allows `[a-z][A-Za-z0-9_-]{0,39}`; images
stay after the mp4 retirement). The web does not show them: `FinalBody` in
`apps/web/components/admin-video-review-card.tsx` uses only `thumbnail` as the video poster, and
`UploadPackage` returns no download for an unknown role. So the owner still cannot see B and C on
/admin/videos, nor download them from the 「可以上架」 card.

The roles keep the file's hyphen on purpose: `UploadPackage` reads every `thumbnail_<x>` as a
language (`localeOf`), so `thumbnail_b` would have been labelled as a language "b".

## Definition of done

- [ ] The final card shows A, B and C side by side (labelled A/B/C) when the review has
      `thumbnail-b`/`thumbnail-c` files; a review without them looks exactly as before.
- [ ] The publish card offers B and C as downloads named `thumbnail-b.jpg` / `thumbnail-c.jpg`,
      not as a language thumbnail.
- [ ] New strings in all five locales; `npm run check:i18n` passes.

## Steps

- [ ] Final card: a small A/B/C strip under the player, from `fileFor(review, "thumbnail-b")` etc.
- [ ] Publish card: a branch for `/^thumbnail-[a-z]$/` before the `thumbnail_` one.
- [ ] Tests in `admin-video-review-card.test.tsx`.

## How to verify

`cd apps/web && npx vitest run components/admin-video-review-card.test.tsx`; `npm run typecheck:web`,
`npm run lint:web`, `npm run check:i18n`.

## Notes

- 2026-10-02 filed by claude-opus-5-5-thumb-variants while doing the tools side.
- `apps/web/messages/*/admin.json` and `apps/web/components/admin-video-reviews.test.tsx` are bound
  in `docs/videos/long-form/review.json`; changing them makes `tools/video/long-form/review.test.mjs`
  fail until that review is redone. Say so in the PR and leave the rebinding to its reviewer, or
  put the new strings where they are not bound.
