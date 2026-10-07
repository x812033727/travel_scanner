---
id: 2026-10-07-a-dub-retake-that-exits-4
title: A dub retake that exits 4 spends its retake round although it made no take
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T07:21:30Z
completed_at:
branch:
depends_on:
  - 2026-10-06-tts-and-a-narration-retake-that
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# A dub retake that exits 4 spends its retake round although it made no take

## Why

`tools/video/automation/flow.mjs` `makeDub` counts a dub retake round (`rounds.retakes += 1`)
before it runs `dub --redo`. A redo that exits 4 (the month's speech characters spent, the speech
routes' rate limit, a vendor away) is deferred, and the next visit counts another round. The same
trouble repeated, with nothing retaken, can therefore spend `MAX_DUB_RETAKE_ROUNDS` and move the
language on to its reword or shorten rounds, or give the dub up, when the lines only needed a
retake.

The narration's retake had the same pattern. `2026-10-06-tts-and-a-narration-retake-that` fixed it
there: `retakeStopped`'s `giveBack` returns the round when the retake made no take. The dub path is
older than that ticket and was outside its scope.

## Definition of done

- [ ] A dub retake that exits 4 without making a take does not count as a retake round; one that
  made takes keeps its round, as for the narration.

## Steps

- [ ] Give the round back in `makeDub` when the redo that exited 4 changed no take of that locale.
- [ ] A test on the dub fixture: the budget is spent for three rounds, the retake rounds stay
  where they were, and nothing is reworded.

## How to verify

`node --test tools/video/automation/automation.test.mjs`. `flow.mjs` and `automation.test.mjs` are
bound by the duration review, so they need an independent rebind.

## Notes

- Found by the review of `2026-10-06-tts-and-a-narration-retake-that` (2026-10-07).
