---
id: 2026-10-22-clarify-jev-sponsorship-question-for-free
title: Clarify Jev sponsorship question for free own-channel subscribe CTA
status: done
priority: P2
area: api
owner: codex-s34-policy-qa
claimed_at: 2026-10-22T02:05:37Z
created_at: 2026-10-22T02:05:34Z
completed_at: 2026-10-22T02:07:37Z
branch: codex/curio-s34-self-cta-policy-20261022
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/tests/test_video_automation_judge.py
  - docs/videos/HANDS-OFF.md
---

# Clarify Jev sponsorship question for free own-channel subscribe CTA

## Why

S34's unchanged historical narration received Jev sponsored scores 0.41–0.44 and failed the
0.30 policy threshold. Its only promotional wording invites a free subscription to its own
YouTube channel. The shared question says a named service "sign up" counts and does not
distinguish that invitation from paid or third-party promotion. The prior scores stay failed;
this change only clarifies future questions.

## Definition of done

- [x] The shared Jev policy question explicitly excludes a standalone free own-channel
  subscription invitation while retaining paid, external, and third-party pitches.
- [x] Tests protect the question used by full videos and cut Shorts, and the numeric
  sponsored gate continues to reject scores above 0.30.
- [x] S34 remains held until a newly recorded assessment of its unchanged script and
  final-cut hashes passes; this PR does not rewrite the historical verdict.

## Steps

- [x] Clarify the Jev question and the documented QA rule.
- [x] Run the touched API tests and lint checks.
- [x] Prepare a reviewable PR and report what must be rerun after deployment.

## How to verify

`cd apps/api && ruff check app/video_automation/judge.py tests/test_video_automation_judge.py`
and `pytest -q tests/test_video_automation_judge.py` using the shared API virtual environment;
`mypy app/video_automation/judge.py tests/test_video_automation_judge.py`;
`npm run check:tasks`.

## Notes

The score threshold and verdict parser are unchanged. Existing S34 QA is 9/11: besides
`policy`, the cloud's YouTube URL check is blocked by a proxy CONNECT failure. A Jev
question update alone cannot make the old QA record pass, and this PR does not deploy code
or submit a new Jev review.

Verification: 46 API judge tests passed; Ruff passed; focused mypy passed; task-board
validation passed (only pre-existing stale and overlapping-claim warnings).
