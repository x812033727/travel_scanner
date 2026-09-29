---
id: 2026-09-29-keep-compilation-chapter-titles-from-giving
title: Keep compilation chapter titles from giving away mid-series answers
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-29T02:27:23Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/series.mjs
  - tools/video/core/compilation.mjs
---

# Keep compilation chapter titles from giving away mid-series answers

## Why

A binge compilation is one YouTube video with one chapter per episode, named
`第 N 集 〈集名〉` (`chapterTitle` and `chapterList` in
tools/video/core/compilation.mjs). All forty names sit in the description, so a
viewer reads every episode title before pressing play.

The 2026-09-29 read of the ten drama plans (docs/videos/series-plans) found 47
places where public text gave away an answer the story holds back: episode
titles such as 「第七次開服」 or 「她還活著」 on the episode-20 world flip,
title candidates naming the ending, pinned comments that promise what episode
40 does. The plans were rewritten and both AUTHORING.md now forbid it, but
nothing in the pipeline checks it:

- `planner:compilation` (prompts.mjs, the description prompt) only asks not to
  spoil the end, and it is handed the premise, which states the answers.
- The writer drafts each episode title with no view of which mysteries are
  still open, and a title becomes a chapter name word for word.

## Definition of done

- [ ] The prompts that write episode titles, compilation descriptions and
  pinned comments say that public text must not give a mystery's answer, the
  mid-series flip or the ending, and they receive the mystery schedule (or the
  answers to avoid) rather than only the premise.
- [ ] A reviewer or judge step for the compilation package looks at the chapter
  list and the description against the mystery schedule, and a hit sends the
  text back instead of publishing it.
- [ ] A series without mysteries behaves as now.

## Steps

- [ ] Find where episode titles are written for a series episode and what the
  model is shown then.
- [ ] Extend the compilation description prompt and its input.
- [ ] Add the check and a test with a fixture whose episode 20 title names the
  answer of a mystery revealed at 20.

## How to verify

`npm run test:tools`; with the fixture, the compilation package is sent back
until the spoiling title is changed.

## Notes

- The plan-side sweep and the rewrites are recorded in
  docs/videos/series-plans/binge-five-20260928/AUDIT-REPAIR-20260929.md.
- Chapter names (篇名) are not public today: packaging has no field for them
  and `chapter_cards` is false for compilations. If that changes, they need the
  same check.
