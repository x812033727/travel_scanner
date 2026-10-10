---
id: 2026-10-10-codex-practical-final-test-locator
title: Codex practical final course test receipt locator
status: done
priority: P2
area: docs
owner: codex-gpt6-practice-design
claimed_at: 2026-10-10T19:06:38Z
created_at: 2026-10-10T19:06:33Z
completed_at: 2026-10-10T19:07:08Z
branch: codex/codex-practical-series-20261011
depends_on: []
scope:
  - docs/videos/codex-practical-series/VALIDATION.md
---

# Codex practical final course test receipt locator

## Why

The final validation table names a historical course test log although evidence/validation.json binds the latest material-guide-paths course test receipt. Readers need the current filename to locate the 11/11 result and its recorded SHA-256.

## Definition of done

- [x] The final course test table identifies the same log as evidence/validation.json.
- [x] A read-only final delivery audit matches current public source bytes and preserved raw receipts.
- [x] The task is done with no duplicate open file; task validation and diff checks pass.

## Steps

- [x] Claim only docs/videos/codex-practical-series/VALIDATION.md after root's completed delivery ticket releases that scope.
- [x] Replace only canonical-course-tests.log with material-guide-paths-20261011/course-guide-path-tests.log.
- [x] Recheck final source/evidence bindings and close this task without commit or push.

## How to verify

Read the table and evidence/validation.json; compare the existing external raw log SHA-256 with `312b8aaba70cc468410a93d85cd46aa27da988c885be2034aa4762a72d1b1142`. The stored log has 11 tests, 11 passing and zero failed. Rerun only the read-only final delivery audit, then `node tools/tasks.mjs check` and `git diff --check`; no test suite or provider call is required for this locator-only correction.

## Notes

2026-10-11: Root explicitly delegated this one-file follow-up. The original test logs, media, metadata, source files and evidence hashes remain unchanged. Exact private paths stay outside Git; external audit records use the existing series runs directory. The previous final audit's only finding was this table locator.

Final audit PASS with no observations. Receipt `runs/final-delivery-audit-oXJYLs/final-delivery-audit.json`, SHA-256 `7c58378a0dae57ba175bcbaf12514256293f04b15f2017cc2b78c8965689c76c`: all seven public source hashes, 16 raw media artifacts, latest approval entries/readback logs, 11/11 QA, 4/4 upload-package checks, four test logs, four delivery receipts and both 18-ZIP builds match. App capture and human playback/learning remain pending; YouTube upload/publication have not started; Traditional Chinese-only requires no extra locale batch. No personal host path is present in the target public records.
