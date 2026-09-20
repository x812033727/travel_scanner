---
id: 2026-09-20-canonicalize-article-localization-release-files-to
title: Canonicalize article localization release files to LF
status: done
priority: P1
area: tools
owner: codex-article-localization
claimed_at: 2026-09-20T04:01:12Z
created_at: 2026-09-20T04:00:58Z
completed_at: 2026-09-20T04:04:42Z
branch: codex/article-localization-render-containers
depends_on: []
scope:
  - docs/article-localization/assemble_bundle.py
  - docs/article-localization/test_assemble_bundle.py
  - tools/article-localization/pipeline.py
  - tools/article-localization/render.mjs
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/artifact-integrity.test.mjs
---

# Canonicalize article localization release files to LF

## Why

Windows assembled article packs and reviewed SVGs with CRLF bytes, while the
repository's `.gitattributes` stores and deploys every text file with LF. The
publisher compares exact hashes, so a reviewed bundle assembled on Windows was
guaranteed to fail the deployed-file check after Git checkout.

## Definition of done

- [x] Pipeline and bundle text files use LF bytes on every platform.
- [x] Bundle assembly rejects reviewed SVGs with CRLF or trailing whitespace.
- [x] Tests cover explicit CRLF input and the full release safety suite passes.

## Steps

- [x] Normalize generated JSON and SVG text at the writer boundary, including
  SVG line-ending and trailing-whitespace canonicalization.
- [x] Add a fail-closed release check and regression tests.

## How to verify

`python -m pytest tools/article-localization/test_pipeline.py docs/article-localization/test_assemble_bundle.py`

`npm run test:tools`

## Notes

The mismatch was reproduced on batch 001: the Git blob and bundle had the same
content but different SHA256 values because only the bundle contained CRLF.

Verified with 37 focused Python tests, 17 renderer integrity/layout tests, the
76-test tools suite (75 passed, one existing platform skip), Ruff and diff check.
