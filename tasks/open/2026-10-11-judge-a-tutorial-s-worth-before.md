---
id: 2026-10-11-judge-a-tutorial-s-worth-before
title: Judge a tutorial's worth with yes-or-no statements before speech is paid for
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-11T09:49:58Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_automation/settings.py
  - tools/video/review/sync.mjs
  - tools/video/automation/flow.mjs
  - apps/api/tests/test_video_judge_worth.py
---

# Judge a tutorial's worth with yes-or-no statements before speech is paid for

## Why

On 2026-10-11 the owner refused a finished tutorial
(`claude-code-mods-delivery-check-tutorial`; the measurements are in
`2026-10-11-tutorial-worth-rules`). Nothing the pipeline runs would stop that film today:

- `lint` gives it 0 errors and 0 warnings.
- The outline judge and the final policy judge ask whether a follow-along demonstration is
  present (`apps/api/app/video_automation/judge.py`, "Outline {key} includes a concrete
  demonstration, walkthrough or worked calculation the viewer can follow along with", passing
  at 0.6). This film scored 0.95 at the outline and 0.91 at the final gate. Two tutorials made
  under the content-value rules scored 0.90 and 0.95, so the score cannot tell them apart.
- The content-value rules reject its brief (no outcome the viewer could not already reach),
  but they are prompt text for the model that writes the brief. No second party applies them,
  and no code reads the 「含金量不足」 or 「要先實作」 a planner is told to write: both strings
  occur only in `tools/video/automation/register.mjs` and its tests.

The three tasks filed on 2026-10-09 would not have stopped it as written:

- `2026-10-09-judge-a-brief-s-viewer-outcomes` is in the right place (the outline judge,
  before any paid speech) but judges an outcome against three exclusions: a lookup, a caution,
  「了解」 something. This brief words every item as an action and passes. It also leaves out
  the file that builds the judge request (`tools/video/review/sync.mjs`).
- `2026-10-09-send-a-final-cut-back-to` acts when the demonstration score is under 0.6.
- `2026-10-09-give-the-automated-route-a-way` adds evidence that something ran, not a
  judgment of whether it is worth teaching. This film had a real run of its core flow.

This task is the check those rules need. Build it together with, or in place of, the first
two.

## What was measured

Thirteen tutorials were read as text (cards and narration) by blind judges answering
yes-or-no questions with a quote for every "yes". Five films were read twice: 63 of 65
answers agreed. The table is in `2026-10-11-tutorial-worth-rules`.

Questions the two owner-refused films failed and the other eleven passed:

- Does the film show the content of the thing it teaches the viewer to use (the lines of the
  configuration, script, rule file, prompt or code that make it work) and say what the lines
  that matter do?
- Does the film contain at least one observed result that a reasonable viewer would not have
  predicted before watching: a measured number, a failure, a case where the obvious approach
  did not do what was expected?
- Is the film's main result shown as the actual output of a real run, not as a summary, a
  reconstruction or an expected result?

Questions that also caught films the owner has not judged:

- Could the intended viewer get the main practical result of the worked example without the
  film's method, using only what they already have and no setup, and lose nothing the film
  demonstrates? (The two refused films, the Codex lesson and three hands-on films: yes.)
- From what the film shows alone, with no package to download, could the viewer make or
  change one for a different need of their own? (The two refused films and one hands-on: no.)
- A count of narration sentences that would be just as true if the subject were never
  mentioned: 28 to 50 in the two refused films and the Codex lesson, 2 to 9 in the ten
  hands-on films. The judges' counts for one film differed by up to eight, so the cut is a
  band, not a number.

A question that did not discriminate: "is any single point made in three or more separate
scenes without new information" failed on 17 of 18 sheets.

For the brief alone, before a script exists, the reading of the refused film's brief gave
these, none of them yet run through a judge model:

- Per outcome: without the tool this video teaches, can the viewer the brief names already get
  this result in about a minute with what they use today? Code, not the judge, then requires
  at least two outcomes answered no.
- Per outcome: does the brief say what the viewer will see that tells them it worked?
- Does at least one outcome have the viewer make or change the thing the video is about,
  rather than only run a supplied copy?
- Does the main example do something the simpler tool named in the brief cannot do?
- Does the viewer carry out, in the script, the action the title names?

## Definition of done

- [ ] Before speech is paid for, a tutorial's brief and its script are each asked a fixed set
      of yes-or-no statements by a model that did not write them, and code decides from the
      answers.
- [ ] A failing brief or script goes back to its writer with the statements it failed. The
      owner sees the reasons on the card when the writer's revisions are used up.
- [ ] The refused film's brief and script fail; `claude-code-hooks-hands-on` and
      `claude-code-headless-hands-on` pass.
- [ ] A film at or past its audio gate is not sent back by this change.
- [ ] A film an agent pushes by hand meets the same check
      (`2026-10-11-hand-driven-film-approved-on-its`).

## Steps

- [ ] Ask the owner first: who decides when it fails (the writer gets it back automatically,
      or the owner sees it), and how many revisions before it becomes theirs. Changing who
      decides at a gate is the owner's call (`docs/videos/HANDS-OFF.md`).
- [ ] Put the statements to the production judge on the thirteen films' briefs and scripts
      and compare with the table before trusting any threshold. A judge's numeric scores have
      sat at one value on this channel until its questions were yes-or-no.
- [ ] Get the owner's own verdict on the four hands-on films the judges called "rework"
      (MCP, Plugins, Skills, context cost). Two owner verdicts are not enough to set a cut.
- [ ] Build it: the request in `tools/video/review/sync.mjs`, the judging and the decision in
      `judge.py`, the worker's send-back in `flow.mjs`, the reason on the card.
- [ ] Tests, and the duration receipt for every bound file.

## How to verify

A fixture brief whose outcomes a viewer can already reach is returned once with the failed
statements, and reaches the owner with them after the last revision. The refused film's
files, as fixtures, fail; a hands-on film's pass.

## Notes

- The judges' "publish" and "rework" are a model's reading of text. Only the two refused
  films carry the owner's own verdict.
- The demonstration score was the one signal that caught the film refused on 2026-10-09
  (0.45). It measures presence, and a film can have a complete, honest, follow-along
  demonstration of something not worth doing.
- The refused film's two outline options were two orderings of one lesson, so choosing
  between them could not reject the lesson.
