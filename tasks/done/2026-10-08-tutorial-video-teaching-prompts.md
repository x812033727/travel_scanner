---
id: 2026-10-08-tutorial-video-teaching-prompts
title: Use one recurring worked example for tutorial video prompts
status: done
priority: P1
area: tools
owner: codex-7645-video-clarity
claimed_at: 2026-10-08T16:11:27Z
created_at: 2026-10-08T16:11:06Z
completed_at: 2026-10-08T16:40:39Z
branch: codex/mods-clarity-20261009
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/register.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/prompts.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/planner.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
  - .agents/skills/youtube-video/references/automated.md
---

# Use one recurring worked example for tutorial video prompts

## Why

The owner found the Mods tutorial less clear than the linked reference. Existing writing prompts require a new physical analogy and plot twist in every chapter, even for step-by-step tutorials. This fragments the explanation and can reward visual activity without helping the viewer understand an operation.

## Definition of done

- [x] Plain-slides tutorial prompts require one worked example, with an observable outcome and evidence-labelled steps.
- [x] Other production routes retain their existing contracts and translation hashes.
- [x] Focused prompt tests pass; repository checks have run and known platform blockers are recorded without a false green claim.

## Steps

- [x] Inspect the source prompts and identify tutorial/story rule collisions.
- [x] Add explicit tutorial routing in the authoring and reviewer prompts and align the reference documents.
- [x] Independently review the resulting prompts and record verification.

## How to verify

Use bundled Node 24.19: `node --test tools/video/automation/prompts.test.mjs tools/video/automation/automation.test.mjs`, then `npm run test:tools`, `npm run test:docs-videos` and `npm run check:tasks` before pushing.

## Notes

2026-10-09 (Taipei): Authorized by the owner's “開始改善”. Changes are local authoring behavior; this task does not deploy code or start paid rendering. The existing exact translation/register hashes are invariants. The prompt-test scope was checked against the board; the overlapping illustrated-slides task is open and unclaimed. Reference files have no existing `.claude` mirror in this checkout; no speculative mirror is added.

Independent prompt review found no blocker. Checks: prompt/register 27/27, targeted automation 6/6, docs-videos 199/199, docs test-discovery guard 2/2 and task format pass. Translation hash tests and 16 drama/story/explainer/register prompt comparisons are unchanged. Full tools run did not pass: it stopped making progress at the existing Windows ESM c: import problem (`2026-10-07-windows-video-test-imports`); isolated reference comparison also reproduces the existing Windows ffmpeg range failure (`2026-10-07-windows-reference-comparison-ffmpeg`). Those sources were not changed. Keep the PR draft pending appropriate CI/owner review.
