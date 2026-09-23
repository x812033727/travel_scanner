---
id: 2026-09-23-localize-four-wordpress-content-guides-batch027
title: Localize four WordPress content guides batch027
status: in-progress
priority: P2
area: api
owner: codex-batch027
claimed_at: 2026-09-23T19:10:40Z
created_at: 2026-09-23T19:10:30Z
completed_at:
branch: codex/article-localization-batch027-wordpress-content
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-posts-pages.json
  - apps/api/app/guides/content/wordpress-taxonomy-navigation.json
  - apps/api/app/guides/content/wordpress-themes-plugins-install.json
  - apps/api/app/guides/content/wordpress-widgets-sidebar.json
  - apps/web/public/guides/wordpress-posts-pages
  - apps/web/public/guides/wordpress-taxonomy-navigation
  - apps/web/public/guides/wordpress-themes-plugins-install
  - apps/web/public/guides/wordpress-widgets-sidebar
---

# Localize four WordPress content guides batch027

## Why

Four existing published WordPress content guides provide only Traditional Chinese. Add complete English, Japanese, Korean and Simplified Chinese documents and localized text-bearing covers/diagrams while preserving the current published source, raw pack metadata and all original assets. This task covers the content and its reviewable PR; CI, deployment, import, publication and public acceptance will be tracked in a separate release task.

## Definition of done

- [x] Inventory all four repository packs, original assets, current complete production rows, existing branch translations, active tasks and open PR scopes; claim this isolated worktree.
- [ ] Read the primary references and inspect all source illustrations; preserve article/page, taxonomy, theme/plugin and classic/block-theme qualifications, source dates, URLs, commands, numbers, audience and credits.
- [ ] Author all 16 complete language documents and 48 localized assets, including 16 editable cover SVGs, 16 1600×900 JPEG covers and 16 diagram SVGs. Preserve 12 original assets and every original zh-TW/raw metadata byte.
- [ ] Independently review all 1,392 translated reader fields, full model structure, numbers and conditions. Actually render and inspect every new image at desktop/mobile sizes, including fonts, glyphs, clipping and layout.
- [ ] Preserve 32 conditional ArticleInline instances and record exact translations of original SVG accessible titles and 16 target-only image-description backfills. Unpublished same-language destinations remain nonclickable.
- [ ] Independently verify and integrate the exact 52 content paths, then run scoped pack/API/publication/frontend/tools/lint/type/i18n/build/task checks and preserve actual skips/advisories.
- [ ] Open a scoped PR and a separate release task with exact versions, hashes and per-article progress. Do not count a merged pack as imported/published or browser-verified.

## Steps

- [ ] Author disjoint pairs outside the repository and complete reciprocal independent reviews.
- [ ] Integrate only approved full documents and assets, run checks, and hand off exact content/CI evidence for release.

## How to verify

Use existing ArticlePack/GuideDocument validation, strict translation fields, original-byte reversal and image render checks. Run the applicable API pack/ingest and publication regression tests, frontend article/image/sitemap tests, localization tools, lint, i18n, types, production build and task validation. Preserve PostgreSQL skip reasons locally and require actual isolated PostgreSQL CI before release. Public five-language desktop/mobile, canonical, reciprocal hreflang, asset bytes, conditional links and complete sitemap verification remain separate release gates.

## Notes

Exact source scope (zero-based image index):

| Slug | Blocks | Sources | Image index | Fields per target |
| --- | ---: | ---: | ---: | ---: |
| wordpress-posts-pages | 30 | 5 | 25 | 86 |
| wordpress-taxonomy-navigation | 31 | 4 | 26 | 86 |
| wordpress-themes-plugins-install | 32 | 4 | 27 | 90 |
| wordpress-widgets-sidebar | 31 | 4 | 26 | 86 |

Fresh read-only production export captured `2026-09-23T19:05:10Z`: all four articles are active/published at article version 2, original zh-TW draft/published/latest version 4, and all four target-language rows are absent. Complete source models, revision hashes, metadata and 16 original files match main `0f9eb1dc02cb5663a0ae3590422e4764c269bde8`. Original source dates remain `2026-09-14`; primary-source rereading and localized image production are not yet complete.

Candidate inventory under `C:/Users/x8120/.codex/article-localization-release/batch027-candidate-inventory-v1/`: `candidate-manifest.json` SHA256 `befb6fc37537e97899cb95b3eee846c6894777ed0e613fd00ae08468abf835b1`; fresh snapshot `live-source-full-20260923T190507Z.json` SHA256 `74e1584cd3b05243bd526c67781bd8451599b754881a7a5185b8f0f6edbbbd26`; root fresh comparison `root-fresh-source-review.json` SHA256 `4a8e19a4ad303ee07ab116cb924d3fd2452c86a1e2e94b1c3140c97f09a6f01e`.

The read-only scan covered 155 readable worktrees, 14,102 task records and 338 local refs without active scoped conflict or existing target translations. Fresh remote PR file checks also found no overlap. These are claim-time evidence, not a permanent lock.

Root owns repository integration and release coordination. Authorized Codex subagents work on disjoint external authoring directories, then cross-review; no agent may change an unrelated source or publish this batch as part of drafting. The newly observed generic “標記” link to `ai-term-token` in `website-information-architecture` is excluded and preserved in `deferred-source-link-findings.json` SHA256 `2bbaf022f8f559ba8eaee79dff964318d9113cc0a746aa314386838bf996957d` for a separate narrow correction task.
