---
id: 2026-09-20-five-language-article-release-tooling
title: Five-language article release tooling
status: done
priority: P1
area: tools
owner: codex-article-localization
claimed_at: 2026-09-20T01:46:51Z
created_at: 2026-09-20T01:38:32Z
completed_at: 2026-09-20T02:27:47Z
branch: codex/article-localization-tooling
depends_on: []
scope:
  - .github/workflows/article-localization.yml
  - tools/article-localization
  - docs/article-localization
---

# Five-language article release tooling

## Why

The localization effort needs a repeatable trust chain from a live read-only snapshot
through translation, review, repository installation, database publication, and final
evidence. A staged translation must never be mistaken for an approved, imported, public,
or browser-verified article.

## Definition of done

- [x] Translation jobs pin source, model attempts, documents, SVG/raster outputs, and reviews.
- [x] Explicit batches contain no more than 20 articles and preserve complete existing prose.
- [x] Installation is resumable and binds exact reviewed artifacts, backups, and destinations.
- [x] Publication uses existing editorial services, version/hash guards, transactions, locks,
      durable intents, private-draft protection, and hub-last ordering.
- [x] Progress reports count only verifiable stage evidence.
- [x] CI exercises lint, artifact integrity, assembly, installation, reporting, and SQLite plus
      PostgreSQL publication behavior.

## How to verify

- `uv run --project apps/api ruff check tools/article-localization docs/article-localization`
- `uv run --project apps/api python tools/article-localization/test_pipeline.py`
- `node --test tools/article-localization/artifact-integrity.test.mjs`
- `uv run --project apps/api pytest -q -o asyncio_mode=auto docs/article-localization/test_assemble_bundle.py docs/article-localization/test_install_bundle.py docs/article-localization/test_report_progress.py`
- `uv run --project apps/api pytest -q -o asyncio_mode=auto docs/article-localization/test_publish_bundle.py`
- GitHub Actions repeats the publisher suite with an isolated PostgreSQL service.

## Notes

This PR intentionally excludes baseline snapshots, translation work directories, release
bundles, article packs, and public images. Those belong to later content PRs built from
fresh production and repository baselines. The legacy sitemap patch was also excluded
because current main already implements the larger section/locale sitemap architecture.
