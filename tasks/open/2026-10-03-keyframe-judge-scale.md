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
  - apps/api/app/video_media/schemas.py
  - apps/api/tests/test_video_media_api.py
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
offered and not chosen), so the fix is the scale the judge scores on, not the number.

## Definition of done

- [x] A shot with no passing take keeps its best-scoring take, not its last.
- [x] A prompt or camera edit sends only that shot back to the judge; every other shot keeps its
      takes and verdicts, failed ones included; `--force` still asks again.
- [x] A judge call cannot lower the owner's bar for itself (`min_score` only raises it).
- [ ] The judge uses the scale: a take with nothing to fix scores 9 or 10, a take with a serious
      fault (wrong finger count, readable text, a floating or duplicated part, the main action
      missing) has that criterion under the server's floor of 4, and the same picture asked about
      twice keeps its verdict. Shown as the distribution of the 163 recorded takes before and
      after, with the owner's `judge_min_score` untouched.
- [ ] Editors' labels hold: the takes they called usable pass, the takes they rejected fail
      (`labels.json` in the calibration folder).

## Steps

- [x] Tabulate the recorded verdicts (`dist.mjs`); confirm the ceiling in the drama's verdicts.
- [x] `bestTake`, `entryStands` and the per-take `judged` stamp in `media/keyframes.mjs`;
      `Stage.imageKey` in `media/stages.mjs`; tests in `look-keyframes.test.mjs`.
- [x] `min_score` is a floor-respecting override in `video_media/admin_api.py`; test.
- [x] Try the anchors from the request (no deploy needed): in `context.scale`, then as a
      start-at-10 deduction rule plus " 10 = no fault found." on every rubric question. 28
      recorded takes each through the site, US$0.56. Neither moved the top: max 7.04 and 7.14,
      no criterion at 8 or more. Not shipped.
- [ ] Try the anchors in the system instruction on the same 28 takes (`host/h1.sh`, built, not
      run: see Notes). If the top moves, measure all 163 takes twice (the second pass gives the
      flip rate) plus 60 takes of the question as it is asked today, as the control.
- [ ] If the system instruction does not move it either: the model lists faults with a severity
      and the server computes the scores (the way `verdict()` already recomputes the overall).
- [ ] Ship whichever was measured: the server takes the scale from the request and puts it in the
      system instruction (a request without one is judged exactly as today, so the drama's judge
      does not change), the keyframes stage sends it for illustrated slides once the server says
      it accepts one, and a warning when no take of a run reaches 9.
- [x] `docs/videos/ILLUSTRATED.md` §judge 的刻度與判定沿用: the numbers, what changed, what is left.
- [ ] Duration receipt increment for `tools/video/media/look-keyframes.test.mjs` by an
      independent reviewer.

## How to verify

```bash
node --test tools/video/media/look-keyframes.test.mjs   # 27 pass
cd apps/api && uv run pytest tests/test_video_media_api.py tests/test_video_media_judge.py -q
node tools/video/long-form/cli.mjs check                # PASS once the receipt increment is in
```

On a video with a drawn storyboard: change one shot's prompt and run `keyframes`; the output
says `N of M drawn shots are unchanged and keep their verdicts`, one picture is drawn and
`media/ledger.json` gains one judge call, not one per cached take.

The scale, once it ships: `node <calibration>/host-report.mjs <label>` (or `dist.mjs` on a
manifest) prints the distribution; the top of the scale must be reached and the labelled takes
must fall on the right side of the bar.

## Notes

- Scope overlap forced at claim time: `2026-10-03-illustrated-slides-round-2-a-family` and
  `2026-10-03-illustrated-slides-lint-heuristics-the-shorts` (both `review`, PR #1172 merged
  2026-10-03 10:34Z) and `2026-10-03-video-worker-narration-takes-made-stale` (PR #1182 merged
  17:05Z) still list these files; their work is on main and nobody is on those branches.
- Spending: the owner allowed up to US$5 of re-judging on 2026-10-04. Spent US$0.56 (two trials of
  28 takes through the site's `/video/media/judge`). Not booked in the video's ledger.
- Why the request cannot fix it: the server's system instruction ("0 (fails completely) to 10
  (flawless). Be strict") outranks anything in the rubric or the context. The low end did follow
  the anchors (an extra arm 4 to 3, readable text 3.5-4 to 3); the top did not move at all.
- The judge also misses faults the editors caught: `kickboards-3` (six digits) and `lane-rope-3`
  (drawn as a tilted photograph of a print) both scored 7 in the trials. That is a second
  problem (what the rubric makes it look for), to measure after the scale.
- The measurement kit is on this machine, outside the repository:
  `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/judge/calibration/`. `rejudge.mjs` asks the
  site's judge about recorded takes (it rebuilds every request from `round2.json`; all 163 cache
  keys match). `host-build.mjs` + `host-judge.py` build one shell script that judges takes
  inside the production API container under a candidate system instruction: read-only, each
  call reserved against the month's judge budget, the key never printed. `host-report.mjs`
  prints before and after. `labels.json` holds the editors' usable and rejected takes.
  The pictures are in the site's media store (kept 14 days from 2026-10-03/04); 58 of the 163
  were overwritten on disk by later redraws, so measure before 2026-10-17.
- 2026-10-04: the owner chose to try the system instruction on the host before writing it into
  the pull request. The auto-mode classifier refused the call that pipes the script into the
  container (skill `deploy`, rule 6), and it was not retried. It needs the owner: run
  `host/h1.sh` themselves, or switch the session to Manual. Until then the pull request carries
  the three tool fixes only, as a draft.
- Not done on purpose: no change to `judge_min_score`, to the rubric questions, or to how a
  drama's keyframes, sheets and clips are judged.
