---
id: 2026-10-03-keyframe-judge-scale
title: Keyframe judge scores saturate at the pass bar: anchor the scale, keep the best take, stop re-judging unchanged takes
status: in-progress
priority: P1
area: tools
owner: claude-fable-5-1-judge-scale
claimed_at: 2026-10-03T23:55:55Z
created_at: 2026-10-03T23:55:43Z
completed_at:
branch: claude/keyframe-judge-scale
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/look-keyframes.test.mjs
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/judge.py
  - apps/api/app/video_media/schemas.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_video_media_judge.py
---

# Keyframe judge scores saturate at the pass bar: anchor the scale, keep the best take, stop re-judging unchanged takes

## Why

The judge that passes or fails every keyframe gives a picture it has no remark on a 7 and never
goes higher, and the owner's bar (`judge_min_score`, drama settings tab) is 7. So a take passes
only when the judge says nothing at all, a 0.2 dip on one criterion fails it, and asking about
the same picture twice flips the verdict.

Measured on the first illustrated-slides video drawn end to end (`openai-devday-2026-recap`,
2026-10-04, 74 shots, look `riso-navy`, gemini-3.1-flash-image at 2K):

- 163 judged takes: overall max 7.04, mean 6.74, median 6.79; 43 (26%) at or above 7, all of
  them at 7.00 to 7.04; of 815 criterion scores 471 are exactly 7 and none reaches 8.
- 24 of the 43 passing takes had problems listed; they passed because the scores stayed at 7.
- One prompt edit reset `keyframes/manifest.json` (it is bound to `pictures_hash`), every cached
  picture went back to the judge, five shots that had passed failed and three that had failed
  passed, with no picture changed.
- For 23 of the 31 shots with no passing take the tool kept a take that was not the shot's
  best-scoring one (it keeps the last).
- US$20.27 for 176 images got 43 of 74 shots through, against a per-video cap of US$25;
  `assemble` refuses while any shot is `needs_review`. Two picture editors found a usable take
  for every one of 18 failing shots they looked at.
- The same ceiling shows in the drama's judge (a look sheet at 7 on every criterion, a clip at
  6.72 with no criterion above 7), so it is the judge's scale, not the illustrated rubric.

The owner decided on 2026-10-04 to keep the bar at 7 (a lower bar and a tool-owned bar were both
offered and not chosen), so the fix is how the judge is asked, not the number.

## Definition of done

- [x] A shot with no passing take keeps its best-scoring take, not its last.
- [x] A prompt or camera edit sends only that shot back to the judge; every other shot keeps its
      takes and verdicts, failed ones included; `--force` still asks again.
- [x] A judge call cannot lower the owner's bar for itself (`min_score` only raises it).
- [x] The top of the scale is reached and the bar means something, with `judge_min_score`
      untouched, shown on the 163 recorded takes before and after: a take with nothing to fix
      scores 10 (96 takes), a take with a fault that must be redrawn has that criterion at 0,
      under the server's floor of 4 (18 takes, each with the fault named), and the same picture
      asked about twice keeps its verdict in 99 of 103.
- [ ] Editors' labels hold: the takes they called usable pass (9 of 9), the takes they rejected
      fail (8 of 12; see Notes for the four the judge does not see).

## Steps

- [x] Tabulate the recorded verdicts (`dist.mjs`); confirm the ceiling in the drama's verdicts.
- [x] `bestTake`, `entryStands` and the per-take `judged` stamp in `media/keyframes.mjs`;
      `Stage.imageKey` in `media/stages.mjs`; tests in `look-keyframes.test.mjs`.
- [x] `min_score` is a floor-respecting override in `video_media/admin_api.py`; test.
- [x] Explain the scale to the judge, on 28 recorded takes each: in the request's `context`, as
      "every criterion starts at 10" plus " 10 = no fault found." on every question, and in the
      system instruction in place of "Be strict". A clean picture stayed at 7 on every criterion
      all three times (max overall 7.04, 7.14, 7.17). Not shipped.
- [x] Change the form of the answer, same 28 takes: a grade per criterion (everything came back
      "minor", never "none" or "serious"), a deduction per criterion (2 to 3 points off every
      criterion, a nitpick invented for every take), then yes/no on one concrete fault per
      question. Only yes/no made the model commit: nothing flagged on a clean picture, the
      blatant faults named.
- [x] One more trial of the checks with the finger count asking only for more than five (four
      stylised fingers had failed four good takes) and the frame check naming a picture drawn
      as a photograph of a print.
- [x] Measure the checks on all 163 takes, and 103 of them a second time.
- [x] Server: `JudgeCriterion.cost`, `CHECK_INSTRUCTIONS`, boolean answers and computed scores in
      `video_media/judge.py`; a rubric without costs is asked exactly as before;
      `limits.judge_checks` in `/video/media/status`. Tests.
- [x] Tool: `keyframeChecks` for illustrated slides when the server announces `judge_checks`; a
      take judged on another question is asked again from its cached picture. Tests.
