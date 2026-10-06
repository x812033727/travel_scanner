---
id: 2026-10-05-speech-journal-releases-never-reached-502
title: Imported-language speech journal lets a paid POST the route never sent go again
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-speech-journal-502
claimed_at: 2026-10-05T23:41:35Z
created_at: 2026-10-05T12:39:17Z
completed_at:
branch: claude/speech-journal-502
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

- [x] A paid speech POST whose first answer is the route's 502 `upstream_unavailable` does not
  leave an `unknown` entry. The native client's next attempt goes out within its bounded attempts,
  and its answer is journaled the way the journal handles a first answer.
- [x] Any other answer that is not 2xx (503 `upstream_unavailable`, 504 `video_speech_answer_lost`,
  any other 5xx, 4xx) is still recorded as `unknown` and holds the slug exactly as today.

## Steps

- [x] In `speech-journal.mjs`, for a 502 whose problem body has the code `upstream_unavailable`,
  remove the pending entry (or mark it not dispatched) instead of writing `unknown`, and return the
  response unchanged. Read the body from a clone so the native client still sees it.
- [x] In `speech-journal.test.mjs`, change the `502 upstream_unavailable` case of "native server
  auth/quota classification is preserved…". Today it expects `video_speech_result_held` after one
  POST. It should expect two POSTs and the second answer's result, with the 503 case unchanged.
- [x] Update the README paragraph that says a lost response holds the slug, so it names this
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
- Claimed with `--force` by claude-opus-5-5-speech-journal-502 on 2026-10-05 at 23:41Z, over
  2026-09-29-resume-imported-long-video-languages (codex-video-stall-followthrough, claimed
  2026-10-04T10:51:05Z, about 37 h old, so stale). Its branch
  `codex/video-approved-final-languages-20261004` is not on the remote. It was merged as PR #1210
  (head 83edc6b7f, merged 2026-10-04T23:41:07Z). In that head, `speech-journal.mjs` and
  `README.md` are byte-identical to origin/main a9e4c3851: `git diff 83edc6b7f origin/main` over
  the directory lists only `speech-journal.test.mjs`, which #1235 and #1302 changed. No open PR
  touches the directory. The codex task was not taken over or edited. Its remaining work is
  activation on the production host, and only the journal's 502 branch changed here.
- What changed: `neverReached(response)` releases only `status === 502` with a JSON body whose
  `code` is exactly `upstream_unavailable`, read from `response.clone()`. The native client still
  reads the original body: the all-five-attempts test sees `code: "upstream_unavailable"` on the
  client's error. The journal is written without the entry from a copy first, and the in-memory
  entry is forgotten only after that write succeeds. If the write fails, the catch still marks the
  entry `unknown` and holds; a test covers this. The retry goes through every gate again (fresh
  identity, STOP, lock, all-succeeded). A STOP between attempts holds it with no POST, and a test
  covers this too.
- The test step was done as a separate test, not by editing the old row in place. The 502 row
  left the classification table. Rows for 504 `video_speech_answer_lost`, an HTML gateway 502 and
  502 `video_speech_upstream_failed` were added, and each still holds a later run. The new tests
  cover 502 then success for speech, transcribe and judge (two POSTs, one `succeeded` entry, an
  empty journal between the attempts, replay with zero POSTs); five 502s (five POSTs, a `service`
  `upstream_unavailable` error, no entry, the next run sends again); a failed release write; and
  STOP after the release.
- The tts journal (`tools/video/tts/speech-journal.mjs`, wrapped around `synthesize` in
  `dubs/cli.mjs`) already removes its own entry on any settled `SpeechError`, so five 502s leave
  nothing held at either level.
- Batches already frozen keep the old journal (runner.mjs copies `speech-journal.mjs` into each
  batch runtime by SHA-256) until they are prepared again. The README says so.
- Verified locally: `node --test docs/videos/imported-long-languages/speech-journal.test.mjs`
  passed 71 of 71, and `tools/video/tts/client.test.mjs` passed 6 of 6. Before this change the
  journal file's new tests failed on origin/main's journal (7 failures), and the
  classification table passed on both versions. `docs/videos/imported-long-languages/runner.test.mjs`
  passed 43 of 44. Its one red, "replay saved raw WAV after consumer interruption", fails the same
  way on unchanged a9e4c3851. It most likely comes from the dub's own journal that #1302 added and
  is filed as 2026-10-05-imported-language-runner-test-still-expects.
