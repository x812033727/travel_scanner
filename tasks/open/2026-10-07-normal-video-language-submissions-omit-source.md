---
id: 2026-10-07-normal-video-language-submissions-omit-source
title: Normal video language submissions omit source manifest and metadata
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-07T03:41:22Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - apps/api/tests/test_video_youtube_language_package.py
---

# Normal video language submissions omit source manifest and metadata

## Why

Ordinary `review-push --gate languages` writes only the legacy speech/choice/parts
artifact and attaches descriptions, captions and dubs. The YouTube consumer now
requires `metadata` and `languages_manifest` attachments, with a schema-version-1
source manifest whose hash is the review content hash. Only renewed-final
submissions currently create that proof. A normal approved language review can
therefore fail with `video_youtube_languages_invalid` and the message
`舊語言審核缺少可驗證的來源清單與 metadata，請重新送審`.

## Definition of done

- [ ] Normal language submissions carry verified metadata and a complete manifest
      bound to the current approved publish/final/script identities and choices.
- [ ] The real Python `read_approved_package` consumer accepts emitted normal
      packages and rejects changed choices, attachment bytes and source reviews.
- [ ] Existing renewed-final binding remains authoritative and unchanged.

## Steps

- [ ] Claim after the existing review/sync scope is released and collision-check
      current worktrees, remote branches and PRs.
- [ ] Add the normal source binding, update mock expectations, and exercise actual
      emitted bytes through the API package consumer.

## How to verify

Run focused Node review/sync tests and API language-package tests, including a
fixture made by the real Node emitter. A mock HTTP 201 or approved status alone
does not prove that the YouTube package consumer accepts it.

## Notes

- Confirmed on origin/main `22fe2ca521f11ff6b617cb6a678228bef68d0da6`
  and the live normal Skills/Gems and Argon reviews on 2026-10-07.
- `tools/video/review/sync.mjs` is claimed by
  `2026-10-06-pictures-keep-best-after-prompt-fixes`; this ticket is deliberately
  unclaimed. No changes were made to that owner's source or to PR #1359.
- Operational resubmission of the two requested Gemini videos is tracked in
  `2026-10-07-resubmit-gemini-language-reviews-with-source`. It reuses actual existing
  media; it is not a deployed native-emitter fix.
- Ready dub tracks keep a new review pending for the owner. Do not copy an old
  decision into a new review or claim Studio upload from a stored audio hash.
