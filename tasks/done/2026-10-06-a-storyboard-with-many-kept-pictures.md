---
id: 2026-10-06-a-storyboard-with-many-kept-pictures
title: A storyboard with many kept pictures can pass the payload limit after its remarks are left out
status: done
priority: P3
area: tools
owner: claude-opus-5-5-storyboard
claimed_at: 2026-10-07T04:45:55Z
created_at: 2026-10-06T16:23:06Z
completed_at: 2026-10-07T05:21:37Z
branch: claude/happy-carson-c1hy91
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

- [x] A storyboard that goes up with no kept pictures also goes up when all its shots are
      kept.
- [x] A kept shot's remarks are sent once on the storyboard.

## Steps

- [x] Send the remarks only in `payload.accepted[].problems` (the card prefers that list,
      `admin-video-review-card.tsx` around line 471), or add a last step that drops the
      per-entry "left out" line and the repeated ids. The card can rely on
      `shots[].accepted`.
- [x] A test in `sync.test.mjs` with the input above.

## How to verify

```bash
node --test tools/video/review/sync.test.mjs
cd apps/web && npx vitest run components/admin-video-kept-pictures.test.tsx
```

`sync.mjs` and `sync.test.mjs` are bound in the duration review receipt, so the change
needs an independent re-bind.

## Notes

Found while verifying `4d296e304` (PR #1344). The scratch reproduction was not kept.
- Claimed with `--force` on 2026-10-07: the tool refused because #1355 (then open) declared
  `tools/video/review` in its scope, but #1355 never changed `sync.mjs` or `sync.test.mjs`
  (checked with `git diff --stat` against its merge), so the overlap was declared scope only.
- Done 2026-10-07 by claude-opus-5-5-storyboard. On a storyboard `withKeptRemarks` now sends a
  kept shot's remarks once: on `payload.accepted` when the list names the shot, and the shot's
  own `judge.problems` goes up empty (its `overall` stays). A kept shot the list does not name
  keeps its own remarks, cut the same way. The final cut is unchanged.
- The last step (no line to spend) was first "drop the list, put the 'left out' line on each
  kept shot". An independent review measured that on the producer's own shape (file hashes,
  `expected_shots`, the sheet list of a board past 48 files): the ticket's input still failed,
  at 266,931 bytes against 247,328 with nothing kept, because each kept shot still cost about
  98 bytes more than the same shot passed by the judge. So the last step now sends a kept shot
  as the site needs it and no more: `accepted: true`, its score, no remarks and no
  `needs_review` (never true on a kept shot). The site takes a kept shot without a verdict
  (`apps/api/app/video_automation/settings.py`, the storyboard check `continue`s on
  `accepted`), and the card shows its score (`admin-video-review-card.tsx`). The list goes but
  for an entry no kept shot stands for, and the summary ends once with
  "保留鏡頭的 judge 意見因審核資料的大小上限略去，全文在 keyframes/manifest.json". A kept shot
  then costs less than the same shot not kept, so DoD 1 holds whatever the board's size.
- Tests: "a storyboard that goes up with nothing kept goes up with every shot kept" builds the
  ticket's input through `review-push` with the prompt sized so the board with nothing kept is
  within 2 KB of the limit, and fails against both earlier versions of `sync.mjs`; "each kept
  shot's remarks go up once" fails against the version before this ticket. `node --test
  "tools/video/review/*.test.mjs"` 178 pass; the card's two vitest files 50 pass.
