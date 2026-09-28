---
id: 2026-09-27-correct-three-wordpress-maintenance-glossary-links
title: Correct three WordPress maintenance glossary links before Batch032
status: done
priority: P2
area: api
owner: codex-batch032-source-links
claimed_at: 2026-09-27T13:30:16Z
created_at: 2026-09-27T13:29:51Z
completed_at: 2026-09-27T13:36:53Z
branch: codex/article-localization-032-source-links
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-comment-spam.json
  - apps/api/app/guides/content/wordpress-performance-plugins.json
  - apps/api/app/guides/content/wordpress-reset-safely.json
---

# Correct three WordPress maintenance glossary links before Batch032

## Why

Three published zh-TW WordPress maintenance articles link ordinary website
terms to unrelated AI glossary pages: moderation「標記」in comment-spam block 9,
the `testnitro=1` URL「參數」in performance-plugins block 16, and a test「標記」
in reset-safely block 20 (zero-based indices). The linked glossary pages define
AI tokens and model parameters, not these WordPress concepts. Batch032 new
locales must not inherit the bad links. This task corrects the existing source
only; publishing the corrected zh-TW revisions and rebinding Batch032 source
versions is a separate guarded release step.

## Definition of done

- [x] Exactly those three inlines become plain text with identical visible
      wording; all neighboring text, article metadata, source URLs/dates,
      image references and assets remain unchanged.
- [x] Pack lint, link tests and an exact three-path semantic diff pass. A
      hash-bound local receipt records the old/new models and production v4
      publication prerequisite. Commit locally without push, PR or host write.

## Steps

- [x] Compare the three repo packs with published zh-TW v4 and confirm each
      misleading destination and its intended ordinary-word meaning.
- [x] Replace only the three ArticleInline objects with TextInline objects.
- [x] Run scoped validation and record exact source/target hashes.

## How to verify

From `apps/api`: `uv run python -m app.guides.pack_cli lint --slug
wordpress-comment-spam --slug wordpress-performance-plugins --slug
wordpress-reset-safely` and targeted guide-pack/link tests. From repo root:
`npm run check:tasks` and `git diff --check`. External validator compares
normalized models, allowing only `/blocks/9/inlines/1`,
`/blocks/16/inlines/1`, and `/blocks/20/inlines/1` respectively.

## Notes

Inventory: `C:\Users\x8120\.codex\article-localization-release\batch032-inventory\batch032-candidate-inventory.json`,
SHA-256 `fa3262b33c0948c125f4a46b93caeade730723d1428ffed0ee8d5d6ccd3a4d73`.
Source published zh-TW v4 hashes: comment-spam
`ef124872b2da725961846d3bb941f65a51b953f8a2c6ed9ac8f0df88467da98d`,
performance-plugins
`b51710d0eaf7b53708f29399103471c22573264b6d68a5e997883b4188922f39`,
reset-safely
`0e35950667a9c14985c34c0c9e30db67c93c100a8b48bb741f4ed5daa87ebfa6`.
The source URLs were checked 2026-09-14. Before Batch032 publication, the
corrected source must be published, source hashes/versions recaptured, and
translations rebound to the new published source. This task does not perform
that production write.

Exact semantic validation receipt:
`C:\Users\x8120\.codex\article-localization-release\batch032-inventory\batch032-source-link-fix-validation.json`,
SHA-256 `848c102856ec4094270d0e074e2ed465820543d81ac8e7cd10905455ed975553`.
It proves only the three specified inline objects changed; all metadata,
sources, dates, images and nine original asset hashes match the published-v4
inventory and base commit. Pack lint checked three entries with zero errors;
existing zh-TW no-summary advisories remain.
Targeted guide content-pack, link and ingest tests: 67 passed, 5 skipped.
`npm run check:tasks` passed; `git diff --check` found no whitespace error.
No push, PR or production change was made.
