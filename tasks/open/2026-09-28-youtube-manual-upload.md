---
id: 2026-09-28-youtube-manual-upload
title: YouTube manual upload guide with downloads and copyable fields
status: in-progress
priority: P1
area: web
owner: codex-manual-upload
claimed_at: 2026-09-28T03:59:10Z
created_at: 2026-09-28T03:58:57Z
completed_at:
branch: codex/youtube-manual-upload
depends_on: []
scope:
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/components/admin-video-manual-upload.tsx
  - apps/web/components/admin-video-manual-upload.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - docs/videos/MANUAL-UPLOAD.md
---

# YouTube manual upload guide with downloads and copyable fields

## Why

When YouTube API quota is exhausted, the owner needs a visible manual mode with the exact
approved files to download and fields to copy into Studio. Existing files are buried in review
history, and a partially uploaded video must not be uploaded again.

## Definition of done

- [x] The API publish form and a stopped sync expose manual mode without making YouTube calls.
- [x] The guide maps final MP4, thumbnail, per-language subtitles, title, full description,
      tags and disclosure/audience settings to Studio steps, with five UI locales.
- [x] Existing video IDs open the original Studio page; full-video, compilation and missing-file
      cases are distinguished, and metadata/clipboard errors remain recoverable.
- [ ] Focused regression tests, lint for changed components, web typecheck and i18n pass.

## Steps

- [x] Inspect existing approved-package and file-download contracts and active work.
- [x] Add isolated manual guide and narrow entry points.
- [ ] Validate and prepare a draft PR.

## How to verify

- npm run test:web -- components/admin-video-manual-upload.test.tsx components/admin-video-youtube.test.tsx components/admin-video-reviews.test.tsx
- npm run lint:web; npm run typecheck:web; npm run check:i18n; npm run check:tasks
- Open a local fixture of a failed sync, switch to manual mode, copy another language and
  inspect desktop/mobile layout.

## Notes

- Worktree: youtube-manual-upload. Original e71b checkout and its Shorts work are untouched.
- Collision check: no active claim or open PR touches admin-video-youtube.tsx. PR #870 touches
  review-card/reviews and admin catalogs; this change avoids its components and only adds the
  distinct videoYoutube.manual catalog subtree. No competing review workflow is introduced.
- Manual mode only reads site resources. It intentionally does not clear failed API status,
  trigger retry, or mark a manual upload complete without evidence.
- No production access, deployment or live YouTube changes are part of this implementation.
- Validation: all 40 tests in the manual-upload, YouTube and review component suites pass,
  using bundled Node 24.19.0. The system Node 24.13.0 is below jsdom's current minimum.
- All five locale catalogs pass check:i18n. The initial web typecheck passed.
  Initial full lint found one set-state-in-effect error, fixed by remounting the package
  loader for reload. Resource pressure prevented completing the full local lint rerun;
  the changed components are checked separately and CI will run the full gate.
- Browser visual validation is explicitly outstanding in 2026-09-28-youtube-manual-browser-validation.
  Chrome tab creation/recovery timed out repeatedly; local available memory reached about 0.26 GiB.
  Preview processes were stopped. This is not a browser/device acceptance receipt.
