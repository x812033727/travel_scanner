---
id: 2026-09-30-a-cut-short-is-not-asked
title: A cut Short is not asked for a demonstration
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-30T01:02:57Z
created_at: 2026-09-30T01:02:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/tests/test_video_story_policy.py
  - docs/videos/SHORTS.md
---

# A cut Short is not asked for a demonstration

## Why

On 2026-09-30, with the channel stance written, the twelve highlight Shorts cut from the
ai-real-world long videos all failed the `policy` item on 「有示範」 (0.07-0.16) while keeping to
the stance (0.87-0.92). A 26-second highlight has no room for a worked example; the example is
in the long video it links back to. The owner decided the cut line is not asked that question.

## Definition of done

- [x] `POST /video/automation/judge/policy` asks a Short whose `shorts_line` is `cut` the
      tutorial's stance, advice and sponsored questions without the demonstration, and passes it
      on the tutorial's thresholds; lab Shorts, tutorials and dramas are asked as before.
- [x] SHORTS.md's QA table says so.

## How to verify

`uv run pytest tests/test_video_story_policy.py tests/test_video_automation_judge.py`; after the
deploy, `node tools/video/shorts/cli.mjs qa --dir <cut build>` shows 「Jev（精華）：…」.

## Notes

- The twelve cuts still fail `metadata` and `links` until their long videos are on YouTube.
- After the deploy the twelve need `qa` + `push` again from
  `mokaair-work/shorts-fixes-20260929/cuts/<slug>/safe-*` (the builds whose `final_sha256`
  matches the pending review), not from `mokaair-work/shorts/`.
