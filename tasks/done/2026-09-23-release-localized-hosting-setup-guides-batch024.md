---
id: 2026-09-23-release-localized-hosting-setup-guides-batch024
title: Release localized hosting setup guides batch024
status: done
priority: P2
area: api
owner: codex-batch024-release
claimed_at: 2026-09-23T16:43:03Z
created_at: 2026-09-23T16:19:58Z
completed_at: 2026-09-23T18:05:39Z
branch: codex/article-localization-024-release-record
depends_on:
  - 2026-09-23-localize-four-hosting-setup-guides-batch024
scope:
  - docs/article-localization/releases/batch024
---

# Release localized hosting setup guides batch024

## Why

The independently reviewed content batch adds 16 complete missing-language documents and 48 localized assets to four published hosting guides. Finish the separate guarded release against current source, Git and host state. Repository content and local checks do not establish publication.

## Definition of done

- [x] Actual content PR checks and PostgreSQL release-safety evidence pass at the exact reviewed head; merged tree and target are recorded.
- [x] Fresh full source and host state match the reviewed scope; the canonical bundle is independently reviewed and frozen with exact inputs and assets.
- [x] Fresh verified database backup and guarded hostinger2 deployment complete under existing locks and an owned hold, with healthy services.
- [x] Exactly 16 target drafts and 16 article publications complete with zero hubs, preserving all source models, metadata, visibility and original assets.
- [x] Database, journal, five-language public and browser acceptance pass; only the owned hold is then cleared and post-clear health is verified.

## Steps

- [x] Claim this task separately; reconcile actual content PR, CI, main and host revisions.
- [x] Read fresh full rows for bluehost-wordpress-setup, hosting-com-wordpress-setup, hostinger-wordpress-setup and managed-hosting-comparison. Recheck the prior article 2 / zh-TW 4 baseline and stop on source, draft, visibility, version or concurrent-edit changes.
- [x] Assemble 20 full models from four preserved source documents and 16 approved translations. Bind all 60 assets, independent review/render evidence, actual local results and current CI before freezing.
- [x] Prepare the explicit four-article × en/ja/ko/zh-CN allowlist and exact target/config/manifest/driver. Preserve all existing locks, source/state guards and durable phase/journal receipts. There are no hubs or source-locale rewrites.
- [x] Verify a fresh pg_dump custom-format backup with pg_restore --list, control competing writes, deploy using hostinger2 and verify actual revision and service health.
- [x] Execute import preview. Confirm only the 16 target locales and required asset references change, then import and publish the explicit targets. Preserve hidden, withdrawn and expired states; stop on concurrent edits.
- [x] Verify all 20 full models, original full rows, article/locale versions, metadata and exact 32 sealed journal operations, actor and progression, with no pending operations and repeat-safe scope.
- [x] Verify all 20 public URLs and 40 desktop/mobile viewport cases with 80 top/diagram screenshots. Check complete body, localized images, descriptions, credits, canonical, reciprocal hreflang, matching-language links and complete paginated sitemap/XML.
- [x] Verify 48 new and 12 original assets, including all 16 explicit target-only image-description backfills. Preserve Mokaair / © Mokaair attribution and unchanged source descriptions.
- [x] Independently review final evidence, stage acceptance, clear only the owned hold, check post-clear health and commit the public release record under docs/article-localization/releases/batch024.

## How to verify

Use the existing ArticlePack / GuideDocument, canonical assembler, publisher, durable release driver and hostinger2 workflow. Retain before/after full snapshots, backup verification, exact CI job/log/dependency identities and sealed journals. Local PostgreSQL skips and HTTP 200 alone do not establish release safety or complete public bodies. Resolve structured links only to actually published matching-language targets; unavailable targets remain unclickable.

## Notes

- Task ID: `2026-09-23-release-localized-hosting-setup-guides-batch024`; dependency: `2026-09-23-localize-four-hosting-setup-guides-batch024`. The date consistently follows the UTC source-claim date. Created through the task CLI as an open, unclaimed release task; the header records its actual creation time.
- Scope: four articles, 16 new documents, 20 full models, 48 new assets, 12 originals, 20 public URLs, 40 viewport cases and 80 screenshots. Body counts are 27 / 27 / 27 / 29; each has four sources. Image indices are 22 / 22 / 22 / 24. Historical source versions are article 2 / zh-TW 4.
- Integration manifest SHA256: `bd34dc880d29c882fe8c610dff9983f643e4a7f9a648c8d71c7aab4c1fa3daee`; independent integration: `484b5a75097c45376ae1a57dc702f69ae9c3a409faf48984074d4464eca8df66`; applied: `2781b52e92a42733f506a8ad9701c8ed67e6be0c8e610d180a41701e58432b74`.
- Evidence root: `C:/Users/x8120/.codex/article-localization-release/batch024-hosting-setup/`. Local summary SHA256 is `70594b2f101aa3727302bcc546dabc4dd6e7805de24df7e513ea822e384b2d94`; fast=v2 and all other groups=v1. Preserve the first-attempt tools WSL-probe failure and the Git Bash retry with 87 real tests passed / zero skips. The 64 PostgreSQL skips describe the historical local run only. Actual PR #699 release-safety CI at the accepted 91-version completed 119 combined SQLite/PostgreSQL tests with zero skips, with the fresh 806-dependency inventory checked. Exact final Git, CI, merge, publication and browser pins are recorded below.
- Preserve Taiwan-reader applicability, currency conditions, product labels, URLs and original checked date `2026-09-14`. Webuzo primary-source retrieval timed out during source review; no new verification is claimed. hosting.com SVG accessible titles completely translate their original shorter asset titles; the full article title and A2 designation remain unchanged.

