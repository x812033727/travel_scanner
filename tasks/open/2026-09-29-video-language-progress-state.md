---
id: 2026-09-29-video-language-progress-state
title: Distinguish video language progress from missing publish approval
status: in-progress
priority: P2
area: web
owner: codex-video-stall-followthrough
claimed_at: 2026-10-04T10:56:37Z
created_at: 2026-09-29T03:53:38Z
completed_at:
branch: codex/video-stall-followthrough-20261004
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Distinguish video language progress from missing publish approval

## Why

The owner sees many long videos labelled "語言製作中" with no pending decision.
`publishState` maps every final-approved, language-decided project whose
`ready_to_upload` is false to `making`. That flag also depends on publish approval;
it does not show whether a producer is running. Chosen language parts without a
successfully submitted language review default to `working` in the API.
Consequently a missing producer report or missing publish approval can look like
active language production indefinitely.

## Definition of done

- [x] Long-video status distinguishes missing language results from missing publish
  approval, using available evidence without claiming a producer is running.
- [x] The UI explains that pending decisions count submitted pending reviews;
  metadata/caption-only batches and batches with all dubs skipped auto-approve.
- [x] Ready, scheduled, uploaded and dropped states retain their current behavior.
- [x] All five admin locales agree. Coordinate ownership before touching shared
  components; this ticket does not own the other conversation's Shorts changes.

## Steps

- [x] Check current main, active worktrees and PRs before claiming implementation.
- [x] Trace publishState, language_states and ready_to_upload; use a neutral label
  when the API cannot prove active work or a failure.
- [x] Update labels and focused state fixtures, then run relevant web/i18n checks.

## How to verify

Exercise final-approved projects with language choices but no reported batch,
completed parts but no publish approval, a pending ready-dub batch, an auto-approved
batch with skipped dubs, and ready/scheduled/uploaded projects. Confirm the text
does not present missing producer evidence as active rendering.

## Notes

- Taken into this recovery branch from the retained uncommitted ticket in 4a7e.
  Fresh checks found no open competing PR or tracked edits in that checkout.
  Scope collisions were already merged PRs #870, #978 and #1186; only this
  ticket was claimed, without changing those other owners' records.
- Live 2026-10-04T10:51Z: all six isolated imported-language producers stopped,
  while the API still calls unreported chosen parts `working`. Preserve that
  data contract and use neutral UI wording; it does not prove an active run.
- The new neutral language label and separate packaging state preserve API data
  and current owner choices. Missing or unknown results stay incomplete; all
  selected ready/skipped/uploaded parts enter packaging until the actual package
  and approval make `ready_to_upload` true. No selected part is forged or skipped.
- Focused UI: 138 tests passed across 10 files; web lint, TypeScript and five-locale
  checks passed. Full web and portable tooling checks remain in progress.
- Exact duration-receipt scope added for independent increment only. Fresh remote
  main and PR inspection found no open competing PR touching those receipts;
  the last landed updates include #1203, #1197, #1193 and #1186. Other task owners
  remain unchanged. The implementation author must not rebind the receipt.

- Read-only production snapshot: 2026-09-29T03:49:54Z, revision
  `717e16280977fb5e024947bde000adbe0fe4d752`, zero `languages` review records.
  Academy's oversized summary still fails every five minutes. PR #964 fixes that
  submission and worker starvation; it was draft, green and undeployed at this check.
- Six `ai-real-world-*` imported long videos have approved finals and chosen locales
  but no project directory/auto.json in the server worker volume. The server loop
  cannot pick them up; this does not prove an external producer is stopped.
- Academy's metadata and captions are ready. English/Korean dubs were skipped after
  two failed retakes; Japanese was skipped after two shortening rounds. A successful
  submission of this particular batch auto-approves because no dub is ready.
- Existing deployment/queue acceptance remains in
  `2026-09-29-verify-video-language-queue-recovery`; filing this ticket does not
  authorize production changes or owner review decisions.
