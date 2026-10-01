---
id: 2026-10-01-setting-planner-writes-character-looks-and
title: Setting planner writes character looks and the ten plans use them
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-setting-looks
claimed_at: 2026-10-01T14:09:17Z
created_at: 2026-10-01T03:45:59Z
completed_at:
branch: claude/setting-planner-looks
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - .agents/skills/youtube-video/references/prompts/series-setting.md
  - docs/videos/series-plans/binge-five-20260928
  - docs/videos/series-plans/claude-binge-five-20260928
---

# Setting planner writes character looks and the ten plans use them

## Why

Since task `2026-09-29-let-a-drama-character-s-look`, a character in a setting book may carry
`looks: [{ id, from, to?, appearance, sheet_prompt?, voice_style? }]`, and an episode a look
covers is drawn and voiced with it (docs/videos/SERIES.md, 換裝與變化). Two places do not use it
yet:

- The setting-book planner is never told about `looks` (the character shape in
  `SERIES_INSTRUCTIONS["planner:setting"]` in tools/video/automation/prompts.mjs, and
  .agents/skills/youtube-video/references/prompts/series-setting.md), so a series the planner
  writes keeps every change in the shot prompts, which can add a coat but cannot take one off.
- The ten forty-episode plans under docs/videos/series-plans keep their clothing and prop states
  in `continuity_notes` (the fourth audit pass, 2026-09-29): a conductor's coat and badge off in
  episode 27, a red wrist cord cut in episode 35, a master in a wheelchair from episode 9, a
  wedding dress for episodes 1-3 only, hospital gowns in episode 38, and voice styles written
  for one stretch of the story (reviews/city-owes-a-light.json lists four). Their AUTHORING.md
  now says those belong in `looks`, and their validators accept them.

## Definition of done

- [ ] The setting planner's instructions describe `looks` (when to write one, that its
  appearance is the whole look, one look per episode, a change inside one episode is a second
  character id) and its reference file says the same.
- [ ] The changes each plan lists in `continuity_notes` that a shot prompt cannot add are
  moved into the characters' `looks`, with the generated files rebuilt (`node build.mjs`) and
  `node validate.mjs` clean for every work.
- [ ] Voice styles written for part of a story move into a look's `voice_style`.

## Steps

- [ ] Prompt text and its test in tools/video/automation/prompts.test.mjs.
- [ ] One plan at a time; the authors' AUTHORING.md says where a look is written.

## How to verify

`node --test tools/video/automation/prompts.test.mjs`; in each plan directory
`node validate.mjs` and `node --test validate.test.mjs`.

## Notes

- The plans' content is the owner's approved story; moving a state into a look changes how it is
  drawn, not what happens. None of the ten works has started an episode (2026-09-28 snapshot).
