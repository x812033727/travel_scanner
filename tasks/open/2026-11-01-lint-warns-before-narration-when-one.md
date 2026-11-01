---
id: 2026-11-01-lint-warns-before-narration-when-one
title: Lint warns before narration when one slide state is estimated over 15 s (outro with three lines on one state)
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-01T10:45:27Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Lint warns before narration when one slide state is estimated over 15 s (outro with three lines on one state)

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Evidence (2026-11-01)

daily-ai-20261030's final QA failed pace (`qa/pace.mjs` MAX_STATE_SECONDS = 15): "1 of 77 slide states
stay over 15 s: outro state 0 (16.9 s)". The outro has three lines (kxwy, jaax, qhg7) and no `reveal`, so
they share one state. The final was auto-approved anyway; fixing it after the fact would mean a new cut,
a new final approval and a new languages batch, so it was left (owner, 2026-11-01).

Why lint did not catch it: `core/cadence.mjs` `cadenceProblems` estimates slide-state length from
`estimateTimeline` but returns early for anything not illustrated (`if (!illustrated(doc)) return []`),
so slides videos and daily briefs get no estimate of the 15 s pace rule before narration.

## Definition of done

- [ ] For every video, lint warns (estimated) when a slide state is expected over
      `qa/pace.mjs` MAX_STATE_SECONDS, naming the scene, state and the lines on it, with the fix
      (a `reveal` on a later line, or split the scene), while the writer can still change it.
- [ ] Regression in lint.test.mjs: an outro of three lines on one state warns; with a reveal it does not.
