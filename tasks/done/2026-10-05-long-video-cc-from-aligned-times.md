---
id: 2026-10-05-long-video-cc-from-aligned-times
title: Long video CC cues cut at measured character times when the timeline carries them
status: done
priority: P2
area: tools
owner: claude-opus-5-5-cc-aligned
claimed_at: 2026-10-06T00:18:30Z
created_at: 2026-10-05T16:08:23Z
completed_at: 2026-10-06T00:49:50Z
branch: claude/long-video-cc-aligned-times
depends_on:
  - 2026-10-05-speech-align-character-timing
  - 2026-10-05-caption-translation-chain-upgrade
  - 2026-10-05-reuse-confirmed-speech-results-across-restart
scope:
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
  - tools/video/tts/synthesis.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/tts/speech-journal.test.mjs
  - docs/videos/DESIGN.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Long video CC cues cut at measured character times when the timeline carries them

## Why

Long-video captions split a line's speech window among its cues by text weight
(`core/captions.mjs timePieces`): a cue starts when the weights say so, not when the first
character is spoken. With character timing from the server
(`2026-10-05-speech-align-character-timing`) every cue can start on the measured character,
which is what viewers reading CC on an 8-minute video notice most on long lines.

## Definition of done

- [x] A line whose `timeline.json` entry carries `timing.chars` splits its cues at the measured
      times (a cue starts when its first character is spoken, ±1 frame).
- [x] A timeline without timing produces byte-identical SRT and VTT to today (regression on
      the fixtures).
- [x] `checkCues` reads speed from measured spans; `speech_hash` is unchanged (timing is derived
      from the audio, never an input).
- [ ] Translated locales keep their own split but inherit the zh-TW cue boundaries' times.
      Not done: `buildCues` cannot reach the narration's text without `core/stages.mjs` (see
      Notes); moved to `2026-10-06-translated-cc-cues-take-their-times`.

## Steps

- [x] `timePieces(pieces, startMs, endMs, rules, canFit, chars = null)`; weights stay the fallback.
- [x] `tts/synthesis.mjs` + `tts/cli.mjs`: store `timing: {source, model, chars}` per line in
      `timeline.json` when the server returned it; `core/stages.mjs` passes it to the captions
      stage unchanged (the timeline carries it).
- [x] Tests on the fixtures (`core/captions.test.mjs`, `tts/tts.test.mjs`); `DESIGN.md` §字幕.
- [ ] Receipt increment by an independent agent (`tts/synthesis.mjs`, `tts/tts.test.mjs`,
      `tts/check.test.mjs`, `DESIGN.md`): for the reviewer, not the author.

## How to verify

```bash
node --test tools/video/core/captions.test.mjs tools/video/tts/tts.test.mjs
node tools/video/cli.mjs captions --slug <video>      # cues start on the spoken character
node tools/video/long-form/cli.mjs check
```

## Notes

