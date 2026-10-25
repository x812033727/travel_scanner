---
id: 2026-10-23-consolidate-c-series-budget-holds-and
title: Consolidate C-series preproduction budget holds
status: done
priority: P1
area: api
owner: codex-gpt6-c-series-budget
claimed_at: 2026-10-23T11:19:20Z
created_at: 2026-10-23T11:18:22Z
completed_at: 2026-10-23T12:28:25Z
branch: codex/c-series-budget-safe-integration-20261023
depends_on: []
scope:
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_budget/RECONCILE.md
  - apps/api/app/video_budget/PENDING_EVERYDAY.md
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_video_automation_ai.py
  - tools/video/core/pending-pilot-budget.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/pending-budget.test.mjs
  - tools/video/media/client.mjs
  - tools/video/media/client.test.mjs
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/tts/cli.mjs
---

# Consolidate C-series preproduction budget holds

## Why

C03–C06 used paid services before a per-film ledger existed. Draft #1749
proposed historical holds but would also open spendable C07/C10/C15 accounts
before supplier, voice, model, region and price checks. Draft #1743 closes
C10/C15 locally and at the API, but is based on draft #1684. The owner scoped
this phase to review-only backend intake and PR closeout. Integrate the
fail-closed guard on main now; leave migration and paid activation to a
separate task, because the current 0137 API cannot roll back from 0138.

## Definition of done

- [x] C03–C06 have no newly spendable balance while historical charges remain
      unresolved; no new account or migration is created in this release.
- [x] C03–C07/C10/C15 remain on a preproduction hold even if an account row is
      accidentally present.
- [x] Attributed API requests and queued subscription stages fail closed for
      every everyday story. Current local TTS, media and automation clients
      hold the series before send, including unapproved slugs paired with an
      older API.
- [x] Focused API and Node tests pass on the exact PR head. The Alembic head
      and original pilot account map remain unchanged. Deployment, billing
      reconciliation, migration and paid work remain separate gates.

## Steps

- [x] Inspect #1684/#1743/#1749 and current main; establish one migration head.
- [x] Integrate local/API holds with narrow tests and preserve the prior-charge
      inventory in the reconciliation guide.
- [x] Verify checks, open a draft PR with `no-auto-merge`, and review CI.

## How to verify

Run focused `apps/api` budget/API pytest, targeted Ruff/mypy, three Node client
suites, `uv run alembic heads`, and `npm run check:tasks`. Before deployment,
prove no old C-series worker with a client that omits speech attribution is
running or able to restart. After any separately approved deployment, read back
refusal for each of the seven attributed slugs and prove existing
accounts/status remain unchanged.

## Notes

The task-board claim overlaps two stale main tickets on `tools/video/tts/cli.mjs`
and `tools/video/tts/`. Their PRs #1548 and #1614 were already merged on
2026-10-17 and 2026-10-20; neither branch still exists on origin. The owner
explicitly requested this C-series consolidation, so `claim --force` handles
only those stale metadata scopes. No other owner's task file is changed.

2026-10-23 split: dropped candidate migration 0138 and account seeding from this
PR. The previous 0137 image cannot classify 0138 as a rollback-compatible
revision, so a migration PR cannot be deployed safely in this closeout phase.
The follow-up task retains the exact billing, account, migration and 480-second
body gates. This guard does not start any provider request.

2026-10-23 final code gate: PR #1782 head
`7d8fdf7f571f7bab7a48ca9e7a173fbdc3c8e916` passed the required API,
video and web/task CI checks and was squash-merged as
`efbb3012f0778f79327394b079a52070d0f12d94`. Local focused API tests
passed 126 with three PostgreSQL-only skips; Node client tests passed 71/71.
The Alembic head remains 0137, the existing pilot account map is unchanged,
and no new C-series account was seeded. Production worker cutover and every
paid activation remain in `2026-10-23-reconcile-c-series-prior-charges-and`.

Local guard check on 2026-10-23 before the final main rebase: 124 API tests
passed, 3 existing PostgreSQL-only tests skipped; Node 24.19 passed 71/71
automation/media/TTS client tests. Targeted Ruff, budget mypy, task check and
`git diff --check` passed. Alembic remains exactly
`0137_video_manga_tier (head)` and `PILOT_LIMITS_USD` is unchanged. CI and
deployed readback are later gates, not represented by these local results.

Independent review found that the speech API still accepts requests with no
`video_slug` or `operation_id` for existing workflows. A legacy C-series client
can omit both, leaving the server unable to identify the film. This branch
does not claim API-only protection against an old worker. Production rollout
must first establish that all old C-series workers are stopped and cannot
restart, or add authenticated project binding in a separate reviewed change.

Read-only production check at 2026-10-23 11:36 UTC through the saved
`hostinger2` session: `travel-scanner-autodeploy.timer` was `not-found` and
inactive, `list-timers` showed zero instances, and the poller file under
`/opt/travel-scanner-autodeploy/` was absent. Live checkout HEAD was
`6f9aec8d1606829d81a3acfe926c8d303bb1b0d9`. The running `video-worker`
container lacked `tools/video/core/pending-pilot-budget.mjs`; its
`tools/video/tts/client.mjs` SHA-256 was
`de583a38f1f10aff0ac3dedee049ba5dd88f380083ddb0685ed8c7e0d1f4d32e`.
`docker top` showed worker entrypoint shells and sleeps, no active Node job at
that instant; `video-ai-worker` had RQ Python processes. A local Windows
command-line scan found no process visibly naming `story-everyday-*`. These
snapshots do not prove an old client cannot restart or use a generic token.
No auto-deploy timer was installed at the check; a future manual or changed
host deployment still needs the old-worker cutover readback before claiming
the C-series paid stop is complete.
