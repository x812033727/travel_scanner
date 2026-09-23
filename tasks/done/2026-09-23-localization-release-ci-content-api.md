---
id: 2026-09-23-localization-release-ci-content-api
title: Run localization release safety for article and API changes
status: done
priority: P1
area: tools
owner: codex-batch021-ci
claimed_at: 2026-09-23T12:02:53Z
created_at: 2026-09-23T12:02:52Z
completed_at: 2026-09-23T12:06:52Z
branch: codex/article-localization-batch021-household-purchasing
depends_on: []
scope:
  - .github/workflows/article-localization.yml
---

# Run localization release safety for article and API changes

## Why

The localization release-safety workflow only watched its own file and the
localization tools/docs directories. A content-only article PR or an API/schema
change could therefore omit its PostgreSQL publication tests. Batch021 exposed
this gap when main gained migration 0083: the previous release's dependency
identity was no longer applicable after synchronization.

## Definition of done

- [x] Both pull-request and main-push filters include article/API changes and the shared Node package manifests/lockfile.
- [x] Preserve the existing job, pinned actions, PostgreSQL service, read-only permissions and test commands.
- [x] Parse the workflow and pass the existing action-pin tests; obtain independent review of the narrow trigger change.

## Steps

- [x] Claim the exact workflow scope and compare old/new trigger coverage.
- [x] Add `apps/api/**`, `apps/web/package.json`, `package.json` and `package-lock.json` to both event filters.
- [x] Validate the YAML structure, equal event path lists and existing workflow-pin tests.
- [x] Prepare the fix for PR #687 so its current API/migration baseline receives an actual release-safety job.

## How to verify

Run `node --test tools/workflow-pins.test.mjs` and parse the YAML with the installed
`js-yaml` package. Check both event path lists and verify the rest of the workflow
is unchanged. The batch021 release task must separately bind the actual completed
PostgreSQL CI job and its exact dependency inventory; local path checks do not
claim that the CI job has already succeeded.

## Notes

- Original workflow Git SHA256: `f9767c61c0b810f54585f4259086f6eb47ab4e43f2cb0fffe3a0014dfef91bfd`.
- Main revision `a588cca1f0573380ace2e1c4d85a3e29b9d822cf` adds the already-reviewed merchant-platform API/schema work. The old batch021 `09eebef7` PostgreSQL applicability proof remains historical and must not be used for the synchronized release.
- Actual local action-pin test log is archived outside Git as `batch021-household-purchasing/workflow-trigger-pins-test.log`; YAML parsing confirms identical event lists, one existing `release-safety` job and unchanged `contents: read` permissions.
- This changes only when existing tests run. No application behavior, credentials, job permissions, publication command or production state is modified.
- Independent review passed 28 checks: outside receipt `batch021-household-purchasing/independent-ci-trigger-review-v1/receipt-pass.json`, SHA256 `dd80ab6c865ff3f46778d39dbb3fb224ad68934af1eef2adb8098ddf97160ee6`. It verified exact YAML reversal, unchanged job/service/permissions/actions/commands, trigger examples and task ownership. Its observation that the initially created task body was still a template is resolved by this completed task description; the reviewed workflow bytes are unchanged.
