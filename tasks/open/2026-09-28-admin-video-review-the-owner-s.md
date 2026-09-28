---
id: 2026-09-28-admin-video-review-the-owner-s
title: Admin video review: the owner's final-cut approvals did not register on 2026-09-28
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-28T09:46:06Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
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
      2026-09-28; any approved by mistake are reported to the owner.
- [ ] If a POST failed there, a failed decision shows an error the owner cannot miss.

## Steps

- [ ] Check the admin audit log (`video_review_approved` for those three review ids) and the API
      access log for the decision POSTs between 09:00 and 09:45 UTC on 2026-09-28: did they
      arrive, and what did they return?
- [ ] Rule out the page listing other projects' final cards (another pipeline's videos were in
      review the same day) and the owner approving those instead.
- [ ] If the POST failed, see why the card's error line (`decideError`) went unnoticed; a failed
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
