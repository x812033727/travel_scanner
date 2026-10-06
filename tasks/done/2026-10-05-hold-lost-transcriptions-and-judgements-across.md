---
id: 2026-10-05-hold-lost-transcriptions-and-judgements-across
title: Hold lost check-audio transcriptions and Jev judgements across a restart
status: done
priority: P2
area: tools
owner: claude-opus-5-5-check-journal
claimed_at: 2026-10-05T23:48:13Z
created_at: 2026-10-05T12:51:09Z
completed_at: 2026-10-06T00:24:26Z
branch: claude/check-journal
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/shorts/check.mjs
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/check-journal.test.mjs
  - tools/video/shorts/check-journal.test.mjs
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

- [x] A transcription or judgement sent by `check-audio` or a Short's check and recorded with no
  confirmed answer is not sent again by a later run; it holds (SPEECH_UNCERTAIN, the owner's)
  until a person clears it with the journal's `forget` command.
- [x] A complete transcript or Jev answer that arrived is reused after a restart, bound to the
  exact request body sha256, and a changed clip, term list, language or line set never reuses it.
- [x] No test calls a live paid endpoint; check-audio's existing cache (`review/check.json`) and
  its thresholds behave as before.

## Steps

- [x] Generalize the journal's saved answer from a WAV to the route's JSON (`{ text }` for
  transcribe, the `results` map for judge), keyed and released the same way, or wrap the
  `transcribe`/`judge` callbacks check.mjs and shorts/check.mjs already take.
- [x] Wire it where each check saves its cache, releasing only after that write.
- [x] Counting-fetch fixtures like `tools/video/tts/speech-journal.test.mjs`: lost POST, broken
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
- Done (claude-opus-5-5-check-journal, 2026-10-06). `speech-journal.mjs` now has one route per
  paid path (`speech`, `speech/transcribe`, `speech/judge`). Each route says what its entry
  records, how its answer is checked and saved, and how the answer is read back. `wrap(send)` is
  unchanged. The new `wrapTranscribe(impl)` and `wrapJudge(impl)` have the contract of
  `transcribeClip` and `judgeLines`. Their keys come from `transcribeBody` and `judgeBody`, which
  mirror client.mjs. A parity test pins those keys to the client's `requestSha256` for every
  combination of terms and language. client.mjs is unchanged, because #1305/#1310 and train E
  #1315 edit it.
- Transcription entries keep the clip's sha256 and size, not its base64. Confirmed transcripts and
  Jev results are kept inline in the entry, with `answer_sha256`; an edited answer holds. JSON has
  no NaN, so a NaN probability (Jev gave no noul) is kept as the string "NaN" and read back as NaN.
- Synthesis (WAV) entries are byte-for-byte unchanged. A scratch script ran origin/main's
  journal and this one with a fixed clock and compared the results:
  - the confirmed entry and the WAV;
  - the held entries for a lost answer, a non-audio answer and a crash;
  - the hold messages and the `list` lines, including an unreadable entry;
  - each version reusing the other's confirmed entry.
  `speech-journal.test.mjs` passes unchanged. Train E #1315 edits that test file, so every new
  test is in a new file.
- check-audio uses the video's journal (`<workdir>/audio/speech-journal`, shared with tts and dub)
  and releases it after every write of `review/check.json`, so the journal only holds what the
  cache lacks. Answers taken from the journal are left out of `transcribed` and `jev_calls`, and
  the run prints `N answers paid for by an earlier run came from the speech journal` as tts does.
  A Short's check keeps its journal in the build directory and releases it after `check.json` is
  saved. Its `transcribe_calls` and `judge_calls` count only the calls this run made, as
  `serverNarration` counts.
- Limits, not fixed:
  - Each Short build directory has its own journal, so a hold in one build does not stop a check
    of a new build with the same clip. The lab only rebuilds after a check has finished, so this
    matters only when a person rebuilds by hand while a hold is open.
  - An answer bought by a stopped run is left on disk when its request is never asked again (for
    example, the clip was remade before the next check). It stays confirmed and holds nothing.
    `list` shows it and `forget` clears it. Synthesis entries already behaved this way.
- Verified:
  - The new `tools/video/tts/check-journal.test.mjs` (19 tests) covers parity, restart reuse,
    changed clip, terms, language and lines, and lost, broken-off, non-JSON, 504 and 500
    answers. It also covers a run that died while a request was out, settled errors, an edited
    answer, and check-audio end to end: a lost transcription with forget, a transcript bought
    before the cache write failed, and a broken Jev answer with a verdict bought before its
    write failed.
  - The new `tools/video/shorts/check-journal.test.mjs` (3 tests) covers the same cases for a
    Short's check.
  - With origin/main's two check.mjs files in place, the 6 end-to-end tests fail.
  - `check.test.mjs` and `batch-recovery.test.mjs` pass unchanged, apart from the known
    Windows-only second-opinion red. That test also passes on this branch when the node path has
    no spaces (its 8.3 short form), so the red comes from the space in Windows' default Node
    install path.
  - `node tools/video/long-form/cli.mjs check` passes and lists nothing stale, because no
    receipt-bound file changed.
- Filed 2026-10-06-from-drama-test-s-brightness-filter for a Windows-only red that came in with
  #1315. It turned up while re-running the Shorts tests after rebasing onto cff4a6ac6.
