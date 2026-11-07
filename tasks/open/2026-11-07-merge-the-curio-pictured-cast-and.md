---
id: 2026-11-07-merge-the-curio-pictured-cast-and
title: Merge the curio pictured cast and beat motion tools into main
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-curio-redo-20
claimed_at: 2026-11-07T16:28:28Z
created_at: 2026-11-07T16:28:01Z
completed_at:
branch: claude/curio-redo-20-episodes-ldnrq0
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/craft.mjs
  - tools/video/core/explainer.test.mjs
  - tools/video/core/explainer-family.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/timeline.test.mjs
  - tools/video/assemble
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - .agents/skills/curio-episode
  - .claude/skills/curio-episode
---

# Merge the curio pictured cast and beat motion tools into main

## Why

The 20 curio redo scripts (handoff on branch `claude/eloquent-hypatia-fxsz7j`,
`docs/videos/curio-redo-handoff/HANDOFF.md`) need two tool changes that are not on main:
PR #2016 (`claude/curio-pictured-cast`: a narrated explainer may list a pictured, silent cast
such as Ada, with a look sheet) and branch `claude/curio-beat-motion` (`still_motion: "beat"`
and `pauses`). Without them lint, keyframes and assemble fail on the new scripts. The owner
chose on 2026-11-07 to land both together in one PR into main.

## Definition of done

- [ ] Both changes are on main, with the conflicts against main resolved.
- [ ] The duration review (`docs/videos/long-form/review.md` / `review.json`) carries an
      independent increment for the merged bound files and `long-form/cli.mjs check` passes.
- [ ] PR #2016 is closed as superseded.

## Steps

- [ ] Merge `claude/curio-pictured-cast` onto main; resolve `tools/video/core/lint.mjs`.
- [ ] Merge `claude/curio-beat-motion`; keep both curio-episode skill paragraphs.
- [ ] Independent duration review increment; rebind hashes.
- [ ] Run the video tool tests and `npm run test:tools`; open the PR; merge when CI is green.

## How to verify

`node tools/video/long-form/cli.mjs check`, `node --test tools/video/core tools/video/assemble`,
`npm run test:tools`, and `node tools/video/cli.mjs lint` on a new-script curio slug.

## Notes

- lint.mjs conflict: main already exempts `isStorySeries(doc)` (curio-/story- slug) from the
  drama hook window; #2016 exempts `isNarratedExplainer(doc)`. Both conditions are kept.
- Claimed with `--force` on 2026-11-07: every overlapping claim (mostly on the shared
  `docs/videos/long-form/review.*` and `tools/video/core/*`) was more than 24 hours old.
