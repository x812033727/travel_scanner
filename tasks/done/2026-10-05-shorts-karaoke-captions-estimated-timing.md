---
id: 2026-10-05-shorts-karaoke-captions-estimated-timing
title: Shorts karaoke captions: highlight the phrase group being spoken, with estimated character timing
status: done
priority: P1
area: tools
owner: claude-fable-5-1-karaoke
claimed_at: 2026-10-05T15:51:38Z
created_at: 2026-10-05T15:50:53Z
completed_at: 2026-10-05T16:06:50Z
branch: claude/shorts-karaoke-captions
depends_on: []
scope:
  - tools/video/shorts/build.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/motion.mjs
  - tools/video/shorts/layouts.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/cli.mjs
  - tools/video/shorts/smoke.mjs
  - tools/video/shorts/karaoke.mjs
  - tools/video/shorts/karaoke.test.mjs
  - tools/video/shorts/motion.test.mjs
  - tools/video/shorts/core.test.mjs
  - tools/video/shorts/pipeline.test.mjs
  - docs/videos/SHORTS.md
  - .agents/skills/youtube-video/references/shorts.md
---

# Shorts karaoke captions: highlight the phrase group being spoken, with estimated character timing

## Why

A Short's caption bar shows the whole phrase at once (`tools/video/shorts/core.mjs` `sceneHtml`,
`.caption`): one transparent card per phrase, held for the phrase's frames. Viewers of
vertical video expect the words to light up as they are spoken; that is what the outside
Shorts generators do with Remotion components fed by per-word timestamps (the research of
2026-10-05, `video-tooling-research-2026-10-05.md`), and what we cannot copy because of
Remotion's company licence and the GPL caption tools.

Two facts shape the in-house version:

- Nothing in the pipeline knows character timing. The server returns WAV bytes only
  (`apps/api/app/video_speech`), Gemini TTS has no timestamps, and the Azure path is REST
  without `WordBoundary`. Ticket `2026-10-05-speech-align-character-timing` adds that; until
  then the timing is estimated inside each phrase, whose clip duration is measured exactly.
- A per-frame renderer is the wrong tool: a 1080p screenshot costs 0.35–0.55 s on Edge /
  Windows ARM64 (`tasks/done/2026-10-02-video-render-stills-differ-run-to.md`). The caption
  only changes when the highlighted group changes, so it is one small transparent PNG per
  group state, laid over the card as its own ffconcat overlay, inside the Shorts motion
  pipeline that already exists (`motion.mjs` `cardsList` / `segmentArgs`).

Decisions: the highlight is per phrase group (6–10 display units, never inside a Latin word
or a number), colour only (no scale, so the layout never moves); the CC file stays one cue
per phrase (YouTube CC has no per-word timing); the default stays `plain` until the owner
has seen a sample, because Shorts are auto-approved on the site.

## Definition of done

- [x] `build --captions karaoke` produces a `final.mp4` whose caption bar highlights the group
      being spoken, group by group, and writes `timing.json` beside `timeline.json` with every
      group's `start`/`end` seconds and `source: "estimated"`.
- [x] `build --captions plain` (the default while `VIDEO_SHORTS_CAPTIONS` is unset) produces
      ffmpeg arguments and card markup identical in shape to today's: the existing
      `motion.test.mjs` and `core.test.mjs` assertions pass unchanged.
- [x] `upload/zh-TW.srt` stays one cue per phrase; the `captions` and `layout` QA items keep
      their pass rules; `checks.json.captions` records `{style, source, groups, states, version}`
      and the `captions` item carries a warning (not a failure) while `source` is `estimated`.
- [x] `node tools/video/shorts/smoke.mjs` runs the karaoke build in CI and asserts the new fields.

## Steps

- [x] `tools/video/shorts/karaoke.mjs` + `karaoke.test.mjs`: tokens, lines, groups, weights,
      speech span from the PCM, group times, states; `timingFile`.
