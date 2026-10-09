---
id: 2026-10-09-hold-every-slides-video-to-content
title: Hold every slides video to content-value rules: outcomes, order, typeable steps, no sourcing talk
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T01:52:18Z
created_at: 2026-10-09T01:52:13Z
completed_at:
branch: claude/video-reference-comparison-14fe9c
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/planner.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Hold every slides video to content-value rules: outcomes, order, typeable steps, no sourcing talk

## Why

On 2026-10-09 the owner compared `claude-code-mods-no-sandbox-before-install` with two reference
tutorials (YouTube `2i3FT1vfcrA`, `xs6-p7fFYH8`) and said the reference teaches and ours does not,
that the problem is the content and not the pictures, and that every video made so far carries
very little. Reading both transcripts against our 108 sentences showed where:

- our whole nine minutes (no sandbox, ask before installing) is about fifteen seconds of the
  reference, which spends the rest on what a mod changes, when to use it instead of a hook,
  installing, making one, keeping and removing it, and five real mods;
- the brief's 觀眾看完能做到的事 was "compare a version number" and "copy three questions";
- one of five chapters taught how to compare 2.1.90 with 2.1.287;
- 24 sentences named where a fact came from, 20 described a metaphor's scene;
- the description said nothing had been installed or run.

The draft on `codex/mods-clarity-20261009` (PR 1390) adds a teaching-card route for tutorials.
It is chosen by the planner, and it leaves every other slides video on the old rules. This task
adds the part that route does not carry, for both routes.

## Definition of done

- [x] The planner, the writer and the listener of every slides video are sent one set of
  content-value rules: what counts as an outcome, proof on screen for each, chapters in the
  viewer's order with a choosing rule, the exact thing to type on a card, no sourcing talk and
  at most two scene-setting sentences, a risk as one chapter, length from substance.
- [x] A subject the viewer operates is planned as a tutorial on the teaching route.
- [x] `lint` warns when the narration names its source more than twice.
- [x] Drama, story, explainer, restyle and translation prompts are unchanged.
- [ ] The duration receipt is rebound by an independent reviewer.

## Steps

- [x] `VALUE_RULES` in `register.mjs`, placed after the teaching route and before the register.
- [x] `SOURCING_FAMILY` and `SOURCING_MAX` in `lint.mjs` (a warning, like the hedge family).
- [x] Tests for the prompts and the lint check.
- [x] `script-writing.md` §含金量, the planner and writer prompt docs, rule 11 in both skill copies.
- [ ] Rebind `docs/videos/long-form/review.json` and `review.md`.

## How to verify

```bash
node --test tools/video/automation/prompts.test.mjs tools/video/automation/register.test.mjs tools/video/core/lint.test.mjs
node tools/video/long-form/cli.mjs check
npm run test:tools && npm run check:tasks
```

The old script is the regression case: `episodeScriptProblems` on its `video.json` reports
"the narration names its source 14 times".

## Notes

- Stacked on `codex/mods-clarity-20261009`: this branch fast-forwarded to its head `6c5c9769c`
  and adds one commit. If that PR merges by squash, check `git diff --quiet 6c5c9769c origin/main`
  on the files it touches before rebasing this one.
- Lint warnings do not reach the host worker's writer (flow.mjs reads errors only), so on the
  automated route the prompts are the lever and the warning is for local agents and the owner.
  Making it an error would stall scripts already in flight.
- Not done here, each needs its own task: (1) the final gate's 「有示範」 score below its
  threshold goes to the owner instead of back to the writer; (2) the host worker cannot run a
  tool, so 「要先實作」 has nobody to answer it on the automated route; (3) the planner's
  outcomes are not judged by anyone before the outline is chosen.
- A hand-made sample in this direction (two mods written and tested on 2026-10-09, script
  checked by `video_kit.py check`) sits untracked in this worktree under
  `docs/videos/claude-code-mods-hands-on/`; the owner has read it and has not asked for it to
  be committed.
