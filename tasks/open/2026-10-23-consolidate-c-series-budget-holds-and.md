---
id: 2026-10-23-consolidate-c-series-budget-holds-and
title: Consolidate C-series preproduction budget holds
status: in-progress
priority: P1
area: api
owner: codex-gpt6-c-series-budget
claimed_at: 2026-10-23T11:19:20Z
created_at: 2026-10-23T11:18:22Z
completed_at:
branch: codex/c-series-budget-safe-integration-20261023
depends_on: []
scope:
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_budget/RECONCILE.md
  - apps/api/app/video_budget/PENDING_EVERYDAY.md
  - apps/api/tests/test_video_pilot_budget.py
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
- [x] Attributed API requests and current local TTS, media and automation
      routes fail closed for the held pilots, while other everyday slugs
      require a reviewed account.
- [ ] Focused API and Node tests pass on the exact PR head. The Alembic head
      and original pilot account map remain unchanged. Deployment, billing
      reconciliation, migration and paid work remain separate gates.

## Steps

- [x] Inspect #1684/#1743/#1749 and current main; establish one migration head.
- [x] Integrate local/API holds with narrow tests and preserve the prior-charge
      inventory in the reconciliation guide.
- [ ] Verify checks, open a draft PR with `no-auto-merge`, and review CI.

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
