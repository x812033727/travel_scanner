---
id: 2026-09-23-localize-four-hosting-transfer-guides-batch025
title: Localize four hosting transfer guides batch025
status: in-progress
priority: P2
area: api
owner: codex-batch025
claimed_at: 2026-09-23T16:32:28Z
created_at: 2026-09-23T16:32:18Z
completed_at:
branch: codex/article-localization-batch025-hosting-transfer
depends_on: []
scope:
  - apps/api/app/guides/content/domain-registrar-transfer.json
  - apps/web/public/guides/domain-registrar-transfer
  - apps/api/app/guides/content/fastcomet-wordpress-setup.json
  - apps/web/public/guides/fastcomet-wordpress-setup
  - apps/api/app/guides/content/hostgator-wordpress-setup.json
  - apps/web/public/guides/hostgator-wordpress-setup
  - apps/api/app/guides/content/siteground-wordpress-setup.json
  - apps/web/public/guides/siteground-wordpress-setup
---

# Localize four hosting transfer guides batch025

## Why

Four existing published guides have only Traditional Chinese. Add complete English, Japanese, Korean and Simplified Chinese documents and localized illustrations while preserving the published source, article metadata, existing revisions and original images. This task covers content and its reviewable PR; a separate release task must track merge, deployment, import, publication and production acceptance.

## Definition of done

- [x] All four scoped packs contain five complete GuideDocuments, with all 16 new translations complete and original zh-TW/raw pack metadata unchanged.
- [x] All 48 new images are present: 16 hero SVGs, 16 1600×900 hero JPGs and 16 diagram SVGs; all 12 original image files remain byte-identical.
- [x] Independent reviewers have read every translated field and actually viewed all desktop/mobile image previews; exact document, asset, render and review hashes are recorded.
- [x] Structure, numbers, source URLs/dates, code/product terms, audience, credits and same-language structured links pass the strict field guard; any canonical image-description backfills have explicit target-only ledgers.
- [x] Applicable scoped pack/API/publication/pipeline checks and frontend content tests, lint, i18n, types, build, tools and task checks have passing selected receipts. Record actual failures, retries, PostgreSQL/platform skips and editorial advisories without concealing them.
- [ ] A content PR exists with its exact final head, honest local-validation results and current CI state. Create a separate release task for all remaining CI/merge/deploy/import/publish/browser work; this content task must not claim production completion.

## Sub-tasks

- [x] Reconfirm the pinned source/claim baseline in the isolated worktree and record the actual claim receipt.
- [x] Author pair A: `domain-registrar-transfer` and `siteground-wordpress-setup`, four new languages per article, eight complete documents and 24 localized assets.
- [x] Author pair B: `fastcomet-wordpress-setup` and `hostgator-wordpress-setup`, four new languages per article, eight complete documents and 24 localized assets.
- [x] Exchange independent prose and image reviews between authors, preserve superseded candidates and require exact final review pins before integration.
- [x] Assemble an outside-repository candidate, independently verify all 52 eventual content paths, 20 models, 16 reviewed translations and 12 original assets, then apply only the approved candidate.
- [x] Run the applicable local checks and preserve immutable command logs, selected receipts and final before/after source pins.
- [ ] Open the content PR, file the separate release task and record its ID, then complete/archive this task only when its content acceptance and PR handoff are true.

## How to verify

Use the exact four-slug scope for article-pack lint and relevant API pack/ingest/publication/pipeline tests. Run frontend guide rendering tests and the repository lint, i18n, type, build, tools and task checks with the approved runtimes. CI results must be attached to the actual final PR head; local PostgreSQL skips do not substitute for a PostgreSQL CI pass.

Compare all original pack metadata and zh-TW content against their pinned source bytes. Compare every new model and image with the corresponding independent PASS receipt. Validate all structured article links against same-language publication state, and keep unavailable targets nonclickable. The dependent release task must complete actual production body/image/canonical/hreflang/link checks, five-language desktop/mobile screenshots and draft/visibility protection before it can be marked done.

## Notes

Scope in canonical order:

| Slug | Source blocks | Sources | Image block | New documents | New assets |
| --- | ---: | ---: | ---: | ---: | ---: |
| `domain-registrar-transfer` | 32 | 5 | 26 | 4 | 12 |
| `fastcomet-wordpress-setup` | 28 | 3 | 23 | 4 | 12 |
| `hostgator-wordpress-setup` | 29 | 4 | 24 | 4 | 12 |
| `siteground-wordpress-setup` | 28 | 4 | 23 | 4 | 12 |

The four sources contain 117 blocks, 16 source entries and nine ArticleInline links. The 16 translated documents preserve 36 structured article-link instances. Keep the source's applicable Taiwan audience and ICANN gTLD versus ccTLD conditions; do not infer nationality from reading language. Keep all `checked_on: 2026-09-14` dates, source URLs, Mokaair attribution, product labels, hypothetical examples and conditional plan/backup/restore rules. Do not insert current promotional prices or claim account/device performance tests.

The valid DNS links in SiteGround and registrar transfer target `dns-records-troubleshooting`, which currently has only published zh-TW and a separate source-correction task. Preserve these structured links; untranslated targets remain nonclickable through the existing resolver. Exclude the four batch024 guides and the pending cable/HTTPS/DNS/Cloudways SSL source corrections from this task.

The normalized source image descriptions are empty. Any canonical target-only expansion must be recorded at `/blocks/26/description`, `/blocks/23/description`, `/blocks/24/description` and `/blocks/23/description` respectively; never backfill or reserialize the original source as part of translation. All four existing JPG heroes contain Chinese text and have editable SVG originals.

Evidence outside the repository:

