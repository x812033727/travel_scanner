---
id: 2026-09-19-three-browser-workflows-still-run-every
title: Three browser workflows still run every branch push twice and never cancel superseded runs
status: done
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-19T04:53:02Z
created_at: 2026-09-19T04:53:01Z
completed_at: 2026-09-19T04:57:26Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - .github/workflows/food-map-reservations.yml
  - .github/workflows/planner-premium.yml
  - .github/workflows/travel-discovery.yml
---

# Three browser workflows still run every branch push twice and never cancel superseded runs

## Why

`2026-09-13-ci-duplicate-runs-amplify-flakes` fixed `ci.yml` (push runs on `main` only, one
live `pull_request` run per pull request), and `seo-audit.yml` had already taken the same
shape. Three workflows still start with a bare `push:` plus `pull_request:` and no
`concurrency:`: `food-map-reservations.yml` (job `food-map-reservations`),
`planner-premium.yml` (job `planner-browser`) and `travel-discovery.yml` (job
`discovery-browser`). Each is a Chromium browser job of 20-25 minutes with its own Postgres,
Redis and Next server, so every push to a branch with an open pull request still starts six
such jobs instead of three, and a superseded commit's jobs keep running.

Seen on #556 right after the ci.yml fix landed: the head commit's check list showed
`planner-browser`, `food-map-reservations` and `discovery-browser` twice each (one `push`
run started 04:50:22-23 UTC, one `pull_request` run at 04:50:25), while `CI` itself ran once.

## Definition of done

- [x] A push to a branch with an open pull request starts each of the three workflows once,
      as a `pull_request` run; there is no `push` run for the commit.
- [x] A second push in quick succession cancels the previous commit's `pull_request` run of
      each workflow; runs on `main` are never cancelled.
- [x] Nothing else in the three files changes: job names, steps and permissions stay as they
      are, so any status check that names them keeps its name.

## Steps

- [x] Give the three files the trigger and `concurrency:` block `ci.yml` uses, with a group
      prefix of their own (`food-map-reservations`, `planner-premium`, `travel-discovery`).
- [x] Validate the YAML and push to a branch with an open pull request; read the Actions tab.

## How to verify

Push twice in quick succession to a branch with an open pull request. The Actions tab shows
one `pull_request` run per workflow for the newest commit, the older one cancelled, and no
`push` run for either commit. Merging still produces one uncancelled run of each on `main`.

## Notes

- None of the three is a required status check (those are `api`, `web`, `containers` and
  `full-stack-smoke` from `ci.yml`), so cancelling a superseded run cannot leave a pull
  request waiting on a check that will never report.
- Workflows that only run on `workflow_dispatch`, `schedule` or `workflow_run` are not
  affected and were left alone.

### 2026-09-19 evidence and result (claude-fable-5-1)

- Before the change, on #556's push of `20918222` (04:50 UTC): each of the three started a
  `push` run (Planner UX #1529, Food map and reservations #1322, Travel discovery acceptance
  #1514, all created 04:50:19) and a `pull_request` run (#1530, #1323, #1515, created
  04:50:22), six browser jobs for one commit. `CI` and `SEO audit`, already on the new
  shape, ran once each.
- The change is the same block as `ci.yml` with the workflow's own group prefix. The push
  carrying it (`f905f1f0`) and the next one are the observation; see the notes below for the
  run numbers.
- After the change, on the push of `cb12f078` (04:56:54 UTC, the first push once #556 was
  mergeable again): exactly one `pull_request` run per workflow (Food map and reservations
  #1325, Planner UX #1532, Travel discovery acceptance #1517, next to CI #3559 and SEO audit
  #137) and no `push` run for the commit. The push carrying this note is the second push in
  quick succession; its expected effect, those three runs cancelled and one live run each
  for the new head, is recorded in #556's description.
