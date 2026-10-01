---
id: 2026-10-01-long-video-renewal-tools-and-ui
title: Connect long video renewal candidates to tools and owner controls
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-01T08:33:00Z
completed_at:
branch:
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
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
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

- [ ] The tools stage a new candidate with source/body/branding hashes while preserving
      original media, pins, approval history and upload artifacts.
- [ ] A content manager can deliberately request renewal from the website, see stale
      version or upload-identity conflicts, and then review the replacement final.
- [ ] A queued worker cannot auto-approve the held replacement, re-adopt the old cut,
      or submit an old language timeline as approved for the new final.
- [ ] After owner approval, new publish/languages/dubs submissions carry the final
      review id and verified final SHA/branding expected by the renewal API.
- [ ] Existing non-renewed videos and imported final-only submissions retain behavior.

## Steps

- [ ] Recheck task, worktree and PR collisions before claiming any implementation scope.
- [ ] Define a staged candidate receipt usable by the owner API without editing the old
      work directory or deleting approvals to bypass branding adoption guards.
- [ ] Bind fresh GET renewal state, old final id/hash, new preview/files and reason to
      POST /admin/videos/{slug}/final-renewal; never retry a stale/ambiguous write blindly.
- [ ] Extend publish/language producers with final_review_id and source manifest bindings;
      verify timeline offsets, subtitles, chapters, dubs and final/branding hashes.
- [ ] Add a narrowly placed owner control and five-locale explanations for the actual
      staged/pending/approved states, stale versions and unreconciled upload identity.
- [ ] Add cross-language producer/API fixtures and workflow/UI regressions; retain a
      separate explicit deploy and media-operation boundary.

## How to verify

Run focused Node tests for the touched producer modules, API renewal/YouTube tests,
web component tests, web lint/typecheck and check:i18n. Use real emitted manifest bytes
in API consumer tests. Validate the final source id/hash/branding and caption time shift,
not merely successful HTTP responses. Run task checks before PR handoff.

## Notes

- Filed unclaimed; no producer or frontend edits are authorized by this filing alone.
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
