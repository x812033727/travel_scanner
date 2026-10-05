---
id: 2026-10-04-audio-stage-incomplete-exits
title: Audio stages distinguish incomplete runs and chapter failures from success
status: done
priority: P2
area: tools
owner: claude-opus-5-5-audio-stage-incomplete-exits
claimed_at: 2026-10-05T01:44:27Z
created_at: 2026-10-04T18:01:08Z
completed_at: 2026-10-05T02:25:08Z
branch: claude/audio-stage-incomplete-exits
depends_on: []
scope:
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/cli.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/dubs/dubs.test.mjs
  - docs/videos/DESIGN.md
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video/references/automated.md
  - .agents/skills/animation-production/scripts/drama_preflight.mjs
  - .agents/skills/animation-production/references/stage-preconditions.md
---

# Audio stages distinguish incomplete runs and chapter failures from success

## Why

The normal TTS command returns exit 0 when a STOP file interrupts its pending synthesis loop before the current timeline and narration are assembled. It also only prints chapter timing problems before returning 0. The audio-check command similarly returns 0 on STOP before producing a complete check summary. An orchestrator that treats exit 0 as completion can advance an interrupted or invalid audio stage. Existing clips and partial transcripts should remain reusable, but success must distinguish them from complete, valid current audio.

## Definition of done

- [x] Interrupted TTS and audio-check runs have an explicit incomplete outcome and cannot be reported as completed current audio.
- [x] Chapter timing failures prevent terminal TTS success; complete valid audio retains the normal successful outcome.
- [x] Existing caches, partial transcripts, source hashes and paid-request uncertainty evidence remain intact; the change does not widen re-recording or retry paid requests.

## Steps

- [x] Coordinate with the existing active narration-cache ticket before claiming overlapping CLI/test paths.
- [x] Add focused offline fixtures for STOP before assembly, chapter timing failure, STOP before full audio-check summary and complete successful runs.
- [x] Correct the outcome contract and update only consumers necessary to preserve safe resumability.

## How to verify

Run the focused tests for tools/video/tts/tts.test.mjs and tools/video/tts/check.test.mjs. Mock providers so the fixtures incur no paid calls. Verify that retained partial caches can resume safely, chapter errors are distinguishable from success, and complete valid runs still return 0. Do not change provider models, budgets or authorization gates.

## Notes

- Read-only observation at prepared Embedding HEAD 00332287b23e353e4f4ad262fdeaa256b1f5518b: cli.mjs:335-337 returns EXIT.ok on STOP before its narration/timeline assembly at 374-380; line383 merely prints checkChapters problems before the unconditional success at386. check.mjs:262-264 returns EXIT.ok on STOP before the summary/flags/recordStage block at379-396. This is a code-contract finding; no interrupted paid run was manufactured to reproduce it.
- Existing task 2026-10-03-video-worker-narration-takes-made-stale is in-progress under claude-opus-5-5 and scopes cli.mjs and tts.test.mjs. This follow-up is deliberately unclaimed; preserve that ownership and coordinate before implementation.
- The active Embedding producer separately verifies actual current narration/timeline, all156 clips and audio-check coverage instead of treating exit0 as sufficient. No shared audio implementation was changed by filing this task.

### 2026-10-05, claude-opus-5-5-audio-stage-incomplete-exits

- Coordination: the narration-cache ticket's claim (2026-10-03-video-worker-narration-takes-made-stale)
  and every other claim on `flow.mjs`/`automation.test.mjs` were released by the board sweep #1231
  (8e8598cf0); its code had landed as #1182 (cf9e04ead). The claim went through without `--force`.
  No open PR or sibling worktree branch touched these files.
- Contract: `EXIT.incomplete = 6` in `tools/video/cli.mjs` (help, DESIGN.md, AUTOMATION.md and the
  skill's `references/automated.md` list it). `tts` returns it when the STOP file ends the request
  loop (takes so far stay in `audio/cache.json` with their SHA-256; `timeline.json`,
  `narration.wav` and the stage record are not written); `check-audio` returns it when the STOP file
  ends the transcript loop (each transcript is already cached; no Jev call, no flags file, no
  stage record).
- Chapters: after `narration.wav` and `timeline.json` are written, `tts` checks the chapters of the
  cut the first build would make (`presentationTimeline` with `selectBrandingForBuild`, the same
  choice `assemble` makes), so a body chapter that the channel intro or outro lengthens is not a
  false failure. Problems record the run with `ok: false, chapters: [...]` (the paid characters
  stay on record), print last, and exit 1. A rerun synthesizes nothing. Videos whose chapters fail
  this way would already have been blocked by `captions` (it checks the same presented chapters);
  the failure now comes before the narration review, render and assemble.
- Worker: exit 6 from `tts` (narration step and both retake loops) and from `check-audio` (narration
  and a dub's check) is `this.later`, never a block, report or review push. A dub whose check was
  stopped is current by its files, so `state.languages[locale].check_stopped` makes the next run
  check it again; the success path deletes the entry. A chapter failure stays a block (as every
  non-zero `tts` was), and its reason is the chapter.
- Tests: the tts and check fake servers now speak 200 ms a character (the voices' 300 a minute;
  at 60 ms every fixture's chapters ran 5–7 s). `dubs.test.mjs` keeps its 60 ms pace, which its fit
  windows are tuned to, and accepts a tts exit 1 that names only chapters (`narrate()` helper);
  hence that file in the scope. The same-duration retake test adds its copy line to the scene
  instead of replacing the scene, so the chapter keeps 10 s.
- Scope beyond the four tts files, and why: `tools/video/cli.mjs` (the exit code), `flow.mjs` and
  `automation.test.mjs` (the worker waits on it), `dubs.test.mjs` (above), the three docs that list
  the exit codes, and the animation-production skill's `drama_preflight.mjs` `EXIT` mirror and
  its reference, which `tools/animation-production.test.mjs` requires to equal `cli.mjs`'s.
- Measured with throwaway probes (not committed): at 60 ms a character the fixtures' chapters were minimal
  5.1/5.1/5.5 s, drama 6.7/6.1/5.1 s, illustrated 5.3–9.1 s; at 200 ms all are 12–31.8 s. The 26
  videos in `docs/videos/` have estimated shortest chapters of 11.9–86.9 s (usually the hook).
- Left for follow-ups: 2026-10-05-dub-exits-incomplete-when-a-stop (`dub` still returns 0 on
  STOP, and render/assemble/compile/keyframes/clips do too),
  2026-10-05-a-narration-retake-a-stop-file (a retake stopped between two paid requests leaves takes
  the timeline does not bind, and the next run's evidence guard blocks; fail-safe, as before),
  2026-10-05-the-worker-passes-over-a-video (a video held by its own STOP file now ends each round
  after one unit; before, the worker spent the round on it or sent unchecked audio).
- Checks on Windows: `tts.test.mjs` 26/26; `check.test.mjs` + `dubs.test.mjs` 30/31 (the known
  Windows-only "a second transcript clears a line only Gemini misheard"); `npm run test:tools`
  1626/1633 with 4 red: that same test, "nginx detector never misses an early marker" (a 90 s
  timeout, red when run alone too, in `tools/nginx-install.test.mjs`, nothing here touches it),
  the duration receipt test (expected: `cli.mjs check` lists `automated.md`, `DESIGN.md`,
  `automation.test.mjs`, `flow.mjs`, `dubs.test.mjs`, `check.test.mjs`, `tts.test.mjs` for an
  independent DURATION_ONLY increment), and the animation-production `EXIT` mirror, fixed after
  that run started and green when rerun.
