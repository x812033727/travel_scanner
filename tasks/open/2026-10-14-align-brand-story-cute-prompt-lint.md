---
id: 2026-10-14-align-brand-story-cute-prompt-lint
title: Align brand story writer prompts with cute-mystery narration
status: review
priority: P1
area: tools
owner: codex-8a78-story-editor
claimed_at: 2026-10-14T16:25:44Z
created_at: 2026-10-14T16:25:14Z
completed_at:
branch: codex/brand-stories-five-20261014
depends_on: []
scope:
  - tools/video/automation/story-prompts.mjs
---

# Align brand story writer prompts with cute-mystery narration

## Why

The new five-story series uses the existing six-chapter story writer with a 10-minute MiniMax cute-mystery look, but its static writer instructions still say 12–15 minutes, about 90 flat cartoon stills, and a two-part outro. The generated result could follow those older instructions despite correct series settings. Update the common prompt to follow the payload's length/look and make the cute route deliver the requested answer, related comment question, and subscription invitation.

## Definition of done

- [x] A 10-minute cute-mystery story receives compatible shot, illustration prompt, and closing instructions; legacy 13-minute custom stories retain their prior directions.
- [x] The writer is told that picture prompts describe one person doing one thing, with style only in `look` and no text/logo/likeness.

## Steps

- [x] Resolve static length/shot count wording for the two supported series profiles.
- [x] State the conditional three-sentence outro requirement for the cute profile without changing legacy story expectations.

## How to verify

Inspect the final writer instruction string exported from `STORY_INSTRUCTIONS` for both routes and run the focused story automation tests. Media and story content remain subject to real script and visual review.

## Notes

The separate `curio-` visual lint files are claimed by `2026-10-14-curio-episodes-keep-the-series-look` (another agent), so this ticket deliberately does not edit those paths. The story writer only emits `shot` body scenes plus one outro, which gives 100% shot share if the model follows the schema; check the actual compiled five films at QA.

2026-10-15: `node --check tools/video/automation/story-prompts.mjs` passed, and importing `STORY_INSTRUCTIONS["writer:story"]` confirmed the 10-minute/80-illustration, one-action prompt and three-sentence cute outro text. No media generation was run.
