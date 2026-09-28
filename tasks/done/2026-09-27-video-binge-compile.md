---
id: 2026-09-27-video-binge-compile
title: Video binge T4: compile command, compilation steps, qa, package and review support
status: done
priority: P1
area: tools
owner: claude-fable
claimed_at: 2026-09-27T11:44:57Z
created_at: 2026-09-27T11:43:46Z
completed_at: 2026-09-27T12:29:26Z
branch: claude/keen-hamilton-plu6kp
depends_on: []
scope:
  - tools/video/compile
  - tools/video/cli.mjs
  - tools/video/core/state.mjs
  - tools/video/core/schema.mjs
  - tools/video/qa
  - tools/video/package
  - tools/video/review
  - tools/video/core/compilation.mjs
  - tools/video/core/compilation.test.mjs
  - tools/video/core/state.test.mjs
  - tools/video/render
---

# Video binge T4: compile command, compilation steps, qa, package and review support

## Why

A finished binge series is N approved 2–4 minute cuts in N work directories. The reference
video is one two-hour upload, so the tools need a compilation: join the cuts in order with a
two-second chapter card between them, merge the five locales' captions with the right
offsets, write YouTube chapters at each episode's start, plan the title, description, tags
and thumbnail, run a compilation's own qa items, and produce an upload package the owner can
download without SSH (docs/videos/BINGE.md).

## Definition of done

- [x] `docs/videos/<series>-full/video.json` (`compilation: {series, episodes, titles, cards,
      outro}`) is a valid drama document; `stepsFor` gives it `COMPILATION_STEPS` (metadata
      planned, cards rendered, video compiled, metadata translated, final video approved,
      upload package, on YouTube) and `status` reads each from the files.
- [x] `compile --slug <series>-full` refuses an episode whose final is not approved, whose
      cut's hash moved or whose checks failed; joins video `-c copy` and rebuilds audio per
      segment (AAC 384k) with the two-second cards; writes `compile/manifest.json`,
      `final.mp4`, `captions/<locale>.srt|.vtt` merged by frame offset, `checks.json` (frames,
      audio/video drift, loudness within 1.5 LU); checks free disk first.
- [x] The chapter cards render through the existing `render` on `thumb`/`chapter` templates;
      the thumbnail draws on an episode keyframe the worker copies to
      `keyframes/thumb-source.png`.
- [x] `qa --slug <series>-full` runs the compilation's items (`kind: "compilation"`);
      `review-push --gate final` sends a 720p preview capped at 2 Mbps; `package` writes the
      upload package with `download: "upload/final.mp4"`, the episode list and the size;
      `review-push --gate publish` carries the download path.

## Steps

- [x] `core/compilation.mjs`: document builder, layout, hash, chapters, caption merge,
      description budget with the 「第 N 集」 fallback, lint.
- [x] `compile/cli.mjs`, `compile/plan.mjs`, `compile/fixture.mjs` (shared by state, qa,
      package and review tests).
- [x] `core/state.mjs`, `core/schema.mjs`, `render/cli.mjs`, `qa/*`, `package/*`,
      `review/sync.mjs`, `cli.mjs`.
- [x] Tests: `core/compilation.test.mjs`, `compile/compile.test.mjs`, additions in state,
      schema, render, qa, package and review tests.

## How to verify

```bash
node --test tools/video/core/compilation.test.mjs tools/video/compile/compile.test.mjs tools/video/core/state.test.mjs tools/video/qa/*.test.mjs tools/video/package/*.test.mjs tools/video/review/*.test.mjs
npm run test:tools
```
A real join needs ffmpeg: on the host, `compile --dry-run` prints the layout and the disk it
needs without writing anything.

## Notes

- 2026-09-27: done on `claude/keen-hamilton-plu6kp`. Video is joined with `-c copy`, so
  every episode must have been cut with the same encoder version; `compile` refuses a mix
  and says which episode to re-assemble.
- The audio is not re-normalised: each episode already sits at −14 LUFS, so the join only
  checks the whole stays within 1.5 LU and reports the number.
- Two hours of 1080p is 5–10 GB and does not go through the review file area; the final
  gate sends a 720p preview (`-crf 28 -maxrate 2M -bufsize 4M`, under 2 GB) and the owner
  downloads the 1080p cut from `/admin/videos` through the API's read-only `video_work`
  mount.
