---
id: 2026-10-05-hold-lost-transcriptions-and-judgements-across
title: Hold lost check-audio transcriptions and Jev judgements across a restart
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T12:51:09Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/shorts/check.mjs
  - tools/video/tts/speech-journal.mjs
---

# Hold lost check-audio transcriptions and Jev judgements across a restart

## Why

`tools/video/tts/speech-journal.mjs` (ticket 2026-10-05-reuse-confirmed-speech-results-across-restart)
now records every paid synthesis that `tts`, `audition`, `dub` and a Short's server narration
send: an answer that came back is reused after a restart, and one that was lost holds the
request until a person runs `node tools/video/tts/speech-journal.mjs forget`. The other two paid
routes are not covered. `check-audio` (`tools/video/tts/check.mjs`, lines ~287 and ~330) and a
Short's listening check (`tools/video/shorts/check.mjs`, `checkAudio`) call `transcribeClip` and
`judgeLines` from `tools/video/tts/client.mjs` directly. When one of those answers is lost the
client throws `SPEECH_UNCERTAIN` once (exit 3), the worker blocks the video, and the owner's retry
runs the command again, which sends the same transcription or Jev question a second time and may
be charged twice. A transcript or Jev verdict that arrived but was not yet written to
`review/check.json` is also bought again.

## Definition of done

- [ ] A transcription or judgement sent by `check-audio` or a Short's check and recorded with no
  confirmed answer is not sent again by a later run; it holds (SPEECH_UNCERTAIN, the owner's)
  until a person clears it with the journal's `forget` command.
- [ ] A complete transcript or Jev answer that arrived is reused after a restart, bound to the
  exact request body sha256, and a changed clip, term list, language or line set never reuses it.
- [ ] No test calls a live paid endpoint; check-audio's existing cache (`review/check.json`) and
  its thresholds behave as before.

## Steps

- [ ] Generalize the journal's saved answer from a WAV to the route's JSON (`{ text }` for
  transcribe, the `results` map for judge), keyed and released the same way, or wrap the
  `transcribe`/`judge` callbacks check.mjs and shorts/check.mjs already take.
- [ ] Wire it where each check saves its cache, releasing only after that write.
- [ ] Counting-fetch fixtures like `tools/video/tts/speech-journal.test.mjs`: lost POST, broken
  body, restart after a confirmed answer, restart after an unknown one, changed request.

## How to verify

`node --test tools/video/tts/speech-journal.test.mjs tools/video/tts/check.test.mjs
tools/video/tts/batch-recovery.test.mjs tools/video/shorts/*.test.mjs`, then
`npm run test:tools`. `check.test.mjs` and `batch-recovery.test.mjs` are bound by the long-form
duration receipt (`docs/videos/long-form/review.json`): put new tests in new files, and report
`node tools/video/long-form/cli.mjs check`'s stale list if a bound file has to change.

## Notes

- Split out of 2026-10-05-reuse-confirmed-speech-results-across-restart, whose Definition of
  done covered the synthesis consumers only.
- The reviewed reference that journals all three routes at the fetch level is
  `docs/videos/imported-long-languages/speech-journal.mjs` (`createSpeechJournalFetch`); it is
  bound to six approved sources and not meant to be switched on elsewhere as it is.
