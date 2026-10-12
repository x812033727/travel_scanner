---
id: 2026-10-12-every-youtube-title-ends-with-a
title: Every YouTube title ends with a per-language CC captions tag
status: done
priority: P2
area: tools
owner: claude-opus-5-5-cc-captions
claimed_at: 2026-10-12T01:59:18Z
created_at: 2026-10-12T01:59:11Z
completed_at: 2026-10-12T04:20:58Z
branch: claude/video-title-cc-captions-660076
depends_on: []
scope:
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/package/metadata.mjs
  - tools/video/core/compilation.mjs
  - tools/video/core/compilation.test.mjs
  - tools/video/package/metadata.test.mjs
  - apps/api/app/video_youtube
  - apps/api/tests
  - apps/web/components/admin-video-slides-requests.test.tsx
  - tools/video/core/narration-locale.test.mjs
  - tools/video/review/sync.test.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Every YouTube title ends with a per-language CC captions tag

## Why

The owner asked on 2026-10-12 that every video title carry 「｜CC字幕」, worded per language,
so a viewer sees in search results that the video has captions.

## Definition of done

- [x] Every title the site sends YouTube (videos.insert, videos.update, every localization, the
      VPS Studio uploader) ends with its language's tag: zh-TW `｜CC字幕`, en `｜CC Subtitles`,
      ja `｜字幕付き`, ko `｜CC 자막`.
- [x] Packages the worker composes from now on already carry it (metadata.json, description.*.txt).
- [x] The tag is added once: a title that already ends with it is left as it is.

## Steps

- [x] `tools/video/core/metadata.mjs` CAPTION_TAGS + withCaptionTag; `package/metadata.mjs` uses it;
      `core/compilation.mjs` counts it in the 100-character check.
- [x] `apps/api/app/video_youtube/requests.py` CAPTION_TAGS + captioned, used by insert_body,
      update_body, localizations; `sync.py` checks the length with it; `vps.py` sends it.

## How to verify

`node --test tools/video/core/metadata.test.mjs tools/video/package/metadata.test.mjs` and
`cd apps/api && uv run pytest tests/test_video_youtube*.py tests/test_video_shorts_publish.py`.

## Notes

- Applied twice on purpose: at package time (so Studio's manual copy has it and the length check
  counts it) and at send time (for packages approved before the rule and for a title the owner
  retypes on the card). language_package.py is left alone: it compares bound files byte for byte.
- `core/lint.mjs` was not changed because docs/videos/long-form/review.json binds its SHA-256; lint
  still checks the bare title, so a title within 7 characters of 100 passes lint and is refused at
  package. A follow-up with a DURATION_ONLY review could count the tag in lint too.
- Localizations already on YouTube that the package does not carry are sent back untouched.
- 2026-10-12: CI went red on `admin-video-slides-requests.test.tsx` "withdraws a queued request": a
  date time bomb (its cancelled_at 2026-10-05T03:00Z fell outside the one-week window at
  2026-10-12T03:00Z), red on main too. Fixed here by pinning the test's clock.
- 2026-10-12: merged as #1455 (1e987faaa) and deployed 04:14:55–04:19:05Z, no migration; host
  verify 13/13 including `captioned` in the api image and `withCaptionTag` in the video worker.
  Titles already on YouTube are not rewritten; a video gets the tag when it is sent or re-sent.