- [x] `docs/videos/ILLUSTRATED.md` §judge 的刻度與判定沿用: every trial, the nine checks, what each
      bar from 7 to 10 means, the before and after.
- [x] Duration receipt increments for `tools/video/media/look-keyframes.test.mjs` by an
      independent reviewer (twice: the tool fixes, then the checks).

## How to verify

```bash
node --test tools/video/media/look-keyframes.test.mjs   # 28 pass
node --test tools/video/media/*.test.mjs                # 86 pass
cd apps/api && uv run pytest tests/test_video_media_api.py tests/test_video_media_judge.py -q   # 12 pass
node tools/video/long-form/cli.mjs check                # PASS
```

The before and after, from the recorded answers (no call is made):

```bash
cd <VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/judge/calibration
node checks-report.mjs fa --quiet     # 163 takes, the 103 asked twice, the editors' labels, bars 7 to 10
```

After the deploy, on the first illustrated-slides video the worker draws: `media-status` shows
`judge_checks` under the limits (`GET /api/video/media/status`), `keyframes/manifest.json` has
`scores` with the nine check keys on every take, clean takes read 10/10 on the contact sheet,
and a shot marked 待修 names a concrete fault. On a video with a drawn storyboard, change one
shot's prompt and run `keyframes`: the output says `N of M drawn shots are unchanged and keep
their verdicts`, and `media/ledger.json` gains one judge call, not one per cached take.

## Notes

- Scope overlap forced at claim time: `2026-10-03-illustrated-slides-round-2-a-family` and
  `2026-10-03-illustrated-slides-lint-heuristics-the-shorts` (both `review`, PR #1172 merged
  2026-10-03 10:34Z) and `2026-10-03-video-worker-narration-takes-made-stale` (PR #1182 merged
  17:05Z) still list these files; their work is on main and nobody is on those branches.
- Spending: the owner allowed up to US$5 of re-judging on 2026-10-04; 462 judge calls were made,
  US$4.62: 56 through the site's `/video/media/judge`, 406 inside the production API container
  with the owner's go-ahead (a read-only script, each call reserved against the month's judge
  budget, the key never printed). Nothing was booked in the video's own ledger.
- What the trials say about this judge model (gemini-3.8-flash): asked for a number, a grade or
  a deduction it settles on a middle default (7, "minor", 2 to 3 off) and no wording moves the
  ends; only an explicit number at the low end is followed (readable text and an extra arm went
  to 3). A yes/no question about one concrete fault is answered plainly. So the scores are
  computed by the server from yes/no answers, the way `verdict()` already recomputed the overall.
- Before and after on the 163 recorded takes at the owner's bar of 7: 43 takes passing (26%)
  became 145 (89%); shots with a passing take 43 of 74 became 73 of 74; every one of the 43
  that passed still passes; the 18 that fail are all redraw faults with the fault named (text 6,
  floating or stray parts 7, a picture drawn as a photograph of a print or with paper showing 3,
  an extra arm or a sixth finger 2). Replayed in seed order the run would have drawn 83 takes
  for 73 shots instead of 163 for 43. At a bar of 8 or 9: 137 takes; at 10 (no fault at all, the
  nearest thing to what 7 used to demand): 96 takes, 60 shots.
- Asked twice (103 takes): the verdict differs in 4; all nine answers the same in 85. The checks
  that flip are the judgement calls (`awkward` 12, `details` 7), which do not decide a take at
  7 on their own; `text` never flipped.
- What the judge still does not see (4 of the editors' 12 rejects pass): `kickboards-3` (six
  digits, no fault found), `pottery-wide-1` (letter-like marks on the wheel stand),
  `kiln-door-1` (the door wide open, read as a missed detail), `bell-tray-2` (read as a missed
  detail). `subject` was never answered true in 163 takes. Follow-up:
  `2026-10-04-fault-checks-for-the-drama-judges`.
- The bar's meaning is in the weights and costs of `keyframeChecks` (the table in
  ILLUSTRATED.md). The questions shipped are byte for byte the ones measured; reword one and it
  has to be measured again.
- Not done on purpose: no change to `judge_min_score`; a drama's sheets, keyframes and clips and
  the explainer's stills are scored as before (not measured; they sit at 7 too).
- The measurement kit is on this machine, outside the repository:
  `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/judge/calibration/`: `rejudge.mjs` (through
  the site), `host-build.mjs` + `host-judge.py` (the container script), `checks-report.mjs`,
  `labels.json` (the editors' usable and rejected takes), `host/*.out` (every answer of every
  trial; `fa.out` is the full measurement). 58 of the 163 pictures were overwritten on disk by
  later redraws and exist only in the site's media store, which keeps files 14 days: anything
  to be measured again on these takes has to happen before 2026-10-17.
- The auto-mode classifier refuses a script piped into the production container (skill
  `deploy`, rule 6). It was refused twice here and not retried; the runs happened after the
  owner switched the session to Manual.
- After merge: deploy (the API and the worker's tools together; no migration), then the checks
  under "How to verify". The DevDay video's remaining shots are drawn from the cache where the
  prompt did not change and judged by the checks.