- Inventory source commit: `048d20f8f4eb84f7dc68f7349cb11b8787cb47ed`; refreshed setup baseline: `2142f22861a1e27c7a536b8cbe7ba480b7cbd5ac`. All 16 selected source files have identical Git blobs and bytes across both commits.
- `C:/Users/x8120/.codex/article-localization-release/batch025-candidate-inventory/ready-claim-manifest-v1.json`, SHA256 `c681fa5b146df516cb6ddc56ad996d36e2c57d647caeec51caf1a1ab7b93860c`.
- `C:/Users/x8120/.codex/article-localization-release/batch025-candidate-inventory/source-review-supplement-v1.json`, SHA256 `0c12ff8128ec857ddde8bbca966a5abe9092cd86398a4fb13c0e1c6ea65f18ce`.
- Fresh read-only snapshot `live-source-full-20260923T161555Z.json`, SHA256 `b1e481f26779cc504557c98b2a258a0aed02b19da94d425adb1c13080f01a924`; source approval `9e1cd28faf6d9faa96a3cceb622868ea3ad7ab80acb0312fb0bad5640290b7ab`. All four articles are active/published article v2, zh-TW draft/published/latest v4; all full normalized models match Git, and all four target-language rows are absent.
- Fresh setup `setup-readonly-v1/receipt.json`, SHA256 `9cae6d6d73078ebacfded7a0b750d1e89d4ab4039d95ef4d4ecc2459ffe26d37`, preserved as its actual HOLD. Its only findings are four historical P: checkout states, resolved by `historical-checkout-triage.json`, SHA256 `52b2663d9e3f621d00eed58fdb8f63ed912c0d6939c996c44101110417cf73b7`. No ownership override, index repair or old-worktree mutation occurred.
- The preflight read 193 registered worktrees, 13,383 open-task records and the fresh open PR file lists; there are no active scoped claims, existing translations, recent selected-content commits or PR conflicts. Two broad related tasks remain unclaimed. Refresh these facts at actual claim rather than interpreting this record as a permanent lock.

Content and local acceptance completed; the PR handoff remains pending. The separate unclaimed release task is `2026-09-23-release-localized-hosting-transfer-guides-batch025`. CI, merge, deployment, import, publication and actual public acceptance remain open there.

Actual content acceptance:

- Claim HEAD `1b01c6075886e49294832dc25dbf948f58c1aa08`; claim receipt `68618a3ecdab893b34aa9193f62eadca57cd6b5d588204a4c2907b1b00b84413`.
- Pair A independent final review `independent-pair-a-review-v1/receipt-pass-v2.json`, SHA256 `a7f2ffb21abc0cbf41e242cde54e8c4eca5ea4dc4916581c989f67cda96e759f`. Pair B independent final review `independent-fastcomet-hostgator-review-v1/receipt-pass.json`, SHA256 `394132a86257e7182e2116614722f8d9346af642d16671d99876a8ae55e9712d`. Together they cover all 16 full translations, 48 assets, 1,336 strict fields and zero numeric exceptions, with actual desktop/mobile image views and fresh SVG layout/font checks.
- Pair A's superseded HOLD remains preserved; its only required final correction was the SiteGround English diagram label from `Test access limits` to `Test environment limits`, with a bounded font adjustment and newly viewed renders. The other 23 pair assets and all eight documents were unchanged. Pair B uses exact independently approved translations of the source SVG accessible titles. No arbitrary title shortening or numeric exception was introduced.
- Outside candidate `integration-candidate-v1/integration-manifest.json`, SHA256 `32ec0073524abf41f116df8032d317e865dc8d82398f75e12b0f9fee16d2e927`; independent integration review `baaaf32b7b7ec84c454ab94b9203819c6365bb1ab2312740f71d8d92193dc2d0` passed 1,992 checks. It verifies exact 52 paths, 20 models, 12 original assets, reversible raw source/metadata preservation, 36 conditional links and 32 accessible-title ledger rows. All 16 description backfills are explicit and target-only.
- The historical v1 assembler rejected noncanonical inventory ordering before producing output. The reviewed v2 validates four unique canonical slug identities without requiring the historical list order; actual source-schema checks and normal/optimized positive/negative guards passed. Original inventories and failed-attempt evidence remain preserved.
- Applied receipt `integration-applied.json`, SHA256 `87d73e6aa82c1b7a4cb5b0a8a0b212b84cd17fc18bcd587344af206e5f67e811`; no files beyond the reviewed 52 content paths were applied.
- Immutable local summary `test-evidence/summary-pass.json`, SHA256 `e2dd24527777c04fdeb83b44fe2b9b8c2fb252539cbfaef0e285107a9492c3de`, binds the 16 actual selected commands in seven groups to HEAD `1b01c6075886e49294832dc25dbf948f58c1aa08`. All selected attempts passed with no failed/incomplete attempt. Results: four pack lints with 24 retained editorial advisories; API 64 passed / 5 PostgreSQL skipped; publication 83 passed / 59 PostgreSQL skipped; nine frontend files / 333 tests; pipeline 32; render integrity/layout 17; tools 87 with zero platform skips; lint, i18n, types, production build, tasks and diff checks passed. The 64 PostgreSQL skips retain their actual reasons and require separately pinned actual CI. Node 24.19.0 and Git Bash were used, with web tests completed before the production build. Every command preserved all content, original images and guarded dependencies.
- FastComet's three primary pages were readable; HostGator's four primary reads returned 403. Historic source dates remain unchanged; neither editorial review nor local checks claim fresh provider-account, payment, performance or physical-device testing.

All relative evidence paths above are under `C:/Users/x8120/.codex/article-localization-release/batch025-hosting-transfer`. The original local summary is not evidence for any later merged HEAD; any post-merge checks receive separate receipts.
