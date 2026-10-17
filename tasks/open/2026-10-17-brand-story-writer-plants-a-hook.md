---
id: 2026-10-17-brand-story-writer-plants-a-hook
title: Brand story writer plants a hook every 30 to 45 seconds
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-story-hooks
claimed_at: 2026-10-17T16:20:05Z
created_at: 2026-10-17T16:16:36Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/story-prompts.mjs
  - tools/video/automation/story-prompts.test.mjs
  - .agents/skills/youtube-video/references/prompts/writer-story.md
---

# Brand story writer plants a hook every 30 to 45 seconds

## Why

The owner (2026-10-18), watching the brand stories: 「講故事也要放鉤子，不然會很無聊看不下去。」
The story writer gets the shared `NARRATIVE_RULES` (`tools/video/automation/register.mjs`), which
ask for one open loop every 60 to 90 seconds of the body and three loops per ten minutes. Measured
on the site, B25 (Seiko, about 11 minutes) went about 70 s without one and A41 (Michelin) over
90 s. A story is one voice over still pictures, so it needs a tighter cadence than the explainer
videos, which keep the shared rules.

## Definition of done

- [x] The story writer (`STORY_INSTRUCTIONS["writer:story"]`) is told: a hook about every 30 to
  45 seconds (130 to 200 spoken characters), never more than 45 seconds without one; every chapter
  but `now` ends on a concrete unanswered question or action that the next chapter picks up; hooks
  stand on facts, not empty promises; at least 8 loops for ten minutes, 3 of them in the hook.
- [x] The shared `NARRATIVE_RULES` are unchanged; the story block says it replaces their cadence
  and loop minimum, so the prompt does not contradict itself.
- [x] The readable copy `references/prompts/writer-story.md` says the same.

## Steps

- [x] `STORY_HOOK_RULES` in `story-prompts.mjs`, sent after `NARRATIVE_RULES`; the loops bullet
  now asks the hook for three.
- [x] Tests in a new `story-prompts.test.mjs` (`story.test.mjs` is in the active scope of
  `2026-10-16-bind-story-audits-and-narration-to`).
- [x] `writer-story.md` updated (only SKILL.md is mirrored under `.claude/skills`).

## How to verify

`node --test tools/video/automation/story-prompts.test.mjs tools/video/automation/story.test.mjs`
and `npm run check:tasks`. The real proof is the next story's script: lint's hook-gap warning and
a listen through the body.

## Notes

- Lint's own checks (`tools/video/core/narrative.mjs`: `HOOK_GAP_SECONDS = 90`,
  `LOOPS_PER_10_MINUTES = 3`) are shared with the explainer videos and are only warnings; they
  were not changed (and that file is in the active scope of `2026-10-14-ai-and-tech-videos-tell-one`).
  A story-only 45-second lint warning would be a follow-up if the prompt alone does not hold.
- `story.mjs` has no loop-count check of its own.
- Claimed with `--force` over `2026-10-14-align-brand-story-cute-prompt-lint` (status review,
  its PR #1499 is merged; the ticket was never closed).
