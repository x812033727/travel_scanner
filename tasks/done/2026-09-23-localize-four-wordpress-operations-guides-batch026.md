---
id: 2026-09-23-localize-four-wordpress-operations-guides-batch026
title: Localize four WordPress operations guides batch026
status: done
priority: P2
area: api
owner: codex-batch026
claimed_at: 2026-09-23T17:52:02Z
created_at: 2026-09-23T17:51:31Z
completed_at: 2026-09-27T05:41:45Z
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

Add complete English, Japanese, Korean and Simplified Chinese to four existing published Traditional Chinese guides. The content scope is 4 ArticlePacks, 16 new GuideDocuments and 48 localized assets: 16 editable hero SVGs, 16 1600×900 hero JPGs and 16 diagram SVGs. All four original zh-TW documents, original raw pack metadata and 12 original assets remain unchanged. The reviewed integration contains exactly 52 content paths and 20 full language models.

| Article | Source blocks | Sources | Image block index | New documents | New assets |
| --- | ---: | ---: | ---: | ---: | ---: |
| `wordpress-admin-basics` | 30 | 4 | 25 | 4 | 12 |
| `wordpress-ftp-file-management` | 30 | 6 | 25 | 4 | 12 |
| `wordpress-local-development` | 29 | 4 | 24 | 4 | 12 |
| `wordpress-website-backup` | 29 | 7 | 24 | 4 | 12 |

Image block indexes are zero-based. The four originals contain 118 blocks and 21 source citations. Fresh read-only production snapshot `2026-09-23T17:49:33Z` recorded article v2 and zh-TW draft/published v4, with all target-language rows absent. Full normalized source models and metadata matched main `81f9f338945de587f5d117029905eec4aeca1a1f`; the isolated claim HEAD was `d0299b21a95905dc8ac3651b25d32a0f6dbe88dc`. These are historical source facts, not a current release authorization.

## Definition of done and actual progress

- [x] Inventory the repository originals, full live source and active scopes; claim an isolated worktree.
- [x] Read the 21 official source references and source illustrations. Preserve default single-site versus multisite roles, block-theme limitations, host-key verification, SFTP/FTPS distinctions, host/plan qualifications, Windows/MAMP settings, WXR limitations and backup/restore exclusions.
- [x] Author all 16 complete documents and 48 localized assets, including source titles, provenance, alt text, captions and accessible SVG text; preserve original source dates and audience.
- [x] Complete independent reciprocal full-field and actual image reviews. Verify 1,312 strict fields, code/commands/paths/URLs/numbers, font coverage and desktop/mobile layouts, with zero numeric exceptions. Both reviewers actually viewed 42 source/render image files per pair; mobile four-pan rendering is local Chromium evidence, not physical-device acceptance.
- [x] Preserve 32 structured ArticleInline link instances. Existing runtime resolution requires the same-language target to be actually published and otherwise renders nonclickable text. No route rewrite or current-publication assumption was introduced.
- [x] Record 32 translations of the original short SVG accessible titles and 16 target-only canonical description backfills. Preserve all source accessible titles and the original empty source image descriptions.
- [x] Independently verify the outside integration candidate and apply the exact approved 52 content files. Original raw packs are byte-recoverable by reversing only the inserted target locales, and all 12 original assets remain byte-identical.
- [x] Complete selected local pack/API/publication/pipeline/frontend/tools/lint/i18n/type/build/task/diff checks and bind the actual summary, attempts, skips and advisories to the tested claim HEAD.
- [x] Create the separate open/unclaimed release task for remaining CI, merge, deployment, import, publication and public acceptance.
- [x] Open the scoped content PR with exact head and honest local results; hand off remaining release gates to the separate task.

## Validation and release handoff

