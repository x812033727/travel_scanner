---
id: 2026-11-19-sothatswhy-heimao-ten-steps-prompts
title: Writer prompts - sothatswhy follows the Heimao ten steps; no intro; one-question hook
status: done
priority: P1
area: tools
owner: claude-opus-elegant-hypatia
claimed_at: 2026-11-19T01:23:29Z
created_at: 2026-11-19T02:00:00Z
completed_at: 2026-11-19T01:41:35Z
branch: claude/elegant-hypatia-07i3yx
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/register.test.mjs
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/automation/story-prompts.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - tools/video/core/lint.mjs
  - tools/video/core/narrative.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - docs/videos/history-curiosity/README.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
---

# Writer prompts: sothatswhy follows the Heimao ten steps; no intro; one-question hook

## Why

Owner 2026-11-19: 「新寫的《原來如此》比照黑猫十步」「三個系列都不放片頭」「全部做」. The host writer
prompts still say "the channel intro plays after it" (奇聞, 原來如此) and 原來如此 still opens on a
30–60 s condensation. The owner allowed taking over stale claims on these files.

## Definition of done

- [x] STORY_OPENING_RULE: no intro bumper; the hook asks ONE question, never a menu.
- [x] 奇聞 profile: no intro in its shape and its tool-added-clips line.
- [x] 原來如此 profile: shape and bible follow the ten steps (hook + promise 40–60 s, no condensation, no intro).
- [x] SERIES_TEXT_PINS refreshed; script-writing.md and the sothatswhy template name the ten steps.

- [x] 原來如此 keeps the 45-second hook cadence and 8 loops per ten minutes (lint TIGHT_CADENCE, writer prompt), owner 2026-11-19.

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```
