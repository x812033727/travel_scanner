---
id: 2026-10-21-an-owner-s-gate-decision-lands
title: An owner's gate decision lands on a review the worker already replaced
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-21T00:36:17Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/web/components/admin-video-reviews.tsx
---

# An owner's gate decision lands on a review the worker already replaced

## Why

Between 2026-10-18 and 10-20 the owner approved a gate on /admin/videos four times and
`review-pull` still read it as pending: A42 audio, C21 audio, B26 look (twice). Each time the
owner had to press again. In the audio cases the gate's history showed a row `superseded` at
the same second as the new `pending` one, so the worker re-pushed the gate while the page
still showed the old row, and the owner's click went to the replaced row. In the B26 case the
second character's look review had never been pushed at all (`look: cartoonist = A; waiting
for reader-kid`, one `look` row only); `review-push --gate look` by hand created it.

## Definition of done

- [ ] A decision on a superseded review is refused with a message that says the review was
      replaced and the page should be reloaded, instead of silently recording nothing.
- [ ] The video page refreshes a gate card when its review is superseded.
- [ ] A multi-character look gate pushes every character's review, or says which one is missing.

## Steps

- [ ] Reproduce: push a gate, push it again, decide on the first id.
- [ ] Fix the service and the card.

## How to verify

The API test for deciding a superseded review, and a web test for the card.

## Notes

- Seen on story-adapt-a4-paper-size, story-adapt-dolby-licensing and
  story-adapt-doraemon-after-fujiko (see 2026-10-16-adapt-the-reference-channel-s-five).
