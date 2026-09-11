---
id: 2026-09-11-seoul-day2-live-requery
title: Re-query the live Seoul Day 2 route after the #387 release
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-11T15:47:18Z
completed_at:
branch:
depends_on: []
scope:
  - docs/seoul-day2-transport-ux.md
---

# Re-query the live Seoul Day 2 route after the #387 release

## Why

`2026-09-10-seoul-day2-transport-ux` let Korean transit fall back to the configured Google key
when ODsay has none, and made the queried boarding, transfer and walking steps the main route
view. It merged as PR #387 (merge commit `a044e4c`) on 2026-09-10. Its last step was never
recorded: once the release is live, re-query the real Seoul Day 2 itinerary that exposed the
problem and confirm what it now shows.

That task was closed on 2026-09-11 so its 27 paths stop blocking other work. This is the part
it left, and it needs only the document that records the result.

## Definition of done

- [ ] Production is confirmed to run a build that contains `a044e4c`.
- [ ] The live Day 2 transit route is re-queried, and the returned steps and preview warning
      are checked before anything is applied.
- [ ] The outcome, or the reason it could not be done, is appended to
      `docs/seoul-day2-transport-ux.md`.

## Steps

- [ ] Confirm the deployed revision.
- [ ] Re-query Day 2 in the live planner and compare it with what the document describes.
- [ ] Record the result in the document.

## How to verify

`docs/seoul-day2-transport-ux.md` ends with the check itself: after deployment, re-query the
transit route and look at the actual returned steps and the preview warning before applying.

## Notes

- Each query is metered Google Routes usage on the owner's real trip. The original task used
  two bounded requests in total; stay within that, and change nothing outside Day 2.
- The original task's notes asked to keep it open until this verification was recorded. It was
  closed anyway, because on this board a merged pull request closes its task, and the
  verification moved here instead of holding 27 paths.
