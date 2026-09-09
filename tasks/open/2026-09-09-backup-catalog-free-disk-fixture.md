---
id: 2026-09-09-backup-catalog-free-disk-fixture
title: Isolate backup catalog test from host free disk capacity
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-09T09:40:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_database_operations_center.py
---

# Isolate backup catalog test from host free disk capacity

## Why

The verified-backup catalog test expects database_overview.available=true, but its prepared executor retains the real 5 GiB minimum disk threshold and reads the host disk containing tmp_path. It fails on otherwise correct code when the developer disk has less free space. Do not weaken the production disk safety gate to fix this test.

## Definition of done

- [ ] The backup catalog test isolates free-disk capacity and passes independently of developer disk space, while retaining separate production low-disk safety coverage.

## Steps

- [ ] Inject/mock sufficient capacity only in the backup catalog fixture/test, without relaxing production minimums.
- [ ] Run this file and explicit insufficient-disk tests in both environments.

## How to verify

From apps/api: python -m pytest tests/test_database_operations_center.py -q. Retain assertions that backups are cataloged, linked to their deployment and validated; keep separate low-disk cases meaningful.

## Notes

- Discovered during discovery-card-details validation on 2026-09-09. Full local API run: 2,265 passed, 139 skipped, one failure at test_deployment_backup_is_visible_in_verified_catalog (line 152, overview.available).
- Reproduced with an unchanged detached main 59c86438e3100129bbff554f9dce3df95e25a2ac in C:/Users/x8120/.codex/worktrees/mokaair-card-baseline-59c86438. No deployment-agent files changed in the discovery task.
- Read-only investigation: AgentConfig.min_free_bytes defaults to 5,368,709,120 bytes; database_overview calls shutil.disk_usage for tmp_path. Host C: free space was about 4.1 GB during the failed run. This is an environment-coupled test, not a confirmed Windows-specific runtime defect.
- Single-variable confirmation on unchanged base: actual free=4,065,091,584 bytes yielded only backup_disk failed, available=false and backup_count=1; mocking just shutil.disk_usage.free to 10 GiB made the original test pass and kept backup_count=1. No production commands or network were executed. Include a low-space assertion that verified backups remain visible even when operations are unavailable.
