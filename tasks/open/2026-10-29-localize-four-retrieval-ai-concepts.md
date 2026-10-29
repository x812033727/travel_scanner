---
id: 2026-10-29-localize-four-retrieval-ai-concepts
title: Localize four retrieval AI concepts
status: in-progress
priority: P2
area: docs
owner: codex-ai-retrieval-four-20261029
claimed_at: 2026-10-29T11:35:34Z
created_at: 2026-10-29T11:35:01Z
completed_at:
branch: codex/localize-ai-retrieval-four-20261029
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-embedding.json
  - apps/api/app/guides/content/ai-term-semantic-search.json
  - apps/api/app/guides/content/ai-term-reranking.json
  - apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json
  - apps/web/public/guides/ai-term-embedding
  - apps/web/public/guides/ai-term-semantic-search
  - apps/web/public/guides/ai-term-reranking
  - apps/web/public/guides/ai-term-retrieval-augmented-generation
---

# Localize four retrieval AI concepts

## Why

Embedding, Semantic Search, Reranking and Retrieval-Augmented Generation are
published only in Traditional Chinese. Add their missing English, Japanese,
Korean and Simplified Chinese documents and localized artwork, preserving each
published source. This is a bounded content-authoring step in the existing
all-article language-completion effort; production publication is a separate task.

## Definition of done

- [x] Confirm exact scope ownership and obtain a fresh read-only source snapshot.
- [x] Independently review the four source documents and the fresh baseline.
- [x] Produce all sixteen translations and localized artwork through the native pipeline.
- [x] Complete independent text, image and glyph review bound to final artifact hashes.
- [ ] Assemble and install a verified exact-scope bundle, preserving normalized source documents, effective metadata and original asset bytes.
- [ ] Pass appropriate local content checks and independent final review.
- [ ] File an unclaimed dependent release task; require exact-head green PR CI and owner approval before merging.

## Steps

- [x] Check active worktree tasks, local/remote branch changes and open PRs; claim narrow scope.
- [x] Capture the four current public source rows and derive the exact-four native baseline.
- [x] Resolve source-readiness findings before starting translation; preserve failed attempts.
- [x] Prepare, translate, render and independently review all sixteen jobs.
- [ ] Install the reviewed bundle, close this authoring task in its content PR and request merge approval.
- [ ] Hand off a separate production-release proposal; do not import or publish under this task.

## How to verify

- Native pipeline status, schema/text invariant checks, render receipts and independent hash-bound reviews.
- Native bundle assembly and installation guards; source document/metadata/asset preservation.
- Appropriate content-pack and localization tests, `npm run check:tasks`, `git diff --check` and PR CI.
- Recheck ownership and source/target freshness before opening the content PR.

## Notes

- Claimed only after a read-only audit of 76 worktrees, 710 branch heads and
  44 open PRs found no active candidate-scope owner or overlapping committed
  candidate changes. Audit SHA-256:
  3d1412e6217d37a037e5d0eac75f8972d877da22147c937462a886b7e1f012b1.
- Reused a clean attached worktree on a new branch from main 1a0c641e6. The
  preceding release-records PR #1920 was separately authorized and merged as
  2464ad1c9, with all 22 CI checks and an independent documentation review.
  It required no deployment; its worktree remains separate.
- Fresh exact-four source snapshot captured 2026-10-29T19:31:11.950577+08:00
  through an actual exit-0 read-only transaction; source draft/public version 8,
  article version 2, no existing target locale rows. API runtime and deployed
  host HEAD 9dc9dca54 remained unchanged throughout. Snapshot SHA-256:
  1df6945ecb302cc3c0b448bd497f3876f7a3f622d2c502960ef973f14f8c5a2b.
- The unchanged native baseline builder was run with external output, then
  reduced to exactly the four actual native source rows and one sixteen-target
  batch. Source differences are empty. Baseline SHA-256:
  bdc10b0cf4788f2a27b516a53900d8780624a3a40e297954ccb26f8f31219d2f;
  binding SHA-256:
  97dece24f01f970c3e13ddea057ce54aa862ca04a61a8aa3e8378e67e0b13444.
  The retained native intermediate is not a global production census.
- Both independent gates passed: source-readiness review SHA-256
  de5043f6ca101b66e08098542aff3ced3f25d1994a3d9941559393d9ad5377ed;
  baseline review SHA-256
  71b792d1ae4608d4618d00338717a64168a264772205c15159060719d78fa5dd
  (34 checks). These complementary reviews bind the local candidate source
  quality and its equality with the fresh production rows.
- Native prepare exited 0 with sixteen jobs outside Git. The unchanged native
  ChatGPT-login pipeline ran from 2026-10-29T11:51:28Z to 12:00:33Z with three
  workers and zero automatic retries. Its actual overall exit was 1: four
  outputs introduced Arabic digits where the source used word numbers.
  Only the affected translated fields were corrected, then native materialize
  and final rendering passed. All original attempts and failures remain intact.
- Independent reviewers also requested natural English table captions. The four
  captions now say "Concept comparison; sources checked in 9/2026." while
  preserving the source numeric tokens. Every final edit was independently
  reviewed. All sixteen final text, image and glyph reviews passed, including
  actual inspection of three rendered images per job. Eighteen successful
  render executions include two English rerenders after caption corrections.
- Unchanged native bundle assembly exited 0 on 2026-10-29T12:13:01Z:
  four packs, sixteen publish locales, forty-eight assets, no source corrections
  and no hubs. Manifest SHA-256:
  1be206c2bbdd0fbdebf45a9a3c1dcdb378304c498e93ca2a00ce31336dbabe5b.
  Assembly is local preparation; installation and publication are distinct gates.
- The pre-PR ownership delta found no new competing owner or overlapping PR.
  Review SHA-256:
  5e66f2d77c5e63026bd0dd50a15d827867440299d34a71119984d2c67a585557.
- Private snapshots, raw attempts, render previews and per-job reviews are kept
  in the owner's durable evidence directory and must not enter Git. The native
  installer's repository-relative input guard will use byte-identical ignored
  local mirrors with their own inventory and installation journal.
- No repository content installation, database writes or public release has
  occurred for this cohort at this preparation checkpoint. Green CI and owner
  merge approval remain mandatory PR gates after local authoring is complete.
- Local dependencies installed with `npm ci --no-audit --no-fund`, exit 0. npm
  reported engine warnings for several transitive packages on the existing
  Node v24.13.0 runtime; no runtime upgrade or dependency-file change was made.
- The actual Playwright 1.64.1 headless launch/close and Sharp 0.35.5 import
  passed. An initial presence check looked for the headed Chromium binary;
  the renderer uses the existing headless shell, so no browser install was needed.
- The separate annotation-link correction task concerns Vector Database and
  Chunking, not these four packs. It remains unclaimed and is not part of this scope.
