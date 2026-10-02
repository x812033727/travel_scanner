---
id: 2026-10-01-youtube-narration-request-transport
title: Use approved narration language in YouTube request transport
status: done
priority: P1
area: api
owner: claude-opus-5-5-yt-transport
claimed_at: 2026-10-01T15:57:29Z
created_at: 2026-10-01T10:31:19Z
completed_at: 2026-10-01T16:08:01Z
branch: claude/youtube-narration-transport
depends_on: []
scope:
  - apps/api/app/video_youtube/requests.py
  - apps/api/app/video_youtube/sync.py
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

- [x] Upload/update use the verified approved narration language as both defaults.
- [x] Foreign zh-TW localization survives for English narration; the own default is excluded.
- [x] Existing zh-TW requests and original metadata/visibility protections stay valid.

## Steps

- [x] Audit claims and approval-bound request construction before implementation.
- [x] Add English/zh-TW insert/update and localization request regressions.
- [x] Run affected sync/request tests plus ruff/mypy without live YouTube operations.

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

### 2026-10-01 claude-opus-5-5-yt-transport

- Claimed with `--force`: the only refusal was 2026-09-30-youtube-approved-languages-sync
  (owner codex-approved-languages-sync) still holding tests/test_video_youtube_sync.py, and
  its PR #1048 merged 2026-10-01T02:20:49Z. That ticket was not edited.
- Audit: the narration language is `metadata["default_language"]` of the approved publish
  package. `sync.read_package` binds metadata.json to the approval by SHA-256,
  `language_package.compose` deep-copies it, checks it is a non-empty string and refuses a
  language batch that changes it. The owner's `PublishIn` carries no language, so nothing on
  the request can override it.
- `requests.narration_language(metadata)`: missing -> zh-TW (legacy packages unchanged);
  allowed values are zh-TW plus `DUB_LOCALES`; anything else (fr, "", EN, a number) raises
  ValueError instead of being sent under a wrong label. `localizations()`, `insert_body` and
  `update_body` use it for both defaults; update still pops the own-language localization by
  exact key, so an English video keeps the package's zh-TW localization and drops `en`.
- Scope grew by sync.py: `compose` calls `localizations()`, so an unsupported language would
  otherwise surface as a 500 at request time or the generic "網站這邊出錯了" in the run.
  `read_approved_package` now checks it first and raises `language_package.invalid`
  (existing code `video_youtube_languages_invalid`, already in all locale messages); every
  caller (request, retry, run `_prepare`/`ensure_current`, VPS) already handles `Refused`.
- The package sha in `compose` compares `localizations(metadata)` with
  `localizations(base)`; for zh-TW packages the result is identical to before. No English
  request is in flight (the 17 renewal candidates are zh-TW), so no pinned request changes.
- Tests: English insert/update and legacy/zh-TW cases in test_video_youtube.py; `_package`
  takes `metadata=` and English runs through the Studio and the upload path, plus a refused
  `fr` package, in test_video_youtube_sync.py. The 9 new tests fail on the old code. Only the
  fake YouTube was used; no credentials, no live calls. Real Studio/upload acceptance of an
  English video stays with the owner and takes effect only after a deploy.
