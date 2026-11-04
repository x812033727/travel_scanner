---
id: 2026-11-03-admin-upload-zip-fails-to-download
title: Admin upload zip fails to download for a 460 MB package
status: in-progress
priority: P1
area: web
owner: claude-opus-5-5-package-zip
claimed_at: 2026-11-04T00:05:51Z
created_at: 2026-11-03T23:48:44Z
completed_at:
branch: fix/admin-package-zip-prune
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_package_zip.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_package_zip.py
  - apps/api/tests/test_video_reviews_youtube.py
  - apps/web/app/api/admin-video-package
  - apps/web/components/admin-video-manual-upload.tsx
  - apps/web/components/admin-video-manual-upload.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/BACKUP.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Admin upload zip fails to download for a 460 MB package

## Why

On 2026-11-04 the owner pressed 「全部下載」 on /admin/videos for `daily-ai-20261103` (Tech Signal 11/3) and Chrome
showed 「daily-ai-20261103-upload.zip 無法在網站上擷取檔案」 (download failed at the site). That package is about
460 MB: final.mp4 121 MB, eight dub tracks 343 MB (`dubs/*.m4a`, ~42 MB each), nine caption files,
nine descriptions, nine thumbnails and metadata.json. The owner's daily workflow is: download the package, upload to
YouTube, upload eight dub tracks in Studio. Tech Signal now ships eight dubs every weekday, so every package is this big.

The zip is built on the fly: the page links `/api/admin-video-package/<slug>?file=<sha>:<name>…`
(`apps/web/components/admin-video-manual-upload.tsx`), the Next route proxies to
`GET /api/v1/admin/videos/<slug>/package.zip` (`apps/api/app/video_reviews/admin_api.py`), which resolves every entry
against the review store (`admin_package_zip.resolve_entries`, 404 `video_review_file_not_found` if a file is no
longer in the store) and streams a stored zip (`stream_zip`).

Not yet known which of these fails: a 404 for an entry the store no longer has (the episode was pushed to
final/publish/languages twice on 11/3 after a re-cut), a 422, a timeout in nginx (`proxy_read_timeout 300s` in
`ops/nginx/mokaair.conf.example`) or in the Next route, or the stream breaking partway.

## Definition of done

- [ ] 「全部下載」 on /admin/videos downloads a complete zip for a package with a final cut and eight dub tracks
      (~460 MB), and the zip opens.
- [ ] When an entry cannot be served, the page says which file and why instead of a browser download failure.

## Steps

- [x] On the host, read the API and nginx logs for the 11/4 morning request to `package.zip` for `daily-ai-20261103`
      (status code, bytes sent, duration) to find which layer failed.
- [x] Fix that layer (missing store file, timeout, or streaming), with a test.
- [x] Make a failed archive visible on the page (e.g. check the entries before handing the link to the browser).

## How to verify

Download the 11/3 package from /admin/videos on production and unzip it; repeat for the next Tech Signal episode.

## Notes

- Workaround meanwhile: the page's per-file download buttons fetch each file on its own.
- `daily-ai-20261101` (183 MB, no dubs) is the largest package known to have been offered before this.

### What failed (2026-11-04, claude-opus-5-5-package-zip)

Not a timeout and not a broken stream: the review store no longer held the files, so the API refused
the zip before its first byte. API log (UTC; Taipei is +8):

- 23:02:56 languages batch approved; 23:03:00 publish approved; 23:03:21 YouTube upload requested
  (unlisted, `BegM82F12jM`).
- 23:05:07 single-file downloads still answer 206/200.
- 23:05:57 Drive backup `done` (37 files, 481 MB, `missing: []`).
- 23:27:49 `GET /admin/videos/daily-ai-20261103` -- the list page runs `prune_published_previews`;
  the store folder's mtime is 23:28 and it is empty since.
- 23:45:25, 23:45:29, 23:45:41, 23:46:34: `package.zip` -> **404 `video_review_file_not_found`**
  (immediately); every `/files/<sha>` 404 from 23:45:10.
- nginx records nothing: the site's server-level `access_log` only logs refusals and crawl files, and
  `error.log` has nothing after 11/3 10:43. The web container logged no error; the Next route's 30 s
  deadline covers only the headers.

Why: `_done_with` (PR #2000, owner 2026-11-03) wipes a video's whole store folder once it is on
YouTube, backed up and every language is made, and `language_states` reads an approved languages
batch as "dubs uploaded in Studio". The owner approves that batch *before* downloading the package
that carries the dubs to Studio, so the store emptied 20 minutes after the backup. The Next route also
replaced the API's problem with a bare `video_package_unavailable`, and the page handed the link
straight to the browser, so Chrome showed only 「無法在網站上擷取檔案」.

Fix (owner chose "wait a week"): the store wipe waits `PREVIEW_RETENTION` (7 days) past `_done_since`
(latest of backup `checked_at`, languages decision, any review decision, publish time; no readable
backup time keeps the files). The page asks `GET /admin/videos/<slug>/package` (Next `?check=1`)
before the download and lists each missing file with `gone` / `not_shown` and the Drive folder.
The 11/3 files were copied back into the store from the worker's surviving
`video_work/daily-ai-20261103/upload/` after the deploy.

Follow-up not done here: the worker's `tidy.mjs` still clears `video_work/<slug>/` the moment the
three conditions hold (BACKUP.md); the review store no longer depends on it, but the 11/3 restore
only worked because tidy had not yet run.
