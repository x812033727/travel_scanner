---
id: 2026-09-30-youtube-approved-languages-sync
title: YouTube sync reads stale publish package after approved languages
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-30T10:35:02Z
completed_at:
branch: codex/youtube-approved-languages-sync-20260930
depends_on: []
scope:
  - apps/api/app/video_youtube/sync.py
  - apps/api/tests/test_video_youtube_sync.py
  - apps/api/app/video_youtube/language_package.py
  - apps/api/tests/test_video_youtube_language_package.py
  - apps/api/app/video_youtube/vps.py
  - apps/api/tests/test_video_youtube_vps.py
  - docs/videos/APPROVED-LANGUAGE-PACKAGE.md
---

# YouTube sync reads stale publish package after approved languages

## Why

On 2026-09-30 the owner reported five recent videos showing only one language in
YouTube Studio. Live read-only audit confirmed that each video's latest approved
languages review includes en, ja, ko and zh-CN metadata and captions, but the
YouTube sync ran from an older approved publish review containing only zh-TW.
All five syncs reported success with one locale and one caption language.

`Automation.languages()` packages the new artifacts and submits a languages
review. `video_youtube.sync.approved_confirmation()` only selects a publish
review, so the later approved language assets are ignored.

## Definition of done

- [ ] Sync includes current approved language metadata and captions alongside the
  approved video and thumbnail, without weakening approval or content-hash checks.
- [x] The requested language version is pinned and stale or changed approvals are
  rejected before sending to YouTube.
- [x] Original-language-only and Shorts sync remain valid, with focused regressions.
- [x] Existing public-video protection and privacy/scheduling behavior are unchanged.
- [ ] Apply the source-bound producer contract after resolving its overlapping scope,
  then validate the actual submission-to-upload path.

## Steps

- [x] Compare live Studio counts, approved review snapshots, sync receipts and host files.
- [x] Implement approval-aware language package selection/composition in API and VPS.
- [x] Run regression tests, lint/type checks and task validation; prepare reviewable diff.
- [ ] Integrate producer contract in tools/video/review/sync.mjs and its test.

## How to verify

Run the API's existing pytest environment against `tests/test_video_youtube_sync.py`
and affected language/Shorts tests, plus scoped ruff/mypy and `npm run check:tasks`.
Cover an older approved zh-TW publish package followed by an approved four-language
review, and negative cases for unapproved, changed or incompatible artifacts.
Production deployment and backfilling existing published videos are separate actions.

## Notes

Read-only audit at 2026-09-30 10:30 UTC: Gemini Connected Apps, Claude Opus 5.5,
Meta account security, Google Vids and OpenAI/Cursor wind-down. Each host upload
package has five locales, five descriptions and five SRT files. Each current
metadata hash differs from the older approved publish package hash.

Artifacts and full receipts are outside the public repository under the task's
`mokaair-work/channel-intro-20260930/language-audit-20260930` directory.
Preparing metadata/captions does not prove Studio publication or audio availability.
Seven en/ja/ko dub files are ready across these videos; eight are skipped. The site
mapping from approved languages to `dub=uploaded` is not independent Studio evidence.
No deployment, live retries, public-video updates, audio uploads or paid generation
were performed by this audit. Backfill approval must identify the existing videos
and translated fields/captions; keep the original video and its visibility intact.

The prepared backfill contains 20 SHA-verified description attachments (first line
is the translated title) and 20 SHA-verified SRT files. Titles were extracted from
those approved attachments, not from the unapproved current metadata.json.
`backfill-manifest.json` and `BACKFILL-REVIEW.md` describe the exact proposed changes.

No implementation or deployment was performed. A safe fix also needs producer
changes in `tools/video/review/sync.mjs` and its test to submit the actual language
manifest and metadata, plus `apps/api/app/video_youtube/vps.py` and its test because
VPS also reads only publish. Expand scope only after rechecking collisions: the
local board still shows the producer paths under the older drama-listener task,
although no open PR currently touches them. Do not release another agent's ticket.

The manifest should bind original publish, final, script where applicable, branding,
language choices and all attachment hashes. API and VPS should share validation;
queued API runs should pin the approved language identities. Legacy complete publish
packages may remain valid, but separate legacy languages reviews with missing source
identity must require resubmission rather than guessed compatibility. Preserve the
existing refusal to update already public videos; manual backfill is a separate action.

## Implementation and remaining scope, 2026-09-30

- API and VPS now share source-bound composition. The API pins both approvals and
  the complete choice for queued runs and retries, rechecks before each write,
  and sends the exact verified subtitle/thumbnail bytes. Original video,
  thumbnail and default-language metadata remain from the publish approval.
- Large file verification runs outside the API event loop. VPS start validates
  full source bytes; staging rechecks identities/manifest and the independent
  service verifies each complete file again before queueing. Status remains
  available when a stale package cannot resume.
- Validation so far: 81 focused API/composition/VPS tests pass. An expanded
  YouTube/review/Shorts run passed 322 tests, with 9 PostgreSQL-only tests skipped.
  Full API ruff/mypy and the uploader's 12 synthetic service/browser tests pass.
- Producer changes are a reviewable patch outside the repository, tested with a
  runtime module overlay (63 tests pass). Actual producer source has not changed:
  its two paths are held by `2026-09-28-drama-listener-stale-check` in another
  worktree. That change was merged in #978, its remote branch is absent, and no
  open PR touches the producer paths, but the old task remains open/review.
- An isolated cross-contract probe captured the actual draft producer's original
  manifest and uploaded bytes, then consumed them using this API's ORM objects
  and a real temporary ReviewStore. Five metadata locales and five captions
  composed correctly, the approved original-language text stayed intact, and
  changed choice/pending approval/inapplicable script cases were rejected.
- The owner has been asked for an exception limited to those two files in this
  independent branch. No old ticket was released or changed, and no force claim
  has been made. Until this is approved and applied, this is an incomplete draft,
  not an end-to-end fix or a deployable release.
- Pending-dub first-upload policy is a separate open task:
  `2026-09-30-clarify-first-upload-of-pending-dubbed`. Pending reviews are not
  silently treated as approved to work around that workflow boundary.
- No merge, deployment, live retry, Google login, video upload or paid generation.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-approved-languages-sync (since 2026-09-30T13:24:06Z) was stale and is released so it stops locking its scope. Landed: #1048 #1101. Still open: Sync includes current approved language metadata/captions end to end (needs the producer side); Apply source-bound producer contract and validate the real submission-to-upload path; Integrate producer contract in tools/video/review/sync.mjs and its test.
