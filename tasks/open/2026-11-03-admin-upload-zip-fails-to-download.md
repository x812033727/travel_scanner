---
id: 2026-11-03-admin-upload-zip-fails-to-download
title: Admin upload zip fails to download for a 460 MB package
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-11-03T23:48:44Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_package_zip.py
  - apps/web/app/api/admin-video-package
  - ops/nginx
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

- [ ] On the host, read the API and nginx logs for the 11/4 morning request to `package.zip` for `daily-ai-20261103`
      (status code, bytes sent, duration) to find which layer failed.
- [ ] Fix that layer (missing store file, timeout, or streaming), with a test.
- [ ] Make a failed archive visible on the page (e.g. check the entries before handing the link to the browser).

## How to verify

Download the 11/3 package from /admin/videos on production and unzip it; repeat for the next Tech Signal episode.

## Notes

- Workaround meanwhile: the page's per-file download buttons fetch each file on its own.
- `daily-ai-20261101` (183 MB, no dubs) is the largest package known to have been offered before this.
