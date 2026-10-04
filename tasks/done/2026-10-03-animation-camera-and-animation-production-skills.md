---
id: 2026-10-03-animation-camera-and-animation-production-skills
title: Animation camera and animation production skills: shot grammar and a cost-and-error production practice for AI drama
status: done
priority: P2
area: docs
owner: claude-fable-5-1-video-craft
claimed_at: 2026-10-03T08:49:28Z
created_at: 2026-10-03T08:49:12Z
completed_at: 2026-10-03T12:50:36Z
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
  - tools/animation-camera.test.mjs
  - tools/animation-production.test.mjs
---

# Animation camera and animation production skills: shot grammar and a cost-and-error production practice for AI drama

## Why

The owner asked on 2026-10-03, after the wedding pilot's 60/100 and the illustrated
slides' 「粗糙、單調、AI 感重」, for two more skills: one for the animation camera
(動畫視角: how a scene is seen through a camera and how that is written so the picture
and video models, lint, the craft rows and the judge all read it the same way) and one
for animation production (動畫製作: the stage order, what must be true before each paid
stage, dry runs, caches, retakes, the catalogue of errors and which check catches each),
"so that production cost drops and errors are fewer". Later the same day:
「我要補hailuo跟kling的方案使用」 and 「kling有MCP可以控，hailuo就需要你用網頁控制了」,
so the production skill also covers clips bought through the Hailuo web subscription
(driven in the browser with the owner's login) and through Kling's MCP, beside the
server's API route. The `youtube-video` skill already holds the measured craft spec
(`references/drama-craft.md`), the ten-anime production spec
(`references/animation-production.md`) and the visual-quality workflow; what was missing
is the camera grammar as one place to read, and the production practice as a checklist
with the money and the error on every line. The host worker never reads a skill, so
anything the worker must obey stays in `tools/video`; these skills are for the agents
that write, direct and run a production by hand.

## Definition of done

- [x] `.agents/skills/animation-camera/SKILL.md` (references `camera-keywords.md`,
      `scene-coverage.md`, `model-misreads.md`; script `shot_reading.mjs`) tells a writer
      how to cover a scene and write `camera`, `prompt` and `motion` so that the keyword
      tables in `tools/video/core/craft.mjs`, `tools/video/core/drama.mjs` and
      `tools/video/assemble/drama.mjs`, the keyframe and clip prompts and the judge rubric
      read the shot as intended, and how the same shot is phrased for Hailuo and Kling; it
      points at `drama-craft.md` instead of repeating it.
- [x] `.agents/skills/animation-production/SKILL.md` (references `cost-model.md`,
      `stage-preconditions.md`, `error-catalogue.md`, `post-mortem.md`,
      `providers-and-plans.md`; scripts `episode_estimate.mjs`, `drama_preflight.mjs`,
      `run_report.mjs`) gives the stage order with the precondition and exit code of each
      paid stage, the cost of one shot and one episode per tier and per route (server API,
      Hailuo web plan, Kling MCP, MiniMax packages) with the levers and the break-even,
      the error catalogue, what an edit re-buys, when to stop retaking, how an external
      clip enters the pipeline today, and a post-mortem form; every number carries its
      source and date, third-party figures are marked unverified.
- [x] Byte-identical `.claude/skills/<name>/SKILL.md` copies (SKILL.md only, as the test
      header prescribes); `node --test tools/skills.test.mjs tools/animation-camera.test.mjs
      tools/animation-production.test.mjs`: 46 passed. The camera test parses the
      `## 例子` table of `camera-keywords.md` through the three readers; the production
      test parses `catalog.py` for the API prices and asserts `gemini_video.py` still
      forwards `negativePrompt`.
- [x] `AGENTS.md` lists the two skills; `drama.md` (and its `.claude` copy) routes to them
      from the 主幹 section and now states the code's pan direction, the PSNR check on
      `locked` stills and exit code 3 for an unapproved gate. The bound
      `youtube-video/SKILL.md` is not changed.
- [x] A fresh agent given only the two skills storyboarded the kitchen-key scene (ten to
      twelve shots) to an accepted `video.json` in three drafts, ran lint, the craft check,
      `shot_reading.mjs` and `episode_estimate.mjs` (server and `--plan hailuo:pro`), and
      reported the places it still had to open code for; those went into the polish pass.

## Steps

- [x] Map what the repository already says (five readers: camera grammar, production line,
      cost, pilot evidence, model limits); design the two skills from three angles
      (cost-first, error-first, writer-first) and a two-judge panel; the writer-first
      outline won with grafts from the other two.
- [x] Write both skills and their scripts (five writers); mirror the SKILL.md copies.
- [x] Verify: a checker ran the tests and the scripts (two rounds, seven failures fixed);
      four audits (numbers, contradictions, a fresh writer, a fresh-eyes editor: 64
      findings) and a polish pass per skill; final check passed.
- [x] Route from `AGENTS.md` and `drama.md`; close this task in the pull request.

## How to verify

```bash
node --test tools/skills.test.mjs tools/animation-camera.test.mjs tools/animation-production.test.mjs
node .agents/skills/animation-camera/scripts/shot_reading.mjs tools/video/core/fixtures/drama/video.json
node .agents/skills/animation-production/scripts/episode_estimate.mjs tools/video/core/fixtures/drama/video.json --tier clips --plan hailuo:pro
npm run check:tasks
```

## Notes

- Branch `claude/animation-skills` was stacked on `claude/video-production-skills-7d87cc`
  (PR #1170, merged 2026-10-03) and rebased onto `main` before the pull request.
- Plan facts were read on 2026-10-03: MiniMax API pricing and video docs (official pages),
  the Hailuo subscribe page and the Kling membership page (both SPAs, read in the in-app
  browser), the Hailuo payment terms, and third-party summaries for Kling's credits per
  video and developer API (marked unverified). Kling's official MCP guide and generator
  need the owner's login; the skill says what to read there before pricing a scene.
- Not verified and said so in the skills: Hailuo's and Kling's camera vocabulary; whether
  the Hailuo form honours the API's bracket commands; which plan the official Kling MCP
  draws from; H3 2K's pixel size against the production profile's native 1920×1080;
  `max_clips_per_video` enforcement; the judge's real price.
- Follow-ups filed: `2026-10-03-clips-import-bring-a-clip-made` (the `clips import`
  command the skills describe as missing) and `2026-10-03-drama-design-documents-say-what-the`
  (the design-document sentences the code has left behind).
- A production-profile series (the ten anime) can only buy clips on the server route
  today: `productionClipProblems` refuses another provider or a non-native 1920×1080
  source; the Hailuo and Kling routes serve pilots and series without a profile until
  the import ticket decides how `provider: "external"` fits the profile.
- The first writing run was lost to the account's usage limit (12 agents refused at
  18:1x; reset 18:20); the second run completed.
