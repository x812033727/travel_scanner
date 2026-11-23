---
id: 2026-11-21-silent-shorts-leave-the-cc-captions
title: Silent Shorts: leave the ｜CC字幕 captions tag off the titles of a Short whose metadata.json says silent
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-11-21T13:54:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_youtube/requests.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/app/video_youtube/vps.py
  - apps/api/app/video_youtube/retitle.py
  - apps/api/tests/test_video_youtube_silent_titles.py
---

# Silent Shorts: leave the ｜CC字幕 captions tag off the titles of a Short whose metadata.json says silent

## Why

The owner's rule of 2026-10-12 puts a captions tag on every title (`requests.CAPTION_TAGS`,
「｜CC字幕」, 「｜CC Subtitles」, …), and the site adds it on the way to YouTube in
`requests.captioned`, called from `insert_body`, `update_body`, `localizations`, `sync.py` (the
length check before a publish), `vps.py` (`_captioned_entry` and `start`) and `retitle.py`. A
zero-dialogue Shorts drama (`docs/videos/shorts-drama/`) has no captions at all, so the tag would
tell viewers in eight languages something untrue. Since
`2026-11-21-shorts-import-silent-zero-dialogue-vertical` the tool writes `"silent": true` into such
a Short's `metadata.json` and uploads no caption track.

## Definition of done

- [ ] A package whose `metadata.json` has `"silent": true` reaches YouTube with its titles (zh-TW
      and every localization) as written: no captions tag added, any already there taken off.
- [ ] Every other package keeps the tag exactly as today.
- [ ] The channel-wide retitle (`retitle.caption_channel_titles`) does not put it back on a silent
      Short (it works from YouTube's video list, so it needs to know which videos are silent).
- [ ] Tests in `apps/api/tests/test_video_youtube_silent_titles.py`.

## Notes

- `requests.py` and `sync.py` were in the scope of `2026-10-19-worker-video-languages-five`
  (status review) and `2026-10-29-daily-brief-on-the-host-worker` (in progress since 10-29) when
  this was filed; check whether those are really still active before claiming.
- Simplest shape: `captioned(title, language, *, story=False, captions=True)` and a
  `has_captions(metadata)` helper at each call site that has the metadata.
