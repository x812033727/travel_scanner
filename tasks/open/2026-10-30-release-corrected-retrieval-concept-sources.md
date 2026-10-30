---
id: 2026-10-30-release-corrected-retrieval-concept-sources
title: Release corrected retrieval concept sources
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-30T08:33:48Z
completed_at:
branch:
depends_on:
  - 2026-10-30-correct-three-retrieval-source-links-and
scope:
  - docs/article-localization/releases/2026-10-30-retrieval-source-corrections
---

# Release corrected retrieval concept sources

## Why

The three reviewed source corrections must reach the published zh-TW documents
before their missing four-language translations can use a new source baseline.
The content task fixes a misleading hybrid-search internal link and first-use
Chinese terminology in hybrid-search, knowledge-graph and agentic-rag.
GraphRAG is unchanged and outside this source-publication scope.

## Definition of done

- [ ] The merged content commit, complete pending deployment range and green CI are verified.
- [ ] Fresh source and asset guards, independent correction review and a native dry-run are bound to a concrete owner-approved release plan.
- [ ] A new full database backup is actually restored in isolation before approved production writes.
- [ ] Only the three zh-TW corrections are published through the guarded source-correction workflow and publicly verified.
- [ ] New source hashes/versions, retained original evidence and a fresh translation baseline are recorded.

## Steps

- [ ] Claim only after the dependent content task is merged; recheck worktrees, branches and PR scopes.
- [ ] Read article-localization source-correction instructions and deploy/release hold rules.
- [ ] Refresh production snapshot and confirm exact documents, draft/public versions, metadata, holds and asset bytes.
- [ ] Compile hash-bound source correction receipts and rehearse the actual target image; disclose the full deployment/migration range.
- [ ] Obtain the concrete production decision, then backup/restore, deploy if needed, publish and verify only this cohort.
- [ ] Verify original assets, three public pages and source-only mutations; record the new baseline before translation begins.

## How to verify

Use the official snapshot/baseline and source_correction.py review workflow,
scoped native dry-run, actual backup/restore and immutable execution receipts.
Compare all three public documents and original assets after publication;
confirm replay is unchanged. Keep localization and publication receipts distinct.

## Notes

This ticket is intentionally open and unclaimed. Current source-only review
SHA-256 is `cf2142fe43ce00aaebc35ed78d3244a6b1f88460093975b41caa70f2b46cd5e8`.
The 2026-10-30 08:23:26 UTC snapshot is
`9abb9ffde5af48277ebea6a7deff129bbc53fda5c074aed66d4298e7cad666e7`;
it shows hybrid-search published/draft v10, knowledge-graph and agentic-rag v8,
article metadata v2 and no en/ja/ko/zh-CN rows. This preparation snapshot is not
a fresh execution-time guard or permission to publish. Full old/new source
hashes are retained in the dependent content task and private review evidence.

The earlier retrieval-four repair finished at target 5c105c01 with native 11/0;
its approvals cover that earlier cohort only. Do not reuse them for this release.
No new translation, deployment or production publication has occurred here.
