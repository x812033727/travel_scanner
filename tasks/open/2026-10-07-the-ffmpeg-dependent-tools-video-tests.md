---
id: 2026-10-07-the-ffmpeg-dependent-tools-video-tests
title: The ffmpeg-dependent tools tests run in no required job, and some in no job at all
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T05:03:42Z
completed_at:
branch:
depends_on: []
scope:
  - .github/workflows/ci.yml
  - .github/workflows/video-tooling.yml
  - .github/BRANCH_PROTECTION.md
  - .agents/skills/dev-and-ci/SKILL.md
  - .claude/skills/dev-and-ci/SKILL.md
  - tools/docs-videos-tests.test.mjs
  - tools/reference-analysis.test.mjs
---

# The ffmpeg-dependent tools tests run in no required job, and some in no job at all

## Why

`npm run test:tools` runs in ci.yml's web-checks job, which has no ffmpeg, so the cases that
need it skip there. On 2026-10-07, run without ffmpeg on PATH it skipped 12: 3 that need
something else (the API runtime, two `VIDEO_RENDER_BROWSER_TESTS` cases) and 9 that need
ffmpeg:

- the six in `tools/reference-analysis.test.mjs` (its skip text says "the main CI job has
  none"), which test `.agents/skills/youtube-video/scripts/reference_analysis.mjs`. No workflow
  runs them with ffmpeg: video-tooling.yml's test step globs `tools/video/**` only.
- the H.264 concat case in `tools/video/review/renewal-handoff.test.mjs`, the brightness-probe
  case and the end-to-end part of `tools/video/shorts/from-drama.test.mjs` (which also needs
  Chromium). These run for real only in `.github/workflows/video-tooling.yml`, which is
  path-filtered to `tools/video/**`, `package.json` and the lockfile and is not a required
  check.

So a change to the reference-analysis script never runs its ffmpeg cases anywhere, and a change
outside `tools/video/**` that breaks the others merges green. With ffmpeg on PATH, 4 skip (3
once Chromium is present too).

2026-10-07-run-the-tests-under-docs-videos added a required `docs-videos` job that already
installs ffmpeg with libx264 for the docs/videos tests. It could carry these too.

## Definition of done

- [ ] Every test under tools/ that skips without ffmpeg runs, on every pull request, in a job the
      required `web` gate waits for, and a red one fails the PR.

## Steps

- [ ] Confirm the list above: run `npm run test:tools` with and without ffmpeg on PATH and
      compare what skips.
- [ ] Run those files again in the `docs-videos` job (renamed, e.g. `video-tests`; keep
      `tools/docs-videos-tests.test.mjs`, `.github/BRANCH_PROTECTION.md` and both dev-and-ci
      SKILL.md copies in step with the new name). Making video-tooling.yml's test step required
      is not enough on its own: it does not run `tools/reference-analysis.test.mjs`. Chromium
      for from-drama's end-to-end part costs about a minute more; say whether it is in or out.
- [ ] Update the "main CI job has none" skip text in `tools/reference-analysis.test.mjs` and the
      header of video-tooling.yml so they stay true.

## How to verify

Break an assertion in one of the ffmpeg cases in `tools/reference-analysis.test.mjs`: the PR's
`web` check goes red (today nothing does).

## Notes

- Filed 2026-10-07 by claude-opus-5-5-docs-ci; the judge panel for the docs/videos CI ticket
  flagged it, and all three designs left it out of that ticket's scope.
