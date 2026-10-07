---
id: 2026-10-07-a-speech-request-waiting-out-a
title: A speech request waiting out a rate limit is held as uncertain if the worker restarts mid-wait
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T05:56:55Z
completed_at:
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

- [ ] A paid request whose only answers so far were the routes' own 429s is not held as uncertain
  after a restart in the middle of its wait. Its next run sends it, and nothing that may have
  reached a provider is sent twice.

## Steps

- [ ] Choose how the journal learns that the request is waiting on a refusal. One way: `call()`
  takes an optional `onRefused` hook, and the journal rewrites the entry as `waiting` before the
  sleep and back to `sent` before the next POST. A `waiting` entry found by the next run is safe
  to send again.
- [ ] Tests: a 429, then a simulated restart during the wait (a new journal opened on the same
  directory) sends the request. A request that went out after the last refusal stays held.

## How to verify

`node --test tools/video/tts/speech-journal.test.mjs tools/video/tts/client.test.mjs`.

## Notes

- Found while doing `2026-10-05-a-burst-of-narration-lines-trips` (2026-10-07). The
  investigation there traced `sendOnce`: a SpeechError that is not SPEECH_UNCERTAIN removes the
  entry, so only a run that dies mid-wait leaves it behind.
