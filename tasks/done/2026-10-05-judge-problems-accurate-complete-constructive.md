---
id: 2026-10-05-judge-problems-accurate-complete-constructive
title: Judge problems that are accurate, complete and constructive: key, fault, and one prompt-level fix
status: done
priority: P2
area: api
owner: claude-fable-5-1-judge
claimed_at: 2026-10-05T17:49:19Z
created_at: 2026-10-05T16:08:25Z
completed_at: 2026-10-05T18:14:30Z
branch: claude/judge-problems
depends_on:
  - 2026-10-04-fault-checks-for-the-drama-judges
  - 2026-10-05-media-budget-estimate-reserve-reconcile
scope:
  - apps/api/app/video_media/judge.py
  - apps/api/tests/test_video_media_judge.py
  - tools/video/media/keyframes.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/look.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/clips.test.mjs
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Judge problems that are accurate, complete and constructive: key, fault, and one prompt-level fix

## Why

The judge's `problems` are free text: a take can fail a criterion with no problem naming it,
or carry a problem that names no failed criterion, and the retake prompt gets nothing it can
act on. The reviewer rules of the CHAI study (accurate: point at the place; complete: scan for
the same fault elsewhere; constructive: every critical finding proposes a fix), used by
OpenMontage's reviewer skill (AGPL — idea only), are the contract to enforce.

## Definition of done

- [x] Every `problems[]` string is `"<criterion key>: <what is wrong and where> → <one
      prompt-level change>"`; the server drops a problem naming no failed criterion and
      synthesises one for a failed criterion without a problem; the instructions ask for the
      fix clause. `JudgeOut`'s shape and the review payload keys
      (`shots[].judge.overall/problems/passed`) are unchanged.
- [x] The tool's retake loops put the fix clause into `needs_review` hints and the next take's prompt.
- [ ] Measured on the 163 recorded takes of the fault-checks ticket: the share of failed takes
      whose problem names the failing criterion, before and after, in this ticket. (Not done:
      the kit, the labels and the recorded answers are off-repo; see Notes for how.)

## Steps

- [x] `judge.py`: instructions, post-processing, tests with fake answers.
- [x] `keyframes.mjs`, `clips.mjs`, `look.mjs`: carry the fix clause; tests.
- [x] `ILLUSTRATED.md` §judge.
- [ ] Receipt increment for the two bound test files (an independent reviewer, not the author).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_judge.py -q
node --test tools/video/media/look-keyframes.test.mjs tools/video/media/clips.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `media/look-keyframes.test.mjs`, `media/clips.test.mjs`.
- Depends on the fault-checks ticket (the questions) and the budget gate (judge calls count).
- Claimed with `--force` over the open, unowned `depends_on`
  `2026-10-04-fault-checks-for-the-drama-judges`: that ticket moves the drama's judges from
  scores to yes/no fault checks and sharpens the `subject` and `anatomy` questions. This one is
  about the wording and completeness of `problems` and feeding the fix into the retake, and
  the server's post-processing works for a scored rubric and for fault checks alike (both are
  tested), so nothing in it is a precondition; whichever lands second rebases the three
  `media/*.mjs` files it shares. Its own DoD and Notes were not touched. The branch starts from
  `claude/media-budget-reserve` (PR #1299, the finished budget ticket) because the `clips.mjs`
  and `clips.test.mjs` edits sit beside its; the parent session merges main when #1299 lands.
- What was built (2026-10-05):
  - `judge.py`: `INSTRUCTIONS` and `CHECK_INSTRUCTIONS` ask for one line per fault in the form
    `<criterion key>: <what is wrong and where> → <the one change to the prompt that would
    prevent it, as the words to put in the prompt>` (`PROBLEM_FORMAT`); the scale sentence and
    the fault-check sentences ("answer true when it is there…", "never reads the prompt") are
    byte for byte what was measured. `failed_criteria()`: a fault check failed when the fault
    was found (score < 10); a scored criterion failed when under `max(min_score, 4)` (a take
    under the bar always has one, since the overall is the weighted mean; a passed take may
    still have one, and keeps its line). `problems()`: a line naming no criterion, a criterion
    not in the rubric, or one that did not fail is dropped (the measured "nothing wrong" seven
    at a bar of seven fails nothing, so its remarks go); the key is read leniently (`Text:`,
    `**anatomy** -`, `identity jingwei:`, `anatomy → …`); a line with no fix gets
    `PLACEHOLDER_FIX` (`write the correction into the prompt`); a failed criterion no line
    names gets `<key>: the judge found it but did not say what or where (asked: <question>) →
    <placeholder>`; the judge's lines first (its order, at most 20, duplicates once), then the
    added ones in rubric order; a line is at most 400 characters, the fix at most 200 and never
    cut off. `JudgeOut` and the review payload are unchanged.
  - `keyframes.mjs`: `FIX_ARROW`, `PLACEHOLDER_FIX`, `fixClauses` (the clause after the arrow,
    once each, the placeholder left out), `fixesBefore(takes, seed)` (the clauses of the judged
    takes with a lower seed, in seed order), `retakePrompt` (`<prompt>. Corrections: a; b`,
    4000 characters). The style plate, every keyframe take, every clip take and every sheet
    candidate after the first is asked with the fixes of the ones before it; what it was asked
    with is recorded as `takes[].fixes` / `candidates[].fixes`; a `needs_review` entry carries
    `fixes` beside `problems`, and stdout prints `  fixes for <id>: …` under the `ERROR` line.
    `entryStands` recomputes each take's key with the same rule, so a shot keeps its takes over
    a prompt edit elsewhere; a manifest from before this change has no arrows, so no fixes and
    the same keys as before. `clips.mjs` and `look.mjs` import the three helpers from
    `keyframes.mjs` (a new module would be outside the scope; `clips.mjs` already imported it).
  - A design choice worth knowing: in `look`, the fixes apply within a round too (candidate B
    is asked with A's fix), not only in the second round; the candidates are drawn one after
    another and a fault's fix does not narrow the owner's choice. Also `clips import` records
    `fixes` on a refused clip, as the hint for the next attempt outside.
  - The placeholder is a cross-component contract on one string: `judge.py` writes it,
    `keyframes.mjs` recognises it; both test files pin the spelling.
- Not measured (DoD 3): the 163 takes, the labels and every recorded answer are in
  `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/judge/calibration/` on the machine that made
  the DevDay video, not in the repo, and the pictures stay in the site's media store only until
  2026-10-17. To do it after this deploys: `rejudge.mjs` through the site on the same 163 takes
  (about US$1.63; ask the owner), then for every failed take count whether a `problems` line's
  key equals a criterion answered true; the "before" is the recorded answers in `host/fa.out`
  with keys matched by keyword (text/letter/word, finger/hand/arm, float/detached, style,
  frame/border). The only change to the system instruction is the "problems" clause; the yes/no
  answers should not move, but that is a claim to measure, not to make.
- Noticed, not done: `drama_preflight.mjs` and `run_report.mjs` print a shot's `problems` and
  could print `fixes` (skill scripts, outside the scope); `review/sync.mjs` sends the full
  lines to the admin page, which shows them after the score as before (an arrow per line now).
- Receipt: `tools/video/media/look-keyframes.test.mjs` and `tools/video/media/clips.test.mjs`
  are the changed files in `REVIEW_FILES`; the author did not touch `review.md`/`review.json`
  (`node tools/video/long-form/cli.mjs check` reports both stale until an independent reviewer
  adds the increment on this branch, with the budget branch's receipt as the baseline).
