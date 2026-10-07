---
id: 2026-10-07-a-speech-request-waiting-out-a
title: A speech request waiting out a rate limit is held as uncertain if the worker restarts mid-wait
status: done
priority: P3
area: tools
owner: claude-opus-5-5-journal-wait
claimed_at: 2026-10-07T07:57:01Z
created_at: 2026-10-07T05:56:55Z
completed_at: 2026-10-07T08:58:25Z
branch:
depends_on: []
scope:
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
---

# A speech request waiting out a rate limit is held as uncertain if the worker restarts mid-wait

## Why

`tools/video/tts/speech-journal.mjs` `journaled()` writes a paid request's entry as `sent`
before `send()` runs. It removes the entry only when `send()` comes back with a settled error.
`client.mjs` `call()` retries a 429 inside that one `send()`. So for the whole time the request
waits out the speech routes' rate limit, its entry says `sent`, although the API's 429 proves
nothing reached a provider.

If the worker stops during the wait (a deploy restarts it; nothing waits for a client-side sleep
to end), the next run finds the `sent` entry. It holds the request as SPEECH_UNCERTAIN, exit 3,
and the video is blocked until the owner runs `speech-journal.mjs forget`.

This was possible before. Since `2026-10-05-a-burst-of-narration-lines-trips` the waits are
longer: one window, up to 61 s, at most four times per request, where before they were 1, 2, 4,
8 and 16 s. So a restart lands inside one more often.

## Definition of done

- [x] A paid request whose only answers so far were the routes' own 429s is not held as uncertain
  after a restart in the middle of its wait. Its next run sends it, and nothing that may have
  reached a provider is sent twice.

## Steps

- [x] Choose how the journal learns that the request is waiting on a refusal. One way: `call()`
  takes an optional `onRefused` hook, and the journal rewrites the entry as `waiting` before the
  sleep and back to `sent` before the next POST. A `waiting` entry found by the next run is safe
  to send again.
- [x] Tests: a 429, then a simulated restart during the wait (a new journal opened on the same
  directory) sends the request. A request that went out after the last refusal stays held.

## How to verify

`node --test tools/video/tts/speech-journal.test.mjs tools/video/tts/client.test.mjs`.

## Notes

- Found while doing `2026-10-05-a-burst-of-narration-lines-trips` (2026-10-07). The
  investigation there traced `sendOnce`: a SpeechError that is not SPEECH_UNCERTAIN removes the
  entry, so only a run that dies mid-wait leaves it behind.
- 2026-10-07 (claude-opus-5-5-journal-wait). Done, more widely than the 429 alone: `call()` waits
  only after an answer that settled the request (the routes' 429, a provider busy, the API's own
  failure, a site never reached), so every wait of a paid request is safe to resume from.
  - `client.mjs`: `withPaidWaits(hooks, send)` runs `send` in an AsyncLocalStorage that `call()`
    reads, for paid requests only. `waiting({ status, code, ms })` comes before each sleep,
    `resending()` after it and before the next POST, and it may throw to stop the request. Through
    the store rather than an option, because `journal.wrap(send)` gets a closure from tts, dub and
    Shorts, and none of them would have to forward it.
  - `speech-journal.mjs`: a new status, `waiting`, carries a random `wait_id` and a `why`
    ("HTTP 429 rate_limit_exceeded; sent again in 61 s"). Whoever turns it back into `sent` (the
    run itself when it wakes, or a later run that finds it) must first create
    `<sha>.<wait_id>.claim` exclusively, then re-read the entry and find it still waiting with
    that id. Only then does it write its own `sent` and POST; it removes the claim afterwards.
    So two runs never both send. A run that wakes to find another run sent it stops with
    `SPEECH_TAKEN_OVER` (the service's, exit 4), leaves the other run's entry as it is, and a
    later run takes that answer.
  - The project lease already keeps a second producer off a video project, so for tts, dub and
    check-audio the claim is defence in depth. A Short's journal runs without a lease.
  - `list` shows a waiting entry with its time and says the next run sends it. It is not counted
    as a hold to forget. A waiting entry without a UUID-shaped `wait_id` reads as unreadable and
    holds, since the id goes into a file name.
  - A crash between creating a claim and removing it (milliseconds: several fsyncs) leaves the
    entry waiting behind a claim. The next run holds it ("another run keeps changing") instead of
    guessing. `list` shows it as `claimed` and counts it among what to forget. `forget` removes
    the entry, its answer and its claims.
  - A wait the journal cannot record stops the request before the sleep, and `sendOnce` holds it.
    The write may have landed (the rename) before its fsync failed, and a waiting entry is one
    another run sends; this run sends nothing more.
- Tests:
  - client: the hooks around each wait (429 with Retry-After, a provider busy, a refused
    connection) for all four paid calls; a `resending` that throws stops the next POST; nothing
    is told after the last try, for a wait too long to take, or for an unpaid call.
  - journal: a restart mid-wait for each settled kind, sent once by the next run with no claim
    left behind; a run that wakes after a second run took it over (and was itself refused and
    waiting) stops without a POST, and the second sends it; a request sent again after its wait
    and lost, or out when the run stopped, still holds; a claim in place, or a malformed wait id,
    holds.
  - tts: a run stopped in the 61 s wait, then the next `tts` exits 0 having sent that body once
    more.
  - All but the stays-held one fail on the old code, and each of eleven mutations (no takeover,
    no claim, no re-read, removing the entry on a takeover, no hook in either retry path, hooks
    for unpaid calls, no wait-id check, waiting counted as held, the claim left behind, the
    entry left waiting) fails a test.
- Review (2026-10-07, three lenses, each finding verified). It included a 120-round stress test:
  six processes on one journal, random 429s and sleeps, about 40% killed mid-run. It found no
  overlapping POSTs, no POST after a 200, and no POST after a run killed mid-POST.
  - Should-fix (found by all three lenses): a waiting write whose rename landed and whose fsync
    then failed left `waitId` unset. The run then resent without a claim while the entry said
    waiting, so a restart or a second run could send the body again. Fixed as above. Test: the
    first fsync after the 429 throws EIO; the run stops with no sleep, the entry is held, and the
    next run sends nothing.
  - Nit: a claim left behind made `list` say the next run sends the entry, while every run held
    it. Fixed as above, with a test.
  - Test gap: weakening `resume`'s re-read passed every test. A new test wakes the first run after
    the other run's POST is still out, after its answer was saved, and after it was released.
    Each must stop with `SPEECH_TAKEN_OVER`, send nothing, and leave the entry, or its absence,
    as it was. Both of the reviewer's mutants now fail.
  - Not defects: a sleep that rejects (no production sleep does); `release` removing a later
    waiting entry (its sleeper stops without sending).
