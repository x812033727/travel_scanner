---
id: 2026-10-02-decide-on-news-candidates-from-old
title: Decide what to do with news candidates filed from old feed posts
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-02T15:20:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/tests/test_news_backfill_cli.py
---

# Decide what to do with news candidates filed from old feed posts

## Why

When the hourly news scanner was switched on (2026-09-24), every feed entry it had not
seen became a candidate however old it was: the first three sources alone filed 87
candidates, most of them posts from weeks or months earlier. Task
2026-09-24-skip-stale-feed-entries-when-a stops that for new scans (a dated entry older
than the source's `max_entry_age_hours` window, 72 hours by default, is left out before its
page is fetched), but it did not touch the rows already filed. Its last Definition of done
item, "the candidates already filed from old posts are dealt with in a way the site owner
chooses", needs the owner, and the agent that did that task could not ask.

Some of the backlog is already gone: the owner had all 140 `needs_evidence` candidates
rejected on 2026-09-25, and the rest has had a week to run through the pipeline. What is
left, if anything, sits in `discovered` or `manual_review`.

## Definition of done

- [ ] The owner has chosen: leave the old-post candidates, or reject the `discovered` and
      `manual_review` ones whose `source_published_at` is older than their source's window
      at the time they were filed, each with an audit reason.
- [ ] If the choice is to reject: it was done through `service.reject_candidate` (one
      audit row each), dry run first, and the count is written down here.

## Steps

- [ ] Count the candidates on the host that match (`source_published_at` more than 72
      hours before `created_at`, status `discovered` or `manual_review`) and show the owner
      the count with a few titles.
- [ ] Ask the owner: leave them, or reject them.
- [ ] If reject: add a `--stale-before-filing` (or similar) option to `backfill_cli` with a
      dry run and `--apply --actor-email`, test it, deploy, run it.

## How to verify

On the host, after the decision: the same count query returns zero (if rejected) or the
owner's choice is written in Notes (if left).

## Notes

- Filed 2026-10-02 by claude-opus-5-5-news-stale-feed while finishing
  2026-09-24-skip-stale-feed-entries-when-a; no production rows were read or changed.
- A one-off script in the api container (the way the 2026-09-25 rejection was done) is
  enough if the owner prefers not to grow `backfill_cli`; then this task's scope is only
  this file.
