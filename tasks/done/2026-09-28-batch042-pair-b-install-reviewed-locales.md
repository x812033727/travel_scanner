---
id: 2026-09-28-batch042-pair-b-install-reviewed-locales
title: Install reviewed Batch042 technical SEO and roadmap locales
status: done
priority: P2
area: docs
owner: codex-batch042-root
claimed_at: 2026-09-28T18:11:48Z
created_at: 2026-09-28T17:57:31Z
completed_at: 2026-09-28T18:14:43Z
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/technical-seo-checklist.json
  - apps/api/app/guides/content/seo-learning-roadmap.json
---

# Install reviewed Batch042 Pair B locales

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

Evidence: docs/article-localization/batch042-pair-b-evidence.md. Pack lint: zero errors. Focused tests: 18 passed, 11 skipped in 37.57s. Installed packs match reviewed final candidates exactly. All-triggered-check current-head CI is required before ordinary merge.

## Notes

Repository authoring is complete; this task does not assert the PR is merged or any locale is imported/published. Original source structure is intentionally preserved. Follow-up tasks are 2026-09-28-batch042-pair-b-source-editorial-followup and 2026-09-28-batch042-pair-b-release-reviewed-locales. Local HTML is not production acceptance; isolated rehearsal infrastructure remains unavailable.
