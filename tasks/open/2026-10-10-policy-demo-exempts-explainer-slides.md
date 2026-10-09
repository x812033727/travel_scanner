---
id: 2026-10-10-policy-demo-exempts-explainer-slides
title: QA policy: the demonstration score is a tutorial rule; an illustrated story (explainer, 奇聞檔案局, So That's Why) is judged without it
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T20:00:00Z
completed_at:
branch:
depends_on:
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

- [ ] `judge_policy` asks the `demo` question only for a tutorial-shaped video: skipped (None)
      when the project's `category` is `explainer` or `story`, or the format is a drama; the
      site decides from its own rows (the category the worker reported or the owner set), not
      from the request body alone.
- [ ] `policy_note` and the review card read 「有示範：不適用（解說）」 instead of a number for
      those videos; `passed` ignores `demo` when it is None (as it does for stories).
- [ ] The tool side (`tools/video/qa/policy.mjs`) shows the same wording in the QA item and the
      tests cover a None `demo`.
- [ ] `docs/videos/HANDS-OFF.md` §自動品管 says which categories are asked the demonstration
      question.

## Steps

- [ ] Read `judge.py` (`judge_policy`, the story branch, `POLICY_MIN_DEMO`) and
      `tests/test_video_judge.py` for how the story exemption is tested.
- [ ] Thread the category: `JudgePolicyIn` keeps its strict shape; the server looks the project
      up by slug (`VideoProject.category`), falling back to asking `demo` when the category is
      unknown.
- [ ] Tests on both sides; `cd apps/api && uv run pytest tests/test_video_judge.py`,
      `node --test tools/video/qa/policy.test.mjs tools/video/qa/checks.test.mjs`.

## How to verify

After deploy, `node tools/video/cli.mjs qa --slug curio-h01` shows the policy item passing
with 「有示範：不適用」 and the final gate approves itself when the other ten items pass.

## Notes

- 2026-10-10 filed from the curio-h01 pilot (`2026-10-10-history-curiosity-pilot`). Until it
  lands, the owner approves the final gate of these videos on /admin/videos; the QA report on
  the card shows every other item green.
