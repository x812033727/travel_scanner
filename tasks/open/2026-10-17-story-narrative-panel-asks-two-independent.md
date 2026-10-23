---
id: 2026-10-17-story-narrative-panel-asks-two-independent
title: Story narrative panel asks two independent readers
status: in-progress
priority: P1
area: tools
owner: claude-opus-5.5-story-panel-two-readers
claimed_at: 2026-10-17T23:15:49Z
created_at: 2026-10-17T23:11:00Z
completed_at:
branch: claude/story-panel-two-readers
depends_on: []
scope:
  - .agents/skills/youtube-video/references/story.md
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
---

# Story narrative panel asks two independent readers

## Why

A brand story (`kind: "story"`) passes the blind storytelling panel (`narrativeGate` in
`tools/video/automation/story.mjs`) before paid narration. On the live site B25 Seiko and A41
Michelin stuck there for more than ten rounds: each round a single reader picked one or two
*different* small lines, and even turned lines it had passed unchanged into a "no" (A41's opening
question was suddenly called a spoiler in round 8). The owner decided on 2026-10-18 to cut that
random misjudgement for brand stories.

## Definition of done

- [x] Each round of a brand story's panel asks two independent readers (two verifier calls, fresh
  sessions, the same narration and questions); a required question fails only when both say "no".
  A "yes" counts only with a quoted line id (the existing `EVIDENCE_LINE_ID` rule).
- [x] The listener is sent only the questions both readers failed, with both readers' evidence.
- [x] `review/narrative.json` keeps each reader's answers next to the merged ones; existing fields
  and `narrativeReviewMatches` are unchanged.
- [x] A failed or timed-out reader call is handled as one call always was; nothing is kept.
- [x] Tutorials and dramas still ask one reader.

## Steps

- [x] `mergePanelVerdicts` and `readers` in `narrativeRecord` (core/narrative.mjs).
- [x] Two calls in `narrativeGate` (automation/story.mjs).
- [x] Tests in narrative.test.mjs and story.test.mjs.
- [x] One line in `.agents/skills/youtube-video/references/story.md`.

## How to verify

`node --test tools/video/core/narrative.test.mjs tools/video/automation/story.test.mjs tools/video/automation/automation.test.mjs`
(automation.test.mjs is unchanged; it pins the one-reader tutorial path)
and `npm run check:tasks`.

## Notes

- Each reader's payload carries `reader: 1|2`. A pilot story's verifier runs go through the durable
  run receipts (`client.mjs` PILOT_STORY_SLUGS), keyed by the request: a second identical request
  in the same step would get the first reader's consumed receipt back, i.e. one reader taken for two.
- `PANEL_RULES_SHA256` is not bumped: the merge only loosens a pass (any reader's cited yes), so a
  single-reader PASS already kept is still a pass under the new rule; failed records are re-asked anyway.
- `tools/video/cli.mjs` (the manual panel answer) still records one reader; out of scope.
- Claimed with `--force` (2026-10-18). The claim was refused for two tasks still marked in-progress
  whose code has merged: `2026-10-14-ai-and-tech-videos-tell-one` (branch
  `claude/ai-video-storytelling`, PR #1504 merged 2026-10-14; its thirteen panel questions are on
  main) and `2026-10-16-bind-story-audits-and-narration-to` (branch
  `codex/a01-lexicon-integration-20261017`, PR #1548 merged 2026-10-17; what it still lists is the
  A01 production migration, not a change to `narrativeGate` or the panel). No open PR touches
  `core/narrative.mjs`; the only open PR on `story.mjs` is draft #1518 (author chapters), which does
  not touch `narrativeGate`.
- The one-reader test for tutorials and dramas lives in story.test.mjs, not automation.test.mjs:
  `docs/videos/long-form/review.json` binds automation.test.mjs by SHA-256, and a change there needs
  an independent DURATION_ONLY receipt increment.
