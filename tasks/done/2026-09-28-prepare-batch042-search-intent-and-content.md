---
id: 2026-09-28-prepare-batch042-search-intent-and-content
title: Prepare Batch042 search intent and content quality localized artwork
status: done
priority: P2
area: api
owner: codex-batch042-root
claimed_at: 2026-09-28T18:01:54Z
created_at: 2026-09-28T15:06:35Z
completed_at: 2026-09-28T18:14:40Z
branch: codex/article-localization-042-seo-a
depends_on: []
scope:
  - apps/web/public/guides/seo-search-intent
  - apps/web/public/guides/seo-content-quality
  - docs/article-localization/batch042-pair-a-evidence.md
---

# Complete Batch042 Pair A localized artwork and evidence

## Why

Two source articles lacked four full language editions and text-bearing artwork. This source task adds independently reviewed translations while preserving the corrected source and existing edits; production release is separate.

## Definition of done

- [x] Verify #942 merge, source task closure and exact main source hashes.
- [x] Install eight full 32-block target documents; preserve source, root metadata, attribution, URLs/dates and link behavior.
- [x] Bind installed LF bytes and 24 image assets to independent full-text/image review.
- [x] Validate 16 SVGs and 20 five-language local desktop/mobile previews.
- [x] Pass installed-pack lint and focused content/link tests; verify immediate rerun unchanged.
- [x] Keep inherited strict source findings explicit in a separate editorial task and open the narrow release task.

## How to verify

Evidence: docs/article-localization/batch042-pair-a-evidence.md. Pack lint: zero errors. Focused tests: 18 passed, 11 skipped in 37.56s. Installed packs match reviewed final candidates exactly. All-triggered-check current-head CI is required before ordinary merge.

## Notes

Repository authoring is complete; this task does not assert the PR is merged or any locale is imported/published. Original source structure is intentionally preserved. Follow-up tasks are 2026-09-28-batch042-pair-a-source-editorial-followup and 2026-09-28-batch042-pair-a-release-reviewed-locales. Local HTML is not production acceptance; isolated rehearsal infrastructure remains unavailable.
