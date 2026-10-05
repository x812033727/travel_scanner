---
id: 2026-10-05-reuse-confirmed-speech-results-across-restart
title: Reuse confirmed speech results and hold unknown ones across a restart
status: done
priority: P1
area: tools
owner: claude-opus-5-5-speech-journal
claimed_at: 2026-10-05T12:26:34Z
created_at: 2026-10-05T00:38:35Z
completed_at: 2026-10-05T13:18:02Z
branch: claude/speech-journal
depends_on: []
scope:
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
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

- [x] Confirmed complete response bytes for a normal consumer (`synthesis.mjs` through
  `tts/cli.mjs`, `shorts/speech.mjs`, `dubs/cli.mjs`) are consumed after a restart without being
  bought again, bound to the exact request body (sha256) that bought them.
- [x] A request recorded as sent with no confirmed answer is not sent again by a later run; it
  stays a visible hold until a person reconciles it with an explicit command.
- [x] A changed request (other text, voice, model, style or language) never reuses another
  request's bytes, and no test calls a live paid endpoint.
- [x] Source, voice, model and budget authority are unchanged, and listening acceptance is
  never inferred from an HTTP response or a local audio check.

## Steps

- [x] Choose the contract: where the journal lives (per workdir, next to `audio/cache.json`),
  what it records before dispatch (path, request sha256, time) and after (status, raw bytes or
  JSON, billable characters), and how a person clears an unknown entry.
- [x] Wire it into the three consumers; `synthesis.mjs` is bound by the long-form duration
  receipt (`docs/videos/long-form/review.json`), so a change there needs the independent
  reviewer's increment.
- [x] Fixtures with an injected counting fetch: lost POST, lost body, corrupt result, changed
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
- Since the review of PR #1235 the main worker (`tools/video/automation/flow.mjs`) blocks the
  video on `video_speech_uncertain` from `tts`, `dub` (and its retake) and `check-audio`, instead
  of giving a dub up; the owner's retry runs the command again and resends the request. That
  resend is what this ticket's hold should stop until a person reconciles it.

### Done (claude-opus-5-5-speech-journal, 2026-10-05)

- Contract, written at the top of `tools/video/tts/speech-journal.mjs`: one file per request,
  `<dir>/<sha256>.json`, keyed on the sha256 of the JSON body exactly as `client.mjs` sends it
  (the same value as `error.requestSha256`). Before dispatch it says `sent` (the body, the time),
  created only where no entry exists (a temporary file hard-linked into place), so two runs on
  one directory cannot both send a body. A complete answer is saved as `<sha256>.wav` (atomic
  write plus fsync) before the entry says `confirmed` (WAV sha256, size, billable characters).
  A lost or unusable answer turns it `held` with why. A settled failure (never sent, refused,
  budget, owner, the API's own 5xx after the client's retries) removes the entry.
- Holds: a later run that asks for a `sent`, `held` or damaged entry throws `SPEECH_UNCERTAIN`
  (who `owner`, exit 3, one line ending in the code, so `automation/flow.mjs` blocks the video)
  without sending. The message names the clearing command:
  `node tools/video/tts/speech-journal.mjs forget --dir "<dir>" --sha <sha>`; `list --dir <dir>`
  shows every entry with its voice and text.
- Where it lives: `<workdir>/audio/speech-journal/` for `tts` and `dub` (one per video),
  `<workBase>/_audition/speech-journal/` for `audition`, and
  `<workBase>/.speech-server/speech-journal/` beside the Shorts phrase cache (so the Shorts lab's
  next round meets the hold in `shorts/speech.mjs`; `lab.mjs` needed no change).
- Each consumer calls `journal.release()` right after its own durable write (tts and dub after
  `cache.json`, Shorts after the phrase WAV, audition after the sample), which drops the
  entries it used. That is what lets `--redo`, `--force` and a flagged Short phrase buy a new
  take of the same body instead of getting the old one back.
- A reused answer bills 0 characters in the run that reuses it (`recordStage` billable, the Shorts
  `calls`/`characters`), because an earlier run paid for it; tts and dub print a line counting them.
- `synthesis.mjs`, `client.mjs`, `tts.test.mjs` and `dubs.test.mjs` are untouched: the journal
  wraps the `send` callback the CLIs pass to `synthesizeRequest`/`synthesizeLines`. The scope
  dropped `tools/video/tts/synthesis.mjs` for that reason, and the long-form receipt stays current.
- `shorts/speech.mjs` now writes a cached phrase with `atomicWrite` (it used `writeFileSync`): a
  half-written phrase would otherwise count as cached, after its journal entry was released.
  `speech.mjs` is part of `shorts/build.mjs`'s code hash, so the next Short builds get new build
  ids; their cached phrases are reused, nothing is bought again.
- Claimed with `--force`: the only overlap was `tools/video/dubs/cli.mjs` in
  2026-10-01-hand-off-owner-approved-renewed-finals (codex-video-stall-followthrough, claimed
  2026-10-04T10:14Z, 26 h old, stale). Its branch `codex/video-approved-final-languages-20261004`
  is on no remote and in no worktree, and no commit since #1208 touches `dubs/cli.mjs`.

- Verified on Windows (2026-10-05): `node --test tools/video/tts/speech-journal.test.mjs` 18/18;
  tts + shorts + dubs suites 263/264 and `npm run test:tools` 1707/1712 (3 skipped), the reds
  being the known Windows-only `check.test.mjs` transcript test and `nginx-install.test.mjs`
  timing out under load (`spawnSync bash ETIMEDOUT`; 6/6 when run alone);
  `node tools/video/long-form/cli.mjs check` PASS with no stale file; `npm run check:tasks` exit 0.

### Limits, and what is left

- The journal sees what `send` returns: the client's complete body after `toNarrationRate`
  (Gemini's 24 kHz upsampled to 48 kHz), not the raw wire bytes or headers. "Complete" means the
  client finished reading the body without error, and the journal also requires 48 kHz 16-bit
  mono PCM before confirming; a body that ends cleanly but short is not detectable at this layer
  (the fetch-level reference in `docs/videos/imported-long-languages/` checks RIFF and
  Content-Length).
- A process killed between a consumer's cache write and its `release()` (two consecutive
  synchronous calls) leaves a confirmed entry for a take already saved. The next run does not
  ask for that body, so it stays (visible in `list`); a later `--redo` of exactly that body would
  get that take back once, and the following redo buys a new one.
- `check-audio` and a Short's listening check (`transcribeClip`, `judgeLines`) are not journaled:
  filed as 2026-10-05-hold-lost-transcriptions-and-judgements-across.
