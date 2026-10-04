---
id: 2026-10-04-fault-checks-for-the-drama-judges
title: Fault checks for the drama's judges (sheets, keyframes, clips) and sharper subject and finger checks
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-04T01:41:03Z
completed_at:
branch:
depends_on:
  - 2026-10-03-keyframe-judge-scale
scope:
  - tools/video/media/look.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/clips.test.mjs
  - docs/videos/DRAMA.md
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Fault checks for the drama's judges (sheets, keyframes, clips) and sharper subject and finger checks

## Why

`2026-10-03-keyframe-judge-scale` measured that the media judge (gemini-3.8-flash), asked for a
score from 0 to 10, gives "nothing wrong" a 7 and never goes higher, whatever the request or the
system instruction says about the scale, so the owner's bar of 7 sits on the model's ceiling. It
moved illustrated slides to yes/no fault checks (`keyframeChecks`, `JudgeCriterion.cost`, scores
computed by the server), which were measured on 163 recorded takes. Two things were left:

1. The drama's judges are still asked for scores and sit at 7 too: a look sheet at 7 on every
   criterion, a clip at 6.72 with no criterion above 7 (the wedding pilot's recorded verdicts),
   and the explainer's stills. They were not changed because none of their takes were measured,
   and their rubrics ask other things (identity against a sheet, motion, a cut inside a clip).
2. The checks miss what the judge does not see. Of twelve takes two picture editors rejected,
   four pass: six digits on one hand with no fault found (`kickboards-3`), letter-like marks
   (`pottery-wide-1`), and two where the main action is wrong but was read as a missed detail
   (`kiln-door-1`: the door wide open in a shot about closing it). `subject` was never answered
   true in 163 takes.

## Definition of done

- [ ] The drama's sheets, keyframes and clips are judged by fault checks whose questions were
      measured on recorded takes of a real drama, with the before and after distribution shown
      and `judge_min_score` untouched; or it is written down, with numbers, why they stay scored.
- [ ] The `subject` and `anatomy` checks catch the labelled misses above without failing the
      takes the editors called usable, measured on the same 163 takes (or the finding that no
      wording does, and what would: a stronger judge model, a second look).

## Steps

- [ ] Collect recorded verdicts of a drama's look, keyframes and clips (the wedding pilot's work
      directory has a few; a full episode is better) and tabulate them as `dist.mjs` does.
- [ ] Draft checks for each kind from the existing rubric questions and the serious faults
      `INSTRUCTIONS` lists (identity against the sheet, a cut inside a clip, the subtitle band).
- [ ] Measure on the recorded takes before changing code; ask the owner before spending
      (about US$0.01 a call).
- [ ] Try a `subject` question that names the shot's one main action, and an `anatomy` question
      that asks for the count of each large hand, on the 28 labelled takes.

## How to verify

`node <calibration>/checks-report.mjs <label> --quiet` on the new runs: the labelled usable takes
pass, the labelled rejects fail, and the verdict of a take asked about twice does not change.

## Notes

- The kit, the labels and every recorded answer are in
  `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/judge/calibration/` on the machine that made
  the DevDay video. The 163 pictures are in the site's media store only until 2026-10-17.
- A reworded question has to be measured again: the shipped questions are byte for byte the
  measured ones.
- What did not work, so nobody tries it again: explaining the scale in the request context, in
  the rubric questions or in the system instruction; a grade per criterion; a deduction per
  criterion. Numbers in `docs/videos/ILLUSTRATED.md` §judge 的刻度與判定沿用.
- A candidate system instruction or answer format can only be measured inside the API container
  or after a deploy; the auto-mode classifier refuses a script piped into the container, so it
  needs the owner (skill `deploy`, rule 6).
