---
id: 2026-09-09-backup-catalog-free-disk-fixture
title: Isolate backup catalog test from host free disk capacity
status: done
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:34:56Z
created_at: 2026-09-09T09:40:53Z
completed_at: 2026-09-19T09:39:59Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/tests/test_database_operations_center.py
---

# Isolate backup catalog test from host free disk capacity

## Why

The verified-backup catalog test expects database_overview.available=true, but its prepared executor retains the real 5 GiB minimum disk threshold and reads the host disk containing tmp_path. It fails on otherwise correct code when the developer disk has less free space. Do not weaken the production disk safety gate to fix this test.

## Definition of done

- [x] The backup catalog test isolates free-disk capacity and passes independently of developer disk space, while retaining separate production low-disk safety coverage.

## Steps

- [x] Inject/mock sufficient capacity only in the backup catalog fixture/test, without relaxing production minimums.
- [x] Run this file and explicit insufficient-disk tests in both environments. (Linux, normally and with the host disk faked to 1 GiB; the test no longer consults the host disk at all, so a Windows run is no longer a variable -- see the note.)

## How to verify

From apps/api: python -m pytest tests/test_database_operations_center.py -q. Retain assertions that backups are cataloged, linked to their deployment and validated; keep separate low-disk cases meaningful.

## Notes

- Discovered during discovery-card-details validation on 2026-09-09. Full local API run: 2,265 passed, 139 skipped, one failure at test_deployment_backup_is_visible_in_verified_catalog (line 152, overview.available).
- Reproduced with an unchanged detached main 59c86438e3100129bbff554f9dce3df95e25a2ac in C:/Users/x8120/.codex/worktrees/mokaair-card-baseline-59c86438. No deployment-agent files changed in the discovery task.
- Read-only investigation: AgentConfig.min_free_bytes defaults to 5,368,709,120 bytes; database_overview calls shutil.disk_usage for tmp_path. Host C: free space was about 4.1 GB during the failed run. This is an environment-coupled test, not a confirmed Windows-specific runtime defect.
- Single-variable confirmation on unchanged base: actual free=4,065,091,584 bytes yielded only backup_disk failed, available=false and backup_count=1; mocking just shutil.disk_usage.free to 10 GiB made the original test pass and kept backup_count=1. No production commands or network were executed. Include a low-space assertion that verified backups remain visible even when operations are unavailable.

### 2026-09-19 done in repo (claude-fable-5-1)

**Cause.** `DeploymentExecutor.database_overview()` appends a `backup_disk` check built from
`shutil.disk_usage(self.config.backup_path.parent).free >= self.config.min_free_bytes`, and
`available` is `all(check != failed)`. In this test `backup_path.parent` is `tmp_path`, so the
check measured whatever disk holds the developer's temp directory against the real 5 GiB
minimum; under 5 GiB free, `backup_disk` failed and `available` came back `False` on correct
code.

**Change** (only `apps/api/tests/test_database_operations_center.py`; `deployment_agent/`
untouched, `AgentConfig.min_free_bytes` still `5 * 1024**3`):

- New helper `pin_free_disk(monkeypatch, free)` stubs `shutil.disk_usage` to answer `free`
  bytes and records every path it was asked about. The executor keeps its real minimum;
  only the measurement is pinned.
- `test_deployment_backup_is_visible_in_verified_catalog` pins `2 * min_free_bytes` and
  additionally asserts the gate measured `backup_path.parent`. Its catalog assertions
  (cataloged, linked to the deployment, validated) are unchanged.
- New `test_low_backup_disk_blocks_operations_but_keeps_the_verified_catalog` is the
  production gate's own coverage: asserts the default minimum is still 5 GiB, that one byte
  under it makes `available` false with `backup_disk` the only failed check (detail
  `可用空間 4 GiB`) while the verified backup stays listed, and that exactly the minimum
  passes (the gate is `>=`).

**Validation** (`cd apps/api`):

```
uv run pytest tests/test_database_operations_center.py -q          # 8 passed
# same file with the real shutil.disk_usage replaced by a 1 GiB answer before pytest
# starts (scratch runner): 8 passed. HEAD's version of the file under that same runner:
# 1 failed (test_deployment_backup_is_visible_in_verified_catalog, available False), 6 passed.
uv run ruff check tests                                            # All checks passed!
```

The remaining `ruff format --diff` line in this file is pre-existing (`hashlib.sha256(...)`
in the manual backup test) and was left alone; CI runs `ruff check` only.
