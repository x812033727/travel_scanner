---
id: 2026-10-13-raise-the-loops-table-from-a
title: Raise the loops table from a warning to an error
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-13T03:40:43Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
---

# Raise the loops table from a warning to an error

## Why

`2026-10-13-narrated-videos-tell-one-story-with` (PR #1478) made every narrated episode carry a
`loops` table: each hook is the line that plants it, the line that pays it off, and one phrase for
what it holds back. A ten-minute episode plants at least three. It shipped as a *warning* on
purpose, because every script already in the repository has none, and an error would have blocked
the host on scripts nobody had rewritten yet.

Once a batch of scripts has passed the gate with real loops, the warning has done its job and the
check should refuse a script without them. A hook that is never paid off is the thing the owner
complained about on 2026-10-13: the video stops being one story.

## Definition of done

- [ ] A narrated zh-TW episode of `MIN_EPISODE_MINUTES` or more with no `loops` table, or with
      fewer than `requiredLoops(minutes)` of them, fails `cli.mjs lint` instead of warning.
- [ ] A loop whose setup sits in the outro, and an opening that plants none, stay warnings or
      become errors by the same decision, written down either way.
- [ ] Every narrated script in `docs/videos/` passes, or is listed here with the reason it does not.

## Steps

- [ ] Count the narrated scripts in the repository that would fail, and fix or list them first.
- [ ] `loopProblems` in `tools/video/core/narrative.mjs`: move the missing-table and the
      short-count problems from `warnings` to `errors`.
- [ ] `tools/video/core/narrative.test.mjs`: the cases move with them.
- [ ] Check no host stage is left mid-flight when it deploys: an error reaches the writer through
      `lint_errors` and starts a revision round.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/core/lint.test.mjs
for d in docs/videos/*/video.json; do node tools/video/cli.mjs lint --slug "$(basename "$(dirname "$d")")"; done
```

## Notes

- The five 奇聞檔案局 v2 scripts (`docs/videos/curio-h01-v2` and the four from
  `2026-10-13-rewrite-four-curio-recuts-storytelling`) are the first batch written with loops; they
  are the evidence this ticket waits for.
- The five delivered recuts (`curio-h01`, `curio-u02`, `curio-l08` and the two whose source folders
  are kept outside this repository) have no loops and would fail. They are superseded by the v2
  scripts, so decide whether they are deleted, left failing, or exempted by a date.
- It is a one-line move in `loopProblems`; the work is the scripts, not the check.
