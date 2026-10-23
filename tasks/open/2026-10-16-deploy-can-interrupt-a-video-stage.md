---
id: 2026-10-16-deploy-can-interrupt-a-video-stage
title: Deploy can interrupt a video stage job started after preflight
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-16T05:58:05Z
completed_at:
branch: codex/video-stage-deploy-race
depends_on: []
scope:
  - .agents/skills/deploy/scripts/host-preflight.sh
  - .agents/skills/deploy/scripts/host-deploy.sh
  - .agents/skills/deploy/references
  - ops/autodeploy
  - ops/release
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

- [x] The incident job's true persisted and RQ states are reconciled without
      redispatching its paid request; preserve the exact previous row and audit
      the resulting status/owner decision.
- [x] The independently reviewed repository candidate guards both host-script
      worker-recreation sites, including a stage admitted after early preflight.
- [x] The same host-script guard is designed for a future automatic deployment;
      offline tests show queued and uncertain work does not block it.
- [x] Preserve the read-only host baseline, focused simulation tests and a
      specific installation/rollback plan. Production installation and the
      post-deploy readback are tracked in the follow-up P1 task below.

## Steps

- [x] Diagnose the exact RQ registry/job state and persisted DB row, without
      calling the job poll endpoint (poll can mutate the row).
- [x] Design and independently review a worker-admission/drain or equivalent
      atomic guard spanning the final pre-recreate check and paid dispatch.
- [x] Add focused tests for an arrival after deploy preflight and for existing
      uncertain/queued rows; update the deployment runbook.
- [x] Apply any production reconciliation only after its specific scope is
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
this investigation. A next #1517 or #1510 deployment requires a safe release
gate even after the row stops reporting `running`.

At 06:10 UTC a narrowly authorized attempt to invoke the existing
`run_jobs._reconcile` path first checked exact RQ failed-registry membership,
UUID, slug and DB state. It **stopped before calling `_reconcile`** with
`DB_NOT_RUNNING`; no write or model call came from that attempt. A separate
read-only SQL query then showed this exact row had already changed at
05:59:47 UTC to `uncertain`, `error_code=video_ai_job_uncertain`, no saved
result, with the original 05:38:53 dispatch timestamp. RQ remained `failed`.
The owner had authorized classification of this one row only; no resend was
authorized or performed. The deploy race itself remains open, and a later
deployment must still protect the worker restart boundary.

The one-row reconciliation step needed no write: the background receipt had
already reached `uncertain`. The authorized check stopped before mutation and
the exact post-check SQL/RQ readback preserved the original ID, slug,
`dispatched_at`, failed-registry membership, and missing result. This closes
only the incident-status portion of the ticket; it does not recover a lost
answer or authorize a replacement model call.

An offline candidate final barrier now lives in `ops/release/` (shell helper,
host-only patcher, tests and install/rollback runbook). The patcher recognized
the real host script SHA-256
`c6e69658cd22351008a179389e807304cb284052136b3aaf1522ffb281a39370`
and inserted exactly two guard calls in a local copy; both shell files passed
`bash -n`. The original host script was mode `0700`, owned by `root:root`.
The normal hook is after `ensure_readable` and before the normal `compose up`;
the rollback hook is after the old SHA reset and `ensure_readable`, before the
rollback `compose up`. The installer refuses SHA/mode/anchor drift, backs up
the original, and restores it under the same flock if a later installation
write or readback fails. The offline simulation covers a job admitted after
preflight, a delayed warm drain, queued/uncertain receipts, DB refusal, an
unresolved drain marker that prevents a second SIGTERM, failed installation
restoration, and both normal/rollback hooks. An independent first review held
the candidate for two failure paths: a refused normal hook after git fast-forward
left the checkout advanced, and a partially failed compose recreation could
remove the worker container and prevent guarded rollback. The current candidate
resets and reads back `LOCAL_SHA` under the deploy lock before reporting refusal;
normal success leaves a nonce-bound receipt so rollback may rebuild from zero
worker containers only after the original SHA and DB `running=0` are verified.
The unguarded manual compose suggestion for `--no-rollback` was removed, and
offline Windows rendering now asserts a POSIX helper path. These remain local
candidate results only: the revised guard passed the second independent review,
but awaits installation and production verification. The production host did not have the
auto timer installed at the read-only check. If later installed from this repo,
its nested deploy timeout is planned at 90 minutes, below its 2-hour systemd
watchdog; offline tests cover an exit-124 paused receipt, not a live receipt.
The second review also found that inherited helper test overrides could redirect
the production check and that automatic failure receipts claimed rollback even
when the worker might remain stopped. The rendered host hook now unsets the
repo/compose/marker overrides before both calls. Poller pause text and failure
notifications require exact deploy/`video-ai-worker` readback without claiming
restoration. Manual wrapper deployments run host-side under nohup. Neither path may claim
success until the worker is Up and the exact receipt state is read back. The
warm-drain marker persists on error/interruption because an outer timeout can
kill the shell without synchronously ending a child `docker stop`; whether a
child holds the inherited flock until it exits depends on that process's
lifetime. A next attempt must inspect the exact marker/worker/RQ/DB state,
and the guard refuses to send RQ a forceful second SIGTERM.

The independent reviewer issued final PASS for the eight-file offline candidate
after two HOLD/rework rounds. Focused WSL release tests passed 12/12, Windows
autodeploy tests passed 30/30, Ruff F/I, `bash -n` on both the helper and the
rendered host script, `npm run check:tasks`, and `git diff --check` passed.
The original host-only script is root-owned mode 0700 at SHA-256
`c6e69658cd22351008a179389e807304cb284052136b3aaf1522ffb281a39370`;
the offline patched rendering has SHA-256
`c8bb3559f6b7e25e11c3bdf207c2f8dabd28835119c78494b3c9ad8bb75bd64f`.
No host script, container or job was modified by this code work. The unresolved
live gate is a separate P1 task:
`2026-10-16-install-reviewed-video-stage-drain-on`.

Task-board closeout limitation: `npm run tasks -- done` wrote a local
`tasks/done/` copy, but Windows reported the original `tasks/open/` file still
present. A narrow PowerShell `Remove-Item -LiteralPath` of that original was
rejected with `blocked by policy`; no alternate deletion was attempted. The
untracked done copy is deliberately excluded from this PR, and this original
open ticket is released for later board reconciliation. The offline code and
independent PASS stand; the production host guard is not installed, so no
live safety claim or paid-operation retry follows from this ticket.
