---
id: 2026-10-05-news-auto-publish-reads-its-switches
title: News auto-publish reads its switches fresh, not the settings held since the run began
status: review
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-05T03:42:20Z
created_at: 2026-10-05T03:13:54Z
completed_at:
branch: claude/news-auto-publish-fresh-switches
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
---

# News auto-publish reads its switches fresh, not the settings held since the run began

## Why

`_auto_publishable` (apps/api/app/news_automation/pipeline.py:236-255) is the last check
before a news story goes out without a person. It reads
`fresh_settings = await settings_row(session)` and decides on `enabled`, `mode == "automatic"`
and `auto_publish_<vertical>`. The read is not fresh. The pipeline's entry point
(pipeline.py:427) already holds the `NewsAutomationSettings` row as `settings` from
`_claim_capacity`, for the whole AI run. `settings_row` (news_automation/service.py:116) is a
plain `select` without `populate_existing`, so SQLAlchemy returns that same object with the
values it had at claim time. App sessions use `expire_on_commit=False`, so the run's commits
do not refresh it either.

The result: if the owner turns automatic publishing off during a run (a settings save, or
the major-error report at news_automation/service.py:1120), the candidate in flight still
auto-publishes. Found during the `with_for_update` audit of
`2026-10-05-shorts-claim-re-reads-its-locked`. Reproduced by the regression test on main's
pipeline.py: with each of the three switches turned off mid-run, the story still came out
`published`. The failure does not depend on SQLAlchemy 2.1.3: the held `settings` is enough
on any version.

## Definition of done

- [x] A switch turned off while a candidate is being drafted stops that candidate from
      auto-publishing. A test turns it off from a second session mid-run and asserts the story
      waits for a person.

## Steps

- [x] `_auto_publishable` reads `enabled`, `mode` and `auto_publish_<vertical>` as columns
      (`select(NewsAutomationSettings.enabled, ...)`), not as the ORM row. A column select does
      not go through the identity map, so it sees the committed values. It also leaves the
      `settings` object the run holds untouched, so the rest of the run behaves as before.
      This was chosen over `populate_existing` or `session.refresh(settings)`, which would
      also have changed that object mid-run. `settings_row` is unchanged.
- [x] Regression test `test_a_switch_turned_off_while_the_story_is_drafted_holds_it_for_the_owner`
      in tests/test_news_pipeline.py, parametrized over the three switches. The switch is
      turned off from a second session during the run's first AI call (the duplicate check).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

## Notes

- Claimed with `--force`. The overlap is `2026-10-04-resume-held-news-drafts-from-their`
  (status review, owner claude-opus-5-5-news-resume), which still lists pipeline.py. Its PR
  #1212 merged on 2026-10-04 (a266a5bba). On 2026-10-05 03:40Z none of the 14 open pull
  requests touched apps/api/app/news_automation/ or tests/test_news_pipeline.py. That task
  was left in review, since its owner may still have deploy follow-up.
- Found in the `with_for_update` audit of `2026-10-05-shorts-claim-re-reads-its-locked`
  (sqlalchemy#13639). This bug does not need 2.1.3: `process_candidate` keeps `settings` in
  a local variable for the whole run, so it is stale on every version.
