---
id: 2026-10-03-jev-noul-criteria-keys-yes-no
title: Jev noul criteria are sent as yes/no; TypeSafe documents true/false
status: done
priority: P2
area: api
owner: claude-opus-5-5-jev-contract
claimed_at: 2026-10-04T14:50:09Z
created_at: 2026-10-03T17:48:46Z
completed_at: 2026-10-04T15:31:28Z
branch: claude/jev-criteria-true-false
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_speech/checking.py
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/api/app/ai/jev.py
  - apps/api/tests/test_jev_client.py
---

# Jev noul criteria are sent as yes/no; TypeSafe documents true/false

## Why

TypeSafe documents a noul's optional `criteria` as an object with `true` and `false`
descriptions: "An object with `true` and `false` descriptions of what a yes and a no mean"
(https://docs.typesafe.ai/primitives/noul, opened 2026-10-03); the API reference lists only
those two properties (https://docs.typesafe.ai/api), and the Python SDK schema forbids extra
keys. The site sends `yes` / `no` instead, in four places:

- `apps/api/app/video_automation/judge.py:228` (`NOUL_CRITERIA`)
- `apps/api/app/video_speech/checking.py:125-126`
- `apps/api/app/news_automation/ai.py:344-345` (publish question) and `:410-411` (duplicate check)

The calls succeed, so the HTTP API accepts the request. Whether it uses or silently ignores the
`yes` / `no` descriptions is undocumented. If it ignores them, every one of these questions has
been answered without the clarification it was written with.

## Definition of done

- [x] All four places send `true` / `false`.
- [x] `NoulQuestion.criteria` cannot be built with any other keys (the type lives in
      `apps/api/app/ai/jev.py:97`; that file is in the scope of
      `2026-10-03-jev-comments-drifted-from-vendor-docs`, so do this after it or widen with care).
- [x] The `checking.py:11-14` docstring says what happens now: a line below the threshold (0.5
      by default, `tools/video/tts/check.mjs:53`) is flagged, and a narration with every line
      checked and none flagged is approved on arrival while the auto-approve setting is on
      (`apps/api/app/video_reviews/admin_service.py:1446-1458`). It currently says the owner
      still approves the narration.

## Steps

- [x] Rename the keys and update the tests that pin them (`apps/api/tests/test_video_automation_judge.py`).
- [ ] Because fixing the keys may change the answers, re-check a few known lines and news
      candidates after deploy and note any shift here.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_automation_judge.py
```

## Notes

- Do not claim the API rejects or ignores `yes` / `no`; only the mismatch with the documented
  contract is established.
- Claimed with `--force` on 2026-10-04 by claude-opus-5-5-jev-contract, on the same branch as
  `2026-10-03-jev-comments-drifted-from-vendor-docs` (done first, as the DoD asks). The
  overlapping claims had all landed on origin/main: `2026-09-27-news-evidence-excerpts-stop-at-8`
  (codex/p1-task-audit) as #966, `2026-09-30-news-duplicate-check-treats-a-new` as #1041,
  `2026-09-30-a-cut-short-is-not-asked` as #998, `2026-09-27-video-drama-room-withdraw-a-one`
  (claude/video-review-manga-workflow-fp1rpz) as #870, and
  `2026-10-03-illustrated-slides-round-2-a-family` as #1172. No open PR touched these files.
- Scope widened by two files: `apps/api/app/ai/jev.py`, where the type lives (the DoD's own
  pointer), and `apps/api/tests/test_jev_client.py`, which pins that the type refuses other keys.
- The type: `NoulCriteria` in `app.ai.jev`, a model with `extra="forbid"` and two required
  string fields `true` and `false`, the name the vendor's Python SDK uses
  (`criteria=NoulCriteria(true=..., false=...)` on /primitives/noul). `NoulQuestion.criteria` is
  `NoulCriteria | None`. A dict with `yes` / `no`, with only one of the two keys, or with a third
  key raises `ValidationError` before a call is spent. The four call sites build `NoulCriteria`
  directly; `guides/jev_review.py` already sent `true` / `false` as a dict, which pydantic still
  accepts. Both descriptions are required because the vendor page describes the object as having
  both, and every caller writes both.
- `judge.NOUL_CRITERIA` is now a `NoulCriteria`, so `tests/test_video_story_policy.py`'s
  `question.criteria == judging.NOUL_CRITERIA` keeps comparing like with like.
- The checking docstring: the 0.5 threshold is `DEFAULT_THRESHOLD` in
  `tools/video/tts/check.mjs`, and the narration decision is
  `app.video_automation.settings.auto_approves_audio` (all lines checked, none flagged, switch on;
  a drama reads its own switch), called from `video_reviews/admin_service.py`.
- Second step left unticked: re-checking known lines and news candidates after the keys change
  needs the deploy and production calls, which this ticket's agent may not make. Whoever deploys
  it can compare `noul` values in the next narration check and the next news `jev-zh-TW` runs
  with earlier ones; the test fixtures here mock Jev and cannot show a shift.
- `jev.py` is not receipt-bound; `apps/api/app/video_automation/judge.py` is (in
  `reviewed_files` of `docs/videos/long-form/review.json`), so the PR is a draft until an
  independent reviewer adds the receipt increment.
