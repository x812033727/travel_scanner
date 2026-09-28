---
id: 2026-09-28-batch039-pair-a-business-porter
title: Localize Batch039 business models and five forces
status: in-progress
priority: P2
area: docs
owner: codex-batch039-pair-a
claimed_at: 2026-09-28T12:18:20Z
created_at: 2026-09-28T12:17:58Z
completed_at:
branch: codex/article-localization-039-strategy-a
depends_on: []
scope:
  - apps/api/app/guides/content/business-models-b2b-d2c.json
  - apps/api/app/guides/content/porter-five-forces.json
  - apps/web/public/guides/business-models-b2b-d2c
  - apps/web/public/guides/porter-five-forces
  - docs/article-localization/batch039-pair-a-evidence.md
  - tasks/open/2026-09-28-batch039-pair-a-business-porter.md
---

# Localize Batch039 business models and five forces

## Why

The two published zh-TW strategy guides have no zh-CN, English, Japanese, or Korean documents. Their hero JPGs and SVG diagrams visibly contain Chinese text. A complete translation must cover article copy and artwork together while preserving the published source, factual caveats, citations, and link behavior.

## Definition of done

- [x] Pin the published source versions and hashes, verify current-main packs/assets, and claim only these two guides.
- [x] Translate all title, description, block, table, alt, caption, source-title, and ArticleInline display text into four target locales.
- [x] Translate both text-bearing SVGs per locale and render matching hero JPGs.
- [x] Review every localized article and artwork preview independently; correct content or layout defects.
- [ ] Run scoped pack lint, meaningful API/web content-link tests, task checks, and an exact content/asset hash audit.
- [ ] Record the source, validation, visual review, and release boundary in the scoped evidence document; open a reviewable draft PR after cross-check.

## Steps

- [x] Confirm the four-lock read-only source capture and frozen main hashes.
- [x] Build four-locale documents and localized artwork for the two assigned slugs.
- [ ] Complete browser and editorial QA, focused checks, and evidence; two focused web files still need a valid rerun or CI evidence after worker-start timeouts.
- [x] Request reciprocal review before PR readiness; the root editor independently reviewed article examples and final contact sheets.

## How to verify

Use the pack CLI lint for each exact life-guide slug, compare normalized zh-TW documents and root metadata to the frozen source, and verify that all source URLs/dates and ArticleInline kind/slug targets are preserved. Render all localized SVGs in a browser and check canvas and card bounds. Run focused guide API/web tests and npm run check:tasks. Before any future import or publication, recheck live source and target versions through the guarded read-only process.

## Notes

The 2026-09-28T11:51:28Z guarded four-lock, REPEATABLE READ READ ONLY receipt is stored outside the repository at C:\Users\x8120\.codex\article-localization-release\batch039-strategy-readonly-inventory-20260928\receipt-20260928T115126Z.json, SHA-256 e156935e618b5233d63a5c8981db2dda0837f9cfceefded365fdd75d9485024f. Both zh-TW published/draft documents were version 4, matching the frozen pack after normalization; no target locale rows existed. The other Batch039 pair owns pestle-business-scan and swot-tows-action-plan. This task does not authorize merge, deployment, import, or publication.

The life-pack lint passed for both slugs. Focused API guide tests passed (29 passed, 13 skipped), and i18n, typecheck:web, and task checks passed. All 16 final artwork SVGs rendered without measured or visible clipping/overlap, and all eight JPGs match their SVG browser renders. The structural audit covers eight target documents and 24 new assets. Root editorial review requested three Japanese/Korean wording corrections in the business-models guide; they are applied. A five-file focused web run passed 58 tests in three files but timed out before two workers started; its command exited 1, and the remaining two files still need separate or CI verification. Npm installation completed successfully after 29 minutes.
