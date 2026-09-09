---
id: 2026-09-09-pr335-funnel-merge-integration
title: Prepare PR 335 funnel integration against current main
status: done
priority: P1
area: api
owner: codex-pr335-delivery
claimed_at: 2026-09-09T06:33:36Z
created_at: 2026-09-09T06:13:49Z
completed_at: 2026-09-09T06:49:21Z
branch: codex/pr335-merge-ready-20260909
depends_on: []
scope:
  - apps/api/tests/test_analytics_events.py
  - apps/api/tests/test_integration_postgres_redis.py
  - docs/user-flow-plan.md
---

# Prepare PR 335 funnel integration against current main

## Why

PR #335 adds the missing flight `offer_attached` funnel event. Its old successful
checks do not validate integration with current main. Prepare an isolated, normally
merged and tested head without reopening the completed observe-the-funnel task.

## Definition of done

- [x] Current main behavior and historical completed task state are preserved.
- [x] Only successful flight attachment emits the expected enum-only event, while
  invalid requests, stale versions and rolled-back writes add no persisted event.
- [x] Relevant regression, Ruff, mypy and task checks pass with explicit local gaps.
- [x] Deliver a clean local head for root's fresh remote CI and guarded merge.

## Steps

- [x] Pin PR head `1a83d64efbaed5db45656ea2ff58e347c6d59371` and current main
  `a899437aaf2f60c7affe2e944d49d62216537c90`; create a narrow integration claim.
- [x] Normally merge current main and resolve only relevant overlaps.
- [x] Independently inspect transaction, privacy and repeat-request semantics.
- [x] Validate and hand back; root owns push, final CI and merge after #343.

## How to verify

From `apps/api`, set PYTHONPATH to this worktree's `apps/api`, then run focused
analytics, flight-attachment and PostgreSQL integration regressions with the matching
test environment. Run Ruff, mypy and repository task checks. Regenerate conflicting
`tasks/BOARD.md` only with `npm run tasks:board`.

## Notes

No production data, provider calls, deployment, push or remote PR mutation is in this
subtask. The old branch still marks planner-calm as review and claims the trip router;
current main has already completed that task. Initial integration scope excludes the
router to avoid an overlapping claim until the normal main merge imports that state.
The existing `tasks/done/2026-09-07-observe-the-funnel.md` remains completed.

## Local integration handoff (2026-09-09)

- Normal merge `c479e8b7e29f4e78177cfde96dbfa7d2057505e8` includes pinned
  main `a899437aaf2f60c7affe2e944d49d62216537c90`. Only `tasks/BOARD.md`
  conflicted; the task tool regenerated it. No main runtime behavior was replaced.
- The sole runtime delta remains the original seven-line flight event hook. The
  analytics service, transaction implementation and existing completed task status
  are unchanged. Independent read-only review found no blocking semantic issue.
- Extended the existing PostgreSQL flight-anchor test, not the endpoint: an isolated
  browser session scopes event checks; outbound and return have enum-only properties;
  exact old-version replay and stale return roll back their events; missing return,
  mismatched date, foreign offer and manual edits add none; DNT and Sec-GPC still
  permit a valid attachment without measurement. A current-version reattachment is
  a new mutation, not an idempotency-key replay; funnel totals deduplicate sessions.
- Local focused analytics/creation/replay/intents/pricing/search/schema regression:
  **105 passed, 1 PostgreSQL case skipped**. A separate analytics/schema and PostgreSQL
  suite collection was **16 passed, 26 skipped**; these counts overlap and are not
  additive. Ruff for the entire API passed; mypy passed all 278 application files.
- Tool tests **27 passed**; five-language validation passed (25 namespaces); task
  checks passed (202 files) with an existing unrelated active-scope warning between
  frontend-flow-discovery-api and planner-route-tones. `git diff --check` passed.
- During the uncommitted merge the i18n staged-change scan classified incoming main
  text as new. The check passed after the normal merge. Initial tool execution lacked
  Playwright; task-local `npm ci --ignore-scripts --no-audit --no-fund` supplied the
  locked dependencies, and the complete tool suite then passed. No lockfile changed.
- No task-owned local PostgreSQL/Redis or Docker CLI is available. Validation used
  `RUN_INTEGRATION_TESTS=0` and database/Redis endpoints at `127.0.0.1:1`, not another
  worker's service or production. Transaction regression assertions still require
  the fresh PR CI before marking the remaining acceptance complete.
- Parent owns the next normal main update after #343, push, fresh fixed-head CI and
  guarded #335 merge. This handoff performs no push, deployment or review-data replay.

## Follow-up after #343 merged

- Reclaimed this same narrow task and normally merged exact main
  `d3426c86ba185326268fdcbb52825a8cfcd1438c` in merge commit
  `16e41ba539e1e011aa061a613c001b3fa1ff12f2`. The only conflict was the
  generated task board; it was regenerated with the task tool.
- No additional runtime edits were needed. Independent read-only review confirmed
  that account-token safety, account deletion, saved-item cleanup and analytics
  internals exactly match new main. The sole runtime delta is still the original
  flight event hook. The previously reviewed test extension is unchanged.
- Re-ran analytics, trip creation/replay/intents/pricing/search, schema, community
  foundation and saved-flow suites: **167 passed, 38 integration cases skipped**,
  with two existing dependency deprecation warnings. The protected local test
  environment remains `RUN_INTEGRATION_TESTS=0` and `127.0.0.1:1` endpoints.
- Full API Ruff passed; mypy passed 278 files; tool tests passed 27; i18n passed
  five locales and 25 namespaces; task checks passed 203 files. Existing unrelated
  stale-claim and active-scope overlap warnings were not altered. Diff checks passed.
- Released the task for parent handoff; PostgreSQL/Redis transaction assertions
  still require fresh fixed-head CI. No push, remote mutation, merge or deployment
  was performed by this subtask.

## Completed verified PR delivery

Root delivered fixed head 63a15c2e792cc32654da40923184787b2c2c9bb3 after all
12 checks passed, including the real PostgreSQL flight/event transaction tests.
PR #335 was squash-merged with the exact-head guard at 2026-09-09T06:48:09Z as
98f8067b3664a956e44d0b6e9f372b27a22775e6. GitHub merged state and main ancestry
were verified. No reviewer threads were unresolved and no check was bypassed.

The same-head PR CI passed on its first attempt. Push CI 34319631682 initially
failed a mobile community test while reading GET /community/me after email
verification; it had not reached the mail-recovery scenario. API, Web and the
other checks passed. One failed-job-only rerun at the same SHA passed; preserve
the first attempt as an intermittent connection-reset observation, not a
runtime fix. The separate CI investigation remains open in PR #365.

At this merge checkpoint, merged-main CI 34320730596, Planner 34320730585 and
Discovery 34320730564 have started and root is following their results separately.
This closes the narrow integration/verified-merge task, not an operational
deployment or the independent CI reliability investigation. No production data,
review operation, paid-provider call, feature activation or deployment occurred.
