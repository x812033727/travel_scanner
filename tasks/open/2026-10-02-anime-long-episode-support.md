---
id: 2026-10-02-anime-long-episode-support
title: Support long anime episodes and closed finales
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-02T04:47:57Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/schemas.py
  - tools/video/automation/series.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/core/duration.mjs
---

# Support long anime episodes and closed finales

## Why

The Borrowed Dawn anime plan preserves the owner's 22-minute story / 30-minute broadcast-slot specification and a quiet closed finale. Current ordinary drama SeriesIn inputs reject more than 8 minutes; the custom genre forces two satisfaction beats per episode; chapter validation forces the final tension score to remain at least 4. Filing a video as anime in PR #1110 changes none of those rules. Do not shorten the story, change it to a nonfiction story/explainer, or fabricate satisfaction beats to bypass them.

## Definition of done

- [ ] An explicit long-anime production policy accepts the intended body duration without relaxing existing shorts, knowledge-video or ordinary-drama guards.
- [ ] Ensemble tragedy and a closed final episode can retain their actual beat and ending policies while ordinary serial episodes keep meaningful checks.
- [ ] The API, writer budgets, narration timeline, media QA and admin UI agree on body, OP/ED and broadcast-slot duration.
- [ ] The plan can be converted into a documented, validated input without claiming that its current planning JSON is an executable SeriesIn request.

## Steps

- [ ] Read docs/videos/series-plans/borrowed-dawn/plan.json and the independent content review before designing the policy.
- [ ] Trace all duration and retention consumers and narrow the implementation scopes before claiming this task.
- [ ] Add meaningful acceptance and boundary regressions; verify the final-episode exception is restricted to the declared last episode of a closed series.
- [ ] Document body versus OP/ED/slot budgets and prepare a validated draft input; leave media generation, activation and publication to their separately authorized workflows.

## How to verify

Run the affected API schema/series tests and Node duration/series/QA tests, web checks if the editor is changed, and npm run check:tasks. Demonstrate a 22-minute anime input succeeds, an invalid duration fails, ordinary drama's 8-minute boundary remains intact, an early episode cannot use the closed-final exception, and the supplied plan still has 120 episodes and a closed ending. No paid provider or production call is needed to validate these boundaries.

## Notes

Recorded while organizing a separate content PR at the owner's request. This is future production support, not unfinished content collation. Existing evidence: apps/api/app/video_automation/schemas.py defines SERIES_MAX_MINUTES = 8 and SeriesIn; tools/video/automation/series.mjs requires tension[4] >= 4 and applies GENRE_SPECS.custom retention rules. PR #1110 supplies only the anime category and its migration. This task is intentionally open and unclaimed.
