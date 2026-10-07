---
id: 2026-10-07-run-the-tests-under-docs-videos
title: Run the tests under docs/videos in CI so the imported-language runner cannot drift unnoticed
status: done
priority: P3
area: tools
owner: claude-opus-5-5-docs-ci
claimed_at: 2026-10-07T04:23:48Z
created_at: 2026-10-07T03:55:50Z
completed_at: 2026-10-07T05:06:47Z
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - package.json
  - .github/workflows/ci.yml
  - tools/docs-videos-tests.test.mjs
  - .github/BRANCH_PROTECTION.md
  - AGENTS.md
  - .agents/skills/dev-and-ci/SKILL.md
  - .claude/skills/dev-and-ci/SKILL.md
  - .agents/skills/dev-and-ci/scripts/run-checks.sh
---

# Run the tests under docs/videos in CI so the imported-language runner cannot drift unnoticed

## Why

`npm run test:tools` globs `tools/**`, so `docs/videos/**/*.test.mjs` (the imported-language
runner, its speech journal, the language batch tooling: 126 tests in
`docs/videos/imported-long-languages` alone) runs in no CI job. Two of its tests went red when
#1342 changed how `makeDub` reports an exit 4, and stayed red for two days until
2026-10-05-imported-language-runner-test-still-expects was fixed by hand.

## Definition of done

- [x] CI runs `docs/videos/**/*.test.mjs` on every pull request, in an existing job or a new one,
      and a red test there fails the PR.

## Steps

- [x] Time `node --test docs/videos/**/*.test.mjs` on Linux (about 20 s for the runner file; the
      native speech fixtures need ffmpeg) and decide whether it joins `test:tools` or gets its own
      script and job.
- [x] Check that nothing under `docs/videos` needs a network or a token (the runner tests stub HTTP).

## How to verify

A deliberately broken assertion in `docs/videos/imported-long-languages/runner.test.mjs` turns the
PR red; reverting it turns it green.

## Notes

- Filed 2026-10-07 by claude-opus-5-5-runner-test.
- Done 2026-10-07 by claude-opus-5-5-docs-ci, from a three-design judge panel (fold into
  web-checks; a separate job; a separate job plus a guard test). Both judges picked the third.
  - `npm run test:docs-videos` is `node --test "docs/videos/*.test.mjs"
    "docs/videos/**/!(demo)/*.test.mjs"`: node expands the quoted globs (no `--test-exclude`
    exists, and a leading `!` is ignored), so any new folder at any depth runs with no edit,
    and a test whose own folder is named `demo` never does. Those are video props whose
    acceptance tests fail on purpose (`docs/videos/ai-bug-fix-pr-review/demo/README.md`).
    Today it selects 8 files and 199 tests, about 15-28 s on 4 cores.
  - A new ci.yml job, `docs-videos`, installs ffmpeg (retried, and checked for libx264, which
    `tools/video/assemble/ffmpeg.mjs` requires) and runs the script; the required `web` gate
    waits for it. ffmpeg stays out of web-checks: there it would change which tools/video cases
    `test:tools` runs. Six runner cases need ffmpeg and fail with ToolMissing rather than skip
    without it, which is deliberate: a lost install cannot pass quietly.
  - `tools/docs-videos-tests.test.mjs` (in web-checks through `tools/*.test.mjs`) fails when the
    glob misses a test under docs/videos, selects a demo prop, or the job or gate wiring is
    undone. Checked: dropping `docs-videos` from the gate's needs, or installing sox instead of
    ffmpeg, turns it red.
  - Nothing under docs/videos needs a network or a token: a run in a network namespace with only
    loopback and no proxy variables passes 199 of 199.
  - How to verify, done locally: changing `"137"` to `"138"` at `runner.test.mjs:753` makes
    `npm run test:docs-videos` exit 1; reverting it exits 0. In the first CI run, check that the
    job's log shows 199 tests and no demo file, and that the `web` gate's echo lists four results.
  - `!(demo)` in an interactive bash triggers history expansion ("event not found"); run it
    through `npm run`.
- The ffmpeg-dependent tools tests still run in no required job: the concat, brightness-probe
  and from-drama cases only in the path-filtered, non-required video-tooling.yml, and the six
  in `tools/reference-analysis.test.mjs` in no workflow at all:
  2026-10-07-the-ffmpeg-dependent-tools-video-tests.
