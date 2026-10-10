---
id: 2026-10-10-policy-demo-exempts-explainer-slides
title: QA policy: the demonstration score is a tutorial rule; an illustrated story (explainer, 奇聞檔案局, So That's Why) is judged without it
status: review
priority: P2
area: api
owner: claude-opus-policy-demo
claimed_at: 2026-10-10T11:16:51Z
created_at: 2026-10-10T20:00:00Z
completed_at:
branch: claude/policy-demo-explainer
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/tests/test_video_judge.py
  - tools/video/qa/policy.mjs
  - tools/video/qa/policy.test.mjs
  - tools/video/qa/checks.mjs
  - docs/videos/HANDS-OFF.md
---

# QA policy: the demonstration score is a tutorial rule; an illustrated story is judged without it

## Why

The final gate's `policy` item asks Jev four questions about the narration
(`apps/api/app/video_automation/judge.py` `POLICY_*_INSTRUCTIONS`): stance, advice, sponsored,
and `demo` — "walks the viewer through a concrete demonstration, setting or worked calculation
they can follow along with", passing at 0.6. Brand stories are already asked without `demo`
(`demo=None`). The first 奇聞檔案局 pilot, `curio-h01` (the Mary Celeste, `format: "slides"`,
`category: "explainer"`), passed the other ten QA items on 2026-10-10 but scored `demo` 0.16–0.18
three times: a history told from court records has nothing the viewer "follows along with", so
the final gate could not approve itself and waited for the owner. So That's Why's T26 passed the
same question only because its subject (how to hold a rice bowl) happens to be a demonstration;
the history-and-curiosity series (docs/videos/history-curiosity/README.md §內容守則) never will
be. The teaching rules (`VALUE_RULES`, 規矩 11) already exempt 原來如此 and this series; the judge
should agree.

## Definition of done

- [x] `judge_policy` asks the `demo` question only for a tutorial-shaped video: skipped (None)
      when the project's `category` is `explainer` or `story`, or the format is a drama; the
      site decides from its own rows (the category the worker reported or the owner set), not
      from the request body alone.
- [x] `policy_note` and the review card read 「有示範：不適用（解說）」 instead of a number for
      those videos; `passed` ignores `demo` when it is None (as it does for stories).
- [x] The tool side (`tools/video/qa/policy.mjs`) shows the same wording in the QA item and the
      tests cover a None `demo`.
- [x] `docs/videos/HANDS-OFF.md` §自動品管 says which categories are asked the demonstration
      question.

## Steps

- [x] Read `judge.py` (`judge_policy`, the story branch, `POLICY_MIN_DEMO`) and
      `tests/test_video_judge.py` for how the story exemption is tested.
- [x] Thread the category: `JudgePolicyIn` keeps its strict shape; the server looks the project
      up by slug (`VideoProject.category`), falling back to asking `demo` when the category is
      unknown.
- [x] Tests on both sides; `cd apps/api && uv run pytest tests/test_video_judge.py`,
      `node --test tools/video/qa/policy.test.mjs tools/video/qa/checks.test.mjs`.

## How to verify

After deploy, `node tools/video/cli.mjs qa --slug curio-h01` shows the policy item passing
with 「有示範：不適用」 and the final gate approves itself when the other ten items pass.

## Notes

- 2026-10-10 filed from the curio-h01 pilot (`2026-10-10-history-curiosity-pilot`). Until it
  lands, the owner approves the final gate of these videos on /admin/videos; the QA report on
  the card shows every other item green.
- 2026-10-10 done on `claude/policy-demo-explainer` (claude-opus-policy-demo):
  - `policy_questions_for` now reads `shorts_line`, `category` and `format` from the video's own
    row in one query and answers a fourth set, `explainer`: the three questions a cut Short is
    asked, read by `read_policy_answers(answers, "explainer")` with the tutorial's thresholds.
    The response's `demo` is null, `questions` is `explainer`, and the note is
    「Jev：符合立場 0.85、有示範：不適用（解說）、建議 0.05、業配 0.10，通過」. `JudgePolicyIn` is
    unchanged, so a request that names a category, a format or a question set is still a 422.
  - Order of the decision: brand-story series (its own five) → cut Short (its own note) →
    category `explainer`/`story` or format `drama` → tutorial. No row, or a row without a
    category on a non-drama format, is asked all four as before.
  - Exempting the drama format also takes the `demo` question away from
    `2026-09-28-video-drama-policy-questions`; what is left of that ticket is the owner's
    decision on whether a drama needs questions of its own (for example the story's "nobody run
    down"). It was not touched here.
  - `curio-h01` passes only if its row says `category: explainer`. The worker reports the
    category from `video.json` and the server takes it only while the row has none; if the row
    was created without it, set it on /admin/videos before running `qa` again.
  - The tests the scope names did not exist: the API cases are in the new
    `apps/api/tests/test_video_judge.py` (the story and cut cases stay in
    `test_video_story_policy.py`, untouched and still green), the tool cases in the new
    `tools/video/qa/policy.test.mjs`. `admin_api.py`, `schemas.py` and `checks.mjs` needed no
    change: the note comes from the server and the tool prints it as it is.
  - `claim` refused at first because `2026-10-09-video-languages-are-four-drop-zh` is still
    marked in progress with a scope of whole directories, although its work merged as #1413;
    claimed with `--force`. That ticket needs `done`.
  - `node tools/video/long-form/cli.mjs check` reports
    `stale duration review binding: apps/api/app/video_automation/judge.py`. The receipt
    (`docs/videos/long-form/review.md`, `review.json`) is left for an independent reviewer.