## Actual release completion

- Content PR #699 is merged at `85b76908543e1fb59256a2c8ec30e9c3e8196275`; accepted content head `91b685627bdf524a9da1ab9da965b845e9dfe19d` has the same full tree. All nine current-head CI checks succeeded before the externally performed merge. The release executor did not merge it. The earlier 70-version merge attempt was refused as behind; original attempts and evidence remain preserved.
- Fresh actual PostgreSQL/tool CI run `35892443001`, job `107287985642`: 32 / 14 / 66 tool checks and 119 combined SQLite/PostgreSQL tests, zero skips. The complete 806 selected Git dependencies, actual checkout and tree were independently checked. CI receipt SHA256 `9baa7112542c3ae740150e27abb171e023cbaf4772d68e58ff1357b6756594c7`; root independent review `1a51b398159ab38e2678cae18a674502ab45326284569a0de56ce9d38fd1ee2c`. Historical local 64 PostgreSQL skips and the tools first-attempt failure remain recorded rather than relabeled as success. Current-runtime local follow-up checks also passed before release.
- Canonical final wrapper independent review SHA256 `7633d939bc1608b0ea9fe9133a7897f88550ef0c77c821d2bf092a40a040c408`; frozen ZIP `183a766eb96964affa964b1445da51916d2a21a353771ee1e766f206b6926039`; actual transport independent review `8f3a6ea2fd1f8f5173e0cbcd3ccc34c6c919e8e5a1bff67e7714a519694c8898`. Scope remains exactly four articles, 20 models, 16 new locales, 48 localized images and 12 preserved originals.
- A fresh custom-format database backup was verified with `pg_restore --list`; durable deployment completed under the existing four locks and owned hold. This deployment includes the independently reviewed 107-file runtime delta and migration `0084_ai_news_automation`. The actual read-only post-deployment probe confirmed disabled news settings, shadow mode, all three automatic-publication flags false and zero enabled sources; SHA256 `3631fb027252f6bd72703508e1fa422ab0daf9bb48fe793ba542ddc03e6180ba`. It did not activate the scheduler or news sources.
- Actual dry-run, 16 drafts, 16 article publications, explicit empty publish-hubs phase and final verification completed. Journal SHA256 `29ad0da55d19dab320ad484a05f8e3e2122a593431816748040717050a19c2a2` seals exactly 32 operations with no pending entry. The four complete source rows stay at article 2 / zh-TW 4; all new locales are published version 2. Independent DB/journal acceptance SHA256 `da24f37585df81c280a63013052ff4096066e0149b1dcddd38c5390605da6de8` covers 219 checks. The first local validator attempt used an incomplete API root and failed before any acceptance output; the corrected current API-root invocation and both logs are preserved.
- Actual public acceptance passed 20 URLs, 40 desktop/mobile viewport cases, 80 individually viewed original screenshots, 20 expanded-description/source checks and all 60 public asset byte comparisons. Main QA SHA256 `4bc15833f42334bf9806930ad2d03721b20bdb1369f82b24af3ad8d027b8e947`; independent visual halves `9cd7696b53b4015132f85de6a16b4dd194ca7d1d42e4ad0132fe50965973e898` and `1cb5196781561c4b7d48be8cd9f06237dcfacadf93df47b203bc17c5430a3f31`. Sitemap pages `[1000, 1000, 16]` contain 2016 unique API rows, all covered by XML. Original descriptions remain empty; only the 16 canonical target descriptions were backfilled from localized SVG descriptions. Credits remain Mokaair / © Mokaair.
- Final evidence SHA256 `7058746b17795bfd8719bea8a7628ecab1792faa2b519be7fa08cc69fd1b29d7` passed independent actual projection review `18a9cd8c9eb325c51d1e24d83e69e86d615e52f05f0542ba3590214754cbd2b7`. Explicit acceptance `fb64a8298d27154a5679b858349a11946b86557323314a23f03536604a7ae9ba` was staged before owned-hold clearance `04374c09397b672a1e40d6e663bc397b6c2d85be181b0669a8ffd31cc58cfcd2`. Post-clear read-only snapshot `dd8a10e88647cf12644844af49fe4088c8ef1ddbd5df8d462dfc5185e493dd46` confirms clean deployed target 85, no hold or foreign pending release, and all three healthy endpoints.
- Public records are `docs/article-localization/releases/batch024/README.md` and `evidence.json`; the latter has 23 immutable evidence references and 20 public locale projections without database IDs, actor IDs or raw snapshots. Independent public projection review SHA256 `070f2f02d202b9ded64d2e7eca01e8c73103aa183d2485bcfc6ba4091d1fca89` passed 165 checks. The delegated record commit contains only these records, this task archive and the separately filed source-correction task; record PR/push remains a separate root handoff and does not change the completed production release.
- The existing desktop global-search placeholder/icon overlap remains tracked in `2026-09-22-fix-desktop-global-search-placeholder-icon`. Mobile screenshots represent browser viewports and center-panned diagrams, not physical devices or full-page visual coverage. No site-wide draft-visibility or entire-backlog completion is claimed.
- Five unrelated glossary links found in four future-batch source articles are separately tracked in `2026-09-23-correct-five-unrelated-ai-glossary-links-before`. That open task records exact proposed inline-only changes, reviewed source hashes and future source/publication gates. Those source articles were not edited, translated or published by this release.
