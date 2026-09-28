---
id: 2026-09-28-correct-batch042-seo-glossary-links-before
title: Correct Batch042 SEO glossary links before localization
status: review
priority: P1
area: docs
owner: codex-batch042-source-links
claimed_at: 2026-09-28T14:59:06Z
created_at: 2026-09-28T14:58:49Z
completed_at:
branch: codex/article-localization-042-source-links
depends_on: []
scope:
  - apps/api/app/guides/content/seo-search-intent.json
  - apps/api/app/guides/content/seo-content-quality.json
  - apps/api/app/guides/content/technical-seo-checklist.json
  - apps/api/app/guides/content/seo-learning-roadmap.json
  - docs/article-localization/batch042-source-links-evidence.md
---

# Correct Batch042 SEO glossary links before localization

## Why

Four zh-TW SEO guides contain five links from ordinary SEO wording to unrelated AI glossary entries. Translation from that source would carry misleading links into four more languages.

## Definition of done

- [x] The five false glossary links no longer appear, while the visible zh-TW article text remains unchanged.
- [x] The four pack revisions and validation evidence are recorded for the localization batch.

## Steps

- [x] Compare the five links with their surrounding source paragraphs and claim exact pack paths.
- [x] Convert only the five incorrect rich-text link inlines to plain text.
- [x] Check parsed structure, visible text, pack links, and task state.

## How to verify

From `apps/api`, run `uv run python -m app.guides.pack_cli lint --kind life --slug seo-search-intent --slug seo-content-quality --slug technical-seo-checklist --slug seo-learning-roadmap` and `uv run pytest tests/test_guides_content_links.py`. From the repository root, run `npm run check:tasks` and `git diff --check`. The full before/after hashes and byte-level scope are in `docs/article-localization/batch042-source-links-evidence.md`.

## Notes

Base commit: `0d30e604c52f5e8abb55c4fc567e8699573010a8`. Draft PR: https://github.com/x812033727/travel_scanner/pull/942. This PR changes repository source packs only. Current live revisions have not been asserted here; compare them again under the guarded release process before any source correction or translated-locale import.
