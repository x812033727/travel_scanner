---
id: 2026-09-20-fix-nonroot-source-mount-permissions-in
title: Fix nonroot source mount permissions in article localization release
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-20T13:07:38Z
completed_at:
branch:
depends_on: []
scope:
  - ops/article-localization-release
---

# Fix nonroot source mount permissions in article localization release

## Why

During the 2026-09-20 guarded release of merged PR #595 at
`5648b84043a09e9db7f773d7a080260d39f9d453`, the first publisher dry-run
failed before any database write with `[Errno 13] Permission denied` opening
`/deployed/docs/article-localization/publish_bundle.py`. The host-side release
driver sets `umask(0o077)` and then creates its extracted `source` directory
with `mkdir(mode=0o755)`, leaving it mode 0700. The publisher container runs as
uid 10001 and bind-mounts that directory read-only at `/deployed`, so it cannot
traverse the root-owned source. The operator corrected only that source directory
to mode 0755; the unchanged manifest hashes then passed dry-run and publication.
This manual step should be captured in a tested release driver.

## Definition of done

- [ ] A fresh guarded release can run the nonroot publisher dry-run without a
      manual permission repair.
- [ ] Source files remain hash-verified and readable to the publisher; runtime,
      backups, journals, and credentials retain their existing restricted modes.
- [ ] A regression test checks effective permissions under a restrictive umask.

## Steps

- [ ] Bring the guarded release driver and publisher invocation into the tracked
      `ops/article-localization-release/` scope, preserving its exact-SHA,
      backup, hold, CI, and hash checks.
- [ ] Explicitly set the extracted source directory to traversable/readable
      permissions after extraction, without changing sensitive directory modes.
- [ ] Run the regression test, an unprivileged dry-run smoke check, relevant
      repository checks, and review the exact change in a separate PR.

## How to verify

Run the permission regression under umask 077, stat source and private release
directories, and invoke the publisher dry-run as uid 10001 against a fixture
release source. Confirm it reads `publish_bundle.py` and performs no DB write.

## Notes

External host driver: `/root/batch001_release_host.py`; publisher:
`/root/batch001_publish_host.py`; local reference copy:
`C:\Users\x8120\.codex\article-localization-release\batch001_release_host.py`.
Release evidence is under `/root/mokaair-localization-5648b84043a0/` on
`hostinger2`. Do not copy credentials or backup files into the repository.
This task records a follow-up; it does not block the already verified #595 release.
