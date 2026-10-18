---
id: 2026-10-07-illustrated-md-still-says-a-storyboard
title: ILLUSTRATED.md still says a storyboard sends a kept shot's remarks twice and always lists them
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-07T12:28:25Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ILLUSTRATED.md
---

# ILLUSTRATED.md still says a storyboard sends a kept shot's remarks twice and always lists them

## Why

`2026-10-06-a-storyboard-with-many-kept-pictures` changed how `tools/video/review/sync.mjs`
sends a storyboard with kept pictures. A kept shot's judge remarks now go up once, on
`payload.accepted[].problems`. The shot's own `judge.problems` goes up empty, unless its list
entry has no remark. There is also a last step in `fitPayload`: a storyboard still past the
240,000-byte budget with every remark left out goes up without `payload.accepted`. Each kept
shot is still marked `accepted: true` with its score, and the summary ends with
「（保留鏡頭的 judge 意見因審核資料的大小上限略去，全文在 keyframes/manifest.json）」.

`docs/videos/ILLUSTRATED.md` §同日後續 (the rows added with #1344) still describes the old
behaviour:

- the 「分鏡關卡自己過」 row says the storyboard always attaches
  `payload.accepted = [{id, overall, problems}]`;
- the 「payload 不會被站台退件」 row says a storyboard carries the remarks twice (on `accepted`
  and in each kept shot's `judge.problems`), says steps (2) and (3) cut and then empty the
  shot's `judge.problems`, and goes straight from "every remark out" to "not sent".

No reader breaks today. The card falls back to `shots[].accepted`, and the server's
`storyboard_check_passed` never reads the list. Someone writing a new reader from this spec,
though, would take the list as always present.

## Definition of done

- [ ] A reader of the section learns what `sync.mjs` does now: the remarks go once, on
  `accepted`; the shot's verdict carries them only when its list entry has none; and the last
  storyboard step leaves `accepted` out and appends the summary note (only when the judge had
  remarks), while a cut keeps `accepted_pictures`.

## Steps

- [ ] The section is a dated decision log: each row records what changed that day, and a later
  change gets its own dated follow-up rather than a rewrite of an earlier row (#1344 added
  「同日後續」 and left rows 444-445 as they were). Add a short 2026-10-07 follow-up under the
  10-06 section with the three points above, without rewriting rows 444 and 459. Read
  `fitPayload` and `storyboardSubmission` in `tools/video/review/sync.mjs` first.

## How to verify

Read the rows against `fitPayload`, `withKeptRemarks` and `storyboardSubmission` in
`tools/video/review/sync.mjs`, and against the tests "a storyboard that goes up with nothing kept
goes up with every shot kept" and "a payload past the site's limit is never posted" in
`tools/video/review/sync.test.mjs`.

## Notes

- Found by the review of `2026-10-06-a-storyboard-with-many-kept-pictures` (2026-10-07), as a
  nit outside that task's scope (`sync.mjs`, `sync.test.mjs`).
- `2026-10-04-still-shot-camera-moves-travel-in` also edits this file (its §成片大小), so the
  two cannot be claimed at the same time.
