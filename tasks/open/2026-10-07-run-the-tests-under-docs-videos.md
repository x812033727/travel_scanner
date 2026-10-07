---
id: 2026-10-07-run-the-tests-under-docs-videos
title: Run the tests under docs/videos in CI so the imported-language runner cannot drift unnoticed
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-docs-ci
claimed_at: 2026-10-07T04:23:48Z
created_at: 2026-10-07T03:55:50Z
completed_at:
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - package.json
  - .github/workflows/ci.yml
---

# Run the tests under docs/videos in CI so the imported-language runner cannot drift unnoticed

## Why

`npm run test:tools` globs `tools/**`, so `docs/videos/**/*.test.mjs` (the imported-language
runner, its speech journal, the language batch tooling: 126 tests in
`docs/videos/imported-long-languages` alone) runs in no CI job. Two of its tests went red when
#1342 changed how `makeDub` reports an exit 4, and stayed red for two days until
2026-10-05-imported-language-runner-test-still-expects was fixed by hand.

## Definition of done

- [ ] CI runs `docs/videos/**/*.test.mjs` on every pull request, in an existing job or a new one,
      and a red test there fails the PR.

## Steps

- [ ] Time `node --test docs/videos/**/*.test.mjs` on Linux (about 20 s for the runner file; the
      native speech fixtures need ffmpeg) and decide whether it joins `test:tools` or gets its own
      script and job.
- [ ] Check that nothing under `docs/videos` needs a network or a token (the runner tests stub HTTP).

## How to verify

A deliberately broken assertion in `docs/videos/imported-long-languages/runner.test.mjs` turns the
PR red; reverting it turns it green.

## Notes

- Filed 2026-10-07 by claude-opus-5-5-runner-test.
