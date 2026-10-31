---
id: 2026-10-31-zhong-tian-clip-backup
title: Zhong-tian: back up the per-shot 1080p clips of e031+ so a re-cut or season 2 does not need a re-render
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-31T10:45:29Z
created_at: 2026-10-31T09:25:51Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/README.md
  - tools/video/import
  - tools/video/automation/backup.mjs
  - tools/video/automation/review-package.mjs
  - tools/video/automation/review-package.test.mjs
  - tools/video/cli.mjs
  - apps/api/app/video_reviews/clips.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_backup
  - apps/api/tests/test_video_review_clips.py
  - apps/api/tests/test_video_backup.py
  - docs/videos/BACKUP.md
---

# Zhong-tian: back up the per-shot 1080p clips of e031+ so a re-cut or season 2 does not need a re-render

## Why

The owner (2026-10-31) wants everything a later conversation or a season-2 production would need kept in one known
place. From e031 the episodes are made on Colab in a cloud session; `node tools/video/cli.mjs import --from DIR` sends
only the cut (final.mp4, srt, dubs, thumbnail, meta.json) to the host, so the host's Google Drive backup
(docs/videos/BACKUP.md, `AI/備份/<series>/<episode>/`) holds the finished episode but not the per-shot 1080p clips
(`<workdir>/zhong-tian-qu-qi-eNNN-dh/clips/sNN-t1.mp4`, about 300 MB per episode). They disappear with the container;
a re-cut, a Short or a compilation would need stages 1-3 again (4-6 G4 hours per episode, different takes).

## Definition of done

- [ ] Every imported Colab episode's `clips/sNN-t1.mp4` ends up under the same `AI/備份/<series>/<episode>/clips/`
      folder the host already fills, checked by the backup's own `rclone check`.
- [ ] `production/README.md` section 2 no longer lists the clips as unbacked.

## Steps

- [x] Decide the route with the owner: (a) let `import --from` carry an optional `clips/` folder to the host's
      `video_work/<slug>/clips/` so the full tier copies it, or (b) a separate upload. **Owner 2026-10-31: (a).**
- [x] Find the path a `--publish` file takes to the host (Notes).
- [x] `import --publish` carries `<from>/clips` or `--clips DIR` as `clip_<shot>` files; the API takes
      them on the publish gate beside its 48 files; the worker fetches an imported video's approved
      package into `video_work/<slug>/` before the backup; BACKUP.md §匯入的影片.
- [ ] Deploy (API + web + video-worker image), then watch the first imported episode reach Drive with `clips/`.
- [ ] Back-fill e033-e039 while their workdirs still exist.

## How to verify

`/admin/videos?tab=settings#video-backup-settings` shows the episode as done with its clips listed.

## Notes

- e031/e032 were made by another account's session; their clips may already be gone.
- **Where a `--publish` file went (2026-10-31, before this change).** `import --publish`
  (tools/video/import/import.mjs `importPublish`) uploads each file with `upload()`
  (tools/video/shorts/push.mjs) in 4 MB parts: `PUT /api/video/reviews/<slug>/files/<sha256>` →
  web BFF (apps/web/app/api/video/reviews/[...path]/forward.ts) → API `upload_part`
  (apps/api/app/video_reviews/admin_api.py) → `ReviewStore` on the API's own `video_reviews` volume
  (`/var/lib/mokaair/video-reviews/<slug>/<sha256>`, sha256 checked when the last part lands), then
  `POST …/reviews` names them on a publish review. **Nothing ever copied them into the worker's
  `video_work` volume**: the API mounts `video_work` read-only, the worker has no access to
  `video_reviews`, and no worker code downloads review files. The backup
  (tools/video/automation/backup.mjs `backupRound`) skips a listed video whose `video_work/<slug>/`
  has neither `auto.json` nor `upload/final.mp4` (BACKUP.md step 1's "手動做的" means a folder someone
  made on the host by hand). So every imported episode (e001-e033) was listed by the site and silently
  skipped: none of them is in `AI/備份` at all, clips or not, and the review store deletes their mp4s
  7 days after YouTube. production/README.md row "成片、字幕、配音…" claims otherwise; it was wrong.
- **What the full tier reads**: `planFiles(workdir, "full")` = all of `upload/` (descriptions renamed to
  `descriptions/<l>.txt`), plus `clips/`, `keyframes/`, `characters/`, `timeline.json`, `narration.wav`
  and unpackaged chosen-language dubs/captions/thumbnails; `contentsOf` reports `clips` (count) to the
  site, whose recount (apps/api/app/video_backup/target.py `missing_files`) requires `final.mp4`,
  `metadata.json` and each chosen language's description/captions/dub.
- **Design and why.** The only channel from a cloud session to the host is the review store, and the
  only reader of it the worker can use is the tool-token route `review-files` already uses
  (`GET /api/video/reviews/<slug>/files/<sha256>`, live reviews only, rate 600/hour). So: (1) clips ride
  the publish review as `clip_<shot>` (mp4 only, publish gate only, up to 120 beside the usual 48;
  `apps/api/app/video_reviews/clips.py` `SubmittedReview`, because `schemas.py` and
  `admin_service.py` are bound by the duration review receipt); they stay out of metadata.json, so
  re-sending `--publish` while the package is pending updates the same review in place; the YouTube
  upload, manual-upload page/zip and language package ignore the role; `prune_published_previews`
  drops them with the other mp4s. (2) The worker config names each imported video's approved package
  (`review_package`; `video_backup/admin_status.py review_packages`). (3) Before the backup looks at a
  video, `tools/video/automation/review-package.mjs` fetches that package into `video_work/<slug>/`
  in `package`'s layout, checking each file's size and sha256, writing `review-package.json`; at most 40
  downloads a round; never into a folder with `auto.json` or one that exists without its record.
  The full tier then copies `clips/` like any other video. No migration: the publish review's `files`
  is a JSON column. A separate gate or a new upload route would have needed a migration, a new
  storage lifecycle and a new reader for the same result.
- The materialised folders are never tidied (tidy only acts on `auto.json` folders): about the cut plus
  300 MB of clips per episode stays on the host disk. A follow-up should let the tidy clear them once
  the backup is done.

