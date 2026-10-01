---
id: 2026-10-01-long-video-renewal-tools-and-ui
title: Connect long video renewal candidates to tools and owner controls
status: done
priority: P1
area: tools
owner: codex-long-renewal-integration
claimed_at: 2026-10-01T09:22:18Z
created_at: 2026-10-01T08:33:00Z
completed_at: 2026-10-01T10:08:21Z
branch: codex/branding-cc-prompt-20261001
depends_on:
  - 2026-10-01-long-video-final-renewal
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal.test.mjs
  - tools/video/import/import.mjs
  - tools/video/import/import.test.mjs
  - apps/web/components/admin-video-renewal.tsx
  - apps/web/components/admin-video-renewal.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/BRANDING.md
---

# Connect long video renewal candidates to tools and owner controls

## Why

The backend final-renewal operation is deliberately owner initiated and version checked,
but the CLI and website cannot yet prepare/select its replacement candidate or carry
the resulting final-review identity into new publish/language packages. Existing
ordinary import preserves old approved languages, which can describe the old timeline.
The owner requested new introductions for existing long cuts; changing only the channel
default is not completion of that request.

## Definition of done

- [x] The tools stage a new candidate with source/body/branding hashes while preserving
      original media, pins, approval history and upload artifacts.
- [x] A content manager can deliberately request renewal from the website, see stale
      version or upload-identity conflicts, and then review the replacement final.
- [x] A queued worker cannot auto-approve the held replacement, re-adopt the old cut,
      or submit an old language timeline as approved for the new final.
- [x] After owner approval, submissions from an already verified normal work snapshot
      carry the final review id and verified final SHA/branding expected by the API;
      an old or unproven snapshot remains held. Activating that snapshot is a separate
      explicitly filed follow-up, not an automatic side effect of owner approval.
- [x] Existing non-renewed videos and imported final-only submissions retain behavior.

## Steps

- [x] Recheck task, worktree and PR collisions before claiming any implementation scope.
- [x] Define a staged candidate receipt usable by the owner API without editing the old
      work directory or deleting approvals to bypass branding adoption guards.
- [x] Bind fresh GET renewal state, old final id/hash, new preview/files and reason to
      POST /admin/videos/{slug}/final-renewal; never retry a stale/ambiguous write blindly.
- [x] Extend publish/language producers with final_review_id and source manifest bindings;
      verify timeline offsets, subtitles, chapters, dubs and final/branding hashes.
- [x] Add a narrowly placed owner control and five-locale explanations for the actual
      staged/pending/approved states, stale versions and unreconciled upload identity.
- [x] Add cross-language producer/API fixtures and workflow/UI regressions; retain a
      separate explicit deploy and media-operation boundary.

## How to verify

Run focused Node tests for the touched producer modules, API renewal/YouTube tests,
web component tests, web lint/typecheck and check:i18n. Use real emitted manifest bytes
in API consumer tests. Validate the final source id/hash/branding and caption time shift,
not merely successful HTTP responses. Run task checks before PR handoff.

## Notes

- Validation: focused tools 85 passed; complete tools 1027 passed / 2 existing skips;
  focused web 38 passed; web lint, final scoped lint, typecheck and five-locale i18n
  passed. Real Node manifest bytes passed the Python consumer for selected locale
  subsets, with stale/rebound proofs correctly rejected. External QA receipt:
  `brand-package-v2-cc/rollout/renewal-integration-validation.json`.
- Full local web run did not provide completed-suite evidence after 18 minutes on
  Windows. Root authorized stopping only the verified task Vitest PID; its exit was
  -1 (npm 4294967295), not a pass. Process/runtime/log diagnostics are retained in
  `renewal-web-full-diagnostic.json`; full web verification remains a CI acceptance
  gate. The final changed components passed their independent focused run.
- This implementation finishes the staged-candidate and manual-pending owner entry
  point. It does not adopt a new canonical worker workdir, manufacture missing source
  checks for imported cuts, or continue renewed compilations. Those acceptance criteria
  moved, with root approval, to the unclaimed dependent task
  2026-10-01-hand-off-owner-approved-renewed-finals. Old worker bytes fail closed.
- Independent review fixes: exact canonical gate proof for review-pull; PNG/JPEG
  thumbnails; persisted owner readback; current compact choices; default and foreign
  captions/chapters before publish; authenticated CLI Origin header; local preview
  hash verification and cleanup even when navigation interrupts hashing.
- No deployment, live stage/import, upload, approval or publication was performed by
  this implementation. Current production review decisions must be read freshly;
  historical inventory below is not a claim that all imported finals remain pending.

- Claimed 2026-10-01 by codex-long-renewal-integration with root authorization to
  override only historical scope declarations on this new ticket. Fresh origin/main
  contains #978 (9656d0d9e42225c19fc0b2e05e64e26d7881f09a: listener/script binding and
  preloaded document order) and #870 (79e26fcdfc8abecbde6639278e3087927119047c: withdraw).
  Both are ancestors of fetched main; their old branches have no active worktree,
  remote head or open PR. No other owner's ticket was changed. PR #1069/#1070 share
  admin catalogs in unrelated keys; this work uses a new videoRenewal namespace.
  The recovery worktree's clean sync changes already landed in #964. The held
  #1048 producer draft will not be applied or modified.

- Originally filed unclaimed; implementation was subsequently authorized and claimed
  as recorded above. The dependent handoff task remains unclaimed.
- Backend dependency: 2026-10-01-long-video-final-renewal. Its GET/POST route uses
  content.manage and preserves superseded decisions and attachments. It intentionally
  refuses any recorded YouTube/upload/session/sync history and completed stage signals.
  The producer reports stage as the next step: on YouTube plus exactly one explicit
  on_youtube.done=false item is waiting to upload, not a completed-stage signal.
- Fresh root audit on 2026-10-01: among six imported cuts, 01/02/03 have approved
  languages + final; 04/05/06 have approved final only. None has approved publish,
  a YouTube id or upload jobs. Re-importing 01/02/03 would leave old languages approved,
  so hold them for source-bound renewal; a new final pending is not full invalidation.
- At deployed source 7606ff50, decision accepts pending only; locale choice updates do
  not invalidate old approved batches. No legitimate revoke-languages API exists there.
  Do not substitute fake skipped language reviews or remove approval records.
- The root's fresh audit found every one of 11 on-YouTube/no-ID rows had
  on_youtube.done=false. This is the producer's legitimate pending-upload next step,
  not a contradiction requiring forced stage rewriting. The renewal API permits that
  exact unambiguous shape while still rejecting missing/true/duplicate checklist items,
  ids, sync/session/history, actual completed stages or VPS activity. Compare complete
  authenticated channel ids/campaign/duration evidence before a live operation to
  catch unrecorded manual uploads; never invent or clear a video id to unlock renewal.
- Scope is a starting exact file list for the integration; adjust only after fresh
  collision checks if a candidate CLI entry point or other supporting file is needed.
