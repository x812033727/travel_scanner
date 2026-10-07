---
id: 2026-09-30-youtube-approved-languages-sync
title: YouTube sync reads stale publish package after approved languages
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-happy-carson
claimed_at: 2026-10-07T07:17:15Z
created_at: 2026-09-30T10:35:02Z
completed_at:
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - apps/api/app/video_youtube/sync.py
  - apps/api/tests/test_video_youtube_sync.py
  - apps/api/app/video_youtube/language_package.py
  - apps/api/tests/test_video_youtube_language_package.py
  - apps/api/app/video_youtube/vps.py
  - apps/api/tests/test_video_youtube_vps.py
  - docs/videos/APPROVED-LANGUAGE-PACKAGE.md
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/review/language-contract.mjs
  - tools/video/review/language-contract.test.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/flow.mjs
  - apps/api/tests/test_video_youtube_language_contract.py
  - apps/api/tests/fixtures/video_language_contract
  - docs/videos/LANGUAGES.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
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

- [x] Sync includes current approved language metadata and captions alongside the
  approved video and thumbnail, without weakening approval or content-hash checks.
- [x] The requested language version is pinned and stale or changed approvals are
  rejected before sending to YouTube.
- [x] Original-language-only and Shorts sync remain valid, with focused regressions.
- [x] Existing public-video protection and privacy/scheduling behavior are unchanged.
- [x] Apply the source-bound producer contract after resolving its overlapping scope,
  then validate the actual submission-to-upload path.

## Steps

- [x] Compare live Studio counts, approved review snapshots, sync receipts and host files.
- [x] Implement approval-aware language package selection/composition in API and VPS.
- [x] Run regression tests, lint/type checks and task validation; prepare reviewable diff.
- [x] Integrate producer contract in tools/video/review/sync.mjs and its test.

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

### 2026-10-07 producer contract (claude-opus-5-5-happy-carson, PR #1361)

- Scope widened after a collision check (no active task, open PR or `+` worktree on these paths;
  the old holder `2026-10-06-pictures-keep-best-after-prompt-fixes` is done). This also covers the
  unclaimed follow-up `2026-10-07-normal-video-language-submissions-omit-source` that PR #1363
  files: close that one when #1363 lands.
- `tools/video/review/sync.mjs`: `bindLanguageSource` binds every language batch that is not a
  renewed final's (`renewal.mjs` stays authoritative for those). It uploads the current
  `upload/metadata.json` as `metadata`, writes the schema 1 manifest to `review/languages.json`
  (what `review-pull` and the worker's `pulled()` record the approval by) and uploads it as
  `languages_manifest`, its hash the review's content hash. `source` names the site's newest
  approved final, the newest confirmation (approved, or pending: one approved unchanged then
  carries the batch) and, for a non-compilation drama, the newest approved screenplay;
  `choice` is the site's normalized choice with its first decision time. Nothing is posted when
  it cannot be bound: no or a rejected confirmation, an unapproved final or screenplay, a package
  of another final, branding or choice, a description that is not its metadata, or narration
  captions that differ from the approved confirmation's. The narration's own dub goes as an
  explicit skip. When the same manifest bytes were sent before as an older review (an owner
  going back to an earlier choice), `follows` names the newest batch, because the server answers
  repeated bytes with the old review while the consumer reads the newest.
- Contract test: `tools/video/review/language-contract.mjs` runs the real `package` and
  `review-push` on the minimal (zh-TW) and en fixtures against a site double that keeps the
  server's ordering, deduplication and auto-approval; the site's rows and stored files are
  committed in `apps/api/tests/fixtures/video_language_contract/` and
  `apps/api/tests/test_video_youtube_language_contract.py` (26 cases) feeds them to the real
  `read_approved_package` with files verified: both compose, and a changed choice, any changed
  attachment byte, a newer or pending final and a newer confirmation are refused.
  `language-contract.test.mjs` fails while the copy is stale (`LANGUAGE_CONTRACT_WRITE=1`
  rewrites it; the floor opt-out only works in the test runner). With the producer change
  removed, the regenerated fixture fails the Python test; regenerating twice is byte-identical.
- The worker's fake site now answers the tool GET with `locales`/`locales_decided_at`, as
  `ProjectOut` does; three worker tests assert the two new attachments, one also the manifest.
- Each new producer rule was removed in turn and a test failed (binder, `follows`, narration
  skip, narration captions, description bytes, screenplay, confirmation status).
- Filed: `2026-10-07-the-worker-sends-a-language-batch` (a batch sent before the confirmation
  is approved is never read, so a ready dub cannot sync), `2026-10-07-a-tidied-video-s-skipped-language`
  and `2026-10-07-imported-long-videos-language-batches-carry` (the other emitters without proof).
- Not done here: deployment; resubmitting the language reviews sent before this change (they
  carry no manifest; the five videos in Why and others need a release action); a live upload.

### 2026-10-07 independent review (4 reviewers, each finding checked by a skeptic)

- Blocking, fixed: a drama with no screenplay review on the site (a brand story, whose screenplay
  `story.mjs` approves locally; a drama made with 「劇本先給我看」 off) was refused, so the worker
  deferred and then blocked it, where the batch used to go up. Producer and consumer now bind a
  drama's screenplay review only when the site holds one (`languageSource`;
  `language_package.py` `_source`), still refusing one that is pending, rejected or changed.
- Should-fix, fixed: an mp3 or wav dub went up as ready with no track (now attached under
  `dub_<locale>` with its own type); the worker translated and dubbed the narration's own
  language, so the dub CLI's refusal blocked an English-narrated video before the batch (now
  skipped in `flow.mjs` `languages()`, with a worker test); the narration's own title is checked
  against the approved confirmation as its captions are; `follows` is idempotent (a re-push of
  the same state adds no review); the site's reviews are checked before any file goes up; a
  batch's summary is built from what is sent (a renewed final's skip reason).
- Should-fix, filed: a choice narrowed or changed back after a batch sends nothing new, so sync
  refuses until a manual push (added to `2026-10-07-the-worker-sends-a-language-batch`). Not a
  regression: every ordinary batch was refused before this change.
- Tests: the contract gains a ready mp3 dub case (owner-approved); the unrealistic "same package
  reviewed again" case is replaced by the confirmation the worker really sends after a batch,
  which composes from its own package (and, with a dub, is refused: the filed ordering ticket).

