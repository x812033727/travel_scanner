---
id: 2026-10-04-audit-all-long-video-bookends-and
title: Audit all long-video bookends and repair DevDay while preserving original thumbnails
status: done
priority: P1
area: docs
owner: codex-video-branding-20261004
claimed_at: 2026-10-04T04:30:11Z
created_at: 2026-10-04T04:29:31Z
completed_at: 2026-10-04T04:57:12Z
branch: codex/video-branding-audit-20261004
depends_on: []
scope:
  - docs/videos/branding-release/2026-10-04-bookend-audit.md
---

# Audit all long-video bookends and repair DevDay while preserving original thumbnails

## Why

The owner reported that the completed DevDay 2026 video lacked animated channel
bookends and requested a full inventory audit. Every replacement must retain the
original approved YouTube thumbnail. The local producer had no channel registry;
the production producer already had the verified five-second opener and
three-second outro. Existing approved cuts require the owner renewal workflow.

## Definition of done

- [x] Audit every current long-video project and distinguish completed, unbuilt,
      uploaded, withdrawn, and renewed-but-unpackaged states.
- [x] Install and validate the existing channel assets in the actual local producer
      work base so future first builds include both bookends.
- [x] Create and validate an isolated DevDay replacement, retaining original body
      video packets and thumbnail; captions and chapters after 00:00 shift five seconds.
- [x] Submit the source-bound candidate through the owner renewal interface and
      verify the persisted pending review without approving or uploading it.
- [x] Record exact evidence and remaining canonical package handoff requirements.

## Steps

- [x] Collision-check live branches, open PRs, latest main, and the board.
- [x] Read the production registry and canonical final/check records in one SSH batch.
- [x] Read all 61 long projects sequentially; inventory also includes 15 Shorts.
- [x] Confirm DevDay is the only active unuploaded completed cut lacking branding proof.
- [x] Preserve the original approved thumbnail SHA-256 as the replacement invariant.
- [x] Finish media validation, stage the exact candidate, and read back the owner review.

## How to verify

Use SHA-256 equality for the original final and original/candidate thumbnails;
validate the branding asset hashes, 150/90 exact frame counts, total duration,
complete ffmpeg decode, every caption offset, and actual presentation chapter times.
Read back the newly submitted review identity and attachment hashes. Run
`npm run check:tasks` for this report-only repository change.

## Notes

Private evidence is outside Git under the owner's `mokaair-work/branding-audit-20261004`.
The 2026-10-04 audit found 36 long projects with final reviews: 23 had branding
proof; the 13 without it comprise ten recorded YouTube uploads, two dropped
projects, and DevDay. Twenty-five long projects have no final review yet.

Seventeen earlier renewals have approved branded finals but no current approved
publish package. Their handoff remains tracked by
`2026-10-01-hand-off-owner-approved-renewed-finals`; superseded old packages are
history, not upload-ready files. That task must preserve each original approved
thumbnail. `free-vs-paid-ai-plans-2026` has one earlier thumbnail discrepancy that
must be reconciled during its handoff. This run does not overwrite that separately
approved revision or alter existing YouTube uploads.

DevDay candidate review `101dc061-4b83-4845-9137-a9a71ff32d27` was submitted at
2026-10-04T04:53:58Z and read back as pending/manual_review. Its final, preview,
unchanged original thumbnail, and offset zh-TW captions are staged attachments.
Original final/publish reviews remain superseded with exactly their previous files;
YouTube identity, schedule, and selected languages did not change. Full decode,
all 24061 encoded body video packet hashes, and all 322 caption timestamps passed.
Canonical adoption and selected-language publish packaging remain open under
`2026-10-04-adopt-approved-devday-bookend-replacement-and`; owner listening/approval
and YouTube publication are outside this audit task's definition of done.

Validation: `npm run check:tasks` exited 0 and validated 1385 task files; existing
age/scope warnings are unrelated to this report. Media spot checks at 2/6/808.5
seconds confirm opener/body/outro order. Both cuts measured -14 LUFS and -0.8 dBTP.
