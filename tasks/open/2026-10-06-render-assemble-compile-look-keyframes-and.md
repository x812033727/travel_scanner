---
id: 2026-10-06-render-assemble-compile-look-keyframes-and
title: render, assemble, compile, look, keyframes and clips exit incomplete when a STOP file ends them
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-06T00:08:13Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
  - tools/video/compile/cli.mjs
  - tools/video/compile/compile.test.mjs
  - tools/video/media/look.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/cli.mjs
  - docs/videos/AUTOMATION.md
  - docs/videos/DESIGN.md
  - .agents/skills/youtube-video/references/automated.md
---

# render, assemble, compile, look, keyframes and clips exit incomplete when a STOP file ends them

## Why

`tts`, `check-audio` and (since 2026-10-05-dub-exits-incomplete-when-a-stop) `dub` return exit 6
(`EXIT.incomplete` in `tools/video/cli.mjs`) when a STOP file ends them before they finish, and
the worker waits for the next run. The other long stages still print "stopped by the STOP file …
rerun to continue" and return exit 0:

- `render` (`tools/video/render/cli.mjs`, "after N new states");
- `assemble` (`tools/video/assemble/cli.mjs`, "after N segments");
- `compile` (`tools/video/compile/cli.mjs`, "after N cards" and "before the join");
- `look` (`tools/video/media/look.mjs`, "after N new sheets");
- `keyframes` (`tools/video/media/keyframes.mjs`, "before the style plate" and "after N new keyframes");
- `clips` (`tools/video/media/clips.mjs`, "after N new clips" and "before <scene> was judged").

The worker reads that exit 0 as done. `media()` in `tools/video/automation/flow.mjs` clears the
stage's failure count and prompt fixes and reports "<stage> done" to the site; the "frames
rendered" and "video assembled" branches log the step as done, and "video assembled" also reports it
and may send the episode recap. Status keeps those steps undone, so the next run repeats them, but
the log line, the site report and the recap are wrong.

## Definition of done

- [ ] Each of these stages exits 6 when a STOP file ends it before its output is complete, keeps
      what it paid for or drew, and writes nothing that reads as current.
- [ ] The worker treats exit 6 from any of them as "the next run continues" (`this.later`). It does
      not report the step as done, clear its counters, send a recap, block the video or start a
      prompt fix.
- [ ] The exit-code lists name every stage that can exit 6: the `tools/video/cli.mjs` help,
      `docs/videos/DESIGN.md` and `.agents/skills/youtube-video/references/automated.md`.

## Steps

- [ ] For each stage, an offline test with a fake that writes the STOP file mid-run: exit 6, the
      cache is kept, and the rerun does only the rest. `compile.test.mjs`, `clips.test.mjs` and
      `look-keyframes.test.mjs` already have STOP cases that match the message: make them assert
      exit 6 too.
- [ ] Return `EXIT.incomplete` from each STOP branch listed under Why.
- [ ] In `flow.mjs`, map exit 6 to `this.later` in `media()` and in the "frames rendered" and
      "video assembled" branches, with a test in `automation.test.mjs` for each.
- [ ] `docs/videos/AUTOMATION.md` says, for the narration (item 3) and the dub (§語言 item 2), that
      a STOP ends the round with exit 6 and the next run continues. Add the same sentence where
      it describes the media stages, the render and the cut.

## How to verify

Use mock providers only, with no paid calls:

```bash
node --test tools/video/render/render.test.mjs tools/video/assemble/assemble.test.mjs tools/video/compile/compile.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/media/clips.test.mjs tools/video/automation/automation.test.mjs
node tools/video/long-form/cli.mjs check
```

`cli.mjs check` will list the receipt-bound files you changed. Open the PR as a draft and leave the
duration receipt to an independent reviewer.

## Notes

- Split out of 2026-10-05-dub-exits-incomplete-when-a-stop, whose Notes named these stages. That
  ticket moved `dub` and `dub --redo` to exit 6 and taught the worker's `makeDub` to wait on it,
  with a local `stopped()` helper. `media()` and the render and assemble branches need the same
  treatment.
- A STOP can also arrive while a media job runs on the server. `media/client.mjs` then throws a
  MediaError with code "stopped" (`media/stages.mjs` has `stoppedError()`), and `clips.mjs` and
  `keyframes.mjs` catch it in several places. Every one of those paths needs the same exit 6, not
  only the messages listed under Why.
