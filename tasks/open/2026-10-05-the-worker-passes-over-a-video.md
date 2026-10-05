---
id: 2026-10-05-the-worker-passes-over-a-video
title: The worker passes over a video its own STOP file holds instead of ending the round on it
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T01:50:50Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
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

- [ ] A video whose own work directory holds a STOP file is not moved by the worker (no stage
      runs for it), and the round goes on to the next video.
- [ ] Bookkeeping that the owner starts (drop, retry) still reaches a held video, or the ticket's
      Notes say why it should not.
- [ ] The global STOP file keeps its meaning: `auto` stops between units.

## Steps

- [ ] Decide with the code which units a held video skips (every `move()`, or only units that run
      a stage command), and write it in the ticket's Notes.
- [ ] Skip held videos in `stepUnit()`; a test with two videos, the older one held at "narration
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
