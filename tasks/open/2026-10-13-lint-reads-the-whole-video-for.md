---
id: 2026-10-13-lint-reads-the-whole-video-for
title: Lint reads the whole video for announcements and summaries
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-13T04:28:06Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
---

# Lint reads the whole video for announcements and summaries

## Why

Five scripts were written to the storytelling rules on 2026-10-13 and read by independent blind
readers (`2026-10-13-narrated-videos-tell-one-story-with`, PR #1478). Two failures repeated in
every single one of them, and neither is a thing lint can currently see:

- **A summary in the close.** The last three sentences re-told the body's turns instead of carrying
  only what is new. Every one of the five did this, and three did it again after one rewrite.
- **An announcement in the middle.** A line whose only job is to say that the explanation follows
  (「所以目前最站得住的解釋，是這樣的。」), and counting scaffolding (「排成一張表，前四個…」「剩下的
  兩個…」「其中一個是…另一個說法是…」). The table-of-contents check in `lint.mjs` only reads the
  first 60 seconds, so a script can carry this at seven minutes and still lint clean.

Both are caught today only by the ten-question panel, which costs a model call per episode and per
rewrite round. A measurable check would catch the obvious cases for free and leave the panel to
judge the ones that need judgement.

## Definition of done

- [ ] A narrated episode warns when a body line's only content is an announcement of what follows.
- [ ] A narrated episode warns on counting scaffolding outside a card: 排成一張表, 前 N 個,
      剩下的 N 個, and 其中一個是…另一個…是 used to enumerate accounts.
- [ ] A narrated episode warns when an outro line repeats a sentence the body already delivered,
      measured as a high overlap of content characters with some earlier narration line, with
      「還記得」「剛剛那」 callbacks exempt.
- [ ] The five v2 Curio scripts, which passed the panel by hand, still lint at 0 warnings, and so
      does every other narrated script in `docs/videos/`. A check that fires on a script a blind
      reader passed is wrong and gets narrowed.

## Steps

- [ ] Write the three checks in `tools/video/core/narrative.mjs` beside `chapterOpenerProblems`,
      tagged `kind: "narrative"` so they reach the writer through `lint_warnings`.
- [ ] Measure them against every narrated script in the repository before settling the patterns;
      count the false positives and write the number down here.
- [ ] Cases in `tools/video/core/narrative.test.mjs`, including a legitimate 其中一個 that must not
      fire and a 還記得 callback in an outro that must not fire.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs
for d in docs/videos/*/video.json; do node tools/video/cli.mjs lint --slug "$(basename "$(dirname "$d")")"; done
```

## Notes

- The close check is the valuable one: five of five scripts failed there, so it is the single
  highest-yield check in this file.
- 其中一個 and 另一個 are ordinary Chinese and firing on them broadly would be noise. The thing that
  makes them scaffolding is that they enumerate a set the narration has just counted, so look for a
  count nearby (前四個, 剩下的兩個, 七種) rather than for the pronoun alone.
- Why this was not done inside PR #1478: four agents were revising those five scripts against lint
  at the time, and moving lint under them would have invalidated every 0 errors 0 warnings they had
  just reached. The rules text was changed in that PR instead
  (`.agents/skills/youtube-video/references/script-writing.md`, `register.mjs` NARRATIVE_RULES).
- Related: `2026-10-13-raise-the-loops-table-from-a` also waits on that first batch of scripts.
