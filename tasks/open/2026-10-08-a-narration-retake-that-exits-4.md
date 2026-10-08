---
id: 2026-10-08-a-narration-retake-that-exits-4
title: A narration retake that exits 4 gives its round back after a paid answer whose bytes did not change
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-08T02:24:32Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# A narration retake that exits 4 gives its round back after a paid answer whose bytes did not change

## Why

On main (#1364, 2026-10-06-tts-and-a-narration-retake-that), a narration retake that exits 4 (a
rate limit, a service away) defers the video, and gives its `retakes` round back when no
flagged take's bytes changed (`changedTakes` against timeline.json, `retakeStopped` with
`giveBack`). A request that was answered and paid for, but whose voice sent back the same
bytes, then also gets its round back. If a later request of the same retake meets a 429 that
outlasts the client's waits, each deferral runs the same round again and buys the same line
again, once per deferral for as long as the limit lasts, and the retakes never run out.

Main's dub ticket (2026-10-07-a-dub-retake-that-exits-4) names this limit and accepts it
because a synthesized voice does not repeat its bytes, so this is P3. #1361 decided by tts's own
progress line instead (`FINISHED_REQUEST`: `<request>[ [speaker]]: N of M lines retaken`), so a
request that was answered kept the round spent; that was dropped when #1361 was rebased onto
main (2026-10-08). Found by the overlap comparison of the two PRs.

## Definition of done

- [ ] A retake that exits 4 after at least one of its requests was answered keeps its round,
      whatever bytes came back; one that answered nothing still gives it back.

## Steps

- [ ] flow.mjs: read the redo's output for a finished request before giving the round back
      (pass `out: redo.out` from `narration()`'s exit-4 call to `retakeStopped`).
- [ ] automation.test.mjs: a retake answered with the same bytes, then a rate limit, keeps its
      round, and the retakes run out.
- [ ] Decide whether `makeDub`'s byte-based `flaggedTakes()` needs the same.
- [ ] Rebind the duration receipt (flow.mjs and automation.test.mjs are bound).

## How to verify

`node --test tools/video/automation/automation.test.mjs`; `node tools/video/long-form/cli.mjs check`.

## Notes

#1361's version: commit f707378a9 (`FINISHED_REQUEST`, the test "a retake that was answered but
exits 4 keeps its round even when the voice gave the same bytes back").
