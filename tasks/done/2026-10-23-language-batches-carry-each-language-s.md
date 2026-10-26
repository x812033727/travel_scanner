---
id: 2026-10-23-language-batches-carry-each-language-s
title: Language batches carry each language's thumbnail and the manual guide reads them
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-23T17:22:36Z
created_at: 2026-10-23T17:22:06Z
completed_at: 2026-10-24T11:03:05Z
branch: claude/language-batch-thumbnails
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - apps/api/app/video_youtube/language_package.py
  - apps/api/tests/test_video_youtube_language_package.py
  - apps/web/components/admin-video-manual-upload.tsx
  - apps/web/components/admin-video-manual-upload.test.tsx
  - docs/videos/APPROVED-LANGUAGE-PACKAGE.md
---

# Language batches carry each language's thumbnail and the manual guide reads them

## Why

After #1789 the manual upload guide lists `thumbnail_<locale>` files, but for
`story-adapt-a4-paper-size` it still showed only the main thumbnail (2026-10-23). Its upload
confirmation is from 10-19, before any other language; its eight languages came in two later
language batches (10-19, 10-21), which carried descriptions, captions and metadata but no
thumbnails, and the guide read only the confirmation. Every video whose languages were added
after its upload had no language thumbnails on the site, and the guide also missed those
languages' captions, titles and descriptions.

## Definition of done

- [x] `review-push --gate languages` sends `thumbnail_<locale>` for each non-narration
  language with a chosen part and `upload/thumbnails/<locale>.jpg`; the manifest names it.
- [x] YouTube sync's `compose` accepts it (JPEG/PNG, chosen language only) instead of refusing
  the batch for an unchosen file.
- [x] The manual guide merges the newest approved language batch newer than the confirmation:
  its metadata.json (all translations), captions, descriptions and thumbnails.
- [x] Duration review increment for `sync.mjs` and `sync.test.mjs` by an independent reviewer (`claude-pr-review-language-thumbnails-20261024`, PASS).
- [x] Merged and deployed. Existing videos get thumbnails on the site only with their next Deployed dac1b1ee3; A4's batch of 2026-10-24 01:51Z carried all eight thumbnails.
  language batch (A4's dub retries will send one).

## How to verify

`node --test tools/video/review/sync.test.mjs` (97 pass);
`cd apps/api && uv run pytest tests/test_video_youtube_language_package.py tests/test_video_youtube_language_contract.py tests/test_video_languages_worker.py`;
`cd apps/web && npx vitest run components/admin-video-manual-upload.test.tsx` (11 pass).

## Notes

- Claimed with --force: `2026-10-22-409` (claude-fable-5.1) also lists `tools/video/review/sync.mjs`, but its code merged as #1697 and only a host check is left, so nothing of it edits the file now.
- 2026-10-24: The owner authorized releasing only `docs/videos/long-form/review.md` and
  `docs/videos/long-form/review.json` from this ticket for C15's independent duration
  review binding. Other scope and pending deploy work stay here.
