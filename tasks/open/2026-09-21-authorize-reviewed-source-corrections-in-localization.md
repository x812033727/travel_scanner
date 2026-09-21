---
id: 2026-09-21-authorize-reviewed-source-corrections-in-localization
title: Authorize reviewed source corrections in localization releases
status: review
priority: P1
area: tools
owner: codex-source-correction
claimed_at: 2026-09-21T22:38:19Z
created_at: 2026-09-21T22:38:13Z
completed_at:
branch: codex/article-localization-source-correction
depends_on: []
scope:
  - docs/article-localization/assemble_bundle.py
  - docs/article-localization/publish_bundle.py
  - docs/article-localization/source_correction.py
  - docs/article-localization/test_assemble_bundle.py
  - docs/article-localization/test_publish_bundle.py
---

# Authorize reviewed source corrections in localization releases

## Why

The localization publisher safely rejects edits to already-public text, but
batch 009 has independently reviewed corrections to published source facts.
The source baseline contains corrected text while the live revision still has
the earlier text. Without an explicit, version-bound exception, assembly and
publication cannot apply that reviewed correction along with translations.

## Definition of done

- [x] A reviewed correction to one published locale can be packaged and
      published alongside selected translations with exact old/new hashes.
- [x] Unreviewed edits, stale live versions, and unpublished editor drafts
      remain protected; re-running the same release does not add revisions.
- [ ] PR CI passes; the tool-only PR is ready for review.

## Steps

- [x] Add portable independent-review receipt and explicit assembler opt-in.
- [x] Validate review, baseline, pack and live state again before every write.
- [x] Cover approved release, default refusal, drift, draft conflict and rerun.
- [x] Open a separate PR after focused checks.

## How to verify

From `apps/api`, run `python -m pytest ../../docs/article-localization/test_assemble_bundle.py ../../docs/article-localization/test_publish_bundle.py -q -o asyncio_mode=auto`
and `python -m ruff check ../../docs/article-localization/{assemble_bundle,publish_bundle,source_correction,test_assemble_bundle,test_publish_bundle}.py`.
Run `npm run check:tasks` from the repository root.

## Notes

The optional `source_corrections` manifest entry pins an independent receipt
under `reviews/<slug>-<locale>.json`. The receipt includes the complete old
published document, old draft and published hashes/versions, corrected hash,
and exact RFC 6901 pointer changes. It can replace `/sources` as one array;
overlapping pointers are rejected. Source SVG old/new hashes can be listed in
`assets`. The assembler requires repeated `--source-correction-review PATH`
and copies each receipt into the bundle. The publisher recomputes all hashes
and rejects an edited or hidden article before it writes.

Local verification: assembler tests 10 passed; publisher tests 49 passed,
48 skipped (optional integration cases); installer regression tests 15 passed;
Ruff and `npm run check:tasks` passed. Existing task-board warnings predate
this task. Both independent batch009 source-correction receipts passed the
exact validator against `baseline-reconciled-v9.json`, including 17/19 pointer
changes and one source SVG binding per article.
