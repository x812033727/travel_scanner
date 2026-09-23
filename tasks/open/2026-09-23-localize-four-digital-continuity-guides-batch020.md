---
id: 2026-09-23-localize-four-digital-continuity-guides-batch020
title: Localize four digital continuity guides batch020
status: in-progress
priority: P1
area: api
owner: codex-batch020
claimed_at: 2026-09-23T09:24:07Z
created_at: 2026-09-23T09:24:05Z
completed_at:
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

- [ ] Sixteen complete translations retain all blocks, table cells, source URLs,
      dates, code, numbers, credits and original readership conditions.
- [ ] Sixteen localized SVG diagrams pass rendered desktop/mobile and glyph checks;
      four existing textless hero images and all original assets stay unchanged.
- [ ] Independent editorial and visual reviews bind every document and asset hash.
- [ ] Scoped pack/API/frontend/tool/task checks pass, followed by a reviewable PR.
- [ ] Record remaining deployment/import/publication/browser gates in a release
      task; content completion alone must not be reported as public publication.

## Steps

- [x] Inventory exact source packs, active worktree/task scopes and open PRs.
- [x] Capture read-only production rows and compare full normalized source models.
- [ ] Draft paired batches outside Git and review each pair independently.
- [ ] Integrate only reviewed content and language-suffix diagrams; validate.
- [ ] Commit exact paths, open PR, and record release follow-up.

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
