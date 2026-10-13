---
id: 2026-10-12-a-youtube-upload-refuses-when-the
title: A YouTube upload refuses when the channel already has the video, and a Studio link never replaces a different recorded one
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-duplicate-upload
claimed_at: 2026-10-12T13:33:37Z
created_at: 2026-10-12T13:33:23Z
completed_at:
branch: claude/duplicate-video-upload-a5fc43
depends_on: []
scope:
  - apps/api/app/video_youtube/sync.py
  - apps/api/tests/test_video_youtube.py
  - apps/api/tests/test_video_youtube_sync.py
---

# A YouTube upload refuses when the channel already has the video, and a Studio link never replaces a different recorded one

## Why

On 2026-10-12 the channel got two identical private copies of curio-l08 (the crop-circle
video). `mLxCEB_wSLk` was uploaded in Studio at 11:03Z but its address was never pasted on the
card, so the site did not know it existed. At 12:24:43Z the card was sent in `upload` mode and
the site's videos.insert created `XSFNRORVuYo` (fully processed, 11:37). At 12:25:16Z the card
was sent again in `studio` mode with `mLxCEB_wSLk`, and the details step overwrote
`youtube_video_id`, leaving `XSFNRORVuYo` on the channel with nothing pointing at it.

## Definition of done

- [x] An `upload` run looks at the channel's fifty newest uploads before videos.insert and fails
      the upload step, naming the video, when one already carries this title (bare or with the
      captions tag, card title or package title). No upload session is started.
- [x] A `studio` run whose pasted id differs from a recorded `youtube_video_id` that is still on
      the channel fails the details step instead of replacing it; once the extra video is deleted
      in Studio, a retry links the pasted one.
- [ ] Deployed.
- [ ] The owner deletes `XSFNRORVuYo` in Studio (keep `mLxCEB_wSLk`: the site links it and its
      EN/JA/KO dubs were uploaded to it).

## How to verify

`cd apps/api && uv run pytest tests/test_video_youtube*.py tests/test_video_shorts_publish.py`
(the two new tests are in test_video_youtube_sync.py).

## Notes

- How it was found: `admin_audit_logs` for `video_project:curio-l08` shows the two
  `video_youtube_sync_requested` rows 33 s apart; the channel's uploads (read through the linked
  connection with `client.playlist_page` + `client.videos`) show both ids with the same title.
  The Studio uploader on the host (`mokaair-studio-uploader-uploader-1`) had no job for it.
- The title check costs 3 quota units (channels.list, playlistItems.list, videos.list).
- `FakeGoogle` now answers channels contentDetails (uploads playlist), playlistItems.list and
  multi-id videos.list, newest first by insertion order.
