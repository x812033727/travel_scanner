---
id: 2026-10-05-dub-exits-incomplete-when-a-stop
title: dub exits incomplete when a STOP file ends it, like tts and check-audio
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T01:47:46Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# dub exits incomplete when a STOP file ends it, like tts and check-audio

## Why

`dub` synthesizes a dubbed track request by request and checks for a STOP file before each one.
When it finds one it prints "stopped by the STOP file … rerun to continue" and returns exit 0
(`tools/video/dubs/cli.mjs`, the loop over `pending`), before the dub's timeline, fit report and
track are written. The worker's `makeDub` (`tools/video/automation/flow.mjs`) reads exit 0 as
"the track is made" and goes straight on to `check-audio --locale`, which then hears a track that
was never assembled, or the previous one. Since 2026-10-05 `tts` and `check-audio` return exit 6
(`EXIT.incomplete` in `tools/video/cli.mjs`) in the same situation and the worker waits for the
next run; `dub` is the one audio stage left on the old contract.

## Definition of done

- [ ] A `dub` run that a STOP file ends before its track is assembled exits 6, keeps every take it
      paid for in its cache, and writes no timeline, fit report or track that looks current.
- [ ] The worker treats a `dub` or `dub --redo` exit 6 as "the next run continues" (`this.later`),
      never as a made track, a given-up language or a blocked video.
- [ ] A rerun without the STOP file finishes the track and buys only the requests that were left.

## Steps

- [ ] Offline fixture in `dubs.test.mjs`: STOP before the first and between two requests (the fake
      server writes the STOP file), exit 6, cache kept, rerun buys only the rest.
- [ ] Return `EXIT.incomplete` from the STOP branch in `tools/video/dubs/cli.mjs`.
- [ ] In `makeDub`, map `made.code` and `redo.code` 6 to `this.later`, with a test in
      `automation.test.mjs` next to "a STOP file that ends a dub's check defers the language".

## How to verify

`node --test tools/video/dubs/dubs.test.mjs tools/video/automation/automation.test.mjs`; mock
providers only, no paid calls. `node tools/video/long-form/cli.mjs check` will list
`dubs.test.mjs`, `flow.mjs` and `automation.test.mjs` as receipt-bound: open the PR as a draft
and leave the receipt to an independent reviewer.

## Notes

- Split out of 2026-10-04-audio-stage-incomplete-exits, which moved `tts` and `check-audio` to
  exit 6 and taught the worker to wait on it (narration, retakes, and the dub's check, where a
  stopped check is heard again next run through `state.languages[locale].check_stopped`).
- The same exit-0-on-STOP pattern is in `render`, `assemble`, `compile`, `keyframes` and `clips`
  (each prints "stopped by the STOP file … rerun to continue" and returns `EXIT.ok`); the worker
  then says the step is done ("<stage> done" from `media()`, "frames rendered", "video
  assembled"). Status keeps those steps undone, so the next run repeats them, but the line and the
  report are wrong. Worth the same audit once `dub` has the pattern.
