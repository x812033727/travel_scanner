---
id: 2026-09-27-video-binge-api
title: Video binge A1: series columns, hands-off document and script rules, compilation job, binge form endpoints, download
status: done
priority: P1
area: api
owner: claude-fable
claimed_at: 2026-09-27T11:44:56Z
created_at: 2026-09-27T11:43:45Z
completed_at: 2026-09-27T12:04:32Z
branch: claude/keen-hamilton-plu6kp
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/api/app/video_reviews
  - apps/api/app/config.py
  - apps/api/migrations/versions/0103_video_binge_series.py
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_series_binge.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_migration_0103_video_binge_series.py
---

# Video binge A1: series columns, hands-off document and script rules, compilation job, binge form endpoints, download

## Why

A binge series (docs/videos/BINGE.md) is planned from one button: the server derives the episode
count from the minutes, decides a hands-off series' documents and screenplays from the checker's
verdicts, yields a compilation job once every episode is cleared for upload, quotes the run
against the month's budgets, and serves the compilation's 1080p cut from the worker's volume.

## Definition of done

- [x] Migration `0103_video_binge_series` (renumbered after `0102_video_youtube_sync` landed on main first): `genre`, `lead`, `hands_off`, `compilation`,
      `visual_tier`, `total_minutes`, `compilation_slug/started_at/finished_at` on
      `video_drama_series` with their checks; `ck_video_drama_series` recreated with
      `series_max_in_flight BETWEEN 1 AND 6`; downgrade refuses while a hands-off or compiled
      series exists.
- [x] `SeriesIn` accepts the one-button form (blank slug, title, premise; `total_minutes`),
      `series_values` derives the shape (`binge_shape`), the slug and the title.
- [x] `doc_problem` holds a retention genre's chapter outline to `hook_type`, `lead_arc`,
      `satisfaction` beats, the no-two-suffering rule and a payoff every four episodes.
- [x] `submit_doc` on a hands-off series approves, sends back or leaves for the owner from the
      checker's verdict (`series_doc_passed`, `auto_doc_status`), audited.
- [x] `auto_approves_script` (`script_check_passed`), and `auto_picks_look` /
      `auto_approves_storyboard` treat a hands-off series as switched on; `submit_review`
      decides `script` reviews and tells the final rule when the video is a compilation.
- [x] `next_job_for` yields `compilation` for a finished compilation series once;
      `start_compilation` / `finish_compilation` and their tool routes; `actions/compile`.
- [x] `GET /admin/video-automation/series/binge-quote` (`binge_quote`) and
      `GET /admin/videos/{slug}/download` (`download_path`, `video_work_dir`);
      `ProjectSummary.compilation` / `download_available`.
- [x] Tests: `test_video_series_binge.py`, the judge, settings and reviews additions, the 0102
      migration integration test.

## Steps

- [x] Models, migration, schemas.
- [x] Rules in judge.py and settings.py; series.py logic; routes.
- [x] Tests; `ruff check`, `mypy app tests`, the video pytest set.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
uv run pytest tests/test_video_series.py tests/test_video_series_binge.py tests/test_video_automation_judge.py tests/test_video_automation_settings.py tests/test_video_reviews.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0103_video_binge_series.py -q   # needs PostgreSQL
```

## Notes

- 2026-09-27: done on branch `claude/keen-hamilton-plu6kp` with the other binge tickets
  (worker, visual tier, compile, web, ops, docs). The script gate's fix loop runs in the worker
  before submission (like the outline pick); the server only approves a passing payload on
  arrival, so a failing screenplay after the rounds waits for the owner with the problems on
  the card rather than looping.
- The contract the worker and the page rely on: `SeriesDocSubmitIn.judge` =
  `{verdicts: {<key>: 有|弱|無}, problems: [], similar_works: [], notes}` with the keys of
  `REQUIRED_VERDICTS[kind]`; a script review's payload = `{coverage: {hook, conflict, turn,
  cliffhanger, satisfaction}, continuity_problems, similar_works, retention: {hook_seconds,
  satisfaction: {count, first_seconds, positions}, cliffhanger_last}}`; a compilation's qa
  report carries `kind: "compilation"` and the six `COMPILATION_QA_ITEMS`.
