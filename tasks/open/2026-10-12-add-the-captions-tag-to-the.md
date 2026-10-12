---
id: 2026-10-12-add-the-captions-tag-to-the
title: Add the captions tag to the titles of videos already on YouTube
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-cc-captions
claimed_at: 2026-10-12T04:43:37Z
created_at: 2026-10-12T04:43:27Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_youtube
  - apps/api/app/cli.py
  - apps/api/tests/test_video_youtube_retitle.py
---

# Add the captions tag to the titles of videos already on YouTube

## Why

#1455 made every title the site sends end with its language's captions tag (「｜CC字幕」...). The
owner asked on 2026-10-12 that the videos already on the channel, public ones included, get it too.

## Definition of done

- [x] `python -m app.cli video-youtube-caption-titles` reports, for every video on the linked
      channel, which titles (default language and each localization) lack the tag; `--apply`
      sends videos.update with everything the video has and only those titles changed.
- [ ] Run on the host: report first, then `--apply` (50 units per video, `--limit` per run).

## How to verify

`cd apps/api && uv run pytest tests/test_video_youtube_retitle.py`; on the host, the report run
after `--apply` shows `to_change: 0`.

## Notes

- A title the tag would push past 100 characters is reported (`too_long`) and left: shortening a
  title is the owner's call.
- The site's sender still refuses to touch a public video (sync.py); this command is the owner's
  one-off exception to that rule, written to AdminAuditLog as `video_youtube_title_captioned`.
