---
id: 2026-11-22-shorts-hand-upload-exclusive
title: Hand-uploaded Shorts: keep them off the site's calendar, package from publish review, record the link
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-22T02:31:21Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_shorts
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/tests/test_video_shorts_manual.py
  - apps/web/components/admin-video-manual-upload.tsx
  - apps/web/components/admin-video-manual-upload.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - docs/videos/SHORTS.md
---

# Hand-uploaded Shorts: keep them off the site's calendar, package from publish review, record the link

## Why

The owner (2026-11-21, as relayed to this task) uploads Shorts by hand, the silent dramas
`shechu-hell-e01`..`e06` (`hand_pushed`) first of all, and the site must not publish them on its
own. PR #2203 put the hand-upload guide on the final review. Two gaps remain, both found by
reading origin/main at 25fbefed5 (not reproduced by running it):

1. No guide after a re-push of an approved cut. `submit_review` returns the decided final as it
   is, so `metadata` is never added to it, and `shortPackageReview` reads only that final.
2. Hand upload and the calendar are not exclusive:
   - an approved publish review always reaches `slots.assign_approved`, hand-pushed or not;
   - `lock_due` also fills empty slots from `library_of`, and prefers a Short with a YouTube id
     until the API audit passes, so a link recorded without a publish time is the first one taken;
   - `publish.send_due` then sends such a Short (consent valid, locked slot, id recorded) through
     `request_sync` in studio mode: it rewrites the details and schedules the owner's video.
     `send_due` itself never uploads a file: with no id it waits for the owner's upload;
   - `start_campaign`, the calendar's `assign`, `claim.waiting_uploads` and the stock count take
     such a Short too.
3. The link cannot be recorded from the page: `UploadedForm` shows only under `readyToUpload`
   (publish approved) with no channel linked, or as `privateOnly`, which refuses Shorts. The
   ordinary `POST /admin/videos/{slug}/youtube` already accepts a Short without a publish review.

## Definition of done

- [ ] The guide shows from a pending or approved publish review of the current cut; the approved
      final is not rewritten.
- [ ] A hand-uploaded Short never gets a slot, leaves one it holds that is not on YouTube yet,
      and is never sent or retried under the standing consent.
- [ ] With the final approved and no publish review, the owner can record the Studio link and
      its publish time; afterwards it is not scheduled or uploaded again.
- [ ] Tests for each of the above; SHORTS.md says so.

## Steps

- [ ] Claim (see Notes: refused on overlapping scope, waiting for the owner).
- [ ] `video_shorts`: one predicate for "uploaded by hand": a live final or publish review with
      `hand_pushed`, or the current id has a `video_youtube_linked` audit row (no migration).
      Use it in `assign_approved`, `library_of`, `lock_due_slots` (release held slots), `_assign`,
      `send_due` and `waiting_uploads`.
- [ ] `video_youtube/sync.py`: check it again under the project lock for automatic `request_sync`
      and `retry_sync`, and before an automatic run's scheduling write.
- [ ] `link_youtube` for a Short: refuse while a sync runs, release the slot with the link.
- [ ] Web: prefer the publish review whose `final_review_id` is the current final (cover from the
      final); show `UploadedForm` with the guide, in place of the send form for a hand upload.
      A link saved without a time needs a way to add the time later (the form hides once linked).

## How to verify

API: pytest for a hand-pushed and a hand-linked Short through approve, lock, tick and claim.
Web: vitest for the publish-only package and the link form. Then the checks in CLAUDE.md.

## Notes

- No code changed yet. `claim` refused on 2026-11-22: nine active claims overlap. Not forced.
  - merged PRs, stale claims: let-managers-link-a-private-studio (#1475),
    dub-narrator-only-explainer-dramas-tool (#1482), worker-video-languages-five (#1614),
    judge-7-judge (#1850), daily-brief-on-the-host-worker (#1918),
    admin-video-delete-dropped (#1943), admin-upload-zip-fails-to-download (#2008);
  - merged PRs, claims under 24 h: shorts-admin-views-above-needs-you (#2203),
    shorts-import-silent-zero-dialogue-vertical (#2200, its task names no branch).
- Open PRs on the same files: #2144 (draft, last updated 11-18: admin_service.py,
  video_shorts/settings.py, sync.py) and #2007 (conflicting, 11-03: sync.py, SHORTS.md).
- Dirty checkouts: only `docs/videos/SHORTS.md` was found modified, in
  agent-a2b4bc4db4c679370 (file dated 10-10). The scan covered this machine's worktrees only,
  with a five-second limit on each, and not cloud sessions.
