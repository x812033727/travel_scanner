---
id: 2026-10-28-resolve-existing-python-dependency-security-audit
title: Resolve the existing Python dependency security audit
status: done
priority: P1
area: api
owner: codex-gpt6-python-security
claimed_at: 2026-10-28T11:23:46Z
created_at: 2026-10-28T11:10:15Z
completed_at: 2026-10-28T11:32:51Z
branch: codex/fix-python-security-audit-20261028
depends_on: []
scope:
  - apps/api/pyproject.toml
  - apps/api/uv.lock
---

# Resolve the existing Python dependency security audit

## Why

Scheduled pip audit run 40667639211 failed on 2026-10-28 at main revision
2668668f after finding 46 records across six locked Python dependencies. GitHub
issue #1646 already tracks the recurring audit failure; this task adds the missing
shared-queue handoff, not a second incident. Deduplicated advisories total 45,
including five Critical and 25 High findings. The article-only PR #1911 did not
change dependency files and did not introduce these findings.

Read-only metadata from the actual production API container confirmed certifi
2026.7.22, dnspython 2.8.0, opentelemetry-api 1.45.0 and Pillow 12.3.0. Filelock
and msgpack were absent from that API container, but present in the lock/audit
environment; other runtime containers were not inventoried.

## Definition of done

- [x] Existing repair PR ownership is reconciled before dependency edits.
- [x] All six affected dependencies are locked to verified patched versions,
      with upstream compatibility and registry artifacts independently reviewed.
- [x] Local frozen installation, security audit, type checks and targeted image,
      media and TLS regression tests pass without suppressing findings.
- [x] Exact-head CI and the enforcing Linux security audit are explicit merge
      gates; production remediation is assigned to the existing release task.

## Steps

- [x] Re-read issue #1646, the current audit output and current Dependabot heads.
- [x] Reuse or coordinate PR #1887 for Pillow where appropriate; do not create a
      competing lockfile change without checking ownership.
- [x] Review upgrades for certifi, dnspython, filelock, msgpack and
      opentelemetry-api as well as Pillow; confirm the final resolved lock.
- [x] Run targeted compatibility tests and the actual local security audit.
- [x] Record the owner's security-first backup/deploy/publish authorization and
      transfer runtime verification to the release task below.

## How to verify

Follow dev-and-ci and deploy skills. Run uv sync --frozen, the same pip-audit
command as .github/workflows/pip-audit.yml, required API checks and image/video
tests affected by Pillow. Check the final exact-head CI and audit output. Use
importlib.metadata inside actual application containers after deployment.

## Notes

- Evidence: https://github.com/x812033727/travel_scanner/actions/runs/40667639211
  and https://github.com/x812033727/travel_scanner/issues/1646.
- Verified available patched versions at investigation time: certifi 2026.10.19,
  dnspython 2.9.0, filelock 4.2.1, msgpack 1.2.3, opentelemetry-api 1.45.1 and
  Pillow 13.0.0. All six support Python 3.13; Pillow and msgpack provide matching
  Linux wheels. No removed Pillow API was found in application usage. Filelock
  and msgpack are reached through the development audit tool's CacheControl.
  The Pillow declaration now requires >=13,<14, preventing unlocked installs
  from choosing the affected 12.x series.
- PR #1886 head 599bf11a still locks all six vulnerable versions despite its
  historical green CI. PR #1887 head d760e401 updates only Pillow to 13.0.0.
  Both were open and behind main; historical checks do not authorize merging.
- The audit was a real vulnerability result, not a network flake. Do not simply
  rerun it, suppress the advisories or claim all main checks are green.
- Full logs and primary advisory/PyPI evidence are retained in the owner's
  private release-preparation evidence directory; no credentials or host IDs
  belong in this task.
- Local validation: uv sync --frozen; ruff; mypy app (489 files) and tests
  (424 files); image/media/TLS regression suite (99 passed, one platform skip);
  pip-audit --local --skip-editable reports no known vulnerabilities. On this
  Windows checkout the audit needs PYTHONUTF8=1 and PYTHONIOENCODING=utf-8 so
  pip can print the non-ASCII checkout path; the first startup errors were not
  audit results and are preserved in private evidence.
- Before merging #1887, require fresh exact-head CI, compare the API test counts
  to main 2668668f, and run the unmodified enforcing pip-audit workflow on that
  branch. Historical Dependabot checks are insufficient.
- The owner explicitly selected security remediation, then backup, deployment
  and publication of the 48 translations. Runtime completion belongs to
  tasks/open/2026-10-28-release-localized-twelve-ai-foundation-life.md: a fresh
  full backup and restore check, security-target deployment, installed-package
  readback, native rehearsal in the new API image, then publication acceptance.
  This code task being done does not assert that deployment has occurred or
  that issue #1646 has been resolved on the production host.