- [x] `core.mjs`: `captionText` option on `sceneHtml`, `captionHtml` for the layer; `core.test.mjs`.
- [x] `motion.mjs`: `MOTION_VERSION` v2, `CAPTION_ORIGIN`, `captionsList` input in `segmentArgs`; `motion.test.mjs`.
- [x] `build.mjs`: the option and env default, `karaoke.mjs` in `codeHash`, the caption pass in
      `renderFrames`, one captions list per scene, `timing.json`, `checks.json.captions`.
- [x] `qa.mjs`: `timing.json` in the input bindings, the warning on estimated timing; `pipeline.test.mjs`.
- [x] `cli.mjs` `--captions`; `smoke.mjs` builds with karaoke and checks the new fields.
- [x] `docs/videos/SHORTS.md` and `references/shorts.md`: the layer, the switch, the 15-unit
      caption line, the known drift of estimated timing.

## How to verify

```bash
node --test tools/video/shorts/*.test.mjs
node tools/video/shorts/smoke.mjs --workdir /tmp/shorts-smoke        # add --channel msedge on Windows ARM64
npm run test:tools
node tools/video/long-form/cli.mjs check                               # PASS: no receipt-bound file in scope
# look at it, every half second:
ffmpeg -i <build>/upload/final.mp4 -vf "select='not(mod(n\,15))'" -fps_mode vfr /tmp/k-%03d.png
```

## Notes

- Technique only: group highlight as the CapCut / VideoCaptioner style captions do; no code
  read from VideoCaptioner or pyvideotrans (GPL) or from any Remotion component.
- Server setting for the style is deferred: it needs a migration, `video_shorts/{schemas,settings}.py`,
  the admin form and the five receipt-bound `admin.json` files. The switch is the CLI flag or
  `VIDEO_SHORTS_CAPTIONS` on the worker host; the owner flips it after seeing a sample.
- Overlaps declared, all unclaimed: `2026-09-28-sothatswhy-shorts-from-episode` (whole `shorts/`;
  its code steps are ticked), `2026-10-03-illustrated-slides-lint-heuristics-the-shorts`
  (`motion.mjs`, `SHORTS.md`; only its receipt step is left), `2026-10-05-video-docs-shorts-worker-cut-line`
  (`references/shorts.md`).
- The still-shot stepping of `zoompan` (`2026-10-04-still-shot-camera-moves-travel-in`) also
  applies to `backgroundChain` here; this ticket does not change that chain.
- Every new build is a new directory (`codeHash` covers these files and `MOTION_VERSION` is
  bumped); approved cuts on the site are bound to their `final_sha256` and stay approved.

### 2026-10-05 done (claude-fable-5-1-karaoke)

- Shipped as designed: `karaoke.mjs` (lines, groups, weights, speech span, states, `timing.json`),
  `captionHtml` + the `caption` option of `sceneHtml`, the caption layer as the last input of
  `segmentArgs` (`MOTION_VERSION` v2), `--captions` on `build` and `from-episode`, the
  `captions` warning and the `timing.json` binding in `qa`, the smoke building with karaoke.
- Measured on the smoke script (11 phrases, stand-in tones): 14 groups in 14 states, 14 state
  pictures of 820×165, every state of a two-group phrase a different picture; frames pulled from
  the final show the lit group in the theme's amber exactly over the card's white glyphs.
- 163 Shorts tests green; `npm run test:tools`, the duration receipt (`long-form/cli.mjs check`)
  and `check:tasks` run before the push.
- Default stays `plain`. To turn it on for the worker: `VIDEO_SHORTS_CAPTIONS=karaoke` on the
  host after the owner has looked at one `--captions karaoke` sample.
- Environment note for the next agent: in the cloud container the root `npm ci` installs
  Playwright 1.63, which looks for `chromium_headless_shell-1243/chrome-headless-shell-linux64/
  chrome-headless-shell`, while `/opt/pw-browsers` ships 1194 under `chrome-linux/headless_shell`;
  two symlinks (version dir and the binary path) make the smoke run without downloading. Not
  needed on the worker image or on Windows with `--channel msedge`.
- Not done here, by design: per-character highlight (needs measured timing first), a server
  setting for the style, Shorts imported from elsewhere (they carry no layer).
