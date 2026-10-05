---
id: 2026-10-05-a-narration-retake-a-stop-file
title: A narration retake a STOP file interrupted resumes instead of blocking on the evidence guard
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T01:48:50Z
completed_at:
branch:
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

- [ ] After a retake a STOP file ended, the next run rebuilds the narration from the takes on disk
      (a plain `tts`, which synthesizes nothing), checks it again and continues the retake rounds,
      without the owner.
- [ ] The guard still blocks a mismatch the stopped retake does not explain (a take changed that
      was not among its flagged lines, or a hash that matches no take the retake made).
- [ ] No line is synthesized twice: the lines the stopped run retook are not retaken again only
      because they were flagged before the stop.

## Steps

- [ ] Record the stopped retake in `auto.json` (its flags file and line ids) when `tts --redo`
      exits 6, and clear it when a `tts` run finishes.
- [ ] Let the guard pass when every mismatching line is one of those ids; add a test with a fake
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
