---
id: 2026-10-09-judge-a-brief-s-viewer-outcomes
title: Judge a brief's viewer outcomes before an outline can be chosen
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T02:41:26Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - tools/video/core/lint.mjs
---

# Judge a brief's viewer outcomes before an outline can be chosen

## Why

`lint` checks that a brief has a 觀眾看完能做到的事 section. Nobody checks what is in it. The
brief of `claude-code-mods-no-sandbox-before-install` listed two outcomes: compare your version
number with the documented minimum, and ask three questions before installing. The outline
judge scored the options on stance, demonstration and advice, picked one at 0.60 and the
setting approved it (`approvals.json`, 2026-10-04). Every later stage built on that brief, and
the brief cannot be edited after approval without a new approval.

The content-value rules (PR 1392) now tell the planner what is not an outcome: something one
line answers, a caution on its own, 「了解」 something. That is an instruction to the model that
writes the brief; it is not a check by anyone else.

## Definition of done

- [ ] Before an outline is chosen, each listed outcome is judged against the rule, and a brief
  with fewer than two that pass is returned to the planner with the reason.
- [ ] The reason is on the review card when it reaches the owner.
- [ ] Briefs already approved are not re-judged.

## Steps

- [ ] Decide where it sits: a fourth score in the outline judge, or a separate check before it.
- [ ] Write the judging prompt from `VALUE_RULES` in `tools/video/automation/register.mjs`, and
  measure it on past briefs before trusting it (the keyframe judge's scores sat at one value
  until its questions were made yes-or-no).
- [ ] Tests, and the duration receipt if a bound file changes.

## How to verify

The old Mods brief is returned with both outcomes named as a lookup and a caution; a brief with
three real outcomes passes.

## Notes

- A lint error on the brief's wording was considered and dropped: the writer cannot edit a
  brief, and an error there has stalled the worker before.
