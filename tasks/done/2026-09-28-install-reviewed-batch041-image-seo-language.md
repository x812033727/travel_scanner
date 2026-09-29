---
id: 2026-09-28-install-reviewed-batch041-image-seo-language
title: Install reviewed Batch041 image SEO language documents
status: done
priority: P2
area: docs
owner: codex-batch041-root
claimed_at: 2026-09-28T17:32:58Z
created_at: 2026-09-28T17:32:57Z
completed_at: 2026-09-28T17:36:07Z
branch: codex/article-localization-041-seo-b
depends_on: []
scope:
  - apps/api/app/guides/content/image-seo-workflow.json
---

# Install reviewed Batch041 image SEO language documents

## Why

Source correction #934 and task closure #948 released this pack for the exact
reviewed four-language candidate. It was installed only after current source
parity and candidate hashes passed.

## Definition of done

- [x] Preserve the approved source, metadata, numeric examples, citations and credit.
- [x] Complete four language documents and matching locale images.
- [x] Bind independent review to exact final documents and image bytes.
- [x] Pass pack/schema/content-link checks and five-locale local visual previews.
- [x] Record unresolved editorial and guarded-release gates in separate tasks.

## How to verify

See docs/article-localization/batch041-pair-b-evidence.md. Two-pack lint has zero
errors; content-pack/link tests have 15 passed and 11 DB skips. Twenty five-locale
standalone previews pass. Current CI and inherited source-summary acceptance
remain pending for draft PR #941; no production action is claimed.

## Notes

Root took over after subagent handoff and preserved exact independent-review
bytes, allowing only Git CRLF-to-LF normalization. #934/#948 are merged; the
corrected image source still needs live reconciliation before publication.
