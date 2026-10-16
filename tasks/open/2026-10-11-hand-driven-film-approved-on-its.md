---
id: 2026-10-11-hand-driven-film-approved-on-its
title: A film an agent drives by hand is approved on its own reviewer's word
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-11T09:50:02Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - apps/api/app/video_automation/settings.py
  - docs/videos/HANDS-OFF.md
---

# A film an agent drives by hand is approved on its own reviewer's word

## Why

`claude-code-mods-delivery-check-tutorial` was not made by the automated worker. One agent
session wrote the brief, the script and the learner materials by hand and pushed single
stages (`review-push --gate outline|audio|final`, `tts`, `render`, `assemble`, `package`)
through the production worker container. The records of that run show:

- Every review of the film (the fact check in `verify-1.md`, the final editorial review, the
  audit of the learner package) is signed `codex-review-own-video`: the authoring session's own
  reviewer.
- The teaching rules the film was held to were written by the same session, and the commit
  that set their final text also added the lesson's draft.
- The outline, audio and final gates were approved automatically within 43 minutes
  (2026-10-08 20:07, 20:41 and 20:50 UTC; 「依設定自動核准」). `review-push` was run without
  `--manual-review`, the flag that keeps a final cut for the owner.
- No person decided at any gate. The owner was the first to judge the film, two days later,
  and refused it.

The automatic approval settings were made for the worker, whose planner, writer and listener
are separate model calls with the channel's rules in their instructions. A film pushed by
hand goes through the same gates with none of that, and the server cannot tell the two
apart.

## Definition of done

- [ ] The owner has decided what a hand-driven film's gates require: the owner's own
      approval, or a judge that is not the author's session, or the same as the worker.
- [ ] The server or the tool enforces that decision; a hand-driven film cannot reach "final
      approved" on its author's review alone.
- [ ] `docs/videos/HANDS-OFF.md` says so.

## Steps

- [ ] Ask the owner. Options: `review-push` from outside the worker always asks for a manual
      review; or it may auto-approve only after the worth check of
      `2026-10-11-judge-a-tutorial-s-worth-before` passes; or leave it and rely on that check.
- [ ] Find how the server could know a submission came from the worker (the worker's token,
      a flag in the submission) and whether an agent could simply set it.
- [ ] Build what the owner chose; tests; the receipt if a bound file changes.

## How to verify

A final cut pushed with `review-push --gate final` from a hand-made work folder waits for the
owner (or for the check), and the worker's own final cut is approved as it is today.

## Notes

- Nothing was published by that run. The cost was one production: 2,955 billable characters
  of speech and the owner's time.
- The duration receipt already refuses a review whose `author_agent` equals its
  `reviewer_agent`. A reviewer the author's session starts under another name passes that test.
