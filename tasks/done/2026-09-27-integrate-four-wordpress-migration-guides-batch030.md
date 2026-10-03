---
id: 2026-09-27-integrate-four-wordpress-migration-guides-batch030
title: Integrate four WordPress migration guides batch 030
status: done
priority: P2
area: docs
owner: codex-batch030-integration
claimed_at: 2026-09-27T11:44:02Z
created_at: 2026-09-27T11:44:01Z
completed_at: 2026-09-27T12:07:16Z
branch: codex/article-localization-030
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-com-migration.json
  - apps/api/app/guides/content/wordpress-domain-migration.json
  - apps/api/app/guides/content/wordpress-host-migration.json
  - apps/api/app/guides/content/wordpress-migration-aftercare.json
  - apps/web/public/guides/wordpress-com-migration
  - apps/web/public/guides/wordpress-domain-migration
  - apps/web/public/guides/wordpress-host-migration
  - apps/web/public/guides/wordpress-migration-aftercare
  - tasks/done/2026-09-27-localize-two-wordpress-migration-guides-batch030.md
  - tasks/done/2026-09-27-localize-wordpress-migration-batch030-pair-b.md
  - tasks/done/2026-09-27-batch030-host-diagram-label.md
---

# Integrate four WordPress migration guides batch 030

## Why

The WordPress migration series has four published zh-TW-only guides. Pair A and Pair B independently completed 16 missing locale documents and 48 language-suffixed assets. Integrate their reviewed commits against current main as one reviewable Batch030 draft PR; preserve the published zh-TW content. PR #855 merged the separate source-link correction in two zh-TW packs. The corrected zh-TW revisions are not yet published on production, so their publication and a fresh source/version rebind remain release prerequisites.

## Definition of done

- [x] Four packs each contain complete zh-TW, en, ja, ko, zh-CN documents, with 48 new assets and 12 original images unchanged.
- [x] Full-batch source/version, structure, link, image/render and test evidence is hash-bound before a draft PR is opened.
- [x] Draft PR has no auto-merge; no merge, deployment, import, or production write is performed here.

## Steps

- [x] Confirm #855 scope is released and claim integration scope in a new worktree.
- [x] Cherry-pick Pair A and Pair B content plus wording correction onto current main.
- [x] Validate all four packs, all images, published source snapshots, links and checks.
- [x] Commit completion evidence and open a draft PR for independent review.

## How to verify

Run scoped pack lint, API pack/link tests, web ContentBlocks tests, check:i18n, check:tasks, and git diff --check. Independently compare fresh read-only production zh-TW documents and 12 original image bytes with the four packs, render all 32 new SVGs at 1600x900, inspect image sheets, verify 16 JPG dimensions and 48 asset hashes.

## Notes

- Base origin/main `095cf0d76d296fae26367f3177c9845ba30fac2d`. Source paths did not change since Pair A/B base `f44555bb97153fa05cf3ca565ffa28db473e86d3`.
- #855 merged into main as `97125ca43d6d6c726abae3dc863d9699f98bb436`. Batch030 merged that main state as `0d709eee835231f0adb8a3c558e173804ba56a35`: its four zh-TW packs equal current main, and all four target locales equal the prior translated content. Read-only production still serves old v4 documents for host/aftercare, differing only in the marker link at blocks 12 and 4. Publish #855 source revisions, then recapture/rebind before Batch030 publication.
- Integration commits cherry-picked from Pair A `4d5be5d0`, Pair B `a7ebd576`, and wording correction `d0ec33cc`. Pair receipts are outside the repository under `.codex/article-localization-release/batch030-pair-a` and `batch030-pair-b`.

- Draft PR: https://github.com/x812033727/travel_scanner/pull/859 (`isDraft=true`, `autoMergeRequest=null`). No production writes or merge by this task.
- Post-#855 validation: `<home>\.codex\article-localization-release\batch030-integrate\integration-validation-post855.json`, SHA-256 `7d989c7b55acbe5d32be26c9b2533b2f79f7715b7b21ef0c62336b761846d1cb`. PASS 902 checks, four packs, 48 new assets, 12 unchanged originals, 32 SVG full-resolution renders, 16 JPGs; four contact sheets visually reviewed, minimum card margin 22.38 px. The first public read attempt returned a transient 502 during an unrelated deployment; a later full read-only recapture passed.
- Post-merge focused checks: pack lint four entries exit 0 (inherited no-summary and three English-length advisories), API pack/ingest/link tests 67 passed and 5 skipped, web ContentBlocks 65 passed. Earlier on this content branch: web lint, typecheck, i18n, build (340/340 static pages), API Ruff and mypy (422 files), and task check all passed.
