---
id: 2026-10-10-outline-pick-demo-exempts-explainers
title: Outline pick: an explainer or story video is not asked for a demonstration either
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T14:52:56Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/tests/test_video_judge.py
  - docs/videos/HANDS-OFF.md
---

# Outline pick: an explainer or story video is not asked for a demonstration either

## Why

PR #1424 (`2026-10-10-policy-demo-exempts-explainer-slides`) stopped the final gate's `policy`
item from asking a video filed as `explainer` or `story` for a demonstration: the question is a
tutorial's rule. The outline gate still asks it of every video. `judge_outline` scores each
option's `demo`, and `outline_pick_passed` / `_pick_passes` require the chosen option to reach
`PICK_MIN_DEMO` (0.6) before the pick approves itself
(`apps/api/app/video_automation/judge.py`). On 2026-10-10 the first MiniMax episode of
原來如此事務所, `sothatswhy-b26` (`format: "slides"`, `category: "explainer"`), was picked by
Jev with certainty (A, 1.00; stance 0.92, advice 0.02) and still waited for the owner because
「有示範 0.33 低於 0.6」. The three 奇聞檔案局 pilots passed the same question only by luck
(0.67 to 0.89). An illustrated story has nothing to follow along with at the outline stage any
more than in its narration.

## Definition of done

- [ ] The outline pick of a video whose own row says `explainer` or `story` is decided on
      stance and advice only: the `demo` question is not asked (or its score is not required),
      decided from the site's row as `policy_questions_for` does, never from the request body.
- [ ] The pick's note reads 「有示範：不適用（解說）」 for those videos, as the policy note does.
- [ ] A tutorial-shaped video, a video with no row and a video with no category are judged
      exactly as today.
- [ ] `docs/videos/HANDS-OFF.md` says which categories the outline pick asks for a
      demonstration.

## Steps

- [ ] Read how #1424 threaded the category (`policy_questions_for`, the `explainer` question
      set) and whether the row already exists when the outline is pushed (the worker reports
      the category from `video.json`; a local `review-push --gate outline` creates the row).
- [ ] Tests beside `apps/api/tests/test_video_judge.py`'s policy cases.
- [ ] `judge.py` is bound by the duration receipt: an independent reviewer re-issues it.

## How to verify

`cd apps/api && uv run pytest tests/test_video_judge.py`; after a deploy,
`node tools/video/cli.mjs review-push --gate outline --slug <an explainer>` prints a pick whose
note does not hold the video back for 「有示範」.

## Notes

- 2026-10-10 filed from `sothatswhy-b26` (ticket `2026-10-10-sothatswhy-minimax-images`).
