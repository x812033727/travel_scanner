---
id: 2026-10-16-deploy-can-interrupt-a-video-stage
title: Deploy can interrupt a video stage job started after preflight
status: in-progress
priority: P1
area: ops
owner: codex-gpt6-deploy-race
claimed_at: 2026-10-16T06:01:30Z
created_at: 2026-10-16T05:58:05Z
completed_at:
branch: codex/video-stage-deploy-race
depends_on: []
scope:
  - .agents/skills/deploy/scripts/host-preflight.sh
  - .agents/skills/deploy/scripts/host-deploy.sh
  - .agents/skills/deploy/references
  - ops/autodeploy
  - apps/api/app/video_automation/run_jobs.py
  - apps/api/tests/test_video_stage_jobs.py
---

# Deploy can interrupt a video stage job started after preflight

## Why

The 2026-10-16 #1521 production deployment had a clean read-only paid-work
preflight at 05:36:36 UTC and began its background rebuild at 05:36:44 UTC.
An unrelated video stage job (`9c8e6388-be65-4b7c-8da1-38caaf152ccb`, slug
`deepmind-ai-wrote-75-percent-code-no-speedup`) was created at 05:38:52 and
dispatched at 05:38:53, while the deploy was already in progress. The deploy
recreated `video-ai-worker` at 05:42:11. At 05:55:48 RQ moved its
`video-stage-…` record to FailedJobRegistry with `AbandonedJobError`, while the
database still showed `running` and `completed_at=NULL` at 05:58. The seven
pre-existing `uncertain` rows did not increase because no client polled this
job after the interruption. A preflight only at deployment start leaves a
race in which a paid request can begin before container replacement.

This ticket records the incident and the deployment guard gap. It is not
permission to retry the model operation or clear unrelated uncertainty.

## Definition of done

- [ ] The incident job's true persisted and RQ states are reconciled without
      redispatching its paid request; preserve the exact previous row and audit
      the resulting status/owner decision.
- [ ] A deployment cannot recreate the video AI worker while a newly started
      paid stage job is in flight, including one admitted after preflight.
- [ ] The guard also applies to automatic deployment and does not block on
      already uncertain or merely queued work.
- [ ] Read-only preflight, simulation/concurrency tests and post-deploy
      readback demonstrate the race is closed without replaying a paid job.

## Steps

- [ ] Diagnose the exact RQ registry/job state and persisted DB row, without
      calling the job poll endpoint (poll can mutate the row).
- [ ] Design and independently review a worker-admission/drain or equivalent
      atomic guard spanning the final pre-recreate check and paid dispatch.
- [ ] Add focused tests for an arrival after deploy preflight and for existing
      uncertain/queued rows; update the deployment runbook.
- [ ] Apply any production reconciliation only after its specific scope is
      authorized, then verify no model request was resent.

## How to verify

Use `host-preflight.sh` plus a read-only SQL projection of stage statuses and
times, and inspect the RQ registry by exact job ID. For code, run the focused
API stage-job tests and the deploy/autodeploy guard tests. Before a later
deployment, verify the exact current host release/hold/lock, zero running paid
jobs at the final protected boundary, and unchanged operation receipts.

## Notes

At 05:42:50 the ordinary host deploy verification passed 12/12 (release SHA
`3cdbbd68b667ea202d10b8fd3c611a97cd809217`, 14 containers Up, zero
restarts, DB migration head `0132_video_pilot_budget`, health 3/3). That check
did not include an after-rebuild stage-job comparison. At 05:55:53 a second
preflight reported 1 `running`/7 `uncertain`; an exact read-only query isolated
the running ID above. `docker inspect` reported the current video AI worker
StartedAt `2026-10-16T05:42:11.085162787Z`; its log recorded the RQ
`AbandonedJobError` at 05:55:48. No host state or job status was changed during
this investigation. The next #1517 or #1510 deployment is blocked while this
running row remains and until a safe release gate is established.
