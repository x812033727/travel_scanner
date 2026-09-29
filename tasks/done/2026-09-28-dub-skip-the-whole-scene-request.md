---
id: 2026-09-28-dub-skip-the-whole-scene-request
title: dub: skip the whole-scene request when its split keeps failing, so a track is not paid for twice
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-28T06:52:56Z
created_at: 2026-09-28T06:26:14Z
completed_at: 2026-09-28T06:54:38Z
branch:
depends_on: []
scope:
  - tools/video/dubs
---

# dub: skip the whole-scene request when its split keeps failing, so a track is not paid for twice

## Why

`dub` sends one request per scene, cuts the returned audio at its silences, and when the pieces
do not look like the lines (`plausibleSplit`), synthesizes every line of that scene again on its
own (`synthesizeRequest` in `tools/video/tts/synthesis.mjs`). Both calls are billed. On the
2026-09-28 English dub of `gpt6-vs-opus55-worth-paying`, 7 of 13 scene requests fell back, and
the track cost 8,895 billable characters for about 5,800 characters of script; the incident
video's English track cost 7,605. With a monthly Gemini allowance, that is most of a video's dubs.

`dub --redo` with every line listed does NOT avoid it: `retakes` only goes line by line when some
of a scene's lines are still current, so a scene with no clips yet is still sent whole. The same
day, five clips from passed-but-wrong splits carried a neighbouring line (a Whisper transcript
showed it), which the fit report exposed as lines "spoken" at 0.4-0.6x the track's rate.

## Definition of done

- [x] A dub track costs about its script's characters once, whether or not the split works:
      `dub --line-by-line` sends one request a line (opt-in; the default is unchanged).

## Steps

- [x] Decided on an opt-in flag first: `--line-by-line` in `tools/video/dubs/cli.mjs`, documented in
      `docs/videos/DUBS.md` and the CLI usage, tested in `dubs.test.mjs` (fails without the change).

## How to verify

```bash
node tools/video/cli.mjs dub --slug <slug> --locale en --dry-run   # the estimate should match what a real run bills
```

## Notes

- Follow-ups, not done here: make `--line-by-line` the dub default once a few tracks confirm
  per-line prosody is fine; leave narration (`tts`) as it is unless the same numbers show up there.

- `--redo` still retakes only the listed lines; with `--line-by-line` a fully new scene also goes
  line by line.
- A clip whose rate is far below the track's measured rate (`fit.json` `over[].seconds` against
  `rates.measured`) is usually a bad split, not a long translation: retake it before shortening.
