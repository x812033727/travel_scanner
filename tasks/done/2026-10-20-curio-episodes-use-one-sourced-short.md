---
id: 2026-10-20-curio-episodes-use-one-sourced-short
title: Curio episodes use one sourced Short
status: done
priority: P1
area: tools
owner: codex-s05-shorts
claimed_at: 2026-10-20T05:30:55Z
created_at: 2026-10-20T05:29:58Z
completed_at: 2026-10-20T05:36:14Z
branch:
depends_on: []
scope:
  - tools/video/shorts/episode.mjs
  - tools/video/shorts/episode.test.mjs
  - tools/video/shorts/cli.mjs
  - docs/videos/curio-s34/shorts.json
---

# Curio episodes use one sourced Short

## Why

Curio's series rules require one `from-episode` Short per episode, but the shared episode
validator requires two. The seven completed S-axis long films have no `shorts.json`.
This task implements the narrow Curio count rule and drafts S34's first Short. S30's
episode directory is claimed by its existing production task, so its Short is held
until that owner releases the scope.

## Definition of done

- [x] A Curio episode with one valid sourced Short passes the episode checker; a
      Curio episode with zero or two fails, while other series still require two.
- [x] `--short 2` for a Curio episode reports its one-Short range instead of
      dereferencing a missing script.
- [x] S34 has one source-safe Short script using reviewed episode shots and it passes
      `from-episode --check` without paid media calls.

## Steps

- [x] Update the count validation and targeted tests.
- [x] Draft and check S34's one Short.

## How to verify

`node --test tools/video/shorts/episode.test.mjs` and
`VIDEO_WORKDIR=/workspace/.video-work node tools/video/shorts/cli.mjs from-episode --slug curio-s34 --check`.

## Notes

S30's `docs/videos/curio-s30` is held by
`2026-10-19-curio-s30-xuanzang-departure-history-episode`; do not force an
overlapping task claim just to add its Short.

S34 script facts follow `research.md` items 11, 13, and 15 (Shackleton, *South*,
chapter IX). `from-episode --check` resolved all six shot keyframes and their
hashes. Seven focused unit tests passed. S30's candidate script is held at
`/tmp/curio-s30-shorts-draft.json` pending scope handoff.
