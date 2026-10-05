---
id: 2026-10-05-shorts-claim-re-reads-its-locked
title: "Locked re-reads take the row's values, not a held copy's (sqlalchemy#13639): Shorts claim, Shorts sender, YouTube check, link maintenance"
status: review
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-05T02:25:50Z
created_at: 2026-10-05T02:25:42Z
completed_at:
branch: claude/claim-locked-reread-populate-existing
depends_on: []
scope:
  - apps/api/app/video_shorts/claim.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/app/video_youtube/connection.py
  - apps/api/app/travel_services/jobs.py
  - apps/api/tests/test_video_shorts_publish.py
  - apps/api/tests/test_video_youtube.py
  - apps/api/tests/test_travel_services_integration.py
---

# Locked re-reads take the row's values, not a held copy's (sqlalchemy#13639)

## Why

A `select(Model)...with_for_update()` takes the row lock and reads the row, but when the
session still has that object loaded, SQLAlchemy keeps the values the object already has
unless the statement carries `populate_existing`. App sessions are
`async_sessionmaker(engine, expire_on_commit=False)` (apps/api/app/db.py), so a commit in
between does not expire anything either. A guard that runs after the lock then decides on
what the row said before the wait, and another writer's commit in that window is lost.

Production runs SQLAlchemy 2.1.3 since the 2026-10-05 deploy (#1226). Upstream regression
sqlalchemy#13639 (fixed only in the unreleased 2.1.4) makes this much more likely: in
2.1.0–2.1.3, iterating a Result (`for x in await session.scalars(...)`, comprehensions,
`list(...)`) keeps the Result alive in a reference cycle, so the objects stay in the
identity map until cyclic GC runs. `.all()`, `.first()`, `.scalar()`, `.one()` do not.

`video_shorts/claim.py` was the path a pre-deploy review found: `waiting_uploads` builds a
dict over `session.scalars(select(VideoProject))`, then YouTube is asked for seconds, then
the locked re-read checks `youtube_video_id is not None`. A Studio sync or a review writing
that column in the window was overwritten.

## Definition of done

- [x] The Shorts claim leaves a `youtube_video_id` another session wrote while it asked
      YouTube, on SQLite and on PostgreSQL.
- [x] Every other `with_for_update` re-read in apps/api/app that guards a decision on a column
      another path writes is fixed, or listed below.
- [ ] SQLAlchemy is on 2.1.4 or later (see "SQLAlchemy 2.1.4" below).

## Steps

- [x] `claim.py`: the locked re-read carries `populate_existing`. `waiting_uploads` is unchanged.
- [x] Regression test `test_a_video_given_while_the_claim_asks_youtube_is_kept`, through a new
      `shared_site` fixture: SQLite always, plus PostgreSQL in its own schema when
      `RUN_INTEGRATION_TESTS=1` (CI). `open_shorts_site` takes `database=` and now tears down
      in a `finally`.
- [x] Audit of all 154 `with_for_update` sites (below). Three more fixed, each with a test that
      fails without the fix.
- [ ] Bump to 2.1.4 once released.

## How to verify

```bash
cd apps/api
uv run ruff check . && uv run mypy app && uv run mypy tests
uv run pytest tests/test_video_shorts_publish.py tests/test_video_youtube.py -q
# PostgreSQL (CI): the [postgresql] case of the Shorts tests and the link-maintenance test
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_video_shorts_publish.py tests/test_travel_services_integration.py -q
```

With the app fixes reverted, each new SQLite test failed locally (2026-10-05). The PostgreSQL
cases, including the link-maintenance test, run only in CI. There is no local PostgreSQL on
the machine that wrote this.

## Notes

### Reproduction on 2.1.3, without the test's help

With the claim fix reverted and nothing in the test holding the project, the identity map
after `waiting_uploads` still held `VideoProject` (plus `VideoShortsSettings` and the two
`VideoReview`s). The claim then wrote `ShortVid001` over the `StudioVid01` that a second
session had committed. The committed tests hold the loaded object themselves. That keeps
them deterministic whenever GC runs, and keeps them meaningful after 2.1.4: holding the
object is the same staleness on every version.

### Audit of `with_for_update` in apps/api/app (2026-10-05, on 8e8598cf0)

154 sites. 34 already carried `populate_existing`, and 108 are not affected (first load in a
fresh session, column-only selects, `session.refresh(..., with_for_update=True)`, or after
`expire_all()`). Fixed here, with a test each:

| Site | Held copy | Decision | Concurrent writer |
| --- | --- | --- | --- |
| `video_shorts/claim.py` `claim` | `waiting_uploads` dict over `scalars()` (2.1.3 only) | `youtube_video_id is not None` | `video_youtube/sync.py`, `video_reviews/admin_service.py` |
| `video_youtube/sync.py` `_locked_project` (from `video_shorts/publish.py` `send_due`) | `due` holds every `(slot, project)` for the whole loop (every version) | `dropped_at`, a run already going, `status == "done"` | `drop_project`, the owner's own request, run leases |
| `video_youtube/connection.py` `connection_row(lock=True)` (from `verify`) | `row` held across the token refresh and `channels.list` (every version) | `channel_id` match | `unlink`, `finish_link` |
| `travel_services/jobs.py` `maintain_links` | `pairs` held across every `verify_link` call (every version) | `version` unchanged since the snapshot | `admin.review_offer` |

`verify` needed one more line. With a fresh read, a check that crosses an unlink would have
written its "another channel" problem onto an unlinked card. It now writes nothing when the
card is no longer linked, or was linked again (`linked_at` moved), while YouTube answered.
`test_a_check_that_crosses_an_unlink_or_a_new_link_writes_nothing` was run against three
versions of connection.py:

- With the fix: both cases pass.
- On main: `unlinked` fails, because the card came back as linked. `linked_again` passes,
  because the stale copy only rewrites `verified_at`.
- `populate_existing` without the guard: both cases fail with the false "another channel"
  problem. That is why the guard is there.
`populate_existing` in `_locked_project` also covers `vps.py` (package/start/current_job),
and in `connection_row(lock=True)` it covers `save_client`/`finish_link`/`unlink`. None of
those callers runs under `no_autoflush`, so autoflush writes any pending change before the
re-read and `populate_existing` cannot drop it.

Left as they are (LOW: no I/O in the window, the column is written only under the same lock,
or nothing is decided). These come from the audit and were not re-verified one by one:

- `guides/admin_service.py:712` `publish_bundle` (GuideArticleLocale): only `published_at`
  and the audit field. The version guard is a database `UPDATE ... WHERE version = expected`.
- `video_shorts/slots.py:548` `_assign` and `:319` `lock_due_slots` (VideoShortsSlot):
  `holds()`/`_held` iterate a Result (2.1.3 only). Milliseconds, no I/O.
- `video_shorts/settings.py:44` from `tick.py:136`: writes `last_tick_at` only.
- `video_automation/run_jobs.py:186` (VideoToolToken.revoked_at): milliseconds.
- `video_reviews/admin_service.py:1732` from `redo_episode` (VideoDramaRequest.status): no
  I/O in between.
- `community/content.py:276`, `community/router.py:117` (User): the lock is only a mutex.

Found in passing, outside `with_for_update`:

- `news_automation/pipeline.py:245` `_auto_publishable`: its "fresh" `settings_row(session)`
  returns the object `_claim_capacity` loaded at the start of the run (pipeline.py:427).
  Verified: owner switches turned off during an AI run (`enabled`, `mode`,
  `auto_publish_<vertical>`) are ignored for that candidate. Filed as
  `2026-10-05-news-auto-publish-reads-its-switches`.
- Not verified, from the audit: `video_shorts/slots.py:292` `unplan` selects under
  `no_autoflush` right after `release()` set a slot back to planned, so it may miss that
  slot. The settings saves in `video_automation/admin_api.py:169`,
  `video_shorts/admin_api.py:220` and `news_automation/service.py:372-382` merge from an
  unlocked read and then write every field under the lock.

### SQLAlchemy 2.1.4

Bump `sqlalchemy` to 2.1.4 as soon as it is released (`uv lock --upgrade-package sqlalchemy`
in apps/api), whether or not Dependabot offers it. The `@dependabot ignore sqlalchemy minor
version` on #958 (2026-09-28) was answered "I won't notify you about version 2.1.x of
sqlalchemy again, unless you unignore it". 2.1.4 is inside 2.1.x, so the ignore may block the
patch too, not just the minor. GitHub's docs do not say whether a manual upgrade into the range
(#1226 moved to 2.1.3 by hand) lifts it. On the next uv Dependabot PR, comment
`@dependabot show sqlalchemy ignore conditions`, and `@dependabot unignore sqlalchemy` if the
condition is still there. Once on 2.1.4, the fixes above stay: they guard against a held
copy on any version.
