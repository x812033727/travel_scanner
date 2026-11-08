---
id: 2026-11-05-keyframe-judge-checks-the-eyes-mismatched
title: Keyframe judge checks the eyes: mismatched or drifting pupils redraw the shot
status: done
priority: P2
area: tools
owner: claude-opus-5.5-focused-hopper
claimed_at: 2026-11-05T16:40:03Z
created_at: 2026-11-05T16:39:43Z
completed_at: 2026-11-06T13:57:07Z
branch:
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
---

# Keyframe judge checks the eyes: mismatched or drifting pupils redraw the shot

## Why

The owner found odd eyes in 原來如此事務所 P05 at 1:00 (`kid-question`: the girl's pupils drift
off to one side, unlike each other) and said it happens more than once. Every take had passed
the keyframe judge, because its `anatomy` question asks about hands, extra limbs and warped
faces but never about the eyes. MiniMax image-01 draws cute-cartoon eyes wrong often enough
that the judge has to look for it.

## Definition of done

- [x] The `anatomy` fault question in `keyframeChecks()` also asks about eyes that do not match
      or look wrong (one pupil turned another way, pupils of different size or misplaced,
      an eye of another shape), so such a take is redrawn like the other six faults.
- [x] The question stays under the server's 400-character limit, and the test pins the clause.
- [x] P05 (and P02) shots re-judged with the new question; failures redrawn.

## How to verify

`npm run test:tools`; `node tools/video/cli.mjs keyframes --slug sothatswhy-p05-down-jacket --dry-run`.

## Notes

- Claimed with --force over three stale claims on the same files (2026-10-04 fault checks,
  2026-10-25 fixprompts, 2026-10-25 manga-blocked), all weeks without activity.
- keyframes.mjs says a reworded question has to be measured on recorded takes again; this
  episode's re-judge is that measurement.
- Rewording a question changes every verdict's stamp (`stampOf` in keyframes.mjs keys the
  verdict by the question asked), so the next `keyframes` run re-judges every drawn shot and
  redraws whatever fails, including pictures the owner already approved. P05's first run after
  the change re-judged from the top and redrew 3 approved shots before it was stopped. For
  episodes already approved, the 20 (P05) and 8 (P02) eye shots were redrawn with the old
  question checked out for that run only, and their eyes checked by an independent agent.
  Open question for a follow-up: should a rubric change keep standing verdicts of approved
  storyboards and only judge new takes with it?
- 2026-11-06: P05 (20 shots) and P02 (8 shots) redrawn for their eyes and checked by an independent agent; both episodes are on YouTube.
