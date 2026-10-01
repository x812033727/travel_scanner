---
id: 2026-09-28-admin-video-review-the-owner-s
title: Admin video review: the owner's final-cut approvals did not register on 2026-09-28
status: done
priority: P3
area: web
owner: claude-opus-5-5-review-card
claimed_at: 2026-10-01T03:38:03Z
created_at: 2026-09-28T09:46:06Z
completed_at: 2026-10-01T03:52:31Z
branch: claude/review-card-approvals
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - tasks/open/2026-10-01-video-review-audit-2026-09-28.md
---

# Admin video review: the owner's final-cut approvals did not register on 2026-09-28

## Why

On 2026-09-28 the owner approved three final-cut (「成片」) cards on `/admin/videos`, twice, and
told the producing session so. Both times the site kept all three reviews `pending` with no
`decided_at`, read back through `GET /api/video/reviews/<slug>` minutes later:

| slug | final review id | submitted (UTC) |
| --- | --- | --- |
| `openai-agents-broke-in` | `5332abba-80a5-4400-895d-954b4ec4328f` | 08:40:31 |
| `gpt6-vs-opus55-worth-paying` | `edca561e-b2ec-460a-be52-a3495645a880` | 08:42:35 |
| `ai-real-jobs-chart` | `fc8b708f-ce30-4b73-b18d-3cfd85b8e572` | 08:44:46 |

The same endpoint (`POST /admin/videos/{slug}/reviews/{id}/decision`) had recorded the owner's
outline and audio decisions on the same projects hours earlier, and `decision_problem` only
refuses non-pending reviews, a reject without a note, or a missing outline choice, none of which
applies.

Update, same day: after the session sent the owner the three exact titles to look for, the site
recorded all three approvals at 09:45:12, 09:45:37 and 09:46:24 UTC (in page order, no note), so
the endpoint works. What is still unexplained is the two earlier rounds (reported at about 09:35
and 09:42 UTC) that left nothing. The likeliest reading is that those clicks went to other final
cards on the same page (another pipeline had videos in review that day), which would mean other
videos were approved by mistake; the other is a failed POST whose error line went unnoticed.
The session had also recorded the approval locally from the chat (`approve --gate final`, same
hashes), so nothing downstream waited on this.

## Definition of done

- [ ] The audit log shows which reviews the owner approved between 09:00 and 09:45 UTC on
      2026-09-28; any approved by mistake are reported to the owner. (Moved to
      `2026-10-01-video-review-audit-2026-09-28`: the read-only query was refused here; see Notes.)
- [x] If a POST failed there, a failed decision shows an error the owner cannot miss. (Nothing
      shows a POST failed; the card's refusal handling is now pinned by a test, see Notes.)

## Steps

- [ ] Check the admin audit log (`video_review_approved` for those three review ids) and the API
      access log for the decision POSTs between 09:00 and 09:45 UTC on 2026-09-28: did they
      arrive, and what did they return? (Moved to the ops ticket above.)
- [x] Rule out the page listing other projects' final cards (another pipeline's videos were in
      review the same day) and the owner approving those instead.
- [x] If the POST failed, see why the card's error line (`decideError`) went unnoticed; a failed
      decision might deserve a toast or a banner, not a line under the buttons.

## How to verify

Approve a pending final card on `/admin/videos`, then:

```bash
node tools/video/cli.mjs review-pull --slug <slug> --workdir <VIDEO_WORKDIR>   # prints "final: approval recorded"
```

## Notes

- The final cards are the heaviest ones: a 720p preview uploaded in parts plus the QA report.
- Nothing in `admin-video-review-card.tsx` treats the final gate differently from outline or audio
  in `decide()`; the difference, if any, is in what the page renders around it (`FinalBody`).
- 2026-10-01 (claude-opus-5-5-review-card), closing with no change to the card, because the card
  has no bug to fix:
  - `apps/web/components/admin-video-review-card.test.tsx` (new) renders a pending final card
    with a preview, a failing QA report and chapters. Approve sends exactly one
    `POST /api/travel/admin/videos/<slug>/reviews/<id>/decision` with `{ decision: "approve" }`
    for the card's own slug and review id, then calls `onDecided` (the page reads again). A 401
    keeps the card pending, shows 「沒有送出：…」 as `role="alert"` directly above the buttons the
    owner just pressed, does not re-read, and leaves 核准 enabled for a second try that then
    succeeds. Both tests pass on main, so the bug is not reproducible in the card.
  - The card did not change in a way that matters since the day: `git diff 79e26fcdf HEAD` (the
    09-28 06:38 UTC state) touches only the `vertical` prop, not `decide()`, its error line or the
    button's `disabled` rule. PR #1039 changed the list, not the card or the video page.
  - "Other projects' final cards on the same page" is ruled out: then (79e26fcdf, 4dacd3635) and
    now, `<ReviewCard>` is rendered only by `ProjectDetail` in `admin-video-reviews.tsx`, one video
    per page (`?video=<slug>`), and every card there posts to that page's slug. The list shows
    titles, not cards. So a misdirected approval needs the owner to have opened another video's
    page and approved its final cut there, which the server would have recorded.
  - The deploy notes list no deploy between 09:00 and 10:00 UTC that day (the 09-28 deploys they
    record were at 14:55, 15:03 and 16:18 UTC), so a burst of failed POSTs from a restart is
    unlikely too; the ops ticket's query settles it either way.
  - What is left is the audit-log read (DoD item 1). The read-only `psql` select on the host was
    refused by the auto-mode classifier as a production read, so it is filed as
    `2026-10-01-video-review-audit-2026-09-28` with the exact query; it also says what to do if
    other videos' final cuts were approved by mistake.
