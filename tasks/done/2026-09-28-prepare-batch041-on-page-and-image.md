---
id: 2026-09-28-prepare-batch041-on-page-and-image
title: Prepare Batch041 on-page and image SEO artwork
status: done
priority: P2
area: docs
owner: codex-batch041-root
claimed_at: 2026-09-28T17:32:51Z
created_at: 2026-09-28T14:23:38Z
completed_at: 2026-09-28T17:35:59Z
branch: codex/article-localization-041-seo-b
depends_on: []
scope:
  - apps/web/public/guides/on-page-seo-workflow
  - apps/web/public/guides/image-seo-workflow
  - docs/article-localization/batch041-pair-b-evidence.md
---

# Prepare Batch041 on-page and image SEO artwork

## Why

Text-bearing source artwork needs four localized editions. This task owns
24 assets and evidence; separate tasks own the two article packs.

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
