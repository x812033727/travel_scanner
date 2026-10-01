---
id: 2026-09-30-clarify-first-upload-of-pending-dubbed
title: Clarify first upload of pending dubbed language reviews
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-30T13:32:38Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - tools/video/automation/flow.mjs
---

# Clarify first upload of pending dubbed language reviews

## Why

The language review stays pending when it contains a ready dub, until the owner
confirms that the track was uploaded in Studio. `language_states()` nevertheless
marks its metadata and captions ready, and `ready_to_upload()` can return true
before that approval. A source-bound uploader must not treat that UI status as
approval. For a new video with no YouTube ID, requiring the entire batch approval
also means the owner needs an explicit initial-private-upload path before they
can upload the dub and confirm the review.

## Definition of done

- [ ] Document and implement the first private upload, translated metadata/CC,
  owner dub upload and final scheduling sequence without a circular dependency.
- [ ] No pending or unbound translation is sent as though already approved.
- [ ] The UI and worker readiness agree with the permitted next operation.
- [ ] Do not infer Studio audio publication from generated audio or a UI state.

## Steps

- [ ] Review the pending-dub approval and upload-consent contract with the owner.
- [ ] Define separate permission for the initial private video if necessary,
  while retaining final scheduling and public-video protection.
- [ ] Add regression coverage for a new video with a ready pending dub, and an
  existing private video whose dub has been owner-confirmed.

## How to verify

Run affected video-review/automation and YouTube sync tests, then perform owner
acceptance of the private-first sequence. Real Google login, upload, audio-track
publication and production activation require their own explicit authorization.

## Notes

Discovered during `2026-09-30-youtube-approved-languages-sync`. Relevant code:
`admin_service.py` language_states(), languages_need_owner(), ready_to_upload()
and the languages review approval handling. This ticket records a separate
workflow decision; the language package fix must not silently bypass approval.
