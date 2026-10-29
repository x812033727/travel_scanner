---
id: 2026-10-29-release-localized-retrieval-ai-concepts
title: Release localized retrieval AI concepts
status: in-progress
priority: P2
area: docs
owner: codex-release-ai-retrieval-sixteen-20261029
claimed_at: 2026-10-29T12:55:20Z
created_at: 2026-10-29T12:25:43Z
completed_at:
branch: codex/release-ai-retrieval-sixteen-20261029
depends_on:
  - 2026-10-29-localize-four-retrieval-ai-concepts
scope:
  - docs/article-localization/releases/2026-10-29-retrieval-ai-concepts
---

# Release localized retrieval AI concepts

## Why

Four published retrieval-concept articles still lack public English, Japanese,
Korean and Simplified Chinese documents. Their sixteen reviewed translations and
forty-eight localized assets are being delivered by the dependent content task.
Publish this exact cohort after its content PR is approved and merged, using a
fresh release plan and explicit action-time authorization.

## Definition of done

- [x] Verify the merged content commit, green CI, fresh source hashes and exact deployment range.
- [ ] Obtain approval for a concrete dry-run, full backup/restore, deployment and publication plan.
- [ ] Complete the authorized release with unchanged native tooling and retained actual receipts.
- [ ] Verify twenty five-language public pages, sixty total assets and desktop/mobile screenshots.
- [ ] Record publication versions/hashes and a fresh whole-site public-language census.

## Steps

- [x] Claim this release task only when the dependent content task is done and its PR merged.
- [x] Read current deploy and article-localization skills; verify live runtime, holds, locks and source/target state.
- [ ] Disclose all pending commits and migrations; prepare the exact image and same-image isolated rehearsal.
- [x] Run a fresh production read-only candidate dry-run for exactly sixteen new documents and zero source/hub changes.
- [ ] Ask the owner to authorize the complete concrete release plan; previous PR1920 approval does not authorize this release.
- [ ] After approval, take a full database backup and prove an actual isolated restore before any production writes.
- [ ] Deploy only as authorized, repeat the same-image rehearsal and fresh dry-run, then publish the exact reviewed bundle with a new journal.
- [ ] Verify database readback, links, idempotent dry-run and every public page/asset; inspect desktop/mobile screenshots independently.
- [ ] Complete final host verification, clear only proven cohort-owned holds, and preserve every backup and failure receipt.
- [ ] Refresh the global public-only locale inventory, record sanitized evidence in this task's scoped release directory and open a records PR.

## How to verify

- Exact cohort: ai-term-embedding, ai-term-semantic-search, ai-term-reranking,
  ai-term-retrieval-augmented-generation; targets en, ja, ko and zh-CN only.
- Candidate source baseline: all four zh-TW documents were public/draft version 8,
  article version 2, with no target rows at the actual read-only snapshot.
  Recheck before release; this historical snapshot is not fresh release approval.
- Use unchanged native publisher, pinned reviewed bundle, same-image rehearsal,
  actual backup/restore receipts, exact runtime/image identity and public QA.
- Expected acceptance: four source pages plus sixteen translations, twelve
  original assets plus forty-eight new assets, and forty desktop/mobile cases.
  Confirm the final screenshot count in the concrete release plan.

## Notes

- The owner explicitly approved merging #1922 and preparing its release plan.
  The exact approved head f9c9c6fafb2c5f88d05c3ddaf8d9f3f96dbc6eb2 passed
  all 22 CI checks and independent review. It was squash-merged at
  2026-10-29T12:52:47Z as f3895e9df12cf68698285a51bc4af8b8fedc718c;
  the reviewed and merged Git trees are identical. This task was then claimed.
  Backup, hold acquisition, deployment, migration and publication are not yet
  authorized. Prepare the complete concrete plan before requesting approval.
- Candidate manifest SHA-256:
  1be206c2bbdd0fbdebf45a9a3c1dcdb378304c498e93ca2a00ce31336dbabe5b.
  Baseline SHA-256:
  bdc10b0cf4788f2a27b516a53900d8780624a3a40e297954ccb26f8f31219d2f.
  Private jobs, reviews, bundle, native install journals and snapshots remain in
  the owner's durable evidence directory and ignored local mirrors.
- The earlier sixteen-document cohort has already been published and verified;
  do not redeploy it or recreate its cleared hold. The latest actual global
  census remains 2,250 public articles, 1,482 complete in five languages, 768
  incomplete and 3,072 missing public locale documents; 120 draft-only rows were
  excluded. Do not reduce these counts for the current unpublished sixteen.
- Fresh native host preflight at 2026-10-29T12:57:32Z observed deployed checkout
  2464ad1c9c0ee0e2a9f0b9e3bb435ffa706be4cc, a clean tree, no hold and a free
  deploy lock. The exact-four READ ONLY snapshot completed at 12:58:55Z:
  all sources remain zh-TW draft/public v8, article v2, and all sixteen target
  rows are absent; API container/image identity stayed unchanged. Verify the
  database migration revision and API/web identities before classifying the
  actual deployment range. Subsequent full observation at 13:29 UTC verified
  schema 0143_video_daily_briefs already applied, stable API/web/Postgres/Git
  identities, healthy endpoints and the same four sources/absent target rows.
- Remote main advanced during preparation. Candidate c1 correctly refused at
  its remote-target gate before entering the database or native publisher;
  its failure and untouched staged payload were retained. The new fixed target
  is d0857cc450db89c064eb7da8b20fd00d1783afb0. From deployed 2464ad1c9 this
  includes #1922 and #1921, exactly two commits and 67 paths. The additional
  application change skips queued daily-brief dates already represented by a
  VideoProject and writes an audit row, allowing subsequent dates to proceed
  under the existing enabled automation. Its test, eight caption JSON files,
  two docs and one task record are also in the range. No new migration,
  dependency or ops changes are present. All 64 reviewed content/media files
  remain byte-identical to #1922; normalized source documents remain unchanged.
- Candidate c2 actually exited 0 at 2026-10-29T13:35:43Z; full evidence download
  exited 0 at 13:37:54Z. It planned exactly 16 start_translation, 16 publish,
  zero hubs and zero source corrections. Eight completed SELECT statements,
  zero rejected statements, unchanged native/selected nine-key state and
  runtime, and an empty-write candidate journal were independently verified.
  This SQLAlchemy no-DML guard is not PostgreSQL-enforced READ ONLY; native
  transaction/locking semantics remain intact. The journal is candidate-only.
  Actual receipt SHA-256:
  438de78a769a0788333fa56d4fa2078d102f6621252a3c4ccc42a000266f41c7.
  Independent actual readback SHA-256:
  7c814769bea7cee84aeaf41b5e3efd0b1787be6859836bcd10997abd2ce77614.
- The new target's 22 validation checks and two update checks all succeeded;
  announce was conditionally skipped. Raw CI evidence SHA-256:
  726aa9f3977db91ff1d323d2545f10046812eb0624d19582e82ce11bf2c0b717.
  CORE/binder, content/QA and census code reviews passed. Actual local prepare
  exited 0 and bound the real candidate, actor and CI while keeping execution
  disabled and approval null. Independent ready-binding review SHA-256:
  67ba780c83b332b2f61eaf143263619c44dfa0b7104241856f7896b7dc023f7f.
  No production backup, restore, hold, deployment or publication was executed.
- Keep the all-article five-language task open until fresh production evidence
  establishes completion. Store only sanitized release receipts in Git.
