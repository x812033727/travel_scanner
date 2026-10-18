---
id: 2026-10-07-resubmit-gemini-language-reviews-with-source
title: Resubmit Gemini language reviews with source manifests and metadata
status: done
priority: P1
area: ops
owner: codex-gemini-language-resubmit
claimed_at: 2026-10-07T03:41:19Z
created_at: 2026-10-07T03:41:05Z
completed_at: 2026-10-07T03:49:21Z
branch: codex/gemini-language-review-resubmit-20261007
depends_on: []
scope:
  - docs/videos/recovery/2026-10-07-gemini-language-review-resubmit.md
---

# Resubmit Gemini language reviews with source manifests and metadata

## Why

The owner requested fresh language reviews for the Skills/Gems and Gemini 4 Argon
videos after the upload consumer refused their approved legacy language reviews.
Both omit the verifiable source manifest and metadata attachments.

## Definition of done

- [x] Both videos have fresh persisted source-bound language reviews with actual
      metadata and manifest attachments, preserving existing selected media.
- [x] The real API consumer validates the candidate bytes before submission;
      actual status and remaining owner gates are recorded after readback.
- [x] Existing final/publish approvals, selected locales and media remain unchanged.

## Steps

- [x] Locate the exact error, inspect current production reviews and worker state,
      and check collisions before filing the operation and native-emitter follow-up.
- [x] Independently validate a frozen source manifest against actual approved files.
- [x] Submit each language review once, read it back, and record actual status.

## How to verify

Compare source/choice/file hashes, run the deployed API `read_approved_package`
consumer on the frozen candidate without database changes, and read the exact
persisted review after the official review POST. Skills' existing English dub
requires a fresh owner confirmation; Argon's explicit dub skips are preserved.

## Notes

- User authorization covers these two language resubmissions. It does not approve
  a new language review, regenerate paid media, or authorize YouTube upload.
- Both workspaces reported `done` at the preflight. Their final and publish
  reviews were approved; neither project had an upload, schedule or YouTube ID.
- Native normal-emitter gap is separately filed as
  `2026-10-07-normal-video-language-submissions-omit-source`; its source scope is
  still held by another active task.
- Both official review POSTs and exact stored-file readbacks succeeded. Argon's
  new language review is autoapproved and its actual composed package passes.
  Skills/Gems is pending for the existing English dub; its actual new source
  metadata and manifest pass in a separate memory-only approval simulation.
- The precise Skills/Gems refusal is now the expected owner approval gate,
  replacing the missing-source-manifest error. No new approval or Studio upload
  was claimed. Existing old language reviews remain preserved.
- Canonical review artifacts were aligned to the verified new manifests after
  exact persisted readback, with original bytes archived and approvals unchanged.
