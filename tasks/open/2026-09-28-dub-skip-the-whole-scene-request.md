---
id: 2026-09-28-dub-skip-the-whole-scene-request
title: dub: skip the whole-scene request when its split keeps failing, so a track is not paid for twice
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T06:26:14Z
completed_at:
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

Passing `dub --redo` a file that lists every line skips the scene request and goes straight to
one request per line (the `retakes` path), which costs the script once. That worked as a manual
workaround the same day.

## Definition of done

- [ ] A dub track costs about its script's characters once, whether or not the split works.

## Steps

- [ ] Decide between synthesizing dubs line by line always, or remembering per locale that splits
      fail (the fallback rate is recorded in `state.json` by `recordStage`) and going line by line
      when they do.
- [ ] Keep narration (`tts`) as it is unless the same numbers show up there.

## How to verify

```bash
node tools/video/cli.mjs dub --slug <slug> --locale en --dry-run   # the estimate should match what a real run bills
```

## Notes

- Workaround: `{"flags": [every line id]}` as `--redo`; a script that lists only lines with no clip yet
  keeps already-made clips.
