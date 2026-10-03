---
id: 2026-10-03-animation-camera-and-animation-production-skills
title: Animation camera and animation production skills: shot grammar and a cost-and-error production practice for AI drama
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1-video-craft
claimed_at: 2026-10-03T08:49:28Z
created_at: 2026-10-03T08:49:12Z
completed_at:
branch: claude/animation-skills
depends_on: []
scope:
  - .agents/skills/animation-camera
  - .agents/skills/animation-production
  - .claude/skills/animation-camera
  - .claude/skills/animation-production
  - AGENTS.md
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video/references/drama.md
  - tools/animation-skills.test.mjs
---

# Animation camera and animation production skills: shot grammar and a cost-and-error production practice for AI drama

## Why

The owner asked on 2026-10-03, after the wedding pilot's 60/100 and the illustrated
slides' 「粗糙、單調、AI 感重」, for two more skills: one for the animation camera
(動畫視角: how a scene is seen through a camera and how that is written so the picture
and video models, lint, the craft rows and the judge all read it the same way) and one
for animation production (動畫製作: the stage order, what must be true before each paid
stage, dry runs, caches, retakes, the catalogue of errors and which check catches each),
"so that production cost drops and errors are fewer". The `youtube-video` skill already
holds the measured craft spec (`references/drama-craft.md`), the ten-anime production
spec (`references/animation-production.md`) and the visual-quality workflow; what is
missing is the camera grammar as one place to read, and the production practice as a
checklist with the money and the error on every line. The host worker never reads a
skill, so anything the worker must obey stays in `tools/video`; these skills are for the
agents that write, direct and run a production by hand.

## Definition of done

- [ ] `.agents/skills/animation-camera/SKILL.md` (with references and a script where an
      agent would otherwise repeat work by hand) tells a writer how to cover a scene and
      write `camera`, `prompt` and `motion` so that the keyword tables in
      `tools/video/core/craft.mjs`, `tools/video/core/drama.mjs` and
      `tools/video/assemble/drama.mjs`, the keyframe and clip prompts and the judge rubric
      read the shot as intended; it does not repeat `drama-craft.md`, it points at it.
- [ ] `.agents/skills/animation-production/SKILL.md` (with references and scripts) gives
      the stage order with the precondition of each paid stage, the cost of one shot and
      one episode per tier with the levers, the error catalogue (error → stage → check →
      cost if missed → prevention), and a post-mortem form; every price and threshold is
      the tools' own constant or the catalog's price, named with its source.
- [ ] Byte-identical `.claude/skills/<name>/SKILL.md` copies; `node --test tools/skills.test.mjs`
      passes (paths exist, no machine paths, body under 300 lines); the new scripts have
      tests under `tools/` like `tools/drama-craft-check.test.mjs`.
- [ ] `AGENTS.md` lists the two skills; `.agents/skills/youtube-video/references/drama.md`
      (and its `.claude` copy) points at them from the drama's step table. The bound
      `youtube-video/SKILL.md` is not changed (duration receipt).
- [ ] A fresh agent given only the two skills storyboards one dialogue scene and prices it
      without asking a question lint, the craft check or a dry run would have answered.

## Steps

- [ ] Map what the repository already says (camera grammar, production line, cost, pilot
      evidence, model limits); design the two skills from three angles and a judge panel.
- [ ] Write both skills and their scripts; mirror the SKILL.md copies.
- [ ] Verify: skill tests, contradiction check against the existing references, a forward
      test by a fresh agent, an audit of every number.
- [ ] Route from `AGENTS.md` and `drama.md`; close this task in the pull request.

## How to verify

```bash
node --test tools/skills.test.mjs tools/animation-skills.test.mjs
node .agents/skills/animation-production/scripts/<estimator> <a drama video.json>
npm run check:tasks
```

## Notes

- Branch `claude/animation-skills` is stacked on `claude/video-production-skills-7d87cc`
  (PR #1170): the skills name `data.source`, `action_seconds` on a cast drama and
  `tools/video/core/craft.mjs`, which exist only there until #1170 merges.
- The `new` command keeps only the last `--scope`; the list above was written by hand.
