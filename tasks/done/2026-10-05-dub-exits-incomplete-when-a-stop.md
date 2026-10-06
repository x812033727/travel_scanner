---
id: 2026-10-05-dub-exits-incomplete-when-a-stop
title: dub exits incomplete when a STOP file ends it, like tts and check-audio
status: done
priority: P2
area: tools
owner: claude-opus-5-5-dub-stop-exit
claimed_at: 2026-10-05T23:46:11Z
created_at: 2026-10-05T01:47:46Z
completed_at: 2026-10-06T00:26:19Z
branch: claude/dub-stop-exit
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/cli.mjs
  - docs/videos/DUBS.md
  - docs/videos/DESIGN.md
  - .agents/skills/youtube-video/references/automated.md
  - docs/videos/AUTOMATION.md
---

# dub exits incomplete when a STOP file ends it, like tts and check-audio

## Why

`dub` synthesizes a dubbed track request by request and checks for a STOP file before each one.
When it finds one it prints "stopped by the STOP file … rerun to continue" and returns exit 0
(`tools/video/dubs/cli.mjs`, the loop over `pending`), before the dub's timeline, fit report and
track are written. The worker's `makeDub` (`tools/video/automation/flow.mjs`) reads exit 0 as
"the track is made" and goes straight on to `check-audio --locale`, which then hears a track that
was never assembled, or the previous one. Since 2026-10-05 `tts` and `check-audio` return exit 6
(`EXIT.incomplete` in `tools/video/cli.mjs`) in the same situation and the worker waits for the
next run; `dub` is the one audio stage left on the old contract.

## Definition of done

- [x] A `dub` run that a STOP file ends before its track is assembled exits 6, keeps every take it
      paid for in its cache, and writes no timeline, fit report or track that looks current.
- [x] The worker treats a `dub` or `dub --redo` exit 6 as "the next run continues" (`this.later`),
      never as a made track, a given-up language or a blocked video.
- [x] A rerun without the STOP file finishes the track and buys only the requests that were left.

## Steps

- [x] Offline fixture in `dubs.test.mjs`: STOP before the first and between two requests (the fake
      server writes the STOP file), exit 6, cache kept, rerun buys only the rest.
- [x] Return `EXIT.incomplete` from the STOP branch in `tools/video/dubs/cli.mjs`.
- [x] In `makeDub`, map `made.code` and `redo.code` 6 to `this.later`, with a test in
      `automation.test.mjs` next to "a STOP file that ends a dub's check defers the language".

## How to verify

`node --test tools/video/dubs/dubs.test.mjs tools/video/automation/automation.test.mjs`; mock
providers only, no paid calls. `node tools/video/long-form/cli.mjs check` will list
`dubs.test.mjs`, `flow.mjs` and `automation.test.mjs` as receipt-bound: open the PR as a draft
and leave the receipt to an independent reviewer.

## Notes

- Split out of 2026-10-04-audio-stage-incomplete-exits, which moved `tts` and `check-audio` to
  exit 6 and taught the worker to wait on it (narration, retakes, and the dub's check, where a
  stopped check is heard again next run through `state.languages[locale].check_stopped`).
- The same exit-0-on-STOP pattern is in `render`, `assemble`, `compile`, `keyframes` and `clips`
  (each prints "stopped by the STOP file … rerun to continue" and returns `EXIT.ok`); the worker
  then says the step is done ("<stage> done" from `media()`, "frames rendered", "video
  assembled"). Status keeps those steps undone, so the next run repeats them, but the line and the
  report are wrong. Worth the same audit once `dub` has the pattern.
- 2026-10-06 (claude-opus-5-5-dub-stop-exit, branch `claude/dub-stop-exit`). Claimed with `--force`
  over 2026-10-01-hand-off-owner-approved-renewed-finals (codex-video-stall-followthrough, in
  progress since 2026-10-04T10:14Z, about 38 h, stale). It holds `tools/video/dubs/cli.mjs`, but its
  work there landed in #1208 (0afd3cc8b), and its branch
  `codex/video-approved-final-languages-20261004` was merged as #1210 (17cfb5f0c, 2026-10-04T23:41Z)
  and no longer exists on origin. What it has left is production activation, not code in this file.
- `dub` (`tools/video/dubs/cli.mjs`): the STOP branch returns `EXIT.incomplete`. A multi-locale run
  stops at the first locale that returns it and returns 6 at once, so `Math.max` across locales
  cannot mix it with another locale's 1. The locales after it are not attempted, and the "next:
  check-audio" line is not printed. `dubLocale` only returns 0, 1 or 6 (owner and vendor problems
  are thrown), so nothing outranks it.
