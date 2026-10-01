---
id: 2026-10-01-youtube-narration-request-transport
title: Use approved narration language in YouTube request transport
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-01T10:31:19Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_youtube/requests.py
  - apps/api/tests/test_video_youtube.py
  - apps/api/tests/test_video_youtube_sync.py
---

# Use approved narration language in YouTube request transport

## Why

The approved language consumer can preserve English narration plus automatic
zh-TW metadata/captions, but YouTube request transport still hardcodes zh-TW.
`requests.localizations` drops zh-TW even when it is a foreign localization,
and insert/update set defaultLanguage/defaultAudioLanguage to zh-TW. Correct
offline package composition therefore does not prove correct English upload.

## Definition of done

- [ ] Upload/update use the verified approved narration language as both defaults.
- [ ] Foreign zh-TW localization survives for English narration; the own default is excluded.
- [ ] Existing zh-TW requests and original metadata/visibility protections stay valid.

## Steps

- [ ] Audit claims and approval-bound request construction before implementation.
- [ ] Add English/zh-TW insert/update and localization request regressions.
- [ ] Run affected sync/request tests plus ruff/mypy without live YouTube operations.

## How to verify

Use existing fake YouTube tests in test_video_youtube.py and
test_video_youtube_sync.py, proving English primary fields/defaults and a foreign
zh-TW localization, along with legacy zh-TW behavior. Real owner-approved Studio
or upload acceptance remains separate from offline tests.

## Notes

Filed unclaimed at root's request; scope is request transport and its existing
tests only. Discovery at shared 50ce HEAD 089c20a01f2426b5f188a3ddd71c9392ad9a7f7f:
requests.py:17 DEFAULT_LANGUAGE='zh-TW'; :85-99 localization helper excludes
that constant at :92; :119-120 insert and :150-152 update use that constant for both
defaults. No transport changes, credentials, live requests or upload occurred.
Current 17 renewal candidates are zh-TW narrated and are unaffected by this
English-only boundary. Do not describe consumer contract acceptance as completed
English YouTube support until this request path and owner acceptance are handled.
