---
id: 2026-10-01-upgrade-urllib3-to-2-8-0
title: Upgrade urllib3 to 2.8.0 for three CVEs
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-01T12:02:50Z
created_at: 2026-10-01T12:02:13Z
completed_at: 2026-10-01T12:07:07Z
branch: claude/urllib3-2-8
depends_on: []
scope:
  - apps/api/uv.lock
---

# Upgrade urllib3 to 2.8.0 for three CVEs

## Why

`uv run pip-audit --local --skip-editable` reports CVE-2026-97687, CVE-2026-97688 and
CVE-2026-97689 in urllib3 2.7.0, fixed in 2.8.0. The CI step in `ci.yml` is advisory
(`continue-on-error`), so it only showed up as a note on PR #1063; the daily `pip-audit.yml`
enforces it. urllib3 reaches the API through botocore (boto3, used for S3/MinIO media and news
assets) and requests (pip-audit, dev only).

## Definition of done

- [x] `apps/api/uv.lock` pins urllib3 2.8.0 and nothing else changes.
- [x] `pip-audit --local --skip-editable` finds no known vulnerabilities.

## Steps

- [x] `uv lock --upgrade-package urllib3` (2.7.0 -> 2.8.0; the lock diff is the version, sdist and wheel hashes only).
- [x] Run the tests that go through boto3: test_community_foundation, test_discovery_community,
  test_news_pipeline (129 passed, 9 skipped: they need Postgres/MinIO, which CI provides).

## How to verify

```bash
cd apps/api && uv sync && uv run pip-audit --local --skip-editable
```

## Notes

Claimed with `--force`: `2026-09-14-redis-py-8-migration` lists `apps/api/uv.lock`, but its claim
(2026-09-19) is far past 24 hours and it is in review with no open PR touching the lock.