- The long video stays CC only: no karaoke burn-in (the owner's 2026-09-29 decision).
- Bound: `tts/synthesis.mjs`, `tts/tts.test.mjs`, `tts/check.test.mjs`, `docs/videos/DESIGN.md`.
- 2026-10-06: dropped `tools/video/core/stages.mjs` from `scope` and
  `2026-10-01-hand-off-owner-approved-renewed-finals` from `depends_on`. Both were there only
  for the shared captions stage in `core/stages.mjs`, which that Codex ticket holds in progress.
  It is not needed: `buildCues` (`core/captions.mjs`) reads `timeline.lines`, and
  `presentationTimeline` (`core/branding.mjs`) spreads every line (`{...entry}`), so a line's
  `timing` reaches the cues without any change to `core/stages.mjs`. A timeline without timing
  keeps byte-identical SRT/VTT, so the caption offsets of renewed finals are unaffected. The
  other three dependencies are done: speech-align and the caption chain landed in #1315,
  reuse-speech in #1302.
- 2026-10-06, claude-opus-5-5-cc-aligned, work in 14a96140c:
  - **Synthesis.** For an Azure voice, `tts` sends each phrase-sized body (the size gate below) to
    `speech/align` first, inside the same speech-journal entry as `speech` (`journal.wrap`), as
    Shorts' `serverNarration` does. A
    null answer (404, `video_align_unavailable`, `video_align_voice_unsupported`) goes on to
    `speech`, unpaid. A lost answer on either route is SPEECH_UNCERTAIN and holds the body. An
    answer the journal kept comes back without timing. Gemini voices never ask.
  - **Which units are a line's.** `synthesis.mjs` mirrors the server's `units_of`: an alias part is
    one unit, a Latin word or number is one, whitespace is none, and any other character is one.
    A request's timing is used only when its units equal the request's own, in order; each line
    then takes its run of them by count. Its clip is located in the answer's audio (an exact
    sample match of what `trimSilence` kept), and the units are shifted to it and clamped to
    `[0, clip length]`. A line with a letter or number unit that starts more than 100 ms
    outside its clip gets no timing. A split that falls back to line-by-line drops the whole
    answer's timing, and each single-line answer times its own line.
  - **Storage.** `audio/<id>.timing.json` holds `{wav_sha256, source, model, chars}`. It is removed
    before a new take is written and read only when `wav_sha256` matches the WAV's bytes. An
    `audio_ref` repeat copies its original's. `timeline.json` gets `timing` (after `audio_sha256`)
    on timed lines only, so the bytes of an untimed narration's timeline, which audio approvals
    bind, do not change. The tts run in `state.json` records `timed: N`. When N > 0, stdout says
    "N of M lines carry measured character times".
  - **Cues.** `measuredStarts` maps pieces to units by letters and numbers only. Spaces and
    punctuation are ignored, so a `say` that only changes punctuation (the fixture's p5vs) still
    lines up. It falls back to weights when the letters differ, when a piece starts inside a unit
    (a term read as one alias unit), or when a start runs backwards or leaves the window. The
    first cue also starts on its first character, not at the line start; the last ends as
    before. MIN_CUE_MS merging uses measured durations (shared `mergeShort`). The weighted path
    is byte-identical: SRT/VTT are pinned from d829b18dc (fixture zh-TW and en, plus a
    three-line set in all five locales), and a scratch differential fuzz of 8,000 cases against
    the original module (not committed) found no difference. On the test line, the measured
    second cue starts on "300" at 6847 ms; the weights put it at 6387 ms.
  - **checkCues** already computes speed from cue spans, so it is unchanged. A test shows a fast
    measured cue flagged while the weighted cue is not.
  - **speech_hash** is unchanged. The aligned run of the minimal fixture asserts the hash that
    `core/drama.test.mjs` pins (`af5d5f5eb75aaa69`). The captions command (unchanged
    `core/stages.mjs`) writes the same measured cues, and a branded presentation timeline keeps
    `timing`.
  - **Not done: translated locales.** `buildCues(timeline, texts, locale)` gets one locale's texts
    and the timeline. Lines carry no text, and `timing.chars` has the narration's units without
    spaces or locale, so the narration's cut could only be guessed. Translations keep their
    weights, and a test asserts this. Follow-up: `2026-10-06-translated-cc-cues-take-their-times`
    (needs `core/stages.mjs`, after the Codex ticket).
  - **Scope additions.** `tts/check.test.mjs` and `tts/speech-journal.test.mjs`: their fake sites
    answered every unknown POST as `/speech` and crashed on `{speech: ...}`. The client rightly
    records that as an uncertain paid request. They now answer `speech/align` with 404, as a
    site from before #1315 does. `check.test.mjs` is receipt-bound.
  - **Receipt.** `node tools/video/long-form/cli.mjs check` lists four stale files: `DESIGN.md`,
    `tts/check.test.mjs`, `tts/synthesis.mjs`, `tts/tts.test.mjs`. `review.test.mjs` is red for
    these four only. The author did not touch `review.md` or `review.json`.
  - **The owner must check live.** No long video in `docs/videos` uses an Azure voice today (all
    30 use Gemini Sulafat or Rasalgethi), so nothing changes for them until a voice switch or
    `2026-10-05-speech-align-gemini-cpu-aligner`. On the first Azure-voiced video, `tts` should
    print "N of M lines carry measured character times", and the zh-TW CC should start on the
    spoken character against the audio; check a few long lines in a player. Only phrase-sized
    requests reach `speech/align` (the size gate), so an aligned answer stays near 2 MB of WAV,
    about 2.7 MB of JSON, far inside the BFF's 180 s. A lost answer is held by the journal, not
    resent. `timeline.json` grows by about 100 bytes per timed character.
  - **Size gate (2026-10-06 follow-up, after the done commit).** Only a phrase-sized request asks
    `speech/align`: `ALIGNED_MAX_CHARACTERS = 59` in `tts/cli.mjs`, counted by
    `alignedCharacters`. That counts every character the voice reads (an alias by its spoken
    form) and each break as the characters 3 a second would read in it, so the 800 ms between
    two lines counts 3. The route answers with the WAV as base64 in JSON, "which suits a phrase
    of a Short; a six-minute scene belongs to the speech route, whose bytes stream"
    (`align_api.py`), so the WAV must stay inside the route's own clip bound,
    `MAX_CLIP_BYTES = 2,000,000`. Riff48Khz16BitMonoPcm (`align.py`) is 96,000 bytes a second:
    (2,000,000 − 44) / 96,000 = 20.83 s, less 1 s of silence = 19.83 s, at a slow 3 characters
    a second (scripts are sized at 250 a minute, 4.17 a second) = 59.5, so 59. A larger request
    goes straight to `speech`: one call, no timing, the same journal entry. The minimal fixture's
    scenes measure 64, 61 and 58, so two of its three stay untimed. A long video's scene request
    usually runs to hundreds of characters, so most long-video lines get timing only once the
    server's CPU aligner ships (`2026-10-05-speech-align-gemini-cpu-aligner`; it could then time
    each line's clip through `alignClip`, Gemini voices included). Until then timing comes from a
    line retaken on its own, a line synthesized alone after its scene's split did not match, and
    a very short scene. Tests: the boundary at 59 and 60, plus the end-to-end and lost-answer
    tests, now read their expectations from the gate.
