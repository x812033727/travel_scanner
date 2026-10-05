---
id: 2026-10-05-news-auto-publish-reads-its-switches
title: News auto-publish reads its switches fresh, not the settings held since the run began
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-05T03:13:54Z
completed_at:
branch:
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
`2026-10-05-shorts-claim-re-reads-its-locked`, and verified by reading the code. Not yet
reproduced in a test. The failure does not depend on SQLAlchemy 2.1.3: the held `settings`
is enough on any version.

## Definition of done

- [ ] A switch turned off while a candidate is being drafted stops that candidate from
      auto-publishing. A test turns it off from a second session mid-run and asserts the story
      waits for a person.

## Steps

- [ ] Read the switches with `.execution_options(populate_existing=True)` in
      `_auto_publishable`, or `await session.refresh(settings)`. Keep `settings_row` unchanged
      for its other callers, or give it a `fresh=` keyword.
- [ ] Regression test in tests/test_news_pipeline.py, failing before the fix.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

## Notes

The task `2026-10-04-resume-held-news-drafts-from-their` (in review) also works in
news_automation. Check its scope before claiming.
