---
id: 2026-10-05-shorts-from-drama-reframe
title: shorts from-drama: reframe an approved 16:9 drama cut to 9:16 following the subject
status: done
priority: P2
area: tools
owner: claude-fable-5-1-fromdrama
claimed_at: 2026-10-05T17:50:26Z
created_at: 2026-10-05T16:08:25Z
completed_at: 2026-10-05T18:24:53Z
branch: claude/shorts-from-drama
depends_on:
  - 2026-10-05-media-locate-subject-boxes
  - 2026-10-05-shorts-karaoke-captions-estimated-timing
scope:
  - tools/video/shorts/from-drama.mjs
  - tools/video/shorts/from-drama.test.mjs
  - tools/video/shorts/cli.mjs
  - docs/videos/SHORTS.md
  - .agents/skills/youtube-video/references/shorts.md
---

# shorts from-drama: reframe an approved 16:9 drama cut to 9:16 following the subject

## Why

A finished 16:9 drama episode cannot become a vertical Short today: `shorts/build.mjs`
refuses `line: "drama"`, `from-episode` keeps a fixed centre strip (31.6 % of a 16:9
picture), and the native 9:16 drama route (`2026-09-28-video-shorts-worker-drama`) is a large
ticket waiting on the drama pilot. The cheap route is post-production: cut the approved
`final.mp4` by shot, crop a 9:16 window that follows the subject box
(`2026-10-05-media-locate-subject-boxes`), and hand the cut to the Shorts QA.

## Definition of done

- [x] `from-drama --slug <episode> --from <s> --to <s> --workdir …` reads the approved
      `final.mp4`, `timeline.json` and `upload/zh-TW.srt`, asks `locate` once per shot keyframe
      (or an extracted frame), and writes a 1080×1920 cut whose per-shot crop window follows the
      box with linear moves between shots (`crop=608:1080:x='…'`, `scale=1080:1920`).
- [x] The zh-TW cues are drawn by the Shorts caption layer (HTML captions, as the karaoke
      ticket does), never by libass, inside the Shorts safe area (bottom ≤ 1600, sides 78/178).
- [x] It writes `checks.json` with a measured `layout`, so `layout` can pass (unlike `import`);
      `check-audio`, `qa`, `package`, `push` then run as for any build (`line: "drama"`, `source.slug`).
- [x] A lavfi-made stand-in episode runs through the test end to end.

## Steps

- [x] `from-drama.mjs`: shot spans from the timeline, boxes, crop expressions, caption layer,
      checks; `cli.mjs` subcommand; tests with lavfi media.
- [x] Docs: `SHORTS.md` §三條內容線 (drama row), `references/shorts.md`.

## How to verify

```bash
node --test tools/video/shorts/from-drama.test.mjs
node tools/video/shorts/cli.mjs from-drama --slug <episode> --from 62 --to 110 --workdir <VIDEO_WORKDIR>
node tools/video/shorts/cli.mjs qa --dir <build> --offline
```

## Notes

- Needs the caption layer of `2026-10-05-shorts-karaoke-captions-estimated-timing` (PR #1292);
  add it to `depends_on` once it is in `tasks/done/`.
- Does not touch `site.mjs` (P1 ticket), `import.mjs` or the native route's files.
- Reframing technique as in the open-source clippers (openshorts, cutawan: MIT); nothing copied.

### 2026-10-05 done (claude-fable-5-1-fromdrama, branch `claude/shorts-from-drama`, on top of #1294)

- `tools/video/shorts/from-drama.mjs` + `from-drama.test.mjs`, `cli.mjs from-drama`. The
  episode's captions live at `captions/zh-TW.srt` (core/stages.mjs), not `upload/zh-TW.srt`;
  the tool looks for `captions/zh-TW.srt`, `upload/captions/zh-TW.srt`, `upload/zh-TW.srt` in
  that order. A branded cut carries the channel intro before the body: the shots are read
  through `presentationTimeline(timeline, appliedBranding(checks.json))`, the clock the
  captions were written on.
- The span is cut by frame number (`trim=start_frame`), never by seeking, as the assemble
  checks pick frames. The window: one `locate` call a shot (keyframe from
  `keyframes/manifest.json` when the work directory has it, else the middle frame of the shot
  pulled with `frameArgs`), labels = the shot's character names from `video.json`, the first
  label found wins, else the surest box, else the centre; cards never ask. Hold through the
  shot, move linearly over the last `MOVE_FRAMES` = `DISSOLVE_FRAMES` (15) before a change, so
  a cut lands on the next window (a pre-cut settle; at a dissolve it hides in the blend). One
  `crop=608:1080:x='if(lt(n,…),…)'` expression over the whole span; `n` restarts at 0 after
  `trim` (verified: the test reads the window back off a luma-ramp stand-in with `signalstats`,
  within 0.5 luma of the model).
- Captions: `core.mjs captionHtml` + one appended rule for the bar's background (the theme's
  `colors.caption`; `themeOf` falls back to `lab:daily` for `drama`, a drama theme in
  `layouts.mjs` would apply automatically), `karaoke.mjs` lines/groups/timing (`--captions`
  as `build`: flag, `VIDEO_SHORTS_CAPTIONS`, else plain; plain is the same layer with no group
  lit), ffconcat list with a blank between phrases, overlaid at `CAPTION_BOX`. Each phrase is
  measured (overflow, bottom ≤ 1600, words in x 78–902); a phrase over two lines of 15 units
  (a drama cue can be 32) fails the build naming the phrase.
- Sound: the episode's mix cut with `atrim`, two-pass loudnorm to −14 LUFS; per-phrase WAVs
  cut from it for `check-audio` and the karaoke timing. `usage.json` reports no narration and
  no `stages`: `costs.py` would book a billed provider's stage calls as an unknown amount, and
  the site already meters locate on the judge budget; `checks.json.reframe.locate` has the count.
- Refusals before any call: final not approved (`approvalState`), a caption cut in half by
  `--from`/`--to` (the message gives the times that do not cut it), a span outside the
  Shorts range (the site's settings), fewer than 3 phrases, a site without
  `limits.locate_labels`. The script groups phrases into 3–12 scenes evenly itself:
  `import.mjs scriptFromImport` leaves 4 phrases in 2 scenes.
- Separate hash discipline: `REFRAME_VERSION` plus this module's own `codeHash`
  (from-drama, build, core, karaoke, layouts, motion); `build.mjs` untouched.
- Checked here: `node --test tools/video/shorts/*.test.mjs` 180 pass; `smoke.mjs` pass;
  `npm run test:tools` 1722 pass, 2 skipped (pre-existing); `long-form/cli.mjs check` PASS;
  `check:tasks`. The end-to-end test skips without ffmpeg or Chromium (the main CI job) and
  runs in `video-tooling.yml`; this container's Playwright 1.63 found `chromium-1243` under
  `/opt/pw-browsers`, so the symlink workaround of the karaoke ticket was not needed.
- Not measured live: no Gemini key here, so the first real cut should compare
  `checks.json.reframe.shots[].subject.box` with the keyframes by eye. Not done, by design:
  a window that follows a subject moving inside one shot (one locate call a shot), a worker
  step for this line (`2026-09-28-video-shorts-worker-drama`), a contact sheet (push sends
  one only when it exists), the Shorts tab drawing `reframe.shots` over the preview.
