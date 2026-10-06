---
id: 2026-10-06-a-storyboard-with-many-kept-pictures
title: A storyboard with many kept pictures can pass the payload limit after its remarks are left out
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-06T16:23:06Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# A storyboard with many kept pictures can pass the payload limit after its remarks are left out

## Why

`tools/video/review/sync.mjs` `fitPayload` shortens a review that is over 240,000 bytes by
cutting the judge's remarks on kept pictures to two lines each, and then leaving them out
(`FEWER_REMARK_LINES = [2, 0]`). After the last step, each kept shot on a storyboard still
costs about 300 bytes. Its id appears again in `payload.accepted` along with an 85-byte
"left out" line, plus `overall` and `"accepted": true`. As a result, keeping pictures can
stop a board that would go up if nothing were kept. A reader verifying PR #1344 found this
input: 200 shots with 165-character ids and 450-character prompts, all kept, each with one
short remark. `review-push` exits 1 with "payload is 270537 bytes … even with the judge's
remarks on the kept pictures left out; nothing was sent". The same board with nothing kept
is 210,720 bytes and goes up. No real video is that large today (a brand story has 85–100
shots), so this is P3.

On a storyboard, a kept shot's remarks also travel twice, in `shots[].judge.problems` and
in `payload.accepted[].problems`, until the last step empties the shot's copy. That spends
half the budget.

## Definition of done

- [ ] A storyboard that goes up with no kept pictures also goes up when all its shots are
      kept.
- [ ] A kept shot's remarks are sent once on the storyboard.

## Steps

- [ ] Send the remarks only in `payload.accepted[].problems` (the card prefers that list,
      `admin-video-review-card.tsx` around line 471), or add a last step that drops the
      per-entry "left out" line and the repeated ids. The card can rely on
      `shots[].accepted`.
- [ ] A test in `sync.test.mjs` with the input above.

## How to verify

```bash
node --test tools/video/review/sync.test.mjs
cd apps/web && npx vitest run components/admin-video-kept-pictures.test.tsx
```

`sync.mjs` and `sync.test.mjs` are bound in the duration review receipt, so the change
needs an independent re-bind.

## Notes

Found while verifying `4d296e304` (PR #1344). The scratch reproduction was not kept.
