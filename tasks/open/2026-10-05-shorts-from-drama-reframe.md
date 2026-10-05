---
id: 2026-10-05-shorts-from-drama-reframe
title: shorts from-drama: reframe an approved 16:9 drama cut to 9:16 following the subject
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:25Z
completed_at:
branch:
depends_on:
  - 2026-10-05-media-locate-subject-boxes
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

- [ ] `from-drama --slug <episode> --from <s> --to <s> --workdir …` reads the approved
      `final.mp4`, `timeline.json` and `upload/zh-TW.srt`, asks `locate` once per shot keyframe
      (or an extracted frame), and writes a 1080×1920 cut whose per-shot crop window follows the
      box with linear moves between shots (`crop=608:1080:x='…'`, `scale=1080:1920`).
- [ ] The zh-TW cues are drawn by the Shorts caption layer (HTML captions, as the karaoke
      ticket does), never by libass, inside the Shorts safe area (bottom ≤ 1600, sides 78/178).
- [ ] It writes `checks.json` with a measured `layout`, so `layout` can pass (unlike `import`);
      `check-audio`, `qa`, `package`, `push` then run as for any build (`line: "drama"`, `source.slug`).
- [ ] A lavfi-made stand-in episode runs through the test end to end.

## Steps

- [ ] `from-drama.mjs`: shot spans from the timeline, boxes, crop expressions, caption layer,
      checks; `cli.mjs` subcommand; tests with lavfi media.
- [ ] Docs: `SHORTS.md` §三條內容線 (drama row), `references/shorts.md`.

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
