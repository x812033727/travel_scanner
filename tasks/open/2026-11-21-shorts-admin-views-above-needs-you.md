---
id: 2026-11-21-shorts-admin-views-above-needs-you
title: Shorts admin: views above needs-you, upload package on the Short final card
status: review
priority: P1
area: web
owner: claude-opus-5-5-shorts-package
claimed_at: 2026-11-21T15:58:15Z
created_at: 2026-11-21T15:54:51Z
completed_at:
branch: claude/shorts-admin-upload-package
depends_on: []
scope:
  - apps/web/components/admin-video-shorts.tsx
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/components/admin-video-manual-upload.tsx
  - apps/web/components/admin-video-manual-upload.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - tools/video/shorts/push.mjs
  - tools/video/shorts/silent.test.mjs
  - tools/video/shorts/bindings.test.mjs
  - tools/video/shorts/pipeline.test.mjs
---

# Shorts admin: views above needs-you, upload package on the Short final card

## Why

Owner, 2026-11-21: the seven Shorts views (月曆、片庫與製作中、成效、花費、題庫、每週報告、
Shorts 設定) should sit above 「需要你」, and a Short must carry an upload package so the owner
can upload it by hand; the site must not upload it on its own.

A Short had no package on its card because none existed on the site: `shorts/cli.mjs push`
sends the package (metadata.json with every language, tags, disclosure) only as the *publish*
review, after the final review is approved and push runs a second time. The API never builds one.

## Definition of done

- [x] The Shorts view bar is the first thing on the Shorts tab, above the status row and 「需要你」.
- [x] `push` attaches `metadata.json` (role `metadata`) to a Short's final review when the package
      is of that cut.
- [x] A Short's video page shows the 「手動上傳到 YouTube Studio」 guide from that final review
      (pending or approved): cut, cover, zip, nine languages' title/description, tags, audience
      and the synthetic-media disclosure; no captions step for a silent drama.
- [ ] After deploy, `shechu-hell-e01`–`e06` are pushed again (same cut, final still pending: the
      site replaces the payload and files of that review in place) so their cards carry it.

## How to verify

`npm run test:tools` (shorts), `npx vitest run components/admin-video-manual-upload.test.tsx
components/admin-video-shorts.test.tsx` in apps/web, then open a Short on /admin/videos.

## Notes

- No new strings: the guide reuses `admin.videoYoutube.manual`. Its intro says the files come
  from an approved package; on a pending final that is slightly ahead of the truth.
- The scope overlapped stale claims on the shared files; claimed with `--force` on the owner's yes.
