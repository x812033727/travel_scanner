---
id: 2026-10-21-stage-prompts-outgrew-the-api-s
title: Stage prompts outgrew the API's 60,000-character limit
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-story-category
claimed_at: 2026-10-21T16:56:44Z
created_at: 2026-10-21T16:55:11Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/schemas.py
  - apps/api/tests/test_video_automation_ai.py
  - tools/video/automation/prompts.test.mjs
---

# Stage prompts outgrew the API's 60,000-character limit

## Why

Found in the post-deploy check of 4e3e37a43 (2026-10-21): the video worker's auto round ended
with 「instructions：內容太長」. #1643 added TEACHING_FLOW_RULES to the planner, writer and
listener prompts, taking the tutorial writer to 64,454 characters and the planner to 60,261,
over `StageRunIn.instructions`' max_length of 60,000, so every tutorial writer and planner run
was refused before the model was called (no spend; the video stays held). The owner chose to
raise the API's limit rather than shorten the rules.

## Definition of done

- [x] `StageRunIn.instructions` takes up to STAGE_INSTRUCTIONS_MAX = 120,000 characters.
- [x] A tools test fails when any composed stage prompt, with room for the standing
      instructions, would pass the limit the API declares.
- [ ] Deployed, and the worker's next writer run is accepted.

2026-10-23 owner-directed narrow C-series handoff: the shared checkout's canonical
`docs/videos/long-form/review.md` and `review.json` were clean. The board steward released
only these two paths for an independent final duration review; this ticket's other scope,
status and deployment check remain.
