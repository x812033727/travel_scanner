---
id: 2026-10-07-the-ffmpeg-dependent-tools-video-tests
title: The ffmpeg-dependent tools tests run in no required job, and some in no job at all
status: done
priority: P3
area: tools
owner: claude-opus-5-5-ffmpeg-ci
claimed_at: 2026-10-07T06:04:38Z
created_at: 2026-10-07T05:03:42Z
completed_at: 2026-10-07T06:28:46Z
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
  - docs/videos/DESIGN.md
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

- [x] Every test under tools/ that skips without ffmpeg runs, on every pull request, in a job the
      required `web` gate waits for, and a red one fails the PR.

## Steps

- [x] Confirm the list above: run `npm run test:tools` with and without ffmpeg on PATH and
      compare what skips.
- [x] Run those files again in the `docs-videos` job (renamed, e.g. `video-tests`; keep
      `tools/docs-videos-tests.test.mjs`, `.github/BRANCH_PROTECTION.md` and both dev-and-ci
      SKILL.md copies in step with the new name). Making video-tooling.yml's test step required
      is not enough on its own: it does not run `tools/reference-analysis.test.mjs`. Chromium
      for from-drama's end-to-end part costs about a minute more; say whether it is in or out.
- [x] Update the "main CI job has none" skip text in `tools/reference-analysis.test.mjs` and the
      header of video-tooling.yml so they stay true.

## How to verify

Break an assertion in one of the ffmpeg cases in `tools/reference-analysis.test.mjs`: the PR's
`web` check goes red (today nothing does).

## Notes

- Filed 2026-10-07 by claude-opus-5-5-docs-ci; the judge panel for the docs/videos CI ticket
  flagged it, and all three designs left it out of that ticket's scope.
- Done 2026-10-07 by claude-opus-5-5-ffmpeg-ci.
  - Measured (TAP, Node 22 and 24, Chromium hidden as in web-checks): without ffmpeg 9 tools
    cases skip for it: the six in `tools/reference-analysis.test.mjs`, the H.264 concat case in
    `review/renewal-handoff.test.mjs`, the brightness probe and the end-to-end Short in
    `shorts/from-drama.test.mjs` (which also needs Chromium). With ffmpeg and Chromium only three
    skip, none for a media tool: the API runtime case and the two `VIDEO_RENDER_BROWSER_TESTS`
    browser regressions.
  - ci.yml's `docs-videos` job is now `video-tests`: it installs ffmpeg and Chromium (`npx
    playwright install --with-deps chromium`, as web-e2e does), runs `npm run test:docs-videos`,
    then every tools test again on `test:tools`' own globs with a TAP copy in `$RUNNER_TEMP`, and
    fails when a skip there still names ffmpeg or Chromium. So any future test that needs either
    tool runs in a required check with no list to keep. The required `web` gate waits for it.
  - The reporters are on the command line: `NODE_OPTIONS=--test-reporter=tap` was tried first
    and breaks the tests that start their own `node --test --test-reporter=tap`
    (`tools/claude-code-series.test.mjs`: "--test-reporter must match the number of
    --test-reporter-destination"). Node 24, which CI uses, prints spec without a TTY, hence the
    explicit TAP destination.
  - `tools/docs-videos-tests.test.mjs` checks the job: ffmpeg and Chromium installed, both suites
    run, the tools globs equal `test:tools`', the TAP copy and the skip check present, the gate
    waiting. Each of those removed or narrowed turns it red (checked one by one).
  - The step was run locally as written: Node 24, ffmpeg present, Chromium hidden: exit 1 on the
    from-drama skip; with Chromium (the local build under the name Playwright expects): exit 0,
    2023 tests, 3 skipped.
  - video-tooling.yml keeps its `node --test "tools/video/**/*.test.mjs"` step (it is not
    required and path-filtered; dropping it would save about two minutes on the pull requests
    that touch tools/video). Its header now says what runs where.
  - Not run in CI yet: the first run of this branch shows the job's real duration (estimated 4 to
    5 minutes: npm ci, the two installs, about 15 s of docs/videos tests and 2 minutes of tools
    tests), which should stay under web-e2e's 5 minutes.
- From the independent review (two reviewers, both "ship"): the two browser regressions in
  `tools/video/render/browser.test.mjs` run only with `VIDEO_RENDER_BROWSER_TESTS=1` and ran in no
  workflow; the video-tests step now sets it (they pass, about 7-14 s), so with ffmpeg and Chromium
  only the API-runtime case skips (2028 tests, Node 24, run locally as written). The guard also
  pins the step's flags (only `--test` and the reporters: a `--test-name-pattern` would leave the
  tests it drops out of the TAP copy, unseen by the skip check) and no `continue-on-error`.
  `docs/videos/DESIGN.md` said every tools/video test is pure and needs neither tool; corrected
  (scope widened; it is bound by the duration receipt, so the branch gets an independent re-bind).
  video-tooling.yml's header now names its real path filter.
