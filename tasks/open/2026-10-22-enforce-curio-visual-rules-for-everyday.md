---
id: 2026-10-22-enforce-curio-visual-rules-for-everyday
title: Enforce Curio visual rules for everyday brand stories
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-22T01:58:23Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/story.mjs
  - tools/video/core/story.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
---

# Enforce Curio visual rules for everyday brand stories

## Why

The owner decided that the `story-everyday-*` series follows the Curio visual rules; C02's task and `docs/videos/brand-stories-everyday-reversals-20261020/README.md` already record this. C03 needed a manual recut because its first accepted plan had 67 illustrations and 27 cards, several of them conceptual lists or questions. Its corrected 73/21 plan passes a manual Curio check, but `curioProblems` runs only for `curio-*` slugs, while `cuteStoryVisualProblems` in the story worker covers `story-five-*` and two named v2 pilots. A future `story-everyday-*` episode can pass ordinary lint without the series' illustration ratio or card-run guard.

## Definition of done

- [ ] `story-everyday-*` episodes with `series.kind: story` fail local lint and the host pre-keyframes gate if the look differs from the exact `cute-mystery` preset, illustrated body scenes are below 70%, or more than three cards run together.
- [ ] The rule applies to C04–C20 and does not change legacy story routes or `curio-*` behavior.
- [ ] The shared brand-story skill states the same Curio illustration acceptance and one-number/name/quote/source card guidance; card meaning still receives editorial review.

## Steps

- [ ] Reuse a shared visual-rule predicate in core lint and the story worker preflight, scoped to the everyday series, without reclassifying a story as Curio.
- [ ] Add positive and negative tests for look, illustrated share, card runs, C03 passing, and unrelated story slugs staying unchanged.
- [ ] Update byte-identical `.agents` and `.claude` brand-story skills.

## How to verify

Run `node tools/video/cli.mjs lint --slug story-everyday-moleskine-c03`, the focused core lint and story worker tests, `npm run test:tools`, and `npm run check:tasks`. Use a temporary test fixture to show that an everyday story at 69% illustrations or four consecutive cards fails before paid keyframes; verify a legacy story does not acquire the new gate.

## Notes

Filed during the C03 Curio-rules recut on 2026-10-22. C03's visual rule audit is recorded at `docs/videos/story-everyday-moleskine-c03/reviews/curio-rules-recut.md`; this ticket is an enforcement follow-up, not authorization for new paid media or changes to the C03 task's scope.
