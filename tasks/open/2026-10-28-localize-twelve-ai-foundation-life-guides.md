---
id: 2026-10-28-localize-twelve-ai-foundation-life-guides
title: Localize twelve AI foundation life guides into four languages
status: in-progress
priority: P1
area: api
owner: codex-gpt6-life-ai-foundations-20261028
claimed_at: 2026-10-28T07:12:50Z
created_at: 2026-10-28T07:12:47Z
completed_at:
branch: codex/localize-travel-life-20261028-next
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-artificial-intelligence.json
  - apps/web/public/guides/ai-term-artificial-intelligence
  - apps/api/app/guides/content/ai-term-machine-learning.json
  - apps/web/public/guides/ai-term-machine-learning
  - apps/api/app/guides/content/ai-term-deep-learning.json
  - apps/web/public/guides/ai-term-deep-learning
  - apps/api/app/guides/content/ai-term-neural-network.json
  - apps/web/public/guides/ai-term-neural-network
  - apps/api/app/guides/content/ai-term-generative-ai.json
  - apps/web/public/guides/ai-term-generative-ai
  - apps/api/app/guides/content/ai-term-transformer.json
  - apps/web/public/guides/ai-term-transformer
  - apps/api/app/guides/content/ai-term-attention-mechanism.json
  - apps/web/public/guides/ai-term-attention-mechanism
  - apps/api/app/guides/content/ai-term-pretraining.json
  - apps/web/public/guides/ai-term-pretraining
  - apps/api/app/guides/content/ai-term-inference.json
  - apps/web/public/guides/ai-term-inference
  - apps/api/app/guides/content/ai-term-model-parameters.json
  - apps/web/public/guides/ai-term-model-parameters
  - apps/api/app/guides/content/ai-term-overfitting.json
  - apps/web/public/guides/ai-term-overfitting
  - apps/api/app/guides/content/ai-term-supervised-fine-tuning.json
  - apps/web/public/guides/ai-term-supervised-fine-tuning
---

# Localize twelve AI foundation life guides into four languages

## Why

The owner requested continued completion of missing travel-information and life
article languages. A fresh public-list census on October 28 identifies 12 intel
articles missing 48 documents and 666 life articles missing 2,664 documents.
These twelve foundational AI life articles are public in Traditional Chinese
and have no repository translations in en, ja, ko or zh-CN. Reuse existing
hash-bound jobs if a matching source is found; otherwise translate the complete
body and text-bearing artwork through the existing localization pipeline.

This is a narrow content child of the existing missing-locale program. The old
coverage document is touched by open PR #1902 and is deliberately not part of
this task's scope. Source corrections, travel-route admission and publication
have separate tasks and evidence.

## Definition of done

- [x] All twelve live sources have fresh source/visibility/version bindings and a source fact review before translation.
- [ ] All 48 missing documents and text-bearing images are complete, schema-valid and independently reviewed with exact artifact/document/asset hashes.
- [ ] Original repository documents/images and existing live source rows are preserved; any repository-only source-description difference has explicit preservation admission.
- [ ] Native bundle assembly/install and replay pass, applicable content checks pass, and a guarded content PR exists.
- [ ] A separate release task depends on this task; no authored or rendered document is mislabeled published.

## Steps

- [x] Verify current repository, active scopes, old jobs and fresh public missing-language census.
- [x] Export a bounded repeatable-read production snapshot for exactly these twelve slugs.
- [x] Review source facts, metadata differences and artwork; record any blocking findings separately.
- [x] Pin a scoped baseline and prepare all 48 missing locales.
- [ ] Complete the ChatGPT-authenticated native translation run, retaining every attempt and failure.
- [ ] Render, independently review each locale and apply only reviewed corrections.
- [ ] Assemble/install the native bundle, check source preservation and idempotency, test and open the content/release PR cycle.

## How to verify

Use the unchanged `docs/article-localization/build_baseline.py` and
`tools/article-localization/pipeline.py` with external baseline/work paths and
exact selected slugs/locales. Keep all source snapshots, jobs, attempts, failed
outputs and reviews outside Git. Run official artifact/layout validation,
`GuideDocument`/content-pack checks and native assembly/install guards. Publish
only after a merged/deployed content revision, fresh database guards, backup,
native dry-run/replay and actual public browser acceptance.

## Notes

- Fresh census SHA256: `3053530178e419d65dd6cf38567d5988fe888ec76363db44099e03851bf0daf0`.
  Its sequential public-list observation excludes hidden/expired/draft-only
  articles and is not a repeatable-read whole-database snapshot.
- The selected production snapshot is a fresh repeatable-read read-only export
  from deployed `b78895e5fad1285d68a49a9e059eb318b846e40d`; it is authoritative
  only for these twelve articles. No publication or article mutation occurred.
- The current task claim found no active overlapping task scope. Historical
  research/verification exists, but different staging/source bytes do not inherit
  an old PASS. Current source review and exact-source job reuse remain required.
- Scoped baseline SHA256:
  `3a496f7b1bc9225b64c3d7e7ac439c314ad816c80285a112722e6c5ff19687c8`.
  All twelve source documents exactly match current repository canonical values;
  no repository preservation admission is needed for this cohort. All 48 target
  database locale rows were absent. Source published versions include 2, 8 and 10.
- All twelve full sources and source artwork passed fresh primary-source review.
  A source-citation redirect in `ai-term-inference` is a separate nonblocking
  maintenance task; the same official term search supports the terminology.
  This does not claim every legacy citation URL is directly healthy.
- Initial AI/ML eight documents completed translation, rendering and independent
  native review. One English terminology correction was applied by the root
  coordinator, materialized and rendered without changing any source, attempt or
  visual asset byte. The original finding and exact-diff closure are retained.
  The remaining forty jobs and disjoint independent review partitions continue.
- PR #1906 was merged after all 22 exact-head checks passed as
  `4422b10853e0ead1e647bf17d11f4f0179989fdb`. That receipt merge itself does
  not deploy or publish this new 48-document cohort.
- Native runner uses the existing ChatGPT login, no new paid provider, at most
  three workers, no automatic quota/auth retries, and an external STOP sentinel.
- The overall missing-language program remains open; this task covers 48 target
  documents and does not claim completion of the remaining 2,712 documents.
