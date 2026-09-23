---
id: 2026-09-23-localize-four-digital-continuity-guides-batch020
title: Localize four digital continuity guides batch020
status: done
priority: P1
area: api
owner: codex-batch020
claimed_at: 2026-09-23T09:24:07Z
created_at: 2026-09-23T09:24:05Z
completed_at: 2026-09-23T10:28:12Z
branch: codex/article-localization-batch020-digital-continuity
depends_on: []
scope:
  - apps/api/app/guides/content/backup-and-restore-home-files.json
  - apps/api/app/guides/content/phone-document-scanning-workflow.json
  - apps/api/app/guides/content/reading-notes-that-you-reuse.json
  - apps/api/app/guides/content/shared-household-calendar.json
  - apps/web/public/guides/backup-and-restore-home-files
  - apps/web/public/guides/phone-document-scanning-workflow
  - apps/web/public/guides/reading-notes-that-you-reuse
  - apps/web/public/guides/shared-household-calendar
---

# Localize four digital continuity guides batch020

## Why

Four published lifestyle guides currently provide only Traditional Chinese.
Complete English, Japanese, Korean and Simplified Chinese documents and diagrams
without replacing the existing published source or changing article metadata.

## Definition of done

- [x] Sixteen complete translations retain all blocks, table cells, source URLs,
      dates, code, numbers, credits and original readership conditions.
- [x] Sixteen localized SVG diagrams pass rendered desktop/mobile and glyph checks;
      four existing textless hero images and all original assets stay unchanged.
- [x] Independent editorial and visual reviews bind every document and asset hash.
- [x] Scoped pack/API/frontend/tool/task checks pass and a reviewable PR handoff is
      prepared; actual PR submission and CI remain in the release follow-up.
- [x] Record remaining deployment/import/publication/browser gates in a release
      task; content completion alone must not be reported as public publication.

## Steps

- [x] Inventory exact source packs, active worktree/task scopes and open PRs.
- [x] Capture read-only production rows and compare full normalized source models.
- [x] Draft paired batches outside Git and review each pair independently.
- [x] Integrate only reviewed content and language-suffix diagrams; validate.
- [x] Prepare exact commit paths and PR description, and record the open release
      follow-up. Commit/PR submission is pending the final main synchronization.

## How to verify

Use ArticlePack/GuideDocument and tools/article-localization/pipeline.py field
guards; check full source model preservation and original asset hashes. Run four
pack lints, relevant content-pack/ingest API tests, frontend article/navigation
tests, lint, typecheck, i18n, build, tools and task checks as applicable. Test
artifacts and renders remain outside Git. Preserve advisory warnings honestly.

## Notes

Source main: 24969fe4e4705545cd3ea5e05868e1e947c00248 (the four source packs and
eight original assets are byte-identical to reviewed main 38ebec88). Article
slugs: backup-and-restore-home-files, phone-document-scanning-workflow,
reading-notes-that-you-reuse, shared-household-calendar. Blocks: 15/15/16/15.

2026-09-23T09:23 UTC fresh database snapshot confirms all four active/published
article v1, zh-TW locale/published v6, equal draft/published source documents,
no target locales and no expiry. Remote open PR inventory has zero candidate
path conflicts. Offline worktree/task scan also found no active overlap.

Outside archive: C:/Users/x8120/.codex/article-localization-release/.
- batch020-candidate-inventory/candidates.json:
  929b1308f785ef018339bec5c22643dc679f3ace43caf558779e2851d152a54e
- batch020-candidate-inventory/live-source-full-20260923T092314Z.json:
  ad9b670268b46e5e79f808ce694a2fcf77548571bf50eb582f3d977f861c2d7f
- batch020-candidate-inventory/live-approval-20260923T092314Z.json:
  0c59aef449798350dbdccf2c8363f01da65ac5a1e935d4abf77e2df3db1a2d1c

All four heroes were actually inspected and have no readable text requiring
translation. Each pack has one diagram requiring four localized SVGs. Preserve
AI illustration attribution and non-photograph descriptions in all languages.
Internal article links remain structured links; availability is resolved against
actual same-language publication. No production write has run for this batch.

## Reviewed content, images and route derivative

The four repository packs now contain complete en, ja, ko and zh-CN documents
alongside the unchanged zh-TW originals. The exact content changes are four packs
and sixteen localized SVGs; all eight original hero/diagram assets remain
byte-identical. Complete source models, metadata, source URLs/check dates, code,
numbers and existing AI illustration identity are preserved. There are no numeric
equivalence exceptions. The existing 15/15/16/15 block structures are retained.

Evidence below is under
`C:/Users/x8120/.codex/article-localization-release/batch020-digital-continuity/`:

- Pair A author map: `author-backup-scan/output-map.json`, SHA256
  `7f9272e92640ccd2271b608eb3de4a65020cd8d6b439b800d6947b984958d179`.
  Independent complete-body and desktop/mobile diagram approval:
  `independent-review-backup-scan/receipt-pass-v1.json`, SHA256
  `da7c973349e62a7e81c404415a1466a64d3d7a770b531432a9f12fe4485c46e3`.
- Pair B author map: `author-notes-calendar/output-map.json`, SHA256
  `7e15bfad528c98b38c7852d946024df207976a74bcadf2c941b19ccea8f86054`.
  Independent complete-body and desktop/mobile diagram approval:
  `independent-review-notes-calendar/independent-review-pass.json`, SHA256
  `048cad0e48324f1b0885f25033aef20d1aaca04bb19819896ee8178d722ca67f`.
  This approval required the separately reviewed reading-notes route derivative;
  it did not approve publishing the author's original cross-language URL.
- Exact candidate: `integration-candidate-v1/integration-manifest.json`, SHA256
  `a80cb36e65a38322e26e640441171263ecebc42641d8c6de78f83414757f9936`.
  Independent final integration review:
  `independent-integration-review-v1/receipt-pass.json`, SHA256
  `601912e1505c835d314a0371d62781803b135102ee1c1137e6b24523d5e297f3`.
  All twenty files, sixteen final documents, eight original assets, 1,040 strict
  fields and four exact URL derivatives passed; 576 independent checks found no
  issue. Source packs at 38ebec88 and integration HEAD 35fd4f8a are byte-identical.
- Actual twenty-file application: `integration-applied.json`, SHA256
  `a8c09d23e4f31924e4db632a561b319463f91dd7b88d7d2b8279227c324b6080`.

For reading-notes only, each new language changes `/blocks/15/url` from
`https://mokaair.com/zh-TW/guides` to the same language's `/guides` index.
Every other authored JSON field and every SVG byte is unchanged, with original
author copies, raw/model hashes and reversible byte differences in the manifest.
The existing verified-site-link pipeline allowlist adds only the exact `/guides`
index; it does not approve arbitrary article routes or unpublished destinations.
This route fix is separately owned by
`2026-09-23-localize-verified-guides-index-links-in` and committed in 7009013e.

Actual five-language public route observations are in
`../batch020-candidate-inventory/guides-root-public-route-v2-20260923.json`, SHA256
`2ccb48c9873e59db9a771142337b273f2ed5255e4e83f41af35b1490067a486e`.
The independent route/code approval is
`independent-route-review/receipt-pass.json`, SHA256
`9532fadd4ac123638f7ff196975c8e33026f5daa44c266b41be15590ce2f642b`.
Those observations concern the index only, not publication of these translations.

## Local validation and explicit release boundary

Final actual validation: `test-evidence/attempt-v2/summary-pass.json`, SHA256
`dfbc3fb5e04a0a1a4b8977f77770550ef346db2a91bfb0b8d0f2b94c967657db`.
Node v24.19.0 and this worktree's own `npm ci` dependencies were used; package
inputs and the lockfile stayed unchanged, and the workspace package link resolves
to this worktree. All twenty content hashes, three route-file hashes, lockfile and
HEAD were verified before and after each command.

- Four scoped pack lints passed with zero errors and 32 advisory `no_summary` or
  `text_length` rows. Existing source structure remains unchanged without padding.
- Scoped content-pack/ingest API tests: 64 passed, five PostgreSQL cases skipped
  because `RUN_INTEGRATION_TESTS=0`; this is not PostgreSQL acceptance.
- The first frontend attempt completed eight files/234 tests but failed to start
  the sitemap worker before timeout. Its raw log and FAIL receipt are preserved.
  The inherited failure-tail console print also hit Windows cp1252; that attempt
  is not treated as a complete frontend pass. After build/lint workers settled,
  the same nine files were rerun with `--maxWorkers 2`: all 333 tests passed.
- Tool tests: 81 passed, one Windows/Bash temporary-directory case skipped.
- Thirty-two route pipeline unit tests, scoped Ruff, frontend lint, i18n,
  production build followed by typecheck, task validation and diff checks passed.

Content authoring, independent review and local validation are complete. This
task's completion is limited to that work and preparation of the PR handoff;
it does not assert that a PR is already open, CI has passed, or anything is live.
The open, unclaimed follow-up
`2026-09-23-release-localized-digital-continuity-guides-batch020` now owns PR/CI,
merge, canonical freeze, backup/deployment, exactly sixteen draft and sixteen
publication operations, and five-language public acceptance. Final synchronization
with reviewed main and actual PR submission remain pending in that follow-up.
