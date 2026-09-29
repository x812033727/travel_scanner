---
id: 2026-09-29-prepare-article-release-approval-plan-from
title: Prepare article release approval plan from audited inventory
status: done
priority: P1
area: docs
owner: codex-article-release-plan
claimed_at: 2026-09-29T02:26:30Z
created_at: 2026-09-29T02:26:12Z
completed_at: 2026-09-29T02:42:03Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/work-status-2026-09-29-article-release-plan.md
---

# Prepare article release approval plan from audited inventory

## Why

The owner requested a concrete per-batch article publication list and execution steps for later confirmation. The 2026-09-29 read-only inventory shows eight unpublished source corrections and 68 missing target documents; existing local content and merged PRs do not prove publication.

## Definition of done

- [x] A durable plan enumerates all 21 inventoried slugs, exact locales and source hashes, eight corrections / 12 inline changes, candidate PRs and assets, remaining gates, staged publication and rollback.
- [x] The plan distinguishes preparation approval from production authorization and identifies unavailable execution values without inventing them.

## Steps

- [x] Compare all 21 repository packs and normalized source documents with the supplied authoritative read-only inventory.
- [x] Reconstruct the eight old source documents from merged PR parents and verify exact before/after changes against live hashes.
- [x] Query PR state read-only and verify four review-receipt hashes against current-head evidence.
- [x] Write docs/work-status-2026-09-29-article-release-plan.md with 48 candidate target-document hashes and explicit missing gates for the other 20.

## How to verify

Read the plan against production-inventory.json (SHA-256 ca2ef0aa181c9bd60f13bdeb35371fd02bbe3b25f78ccd6cfa6574040d74a17a). The local collector asserted 21 matching packs/source documents, eight source corrections containing exactly 12 inline changes, and four matching PR receipt hashes. The plan generator asserted 48 candidate target hashes and matching source hashes. Run npm run check:tasks and git diff --check.

## Notes

2026-09-29: Delivered the plan only; no production connection/write, merge, deployment, publication, source-content edit or asset generation. Closing this documentation task does not close any original publication task. Onsen zh-TW v8 is already corrected and published; only its four target locales remain. PRs #940/#941/#953/#954 are currently open and non-draft. PR #966 includes the required publisher-hold fix and an unrelated startup-token guard; the plan explicitly blocks deploying it until the unset production token configuration is resolved with authorization or a separately reviewed publisher change is available. Root controls commits and PRs; independent review requested from audit_video.
