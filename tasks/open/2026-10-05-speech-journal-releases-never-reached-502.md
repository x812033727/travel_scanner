---
id: 2026-10-05-speech-journal-releases-never-reached-502
title: Imported-language speech journal lets a paid POST the route never sent go again
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T12:39:17Z
completed_at:
branch:
depends_on:
  - 2026-10-05-speech-client-retries-paid-upstream-unavailable
scope:
  - docs/videos/imported-long-languages/speech-journal.mjs
  - docs/videos/imported-long-languages/speech-journal.test.mjs
  - docs/videos/imported-long-languages/README.md
---

# Imported-language speech journal lets a paid POST the route never sent go again

## Why

The imported-long-languages runner wraps the native speech client's fetch with a local journal
(`createSpeechJournalFetch` in `docs/videos/imported-long-languages/speech-journal.mjs`). It
records any answer that is not 2xx as `unknown` ("Even a retryable failure has no local authority
to submit another POST"). After that, every later paid speech POST for that video gets a local
409 `video_speech_result_held` until the owner inspects the journal.

Since 2026-10-05-speech-client-retries-paid-upstream-unavailable, `tools/video/tts/client.mjs`
sends a paid POST again when the speech route answers 502 `upstream_unavailable`. The route only
answers that when it never reached the API: since #1272 it answers a lost answer with 504
`video_speech_answer_lost`, and production serves #1272 since c12e159d0. Under the journal, that
second POST meets the 409. An API restart during a deploy therefore still holds an imported video
for the owner, although nothing ran and nothing was charged. This is the case the client change
fixed for the normal worker.

## Definition of done

- [ ] A paid speech POST whose first answer is the route's 502 `upstream_unavailable` does not
  leave an `unknown` entry. The native client's next attempt goes out within its bounded attempts,
  and its answer is journaled the way the journal handles a first answer.
- [ ] Any other answer that is not 2xx (503 `upstream_unavailable`, 504 `video_speech_answer_lost`,
  any other 5xx, 4xx) is still recorded as `unknown` and holds the slug exactly as today.

## Steps

- [ ] In `speech-journal.mjs`, for a 502 whose problem body has the code `upstream_unavailable`,
  remove the pending entry (or mark it not dispatched) instead of writing `unknown`, and return the
  response unchanged. Read the body from a clone so the native client still sees it.
- [ ] In `speech-journal.test.mjs`, change the `502 upstream_unavailable` case of "native server
  auth/quota classification is preserved…". Today it expects `video_speech_result_held` after one
  POST. It should expect two POSTs and the second answer's result, with the 503 case unchanged.
- [ ] Update the README paragraph that says a lost response holds the slug, so it names this
  exception.

## How to verify

From the root: `node --test docs/videos/imported-long-languages/speech-journal.test.mjs
tools/video/tts/client.test.mjs` (fake transports only, nothing paid). Nothing in CI runs the
first file.

## Notes

- Filed by claude-opus-5-5-speech-client-upstream-unavailable while closing
  2026-10-05-speech-client-retries-paid-upstream-unavailable. That PR pins today's behaviour (the
  journal holds the resend) in `speech-journal.test.mjs` and does not change the journal.
- This is a trade-off, not a bug in the journal's own terms. Its author chose to give it no
  authority to resend. Settle only the route's 502, as the client does: no speech route answers
  `upstream_unavailable` with another status. Also, a host from before #1272 answers that 502 for
  a lost answer too.
- `docs/videos/imported-long-languages` is the whole scope of the in-progress claim
  2026-09-29-resume-imported-long-video-languages (codex-video-stall-followthrough, stale since
  2026-10-05 10:51Z, with no branch on the remote). Check it before claiming this ticket.
- 2026-10-05-reuse-confirmed-speech-results-across-restart builds a journal for
  `tools/video/tts`. It should make the same choice for the route's 502.
