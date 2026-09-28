---
id: 2026-09-28-shorts-scheduling-consent-guards
title: Guard Shorts wall times and consent acknowledgements
status: done
priority: P2
area: web
owner: codex-pr912-review
claimed_at: 2026-09-28T12:23:27Z
created_at: 2026-09-28T12:22:53Z
completed_at: 2026-09-28T12:27:50Z
branch: codex/pr912-settings-guards
depends_on: []
scope:
  - apps/web/components/admin-video-shorts-data.ts
  - apps/web/components/admin-video-shorts-settings.tsx
  - apps/web/components/admin-video-shorts-calendar.test.tsx
  - apps/web/components/admin-video-shorts-settings.test.tsx
---

# Guard Shorts wall times and consent acknowledgements

## Why

The merged Shorts UI accepts a datetime-local value in a daylight-saving gap and
silently converts it to a different wall time. For example, Los Angeles
2027-03-14 02:30 becomes 01:30. Its consent card also retains a checked read box
when saving changed settings replaces the server's consent wording and hash.

## Definition of done

- [x] Nonexistent local times are rejected without changing the existing fall-back choice.
- [x] A changed consent offer requires a new acknowledgement before it can be submitted.
- [x] Both regressions are represented in the existing component test suites.
- [x] Record completed checks separately from the React/CI checks still required.

## Steps

- [x] Check local branches, remote branches, open PR file scopes and main history before claiming the four-file scope.
- [x] Apply the reviewed patch to a new branch based on current main.
- [x] Run lightweight verification and review the exact diff.
- [x] Prepare the follow-up PR and close this owned task with the implementation.

## How to verify

The executable Node regression covers Taipei, Tokyo, UTC, Los Angeles spring-gap
and fall-back behavior, Lord Howe's half-hour gap, invalid dates, zones and formats.
The new settings test checks the old offer, edits/saves scope, receives a new hash,
requires a new check, and verifies the submitted hash.

CI must run the existing suites:

```text
cd apps/web
vitest run components/admin-video-shorts-calendar.test.tsx components/admin-video-shorts-settings.test.tsx
```

Run the task-board check and git diff whitespace check before pushing. Full web
lint/typecheck and the React suites must pass in CI before merge if local resource
limits prevent running them.

## Notes

- Follow-up to the independent review of merged PR #912, exact source commit
  `6636307a51e0fd30050759841f938268ee92e94c`.
- New branch base: `c54594e488f48e3655566cc8a86d45e9dc2e004e` from a fresh main fetch.
  Main history contains PR #912's implementation in `1923ec62` and no later edits
  to the two affected implementation files at claim time.
- Collision check: local branch/worktree inventory and remote branches show no
  existing PR912 guard branch; the fresh open-PR file list has no overlap with
  these four paths. Planned W2 task `2026-09-28-video-shorts-admin-automation`
  overlaps settings files but is unclaimed (`open`, no owner or branch). No other
  task file was changed.
- Reused the explicitly released managed checkout, preserving
  `codex/pr910-start-quota-followup` at `f59cc4483e6ea7318e0f05a5caef5458f5183f33`.
- The prior private Node regression was 8 passed/3 failed before and 11 passed
  after. React execution was held before launch when only 278424 KiB physical RAM
  was free; it is not represented as passed. This checkout has no node_modules;
  no dependency installation or full build is planned under that constraint.
- Replayed that Node harness against this branch's original and modified helper:
  before **8 passed / 3 failed**, exit 1 as expected; after **11 passed / 0 failed**,
  exit 0. The tested modified file and tracked helper have the same SHA256
  `800fbb311688e82cba49503a17c56c869f84aeb0872cbc490ef556571d77b605`.
- All four edited TypeScript/TSX files pass syntax parsing with TypeScript 6.0.3,
  matching this branch's package lock; this is explicitly not lint, typecheck or
  execution of React tests. `git diff --check` passes.
- The task-board checker passes: **1045 task files validated**, exit 0. Its
  existing stale-claim and other-task overlap warnings were not changed.
- The final local free-memory observation was 682232 KiB and another agent owns
  the bounded backend verification window. React regressions remain **unrun**;
  required web CI must execute them and complete lint/typecheck before merge.
