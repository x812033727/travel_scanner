---
id: 2026-09-23-localize-four-wordpress-operations-guides-batch026
title: Localize four WordPress operations guides batch026
status: in-progress
priority: P2
area: api
owner: codex-batch026
claimed_at: 2026-09-23T17:52:02Z
created_at: 2026-09-23T17:51:31Z
completed_at:
branch: codex/article-localization-batch026-wordpress-operations
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-admin-basics.json
  - apps/api/app/guides/content/wordpress-ftp-file-management.json
  - apps/api/app/guides/content/wordpress-local-development.json
  - apps/api/app/guides/content/wordpress-website-backup.json
  - apps/web/public/guides/wordpress-admin-basics
  - apps/web/public/guides/wordpress-ftp-file-management
  - apps/web/public/guides/wordpress-local-development
  - apps/web/public/guides/wordpress-website-backup
---

# Localize four WordPress operations guides batch026

## Scope and source

Four existing public zh-TW lifestyle articles: `wordpress-admin-basics`, `wordpress-ftp-file-management`, `wordpress-local-development`, `wordpress-website-backup`. Add complete en, ja, ko and zh-CN documents and their editable SVG cover/diagram plus raster cover, preserving original zh-TW bodies and 12 original assets. Exact scope: 4 packs, 16 new documents, 32 SVGs and 16 JPEGs (52 content paths).

Fresh read-only production snapshot at 2026-09-23T17:49:33Z confirms article version 2, zh-TW draft/published version 4, no target-language rows, and full normalized source models/metadata equal repository main `81f9f338945de587f5d117029905eec4aeca1a1f`. Source includes 118 blocks, 21 source citations and 328 document/SVG fields per target language. Current source date remains 2026-09-14; code, commands, paths, URLs, product names and numeric conditions remain exact.

## Definition of done

- [x] Inventory repository originals, current full live source and local active scopes; claim an isolated worktree.
- [ ] Review primary references and source illustrations; preserve role/site-type, host-key/protocol, operating-system and backup-scope conditions. Preserve distinct short SVG accessible titles with explicit translation ledgers.
- [ ] Author all 16 complete documents and 48 localized assets; no summaries, placeholders or copied source prose.
- [ ] Independently review all translated fields, full models, numeric/code/URL preservation and original-file hashes; render every SVG/JPEG and check desktop/mobile geometry, fonts and glyphs.
- [ ] Keep structured article links conditional on actual publication of the same language. Unpublished targets remain non-clickable; do not rewrite original source links.
- [ ] Integrate exact reviewed files; run scoped pack/API/publication/frontend/tools/lint/type/i18n/build/task checks and required CI.
- [ ] Open a scoped content PR, and create a separate release task for guarded deployment/dry run/16 missing-locale imports/publications and public browser verification.

## Evidence and ownership

Evidence archive: `C:/Users/x8120/.codex/article-localization-release/batch026-wordpress-operations/`.
Candidate inventory: `../batch026-candidate-inventory-v1/candidate-manifest.json`, SHA256 `e5a74830d7c067658651362bf4a31614b16db0aad5b9665e65562e2bc86c412f`.
Root full source comparison: `../batch026-candidate-inventory-v1/root-fresh-source-review.json`, SHA256 `1388b1378e44fafbf9b5bf6aac4ffff6e57d67caaf5b4962edc468c9d928caef`.
Snapshot SHA256: `55b9441834486b77c7abb6852a6b9f2b4d825aefa27194b5a6e2f3884bbb756c`.

Root owns integration/PR/release coordination. Authorized Codex subagents author disjoint pairs outside the repository and cross-review before integration. Primary-source review and original-image visual inspection remain pending; saved inventories are not completion evidence. No production mutation is performed by this task; a merged pack is not imported/published content.

Previously discovered incorrect AI glossary links in other website articles are excluded and separately filed in `2026-09-23-correct-five-unrelated-ai-glossary-links-before`; existing cable and URL-parameter corrections remain separate.
