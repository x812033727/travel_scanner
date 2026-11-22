---
id: 2026-11-22-shorts-hand-upload-exclusive
title: Hand-uploaded Shorts: keep them off the site's calendar, package from publish review, record the link
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-shorts-hand-upload
claimed_at: 2026-11-22T02:40:00Z
created_at: 2026-11-22T02:31:21Z
completed_at:
branch: claude/fervent-jang-97f73d
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
  - apps/api/app/video_youtube/vps.py
  - apps/web/components/admin-video-short-link.tsx
  - apps/web/components/admin-video-short-link.test.tsx
  - apps/web/lib/admin-video-short-link-copy.ts
  - apps/web/lib/admin-video-short-link-messages
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

- [x] The guide shows from a pending or approved publish review of the current cut; the approved
      final is not rewritten.
- [x] A hand-uploaded Short never gets a slot, leaves one it holds that is not on YouTube yet,
      and is never sent or retried under the standing consent.
- [x] With the final approved and no publish review, the owner can record the Studio link and
      its publish time; afterwards it is not scheduled or uploaded again.
- [x] Tests for each of the above; SHORTS.md says so.

## Steps

- [x] Claim (refused on overlapping scope; forced on the owner's yes, see Notes).
- [x] `video_shorts`: one predicate for "uploaded by hand": a live final or publish review with
      `hand_pushed`, or the current id has a `video_youtube_linked` audit row marked `by_hand`
      (no migration).
      Use it in `assign_approved`, `library_of`, `lock_due_slots` (release held slots), `_assign`,
      `send_due` and `waiting_uploads`.
- [x] `video_youtube/sync.py`: check it again under the project lock for automatic `request_sync`
      and `retry_sync`, and before an automatic run's scheduling write.
- [x] `link_youtube` for a Short: refuse while a sync runs, release the slot with the link.
- [x] Web: prefer the publish review whose `final_review_id` is the current final (cover from the
      final); show `UploadedForm` with the guide, in place of the send form for a hand upload.
      A link saved without a time needs a way to add the time later (the form hides once linked).

## How to verify

API: pytest for a hand-pushed and a hand-linked Short through approve, lock, tick and claim.
Web: vitest for the publish-only package and the link form. Then the checks in CLAUDE.md.

## Notes

- `claim` was refused on 2026-11-22 (nine active claims overlap). The owner answered in the
  session, 2026-11-22: 「可以強制認領」. Claimed with `--force`; those nine tasks and the two open
  PRs below are untouched.
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

### Decisions while implementing

- `by_hand` is only marked when no upload package was approved at link time (or the Short is
  hand-pushed). A link after approval stays on the calendar: `vps.action("record")` calls
  `link_youtube` too, and SHORTS.md's fallback for the claim pastes an address after approval.
- Added to the scope, none of them claimed by another task: `video_youtube/vps.py` (refuses to
  upload a second copy) and the link form with its copy. The copy is JSON beside the component's
  lib file because the five admin.json files are bound by the duration receipt; that is also why
  the form is its own component and not `UploadedForm`, whose help promises the site schedules.
- The consent text is unchanged on purpose: its SHA-256 binds the owner's consent, and a new
  wording would void it.

### Known limits

- Worker-made Shorts stay automatic. The owner was asked in passing whether every Short should
  be manual and has not said so.
- A worker's Short linked by hand before approval loses the link form once its package is
  approved: the page cannot tell it from a claimed one (`ProjectOut` has no such field).
- A linked Short with no time and no approved package still reads `making` on the Shorts tab.
- The calendar's picker still lists hand uploads; choosing one is refused with the reason.
- A slot already `scheduled` on YouTube is left alone; the owner recalls it.
- Local tests ran on SQLite only (Docker in WSL needs elevation); PostgreSQL runs in CI.
