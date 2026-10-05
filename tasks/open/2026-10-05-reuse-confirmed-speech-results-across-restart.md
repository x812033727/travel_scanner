---
id: 2026-10-05-reuse-confirmed-speech-results-across-restart
title: Reuse confirmed speech results and hold unknown ones across a restart
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-05T00:38:35Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
  - tools/video/tts/synthesis.mjs
  - tools/video/tts/cli.mjs
  - tools/video/shorts/speech.mjs
  - tools/video/dubs/cli.mjs
---

# Reuse confirmed speech results and hold unknown ones across a restart

## Why

Since `tools/video/tts/client.mjs` stopped resending paid POSTs (ticket
2026-10-04-prevent-paid-speech-retries-after-ambiguous), a paid synthesis, transcription or
Jev judgement whose answer is lost throws `SPEECH_UNCERTAIN` (`video_speech_uncertain`,
who "owner", exit 3) and is sent once. That protection lasts one process only. Nothing on disk
remembers that the request went out, so the next run of `tts`, `dub` or a Short's build sends
the same body again and may pay twice. The Shorts lab makes this automatic: its owner branch
(`tools/video/shorts/lab.mjs`, "waits for the owner at <phase>") runs the same phase again on
the next round, so an uncertain phrase is resent a round later.

The other half is the opposite loss: a result that did arrive complete but was not yet written
by its caller (a crash or STOP between the answer and the caller's `atomicWrite`) is bought again
on the next run. `docs/videos/imported-long-languages/speech-journal.mjs` already preserves raw
WAV/JSON and holds unknown results for its six approved sources; it is a reviewed reference, not
something to switch on for unrelated projects.

Split from 2026-10-04-preserve-normal-speech-results-before-retrying: its no-replay half
landed with the client change; this ticket holds its result-preservation contract.

## Definition of done

- [ ] Confirmed complete response bytes for a normal consumer (`synthesis.mjs` through
  `tts/cli.mjs`, `shorts/speech.mjs`, `dubs/cli.mjs`) are consumed after a restart without being
  bought again, bound to the exact request body (sha256) that bought them.
- [ ] A request recorded as sent with no confirmed answer is not sent again by a later run; it
  stays a visible hold until a person reconciles it with an explicit command.
- [ ] A changed request (other text, voice, model, style or language) never reuses another
  request's bytes, and no test calls a live paid endpoint.
- [ ] Source, voice, model and budget authority are unchanged, and listening acceptance is
  never inferred from an HTTP response or a local audio check.

## Steps

- [ ] Choose the contract: where the journal lives (per workdir, next to `audio/cache.json`),
  what it records before dispatch (path, request sha256, time) and after (status, raw bytes or
  JSON, billable characters), and how a person clears an unknown entry.
- [ ] Wire it into the three consumers; `synthesis.mjs` is bound by the long-form duration
  receipt (`docs/videos/long-form/review.json`), so a change there needs the independent
  reviewer's increment.
- [ ] Fixtures with an injected counting fetch: lost POST, lost body, corrupt result, changed
  request, restart after a confirmed answer, restart after an unknown one.

## How to verify

`node --test tools/video/tts/speech-journal.test.mjs tools/video/tts/*.test.mjs
tools/video/shorts/*.test.mjs tools/video/dubs/*.test.mjs`, then `npm run test:tools` and
`node tools/video/long-form/cli.mjs check` (report its stale list; do not edit the receipt).

## Notes

- Split from 2026-10-04-preserve-normal-speech-results-before-retrying (its DoD 2 and both
  Steps); the client half closed with 2026-10-04-prevent-paid-speech-retries-after-ambiguous.
- The client already exposes what a journal needs on the error: `error.path` and
  `error.requestSha256` (sha256 of the JSON body sent). Its settled/never-sent classification is
  in `tools/video/tts/client.mjs` (`SETTLED_CODES`, `NEVER_SENT`).
- `tools/video/shorts/lab.mjs` is not in scope; if the hold has to live there instead of in
  `shorts/speech.mjs`, check claims and widen the scope first.
