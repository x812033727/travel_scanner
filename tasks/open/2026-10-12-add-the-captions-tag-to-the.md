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
  - apps/api/tests/test_video_youtube.py
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/core/compilation.test.mjs
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
- 2026-10-12 first report on the host (after #1459): 35 videos, 18 to change, 16 too long (mostly
  English localizations near 100 characters), and uZ9TlblvrCw already carried a hand-added
  「｜ CC字幕」 in all four languages, which the first version would have tagged twice. The owner
  chose: the short tag 「｜CC」 when the full one does not fit (for new uploads too), and skip the
  OAuth verification demo 5qjK1zopOkI (`--skip`). `captioned`/`withCaptionTag` now replace any
  trailing captions tag instead of adding beside it.
- 2026-10-12 06:0xZ: `--skip 5qjK1zopOkI --apply` on the host changed 28 videos (1,400 units); the report after
  showed to_change 0. Five videos stayed whole because their English title cannot take even
  「｜CC」 (htv6rUYkVkE, jSTz6qnilmk, UWYoO3JfOK0, KurEPz5z7hA, itKTQl3ehQE). The owner chose to
  leave only that one title and tag the rest, so a too-long title no longer holds back the video.
