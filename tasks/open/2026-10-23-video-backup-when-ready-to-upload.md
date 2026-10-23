---
id: 2026-10-23-video-backup-when-ready-to-upload
title: Back up a video once it is ready to upload, not only after YouTube
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-23T12:41:14Z
created_at: 2026-10-23T12:41:05Z
completed_at:
branch: claude/backup-file-planning-2137f2
depends_on: []
scope:
  - apps/api/app/video_backup/admin_status.py
  - apps/api/app/video_backup/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_backup.py
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - docs/videos/BACKUP.md
  - apps/web/lib/video-backup-messages
  - apps/web/components/admin-video-backup.test.tsx
---

# Back up a video once it is ready to upload, not only after YouTube

## Why

The Drive backup (docs/videos/BACKUP.md) only takes videos with a YouTube id. A video that is
finished and approved but not yet uploaded (waiting on the 60-drafts-a-month limit, or meant for
a hand upload, like the brand-story episodes Seiko and Doraemon on 2026-10-23) lives only on the
host until it is uploaded. The owner (2026-10-23): back a video up as soon as it can be put on
YouTube; if it is revised later, overwrite it then.

## Definition of done

- [x] The site lists for the worker, and the card counts, every video that is on YouTube or
  ready to upload (`ready_to_upload`: upload confirmation approved, languages decided and settled,
  not dropped; a Short needs only its confirmation).
- [x] A ready video is backed up the same way as an uploaded one; its backup.json has
  `youtube_video_id: null` until it is uploaded, then the round sends backup.json again with the id.
- [ ] Deployed, and a video that is ready but not uploaded shows up in Drive.
- [x] A revision (a renewed final cut supersedes the upload confirmation) takes the video off the
  list, so nothing is copied mid-revision; once it is ready again the changed files are copied
  over the old ones, which move to `_舊版/<time>/` as before.
- [x] A report for a video that is neither uploaded nor ready is refused.
- [x] BACKUP.md and the card's text in five locales say "uploaded or ready to upload".

## How to verify

`cd apps/api && uv run pytest tests/test_video_backup.py`;
`node --test tools/video/automation/backup.test.mjs`; vitest on admin-video-backup.test.tsx.

## Notes

- Claimed with `--force`: `2026-10-23-full-backup-keeps-each-chosen-language` still reads
  in-progress over the same files, but its code (PR #1761) is merged and deployed; only its
  deploy check is open, which changes no file.
- The tidy is unchanged: it clears only uploaded videos, which are still all listed.
- `ready_unuploaded` in `video_reviews/admin_service.py` reuses the list's own rule
  (`ready_to_upload`, `_confirmations`, `_language_batches`), so the backup and the review page
  never disagree about which video is ready.
- On Windows, `node --test tools/video/automation/backup.test.mjs` fails three tests: the two
  noted in the full-backup task and the new revision test, all at the second copy into the fake
  Drive. They are expected to pass on Linux CI; check it there.
