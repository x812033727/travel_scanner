---
id: 2026-09-28-use-runner-owned-tracing-in-community
title: Use runner-owned tracing in community smoke tests
status: done
priority: P2
area: web
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T02:52:03Z
created_at: 2026-09-28T02:51:51Z
completed_at: 2026-09-28T02:55:25Z
branch: codex/preserve-smoke-ci-evidence
depends_on: []
scope:
  - apps/web/e2e/community.spec.ts
---

# Use runner-owned tracing in community smoke tests

## Why

PR #884 enables first-failure traces across the full-stack smoke suites. The pet
community journey also starts a manual administrator trace, causing both desktop
and mobile cases to fail immediately with "Tracing has been already started".
Use one trace owner while retaining evidence for every browser context.

## Definition of done

- [x] Community journeys run without attempting to start an already active trace.
- [x] Failed tests retain actions from both member and administrator contexts.
- [x] Feature assertions, timeouts and retries remain unchanged.

## Steps

- [x] Inspect CI job 108767410631 and its preserved browser artifacts.
- [x] Let the Playwright runner own community traces for CI and direct local runs.
- [x] Reproduce the duplicate-start error, then verify two-context trace retention.
- [x] Validate the scoped change; the submitted PR remains gated on full-stack CI.

## How to verify

Run a real two-context browser probe with the repository's Playwright, first
with the old manual trace start and then using runner-owned traces. Inspect the
retained archive for actions from both contexts. Run scoped ESLint and task
checks, then verify the full-stack-smoke job on the updated PR head.

## Notes

The failure is introduced by the interaction between #884's trace flag and the
old manual trace, not the original PR #883 navigation timeout. Its artifact
survived two later passing suites, verifying the separate-output fix in real CI.
Artifact 10949376612 contains desktop/mobile error contexts and trace archives.

On 2026-09-28, a real Playwright 1.63.0 / installed Edge probe reproduced the
manual-start error on desktop and mobile, then used runner-owned tracing in
both local and CI-flag configurations. All four resulting trace archives
contained distinct member and administrator setContent actions, even after the
administrator context closed. The intentional assertion failed at the expected
step rather than tracing setup. Local receipt (ignored diagnostic):
test-results/ci-trace-owner-probe/receipt.json.

Scoped ESLint, task validation and git diff --check passed. End-to-end service
validation remains enforced by the PR's required full-stack-smoke check.
