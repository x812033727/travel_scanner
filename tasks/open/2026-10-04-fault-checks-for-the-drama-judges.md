---
id: 2026-10-04-fault-checks-for-the-drama-judges
title: Fault checks for the drama's judges (sheets, keyframes, clips) and sharper subject and finger checks
status: in-progress
priority: P2
area: tools
owner: claude-fable-5.1-elated-lamarr
claimed_at: 2026-10-23T16:04:00Z
created_at: 2026-10-04T01:41:03Z
completed_at:
branch: claude/elated-lamarr-9f0ed3
depends_on:
  - 2026-10-03-keyframe-judge-scale
scope:
  - tools/video/media/look.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/clips.test.mjs
  - docs/videos/DRAMA.md
  - docs/videos/BINGE.md
  - docs/videos/ILLUSTRATED.md
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
- [x] Draft checks for each kind from the existing rubric questions and the serious faults
      `INSTRUCTIONS` lists (identity against the sheet, a cut inside a clip, the subtitle band).
      Done for keyframes (2026-10-24, manga tier only, shipped: see Notes); sheets and clips
      are still drafts to write.
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

### 2026-10-24: the manga tier's keyframes take the checks (claude-fable-5.1)

- Why now: 《系統說我是 BUG》e001 (46 shots, image-01 stills, `visual_tier: "manga"`) blocked on
  2026-10-23 15:11Z with "keyframes still fails after 2 prompt fixes": best take per shot
  5.08–7.03, one shot ≥ 7; the judge's problems were the letterbox bars (42 lines), `clean`
  (85), style "looks 3D", `no_text` (20). The scored ceiling of 7 again, so the measured route
  was taken without a new measurement: the checks are what gets measured on e001–e004.
- What shipped (`media/keyframes.mjs`, `docs/videos/DRAMA.md` §manga 等級的關鍵影格用是非題):
  `keyframeChecks({ characters, subtitleBand, craft: false })` for `visual_tier === "manga"`
  on a server with `limits.judge_checks`. The seven measured questions word for word
  (`text`, `anatomy`, `detached`, `subject`, `frame`, `details`, `awkward`), plus one
  `identity_<id>` redraw check per character in the shot (against the sheet the judge is
  shown; the shot-look variant cuts the appearance to the 400-character limit), `style` held
  to the sheets (3D render, photograph, another palette or finish), `subtitle_band` (cost 3,
  weight 1) when subtitles are burned in; no `generated`, since its fix clauses would be
  written into an anime still's retake prompt. `needs_review` only when a redraw check is
  answered true (every redraw check is cost 10, under the floor of 4); at a bar of 7 two
  second-look flaws pass and three fail. `judge_min_score` untouched. Other tiers scored as
  before.
- The judge is shown the cut-in copy for manga (trim first, `stage.upload`, then judge), on
  any server: image-01's bars and edge marks are inside what `trim.mjs` cuts, and judged whole
  the bars failed 42 of 46 shots and their fix clauses went into every retake.
- Not measured on recorded takes: `identity_*`, the sheets variant of `style`, `subtitle_band`,
  and judging the cut copy. The before/after on e001 after the deploy is written below.
- Still open on this ticket: the look sheets and the clips (scored; no recorded takes
  measured), and the sharper `subject`/`anatomy` wording on the 28 labelled takes.
- A candidate system instruction or answer format can only be measured inside the API container
  or after a deploy; the auto-mode classifier refuses a script piped into the container, so it
  needs the owner (skill `deploy`, rule 6).
- 2026-10-24: The owner authorized releasing only `docs/videos/long-form/review.md` and
  `docs/videos/long-form/review.json` from this ticket for C15's independent duration
  review binding. All other scope and unfinished judge work stay here.
