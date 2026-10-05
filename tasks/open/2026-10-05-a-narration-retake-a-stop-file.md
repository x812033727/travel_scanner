---
id: 2026-10-05-a-narration-retake-a-stop-file
title: A narration retake a STOP file interrupted resumes instead of blocking on the evidence guard
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-flow-stop-and-repackage
claimed_at: 2026-10-05T12:26:33Z
created_at: 2026-10-05T01:48:50Z
completed_at:
branch: claude/flow-stop-and-repackage
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# A narration retake a STOP file interrupted resumes instead of blocking on the evidence guard

## Why

When `check-audio` flags narration lines, the worker's `narration()` runs `tts --redo <flags>`.
A retake of several requests can be ended by a STOP file after some of them were paid for: those
lines' new takes are on disk and in `audio/cache.json`, but `timeline.json` still binds the old
takes. Since 2026-10-05 `tts` exits 6 there and the worker waits for the next run (`this.later`)
instead of checking and sending the half-retaken narration. On the next run, though, status sees
takes that differ from `timeline.json`, so "narration synthesized" is undone again, and the
worker's guard before `tts` (`audio evidence no longer matches the saved takes`, in the
"narration synthesized" step of `tools/video/automation/flow.mjs`) blocks the video for the
owner. The mismatch is fully explained by the stopped retake, so the block only costs the owner a
retry.

## Definition of done

- [x] After a retake a STOP file ended, the next run rebuilds the narration from the takes on disk
      (a plain `tts`, which synthesizes nothing), checks it again and continues the retake rounds,
      without the owner.
- [x] The guard still blocks a mismatch the stopped retake does not explain (a take changed that
      was not among its flagged lines, or a hash that matches no take the retake made).
- [x] No line is synthesized twice: the lines the stopped run retook are not retaken again only
      because they were flagged before the stop.

## Steps

- [x] Record the stopped retake in `auto.json` (its flags file and line ids) when `tts --redo`
      exits 6, and clear it when a `tts` run finishes.
- [x] Let the guard pass when every mismatching line is one of those ids; add a test with a fake
      `tts --redo` that replaces one of two flagged takes and exits 6.

## How to verify

`node --test tools/video/automation/automation.test.mjs` (the narration gate tests and the new
one). `flow.mjs` and `automation.test.mjs` are bound to the duration receipt: open the PR as a
draft and leave `node tools/video/long-form/cli.mjs check` to an independent reviewer.

## Notes

- Noticed while doing 2026-10-04-audio-stage-incomplete-exits. Before that change a stopped retake
  returned exit 0, the worker went on to `check-audio` (which with the STOP file still present
  also returned 0) and `review-push`, and the next run hit the same guard; so the block is not
  new, only the way to it is.
- A STOP placed before the retake starts buys nothing and leaves the evidence intact; the next run
  just checks and retakes again. Only a stop between two paid requests leads here.
- Done 2026-10-05 (claude-opus-5-5-flow-stop-and-repackage, branch
  `claude/flow-stop-and-repackage`, with 2026-10-05-the-worker-passes-over-a-video and
  2026-10-05-re-package-when-the-language-choice in the same two files).
- Record: at both `tts --redo` sites in `narration()` (check-flags.json, and a rewrite round's
  rewrite-flags.json) an exit 6 goes through `retakeStopped()`, which still returns `this.later`
  (#1242: a STOP is a later-retry, never a block). It writes `auto.json` `stopped_retake = { flags
  (relative to the work directory), ids (the flagged lines, plus the original of any flagged
  audio_ref repeat, which tts --redo retakes instead), takes: { id: sha256 } }`, where `takes` are
  the takes of those lines that differ from timeline.json right after the stop, i.e. the ones
  the retake made: `narration()` only starts once every take matches timeline.json, so nothing
  else changed them in between. A retake stopped before its first request made no take and
  records nothing (the existing STOP test now asserts that). Takes are hashed from disk rather than
  read from audio/cache.json, so the record does not depend on the cache's format.
- Guard: in the "narration synthesized" step a mismatch passes only when every take that differs
  from timeline.json is in `stopped_retake.takes` with exactly that hash and narration.wav (which
  a stopped tts never writes) still matches its binding. Then a plain `tts` runs (no --redo, no
  --refresh-evidence: every take is cached, so it synthesizes nothing and binds the takes on
  disk), and `stopped_retake` is cleared once it exits 0; the line says "narration synthesized
  from the takes of the retake a STOP file ended". Any other mismatch (another line's take,
  other bytes on a retaken line, a missing take) blocks as before, and the record stays for the
  owner's retry. `state.retakes` is not reset: the round the stopped retake spent stays counted.
- No second synthesis: the next round's check-audio judges the retaken line on its new take
  (verdicts are bound to the take's hash), and check-flags.json is rewritten with what is still
  flagged, so `tts --redo` gets only the lines not yet retaken. The test shows the second redo is
  `["b3tn"]` alone after the first, stopped one was `["x9fe", "b3tn"]`.
- A stopped rewrite-round retake never reached the guard (its rewritten lines change the speech
  hash, so a plain tts already resumed it); it is recorded the same way and cleared by that tts.
- Tests: "a retake a STOP file ended is bound from the takes it made on the next run, …" and
  "after a stopped retake, a take changed on another line, or to bytes the retake did not make,
  still blocks the video before tts" (two subtests). Turning the guard's exception off, recording
  nothing, or explaining every take each turn a test red.
- `#1235`'s rule is untouched: a speech command that lost a paid answer (SPEECH_UNCERTAIN, exit 3)
  still blocks for the owner; only exit 6 goes through `retakeStopped()`.
