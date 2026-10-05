---
id: 2026-10-05-the-worker-passes-over-a-video
title: The worker passes over a video its own STOP file holds instead of ending the round on it
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-flow-stop-and-repackage
claimed_at: 2026-10-05T12:25:17Z
created_at: 2026-10-05T01:50:50Z
completed_at:
branch: claude/flow-stop-and-repackage
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/DESIGN.md
---

# The worker passes over a video its own STOP file holds instead of ending the round on it

## Why

A STOP file can hold one video (`<work base>/<slug>/STOP`) as well as the whole worker
(`<work base>/STOP`). `auto` checks only the work base between units; `stepUnit()` in
`tools/video/automation/flow.mjs` moves the oldest movable video without looking at its own STOP
file. Its stages then see the STOP file and stop at once. Since 2026-10-05 `tts` and
`check-audio` exit 6 there and the worker waits for the next run with `this.later`, which ends the
round (`halted`). So a held video that is first in line ends every round after one unit, and no
later video moves until someone removes the file. Before that change those stages returned 0:
the worker repeated `tts` on the held video for every unit of the round, or sent a narration or a
dub whose check had not run, and moved on.

Per-video STOP files exist in practice: the renewal handoff keeps one in the canonical work
directory after activation until the readback is verified
(`tools/video/review/renewal-handoff.mjs`), and `tidy` already treats such a video as held.

## Definition of done

- [x] A video whose own work directory holds a STOP file is not moved by the worker (no stage
      runs for it), and the round goes on to the next video.
- [x] Bookkeeping that the owner starts (drop, retry) still reaches a held video, or the ticket's
      Notes say why it should not.
- [x] The global STOP file keeps its meaning: `auto` stops between units.

## Steps

- [x] Decide with the code which units a held video skips (every `move()`, or only units that run
      a stage command), and write it in the ticket's Notes.
- [x] Skip held videos in `stepUnit()`; a test with two videos, the older one held at "narration
      synthesized", shows the newer one moving in the same round and the older one untouched.

## How to verify

`node --test tools/video/automation/automation.test.mjs`. `flow.mjs` and `automation.test.mjs`
are bound to the duration receipt: open the PR as a draft and leave
`node tools/video/long-form/cli.mjs check` to an independent reviewer.

## Notes

- Found while doing 2026-10-04-audio-stage-incomplete-exits (exit 6 for `tts` and `check-audio`).
  That change follows the rule that a STOP is a later-retry, never a block; this ticket keeps
  that rule and only stops a held video from taking the whole round.
- `docs/videos/DESIGN.md` says a STOP file "in the work directory or the one above it" stops long
  stages after their current piece; the status command prints the same. Neither says what the
  worker does with a held video; write it down there once decided (add `docs/videos/DESIGN.md`,
  also receipt-bound, to the scope).
- Done 2026-10-05 (claude-opus-5-5-flow-stop-and-repackage, branch
  `claude/flow-stop-and-repackage`, together with 2026-10-05-re-package-when-the-language-choice
  and 2026-10-05-a-narration-retake-a-stop-file, which change the same two files).
- Decision: a held video skips every `move()`, not only the units that run a stage. `move()` is
  `advance()` then `languages()`, and nearly every branch of both runs a command (tts, check-audio,
  captions, package, i18n-sheet, dub, review-push) or a paid model stage; the few that do not
  (waiting on a review) would only return null. The check is the video's own
  `<workdir>/STOP` alone, not `stopRequested()`, which also reads the work base: the work base's
  STOP stays `auto`'s, between units (`tools/video/automation/cli.test.mjs` "STOP found; stopping
  between units" still passes).
- Bookkeeping is unchanged: the owner's drop reaches a held video (the new test drops one); a
  retry still waits until STOP is removed, as `bookkeeping()` (`stopRequested`) and
  `client.mjs` ("STOP prevents this owner retry") already refuse it on purpose, so a retry cannot
  start paid stages the owner held. A pasted YouTube id, a blocked-reason report and a finished
  compilation's notice are bookkeeping without a stage and still reach it. Discussion threads
  (`discussStep`) answer the owner's own lines and were left as they are.
- `docs/videos/DESIGN.md` (added to the scope) now says the worker passes over such a video, a
  drop still reaches it, and a retry waits for the file to go.
- Test: "a video its own STOP file holds is passed over: …" in `automation.test.mjs` (the older
  video back at "narration synthesized" with `<workdir>/STOP`, its tts answering exit 6 as the
  real one does; the newer one moves in the same round, `halted` stays false, no command runs and
  auto.json is byte for byte the same; with the file removed it moves; held again, the drop
  reaches it). Removing the skip turns this test red.