- Worker (`makeDub` in `flow.mjs`): a new local helper `stopped(what, result)` sets
  `rounds.check_stopped`, saves the state and returns `this.later("<slug>: <l> <what> stopped
  (…); the next run continues")`. It handles `dub` right after the shortening loop (so a re-run
  inside the loop is covered), the `dub --redo` right after it runs, and the existing stopped
  check, which now goes through the same helper with the same line. The flag matters for a
  stopped retake: a retake keeps every line's words, so the old track still reads as current
  (`dubsStatus` compares hashes only), and without the flag the languages loop would skip the
  locale. With it, the next run's plain `dub` buys nothing (every take is in the cache), lays the
  track out again and hears it. A stopped retake keeps the retake round it started, as a stopped
  narration retake does (`state.retakes`).
- Tests: `dubs.test.mjs` "a STOP file ends a dub as incomplete…" covers a STOP before the first
  request (0 of 3, nothing bought), a STOP that the fake server drops while answering request 1 of
  3 under `--locale en,ja` (exit 6, request 1's takes in cache.json, no fit, timeline, narration
  or track, ja not started, no "next:"), a rerun with the STOP still there (0 of 2), and a rerun
  without it (exit 0, exactly 2 more requests). Then a `--redo` of lines in two requests is stopped
  after the first: fit, timeline, narration and track are byte-identical, and the plain rerun buys
  nothing. `automation.test.mjs` "a STOP file that ends a dub or its retake…" stops `dub`, then
  `dub --redo`, and checks the run lines, `check_stopped`, `retakes`, and that the third step
  ends "ja dub made after 1 retake". With the worker change disabled, both tests fail: the old
  code blocks with "dub ja failed" and "dub ja retake failed". With `EXIT.ok` restored in `dub`,
  the dub test fails on its first exit code.
- Docs: `dub` is named beside `tts` and `check-audio` in the exit-6 lists in the `tools/video/cli.mjs`
  help, `docs/videos/DESIGN.md` and `.agents/skills/youtube-video/references/automated.md`, and
  `docs/videos/DUBS.md` gains a paragraph on STOP. `docs/videos/AUTOMATION.md` §語言 item 2 names
  `dub` and `dub --redo` beside `check-audio --locale`. All five were added to the scope. The
  AUTOMATION.md edit waited until train #1315 had landed, since it rewrote line 153 just above and
  git treats edits on adjacent lines as a conflict (checked with `git merge-file`); #1312 and #1301
  closed with it. There is no `.claude/skills` copy of `automated.md` (only SKILL.md is mirrored).
- Follow-up: 2026-10-06-render-assemble-compile-look-keyframes-and holds the audit from the note
  above (render, assemble, compile, look, keyframes, clips).
- `npm run test:tools` on this Windows machine: 1767 of 1775 pass, 3 fail, the rest skipped. The
  3 are the known Windows red "a second transcript clears a line only Gemini misheard", the
  receipt test "the shipped independent duration review binds…" (expected: the receipt-bound files
  above wait for an independent increment), and `tools/reference-analysis.test.mjs` "--compare
  matches the measured cuts…". That last one has nothing to do with this change: it is ffmpeg on
  Windows, it fails alone too, and CI on main is green. Draft PR #1323 files it as
  2026-10-06-reference-analysis-compare-range-4-6.
