---
id: 2026-09-28-preserve-full-stack-browser-failure-evidence
title: Preserve full-stack browser failure evidence across suites
status: done
priority: P2
area: ops
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T02:34:55Z
created_at: 2026-09-28T02:34:53Z
completed_at: 2026-09-28T02:45:09Z
branch: codex/preserve-smoke-ci-evidence
depends_on: []
scope:
  - .github/workflows/ci.yml
---

# Preserve full-stack browser failure evidence across suites

## Why

PR #883's full-stack smoke job 108762801658 failed the mobile hotel-settings
journey at page.reload(), then ran the admin-operations suite. The final
artifact step reported that apps/web/test-results did not exist. Sequential
Playwright invocations share and clear that directory, so a later passing
suite can remove the earlier error context. The default on-first-retry trace
also produces no trace because these suites do not configure retries.

## Definition of done

- [x] A later passing suite retains an earlier suite's error context and trace.
- [x] A first-attempt failure records a trace without adding retries or changing assertions.
- [x] Existing failure/cancellation-only artifact uploads and retention remain intact.

## Steps

- [x] Inspect the actual failed job log and artifact warning.
- [x] Give each full-stack invocation a distinct output directory and retain failure traces.
- [x] Reproduce evidence loss with a shared directory and verify isolated directories preserve it.
- [x] Run scoped workflow checks and close the implementation task; validate the submitted PR through required CI.

## How to verify

Run node --test tools/ci-images.test.mjs and npm run check:tasks. Use the
repository's installed Playwright to run an intentional failure followed by
a passing test, first with shared output and then with distinct suite output.
Assert that the earlier error context and trace survive only the distinct
directory case. Inspect the workflow diff and GitHub CI.

## Notes

Observed failure: https://github.com/x812033727/travel_scanner/actions/runs/36369551568/job/108762801658.
The original test timeout is not explained or fixed by this diagnostic change.
PR #883 was updated from main as separately required; the new full-stack smoke
job 108764586513 passed. This does not establish the original timeout's cause.
No checks, timeouts, retries, or upload-on-success behavior are relaxed.

Validation on 2026-09-28:

- Installed Microsoft Edge with repository Playwright 1.63.0: four real browser
  runs reproduced shared-output evidence deletion, then proved distinct suite
  directories retain the earlier error-context.md and trace.zip after a passing
  run. The probe also confirmed on-first-retry records no trace with zero retries.
  Local receipt: test-results/ci-evidence-probe/receipt.json (ignored diagnostic).
- node --test tools/ci-images.test.mjs: 5 passed, 1 skipped because Bash cannot
  access the Windows temporary fixture path, 0 failed.
- npm run check:tasks passed; existing stale-claim warnings remain unrelated.
- Parsed the workflow with js-yaml and verified all four browser invocations
  use unique output directories and retain-on-failure traces; git diff --check passed.
