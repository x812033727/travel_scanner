---
id: 2026-09-28-correct-false-ai-glossary-links-in
title: Correct false AI glossary links in Batch040 sources
status: done
priority: P1
area: docs
owner: codex-source-pr-pipeline
claimed_at: 2026-09-28T16:06:37Z
created_at: 2026-09-28T13:10:38Z
completed_at: 2026-09-28T16:08:05Z
branch: codex/article-localization-040-source-task-close
depends_on: []
scope:
  - apps/api/app/guides/content/affiliate-marketing-basics.json
  - apps/api/app/guides/content/ecommerce-product-seo.json
  - apps/api/app/guides/content/zero-click-search-strategy.json
  - tasks/open/2026-09-28-correct-false-ai-glossary-links-in.md
  - tasks/done/2026-09-28-correct-false-ai-glossary-links-in.md
---

# Correct false AI glossary links in Batch040 sources

## Why

Four ordinary marketing and search terms in three zh-TW source articles point to
unrelated AI glossary articles. A reader selecting `標記` in a paragraph about
`rel="sponsored"`, product structured data, or featured snippets lands on the AI
token article; `參數` in a paragraph about product variant URLs lands on the model
parameters article. The Batch040 translations must not reproduce these false links.

## Definition of done

- [x] The four unrelated glossary links are plain text with the same visible wording.
- [x] All other source-article fields, paragraphs, sources, images, and inline links
      are unchanged; the three original pack versions and hashes remain recorded.
- [x] Pack lint, content-link checks, and task checks pass.
- [x] The source-correction PR is merged after green CI.
- [x] The still-pending guarded live zh-TW revision is tracked separately in
      `2026-09-28-batch040-live-source-reconciliation`.

## Steps

- [x] Confirmed the four links against their surrounding zh-TW source paragraphs.
- [x] Changed only the four `article` inlines to `text` in the three packs.
- [x] Confirmed structural parity: only the four specified inline objects differ.
- [x] Completed relevant checks and merged PR #930 after full CI passed.

## How to verify

From `apps/api`:

```bash
uv run python -m app.guides.pack_cli lint --slug affiliate-marketing-basics
uv run python -m app.guides.pack_cli lint --slug ecommerce-product-seo
uv run python -m app.guides.pack_cli lint --slug zero-click-search-strategy
uv run pytest tests/test_guides_content_links.py
```

From the repository root: `npm run check:tasks` and `git diff --check`.

## Notes

Original source snapshot: `origin/main` commit
`27755064e429605bf6e786cd66acd508c1de3645`. The subsequent main merge
`ebde813d6a7fa9cdd8282bfa2400d002c0a6add8` did not touch these packs.
Original UTF-8 pack SHA-256 values before this change:

- `affiliate-marketing-basics.json`: `58a8faaebf1104e0fc194a2cf33e7a1bc5eb70ee0e6764494b4382f14b8bfe21`
- `ecommerce-product-seo.json`: `2e44ea4d0e0b451bdb1f82defcb37bc1d6e581fe17ab4da2c9476bbd8a767fe2`
- `zero-click-search-strategy.json`: `9e1d23f07e0cd6370d06f2f50006e25cd27b2afd471399bb4879f8f67dcfadc5`

Zero-based block indexes: affiliate 17 (`標記`); ecommerce 1 (`標記`) and
12 (`參數`); zero-click 11 (`標記`). The text and its neighboring inline
segments are preserved. No live backend read, import, or publication was performed;
the release process must still compare the current published zh-TW revision before
applying any correction.

Local checks: structural JSON parity passed for all 33 blocks in each pack;
`pack_cli lint` checked all three entries with only the existing `no_summary`
warnings; `tests/test_guides_content_links.py` passed 3 tests;
`npm run check:tasks` validated 1046 task files with unrelated existing warnings;
`uv run alembic heads` returned the single `0111_video_story_series` head.

PR https://github.com/x812033727/travel_scanner/pull/930 merged at
`2026-09-28T15:48:32Z` as `d68ab5db9a417f8f764b8bb9b39ace058c350e68`.
All nine GitHub checks passed on head
`f79d1dc85ad676b7eb329189048af4ea96927891`. This task closes only the
repository source correction. The live zh-TW revisions have not been changed,
and no translation has been imported or published. The guarded release must
reconcile all three live source versions under the separate task before locale
publication.
