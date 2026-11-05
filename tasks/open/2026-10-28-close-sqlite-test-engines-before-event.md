---
id: 2026-10-28-close-sqlite-test-engines-before-event
title: Close SQLite test engines before event-loop teardown
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-28T11:51:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_news_automation_settings_models.py
---

# Close SQLite test engines before event-loop teardown

## Why

Full API shard 1 emits PytestUnhandledThreadExceptionWarning from aiosqlite
connection workers calling call_soon_threadsafe after the event loop closes.
The warnings are attributed to test_news_automation_settings_models.py. Main
2668668f had two occurrences; security repair a8922d97 had six. Both runs passed
the identical 2805 tests in this shard and 8327 across all shards, with 25 total
skips. This is a pre-existing test teardown problem, not evidence that the six
security dependency updates introduced a new warning family.

## Definition of done

- [ ] SQLite connections/engines created by this test module finish cleanup
      before their event loop closes, without suppressing thread warnings.
- [ ] Targeted tests and the normal full shard pass with unchanged test coverage;
      the original event-loop-closed thread warnings are absent.

## Steps

- [ ] Inspect this module's database fixtures and engine ownership; reproduce
      under the normal shard workload before changing shared fixture scope.
- [ ] Await the actual connection/engine cleanup and check the full shard log.
      Narrowly expand the task scope first if another fixture owns the resource.

## How to verify

Run the affected module with thread warnings visible, then the repository's
normal API shard 1/4 environment. Compare passed/skipped counts and warning
stacks; a successful isolated run alone may miss the timing-dependent issue.

## Notes

- Baseline run 40665965334 / job 122740394525; repair run 40681003219 /
  job 122791372004. No new warning type appeared. aiosqlite 0.22.1, pytest 9.1.1,
  pytest-asyncio 1.4.0, SQLAlchemy 2.1.3 and related source/test blobs were unchanged.
- tasks/done/2026-09-28-sqlalchemy-2-1-upgrade.md also records the same six-warning
  family under full load. The observed warning count varies with timing.
- This queued test-quality follow-up does not block the separately verified
  security repair or assert a production failure. Do not rerun failed audits or
  suppress security findings as a workaround for these test warnings.
