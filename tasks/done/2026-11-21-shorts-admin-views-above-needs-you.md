---
id: 2026-11-21-shorts-admin-views-above-needs-you
title: Shorts admin: views above needs-you, upload package on the Short final card
status: done
priority: P1
area: web
owner: claude-opus-5-5-shorts-package
claimed_at: 2026-11-21T15:58:15Z
created_at: 2026-11-21T15:54:51Z
completed_at: 2026-11-22T13:38:51Z
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
- Dropped on the owner's word (2026-11-22), not completed: `shechu-hell-e01`–`e06` pushed again
  so their cards carry the package. Five were; e03 was not. See the notes.

## How to verify

`npm run test:tools` (shorts), `npx vitest run components/admin-video-manual-upload.test.tsx
components/admin-video-shorts.test.tsx` in apps/web, then open a Short on /admin/videos.

## Notes

- No new strings: the guide reuses `admin.videoYoutube.manual`. Its intro says the files come
  from an approved package; on a pending final that is slightly ahead of the truth.
- The scope overlapped stale claims on the shared files; claimed with `--force` on the owner's yes.
- 2026-11-22: e01, e02, e04, e05 and e06 were pushed again with the cut the site already had;
  read back, each kept its pending final review (same id) and gained `metadata`. e03 was not
  pushed: its final had been approved on 2026-11-21T15:48:35Z, and a push would have sent a
  publish review instead of attaching the package. (The #2203 description says all six were
  pending; that was wrong.)
- All six cuts on the site are superseded by a later re-edit. The owner then decided
  「完成後上架包放雲端我自己手動上架就好」: the new cuts go to Google Drive as upload packages and
  are not imported or sent for review. Do not approve, upload or publish the site's old cuts,
  and do not push the new ones.
- What #2203 left open (no package on an already approved final, no exclusion between a hand
  upload and the site's own publishing) went to #2210, merged 2026-11-22.
- Not verified here: that production runs #2203; the guide was never looked at on the live page.