All seven local groups and 16 selected commands passed at claim HEAD `d0299b21a95905dc8ac3651b25d32a0f6dbe88dc`, with no failed or incomplete attempts. Results: four pack lints; API 64 passed / 5 PostgreSQL skipped; publication/assembly 83 passed / 59 PostgreSQL skipped; frontend 333 tests in nine files; pipeline 32; render integrity/layout 17; tools 87 with zero skips; i18n, web lint, typecheck, build, task and diff checks passed. The 64 PostgreSQL cases require isolated integration services and were not executed locally. All actual skip reasons and 24 pack-lint advisory rows remain in the immutable summary. A fresh real PostgreSQL release-safety CI result is still required. Do not reattribute these local receipts to a later main merge without a separate applicability check.

Local summary: `test-evidence/summary-pass.json`, SHA256 `c33f006afa69f0558ceea7abe79f17b021524b24df069d480d29206532f28b14`. The root-reported cached main for the next handoff is `0f9eb1dc02cb5663a0ae3590422e4764c269bde8`; no main merge, final content head, PR creation or CI result is asserted by this documentation preparation.

Release task created through the task CLI: `2026-09-23-release-localized-wordpress-operations-guides-batch026`, open and unclaimed. Its repository scope is `docs/article-localization/releases/batch026`. Required CI, actual PostgreSQL evidence, merge, fresh backup, guarded deployment, dry run, 16 draft creations, 16 article publications, journal/database acceptance and five-language public browser verification remain open there. This content work has not deployed, imported or published batch026.

## Evidence and limitations

Evidence archive: `<home>/.codex/article-localization-release/batch026-wordpress-operations/`. Keep detailed evidence outside Git; use its immutable references for the handoff.

- Source snapshot SHA256: `55b9441834486b77c7abb6852a6b9f2b4d825aefa27194b5a6e2f3884bbb756c`; fresh source comparison: `1388b1378e44fafbf9b5bf6aac4ffff6e57d67caaf5b4962edc468c9d928caef`.
- Admin/SFTP independent review: `independent-admin-sftp-review-v1/receipt-pass.json`, SHA256 `afb04be1e367cff62f0c3129e7f6856d26d33364a9cc7a37df8361a44971fd52`.
- Local-development/backup independent review: `independent-local-backup-review-v1/receipt-pass.json`, SHA256 `1669d12cfbce43163d814d6e3156e41d3ccaeaef2ec813241b6435fe32d138f0`.
- Integration manifest: `integration-candidate-v1/integration-manifest.json`, SHA256 `c294be54bdcfa1e4e954f153aa398624c1ce6132aa646b6fd00622bac6a6516f`.
- Independent integration review: `independent-integration-review-v1/receipt-pass.json`, SHA256 `9bbed398ba2d7580d5a96bcc4a242de0e3dd232e3dd7ee2e6363359540d7c606`, 1,988 checks and 1,312 strict fields.
- Applied integration: `integration-applied.json`, SHA256 `c19fe2c4738b0d6aeb3a01c3f978ddaf46e93da607116288829273436fb32012`.

All original `checked_on: 2026-09-14` dates and source URLs remain intact; new source reading is separately recorded. No hosting account, installed MAMP/WordPress instance, real backup/restore, paid plan or physical mobile device was operated for editorial acceptance. The authors recorded 20 editorial advisory rows in their jobs; repository pack lint independently records 24 advisory rows across the complete five-language packs. These are separate actual counts.

Previously identified incorrect AI glossary links in other articles remain excluded and tracked by `2026-09-23-correct-five-unrelated-ai-glossary-links-before`. Cable and URL-parameter/source corrections remain separate. Root owns repository integration/PR/release coordination; disjoint outside-repository authoring and reciprocal review do not authorize an unrelated source change.

## PR handoff, 2026-09-27

Content PR #842: https://github.com/x812033727/travel_scanner/pull/842. The opened content head is 30adba8caf07fb03236376b38c801f34992954c6, targeting current main cef32b0497f403b138de579d5e33efc45cb5ad6d. The article/image scope is unchanged from the independently reviewed integration. Selected post-integration API, publication, task and diff checks passed; the full PR CI is running against that base and remains a release-task gate. PR creation is content handoff only: no merge, deployment, import, publication or public browser acceptance is claimed here.
