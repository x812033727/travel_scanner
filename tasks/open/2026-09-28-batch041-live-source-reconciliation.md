---
id: 2026-09-28-batch041-live-source-reconciliation
title: Reconcile Batch041 live zh-TW image SEO source revision before locale release
status: blocked
priority: P1
area: ops
owner: codex-source-pr-pipeline
claimed_at: 2026-09-28T16:17:39Z
created_at: 2026-09-28T16:16:06Z
completed_at:
branch: codex/article-localization-040-source-task-close
depends_on:
  - 2026-09-28-correct-false-ai-glossary-link-in
scope:
  - docs/article-localization/batch041-live-source-reconciliation.md
  - tasks/open/2026-09-28-batch041-live-source-reconciliation.md
  - tasks/done/2026-09-28-batch041-live-source-reconciliation.md
---

# Reconcile Batch041 live zh-TW image SEO source revision before locale release

## Why

PR #934 corrected one misleading AI-glossary link in the repository's zh-TW
`image-seo-workflow` source. The published zh-TW article still contains the
earlier revision, and the four target locales are absent. Reconcile the live
source before importing or publishing those translations, preserving any
intervening editor changes.

## Definition of done

- [ ] A fresh guarded read-only snapshot records the live article's status,
      revision, version and content hash; any conflict with the repository
      source stops the item for editorial reconciliation.
- [ ] The exact API image release path has a successful isolated rehearsal and
      the production backup is verified before any live mutation.
- [ ] Only the incorrect `標記` inline link is removed in the live zh-TW article
      through the existing revision/publish service, with expected version and
      content hash; hidden, withdrawn or expired state is preserved.
- [ ] A read-back receipt proves the corrected text and publication state,
      unchanged unrelated content, and no target-locale publication.

## Steps

- [ ] Re-read this exact slug under the four-lock read-only procedure and
      compare with the Batch041 inventory and corrected repository hash below.
- [ ] Resolve any source drift and rerun the guarded dry run; stop on conflict.
- [ ] Complete the isolated image-equivalent rehearsal, verified database
      backup, guarded source revision, and read-back checks; write the evidence.

## How to verify

Use the existing `hostinger2` guarded release procedure and an exact
article/lang manifest. Verify `pg_dump -Fc` with `pg_restore --list`; compare
the preflight, dry-run, write receipt and read-back revision/content hash for
`image-seo-workflow`. Render its live zh-TW page and check that the ordinary
word `標記` no longer links to the AI token article. This task does not
authorize or perform a production write by its presence in the queue.

## Notes

The repository pack after PR #934 merged as
`7654e7b5ed14f3e3a118d7a271c887d4c9b1e977` has SHA-256
`b10f6e1f633cff9a13ef0470af157fdd4d0b5616b560141c6e17819fda7c0357`.
The preceding source pack was
`ecab2da5004ad12b46093e53c93baa36e88a2963c97c3246545ab9e64bad9367`.

The read-only Batch041 receipt is
`C:\Users\x8120\.codex\article-localization-release\batch041-seo-readonly-inventory-20260928\receipt-20260928T134834Z.json`
(SHA-256 `01da33a9f151c5472997a449408593b2b8f4e789dcef06b7f0f9084f1760bb99`).
It found this article active/published v2, with zh-TW draft/published v4
matching the pre-correction source and four target locales absent. Re-read
current live state; this receipt is only a prior baseline.

As of this task's creation, no nonproduction Docker environment is available
for the exact pinned production API image rehearsal. No live source revision,
deployment, import, publication or browser verification has occurred.
