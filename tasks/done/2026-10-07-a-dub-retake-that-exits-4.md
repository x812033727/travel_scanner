---
id: 2026-10-07-a-dub-retake-that-exits-4
title: A dub retake that exits 4 spends its retake round although it made no take
status: done
priority: P3
area: tools
owner: claude-opus-5-5-dub-retake
claimed_at: 2026-10-07T10:30:07Z
created_at: 2026-10-07T07:21:30Z
completed_at: 2026-10-07T11:40:07Z
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

- [x] A dub retake that exits 4 without making a take does not count as a retake round; one that
  made takes keeps its round, as for the narration.

## Steps

- [x] Give the round back in `makeDub` when the redo that exited 4 changed no take of that locale.
- [x] A test on the dub fixture: the budget is spent for three rounds, the retake rounds stay
  where they were, and nothing is reworded.

## How to verify

`node --test tools/video/automation/automation.test.mjs`. `flow.mjs` and `automation.test.mjs` are
bound by the duration review, so they need an independent rebind.

## Notes

- Found by the review of `2026-10-06-tts-and-a-narration-retake-that` (2026-10-07).
- 2026-10-07 (claude-opus-5-5-dub-retake). `flow.mjs` `makeDub`:
  - `flaggedTakes()` hashes each flagged line's `dubs/<locale>/audio/<id>.wav` before the
    retake, since a retake rewrites the take of every line it makes. A retake that exits 4 with
    none of them changed gives its round back; one that made a take keeps it, as for the
    narration (`retakeStopped`'s `giveBack`).
  - Found while testing this, and fixed here since it is the same path: a visit that ended
    after `dub` wrote a track, other than by Jev passing it, could leave the track reading as
    heard. `dubsStatus` reads a track as current once its words and voice are, so the next
    visit skipped the locale and sent the language batch with the flagged lines neither retaken
    nor heard again: a dub Jev had flagged went to the owner for upload. That covered:
    - a retake or a check that exited 4;
    - the plain `dub` exiting 4 after a retake that no longer fit;
    - a rewording or shortening answer that could not be used;
    - a block and the owner's retry.
    Only a STOP and a lost answer used to set the mark (`check_stopped`). `makeDub` now sets it
    at the start of every visit. Only the two final endings clear it: Jev passing the track
    (the rounds deleted) and `giveUpDub`. `stopped`, `lost` and `unfinished` no longer set it
    themselves. Every exit 4 goes through `unfinished()`, whose deferral keeps its own kind
    (`dub`, or `check-audio` for the check). The language step's comment says what leaves a
    track unheard.
  - The JSDoc says what exit 4 and a STOP do now: they defer this video only. This is
    `2026-10-06-makedub-s-comment-still-says-a`, which asked to ride along with the next change
    to `flow.mjs`.
- Tests (`automation.test.mjs`), each failing on the old code:
  - three budget-spent retakes give the round back each time, with nothing reworded and no
    batch, then the retake runs and the dub is made after one retake;
  - a retake that wrote the flagged line's take before it exited 4 keeps its round;
  - a vendor that keeps failing the retake blocks at the seventh try as `deferred:dub`, with no
    retake spent;
  - a check that exits 4 leaves the track unheard, and the next visit runs `dub` and the check
    instead of sending the batch;
  - a check a vendor keeps failing blocks as `deferred:check-audio`;
  - from the review, a visit that ends with an unusable rewording answer, or an unusable
    shortening answer after a retake that no longer fits, or the plain `dub` away after such a
    retake: the next visit runs `dub` and the check and sends no batch.
  Mutations (no give-back, always giving back, the unheard mark dropped, the check's old path,
  the check's kind as `dub`) each fail a test. Removing the mark set at the start fails 11.
- Review (2026-10-07, two lenses, each finding verified):
  - Confirmed, about how the round is counted: `dub --redo` writes `<id>.wav` only for the
    flagged lines; stretched copies come after synthesis; a paid answer never written stays in
    the speech journal, so no round is given back after a take that was paid for. Making the
    track again on the next visit buys no speech (the dub's cache) and pays only for clips whose
    hash changed (check-audio caches by clip hash).
  - Confirmed, about the visit flow: `check_stopped` is cleared only on success and in
    `giveUpDub`. No exit loops for ever: a vendor's exit 4 blocks at `DEFER_LIMIT`, and
    everyone's waits with backoff.
  - Fixed: the two should-fix findings above (the plain `dub` exit 4 after a refit, and the
    other non-final exits), and the nit on the language step's comment.
  - Not defects: AUTOMATION.md's wording; a STOP between the check and the retake's first
    request spending a round (a STOP keeps its round, as for the narration).
- Duration re-bind (2026-10-07, independent reviewer `claude-pr-review-dub-retake`): PASS,
  duration-only; the increment is in `docs/videos/long-form/review.md`. It noted one limit, not
  a length issue: `flaggedTakes` tells a made take by its bytes, so a retake that wrote a take
  byte-identical to the old one and then exited 4 would get its round back. A synthesized voice
  does not repeat its bytes, and the cost would be one more retake round, so it is left as is.
