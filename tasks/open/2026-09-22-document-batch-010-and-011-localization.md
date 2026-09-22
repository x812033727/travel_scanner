---
id: 2026-09-22-document-batch-010-and-011-localization
title: Document batch 010 and 011 localization release evidence
status: review
priority: P1
area: docs
owner: codex-batch012-release-evidence
claimed_at: 2026-09-22T03:20:23Z
created_at: 2026-09-22T03:20:02Z
completed_at:
branch: codex/localization-release-evidence-010-011
depends_on: []
scope:
  - docs/article-localization/releases/2026-09-22
  - tasks/open/2026-09-22-document-batch-010-and-011-localization.md
  - tasks/done/2026-09-22-document-batch-010-and-011-localization.md
---

# Document batch 010 and 011 localization release evidence

## Why

Batch 010 Singapore and batch 011 Jeju were independently reviewed, merged,
deployed, published and browser-verified, but their release evidence existed only
in local hash-bound artifacts. Later task-only PRs repeated intermediate Singapore
HOLD findings as if they were still current. Commit a small, shareable evidence
record without production snapshots, logs, credentials or screenshots.

## Definition of done

- [x] Singapore and Jeju release phases, exact Git and artifact hashes, QA counts
      and all public locale URLs are recorded in the repository.
- [x] Small independent editorial, source-correction, numeric/structural and SVG
      JSON receipts are preserved byte-for-byte with their original SHA-256.
- [x] The record distinguishes zero GitHub review objects from independent
      hash-bound editorial review and resolves the stale #639/#647 assertions.

## Steps

- [x] Reconcile final batch010 v6 and batch011 v2 release receipts and journals.
- [x] Copy only the required small review receipts and add structured evidence.
- [x] Validate JSON, receipt hashes, operation counts, task metadata and diff.

## How to verify

`Get-ChildItem docs/article-localization/releases/2026-09-22 -Recurse -Filter *.json`
parsed through `ConvertFrom-Json`; copied receipt SHA-256 values were checked
against their source artifacts. `npm run check:tasks` and `git diff --check` pass.

## Notes

The requested P: worktree could not be checked out because device writes returned
“A device attached to the system is not functioning.” Its path and registration
were preserved. Work continued in a C: sparse worktree under 15 MB with no package
installation. PR #639's task file and PR #647 were not edited or closed.
