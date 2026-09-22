---
id: 2026-09-22-compare-deployed-localization-packs-by-validated
title: Compare deployed localization packs by validated content
status: review
priority: P1
area: tools
owner: codex-deployed-pack-guard
claimed_at: 2026-09-22T00:31:34Z
created_at: 2026-09-22T00:31:15Z
completed_at:
branch: codex/article-localization-deployed-pack-semantics
depends_on: []
scope:
  - docs/article-localization/publish_bundle.py
  - docs/article-localization/test_publish_bundle.py
---

# Compare deployed localization packs by validated content

## Why

Batch 008 dry-run stopped before any database write because the deployed JSON
pack's raw SHA differed from its reviewed release-bundle copy. Both packs
validate to the same complete ArticlePack (including all five locale documents);
only JSON field order and explicit default serialization differ. The manifest
must remain byte-pinned, but deployment should accept equivalent pack content.

## Definition of done

- [x] Dry-run accepts a deployed pack whose validated ArticlePack matches the
      reviewed bundle, despite different JSON serialization.
- [x] Any changed document or metadata still stops before a database write;
      bundle manifest, pack and asset hashes stay byte-pinned.
- [ ] Focused tests and PR CI pass.

## Steps

- [x] Compare deployed pack content after ArticlePack validation when raw hashes
      differ; retain fast-path raw hash and exact asset checks.
- [x] Add equivalent serialization and changed-content/metadata regressions.
- [x] Open and validate a narrowly scoped PR.

## How to verify

From `apps/api`, run `uv run pytest ../../docs/article-localization/test_publish_bundle.py -q -o asyncio_mode=auto`
and `uv run ruff check ../../docs/article-localization/publish_bundle.py ../../docs/article-localization/test_publish_bundle.py`.
Run `npm run check:tasks` and `git diff --check` from repository root.

## Notes

The previously merged source-correction task remains marked `review`, so task
claim required `--force` against that now-merged, inactive scope. Its owner will
close it separately; do not edit that task from this branch.

Focused local checks: publisher tests 52 passed, 51 skipped (optional integration
fixture), Ruff passed, `git diff --check` passed, and task check exited 0 with
existing warnings including the merged #637 task overlap.
