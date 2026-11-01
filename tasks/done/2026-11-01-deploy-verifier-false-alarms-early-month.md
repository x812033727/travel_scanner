---
id: 2026-11-01-deploy-verifier-false-alarms-early-month
title: Deploy verifier false alarms: early-month dates and test-only api commits
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-11-01T15:14:19Z
created_at: 2026-11-01T15:14:01Z
completed_at: 2026-11-01T15:16:03Z
branch:
depends_on: []
scope:
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
---

# Deploy verifier false alarms: early-month dates and test-only api commits

## Why

The deploy of `b53cd5eb7` on 2026-11-01 verified 9/11 with a healthy site. Both failures were the
verifier's own:

- `video-worker-started`: the log classifier compared `substr(...) < 1` as strings, so `"01"` to
  `"09"` sorted below `"1"` and every timestamp on days 1-9, or in months 1-9, was malformed. Each
  log line and the start time counted as an error (3 lines gave `context_errors=4`).
- `containers-rebuilt-this-deploy`: the api cutoff read `git log -- apps/api`, but
  `apps/api/.dockerignore` keeps `tests`, `deployment_agent` and `tools` out of the image. A
  test-only commit (`b7a4f37ee`) built nothing, and the image read as stale.

## Definition of done

- [x] Real early-month timestamps pass; impossible ones (month 0 or 13, day 0 or 32) still fail.
- [x] A commit touching only what `.dockerignore` excludes does not make the api image stale.

## How to verify

`node --test tools/deploy-host-verify.test.mjs`

## Notes

The other date fields compared safely as two-digit strings, but all now use `+0` alike.
A new test ties the excludes to `apps/api/.dockerignore` so they cannot silently drift apart from it
in this direction; an entry added to `.dockerignore` is not picked up automatically.
