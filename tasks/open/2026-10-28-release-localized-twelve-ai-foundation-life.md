---
id: 2026-10-28-release-localized-twelve-ai-foundation-life
title: Release localized twelve AI foundation life guides
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-28T07:58:43Z
completed_at:
branch:
depends_on:
  - 2026-10-28-localize-twelve-ai-foundation-life-guides
scope:
  - docs/article-localization/releases/2026-10-28-ai-foundations
---

# Release localized twelve AI foundation life guides

## Why

The dependent content task adds en, ja, ko and zh-CN documents and translated
artwork for twelve already-public Traditional Chinese life articles. Repository
installation does not create or publish production locale rows. This separate
task owns the guarded release and its public acceptance evidence.

## Definition of done

- [ ] The exact merged content revision has green checks and is present in the deployed revision.
- [ ] A fresh production snapshot, publish holds, source versions and a pinned native bundle authorize exactly 48 missing target locale rows.
- [ ] The owner approves the concrete deployment/publication scope; a fresh database backup is verified before any production write.
- [ ] All four native publisher phases and their replay pass, with no pending journal operation and no change to the twelve zh-TW sources.
- [ ] All sixty public pages pass document/image/canonical/hreflang/link checks and actual desktop/mobile visual acceptance.
- [ ] Only sanitized release evidence is committed under the declared release directory.

## Steps

- [ ] Confirm the dependent content PR is merged and its exact-head checks passed.
- [ ] Inspect the full pending deployment range, migrations, active hold/lock state and production publish holds before proposing deployment.
- [ ] Bind a fresh repeatable-read snapshot, source versions and current absence of target rows to the reviewed native bundle; stop on drift.
- [ ] Run the native production dry-run and present the exact create/publish counts for owner approval.
- [ ] Take and verify a fresh pg_dump backup, then deploy the approved content revision under the release driver's hold ownership.
- [ ] Execute drafts, publish-articles and publish-hubs using the same bundle, baseline, manifest SHA and durable state directory; rebuild/check links.
- [ ] Reconcile database rows and journal, replay without writes, verify all public pages/images and inspect desktop/mobile screenshots.
- [ ] Write README.md and evidence.json, close this task in the evidence PR, and remove only the release driver's own hold after successful final verification.

## How to verify

Follow the article-localization and deploy skills, the native publisher's guards
and `ops/release/README.md`. Use `report_progress.py` with the actual journal and
hash-bound browser evidence; files existing locally or green CI cannot establish
publication. Retain source snapshots, backup receipts, logs and screenshots in a
persistent directory outside Git. Inspect release-safety CI with real PostgreSQL.

## Notes

- This task is intentionally open and unclaimed while content authoring is active.
- Exact cohort: ai-term-artificial-intelligence, ai-term-machine-learning,
  ai-term-deep-learning, ai-term-neural-network, ai-term-generative-ai,
  ai-term-transformer, ai-term-attention-mechanism, ai-term-pretraining,
  ai-term-inference, ai-term-model-parameters, ai-term-overfitting,
  ai-term-supervised-fine-tuning.
- Target locales: en, ja, ko, zh-CN. No hub or source correction is authorized by
  this release task. The inference citation redirect has a separate maintenance
  task and is not silently changed here.
- The source authoring baseline SHA is
  `3a496f7b1bc9225b64c3d7e7ac439c314ad816c80285a112722e6c5ff19687c8`;
  release must obtain and reconcile a fresh snapshot rather than treating this
  authoring snapshot as current production state.
- The owner's earlier eight-document release and PR #1906 receipt merge are
  separate completed cohorts. They do not publish these 48 new documents.
