---
id: 2026-10-06-a-storyboard-with-many-kept-pictures
title: A storyboard with many kept pictures can pass the payload limit after its remarks are left out
status: done
priority: P3
area: tools
owner: claude-opus-5-5-kept-board
claimed_at: 2026-10-07T11:36:56Z
created_at: 2026-10-06T16:23:06Z
completed_at: 2026-10-07T13:20:41Z
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

2026-10-07 (claude-opus-5-5-kept-board), `tools/video/review/sync.mjs`:

- `storyboardSubmission` sends a kept shot's remarks once, on `payload.accepted[].problems`
  (the card prefers that list). The shot's own `judge.problems` goes up empty, keeping its
  score. The exception is a kept shot whose list entry has no remark: then the shot's verdict
  still carries what the judge said, since the card falls back to it.
- `fitPayload` has one more step, for a storyboard alone. If the payload is still past the
  budget with every remark out, `payload.accepted` stays home too. Every kept shot is still
  marked (`accepted: true`, its score), which is what the card and the server's check
  (`storyboard_check_passed`) read. The summary ends with a note saying where the remarks are
  (`KEPT_LIST_LEFT_OUT`), cut to make room so the note stays whole. A cut keeps its
  `accepted_pictures`, since that list is the only place it names its kept pictures.
- A board shaped like the ticket's goes up: 200 shots, 165-character ids, 450-character
  prompts, all kept. The reader's own board was 270,537 bytes and was not kept; the test's
  board was refused at 274,137 bytes on ea110f00 and now goes up at 216,723, against 213,120
  for the same board with nothing kept.
- What stays: a kept shot still carries `"accepted": true` (18 bytes in the server's measure),
  and the board's score goes null when every shot is kept. So a board within about 18 bytes a
  kept shot of 262,144 with nothing kept is still refused once every shot is kept; review-push
  then exits 1 and says how large it is. No video comes near that today (a brand story has
  85-100 shots), and the marker is what the card and `storyboard_check_passed` read.
- Tests (`sync.test.mjs`):
  - that board end to end;
  - a unit case of the last step: the list dropped, the note kept whole at the 500-character
    limit, and a cut's list kept;
  - the kept shot whose list has no remark;
  - the two tests that pinned the remarks on the shot's verdict.
- Mutations, each failing a test:
  - no last step;
  - the last step at the limit instead of the budget;
  - the note cut with the summary;
  - no note;
  - remarks sent twice;
  - no fallback for a list entry with no remark;
  - a cut dropping its list.
- `cd apps/web && npx vitest run components/admin-video-kept-pictures.test.tsx` passes 43/43.
- Ride-along: `2026-10-07-the-final-gate-s-owner-exit-names`. `qualityCheck`'s owner exit now
  names the token or a site setting and points at the failing item and `review/qa.json`.
  A test covers it: the policy route answers 503 `provider_unavailable`, and the push exits 3
  with the item's "尚未設定 Jev API 金鑰" printed.
- Review (2026-10-07, two lenses, each finding verified):
  - Consumers: the card, `storyboard_check_passed`, `ReviewIn`, review-pull, flow.mjs
    (`storyboardGate`, `fixPrompts`, `acceptBestPictures`, `gate`) and the other tools read a
    kept shot through `shots[].accepted`, never through the list or the shot's remarks, so
    nothing behaves differently. The docstrings of `fitPayload` and `withKeptRemarks` now
    describe the last step; `docs/videos/ILLUSTRATED.md`, outside this scope, is
    `2026-10-07-illustrated-md-still-says-a-storyboard`.
  - Fixed, nit: the comment said a board with every shot kept costs no more than one with none
    (the 18-byte marker above), and the DoD tick is read with that window.
  - Fixed, nit: the last step added its note even when no kept shot had a remark (a shot kept
    "below the bar" has `accepted_with_problems: []`). The note, the two cut steps and the
    "remarks left out" words of the size error now need a remark to exist
    (`keptRemarksIn`), so review-push no longer says remarks were cut or left out when there
    were none. The list still goes. A unit case covers it, and four mutations of the condition
    each fail it.
  - Fixed, nit: the `withKeptRemarks` docstring and a test comment described the old builder;
    the byte counts in these notes and the test comment were the reader's board, not the test's.
  - Not defects: the ride-along's task file is closed with this task, as the dub ticket's was.
- Duration re-bind (2026-10-07, independent reviewer `claude-pr-review-kept-board`): PASS,
  duration-only, committed as 0c583909. `submission()` and `reviewPush` are byte-identical, a
  final cut's body and bytes are the same for every input (a differential run of 4,000 random
  final payloads, 16,000 other gates and 4,000 storyboards), and each shot's `seconds` still
  comes from timeline.json.
