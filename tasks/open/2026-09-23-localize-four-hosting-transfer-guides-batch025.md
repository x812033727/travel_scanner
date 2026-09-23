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

- [ ] All four scoped packs contain five complete GuideDocuments, with all 16 new translations complete and original zh-TW/raw pack metadata unchanged.
- [ ] All 48 new images are present: 16 hero SVGs, 16 1600×900 hero JPGs and 16 diagram SVGs; all 12 original image files remain byte-identical.
- [ ] Independent reviewers have read every translated field and actually viewed all desktop/mobile image previews; exact document, asset, render and review hashes are recorded.
- [ ] Structure, numbers, source URLs/dates, code/product terms, audience, credits and same-language structured links pass the strict field guard; any canonical image-description backfills have explicit target-only ledgers.
- [ ] Applicable scoped pack/API/publication/pipeline checks and frontend content tests, lint, i18n, types, build, tools and task checks have passing selected receipts. Record actual failures, retries, PostgreSQL/platform skips and editorial advisories without concealing them.
- [ ] A content PR exists with its exact final head, honest local-validation results and current CI state. Create a separate release task for all remaining CI/merge/deploy/import/publish/browser work; this content task must not claim production completion.

## Sub-tasks

- [ ] Reconfirm the pinned source/claim baseline in the isolated worktree and record the actual claim receipt.
- [ ] Author pair A: `domain-registrar-transfer` and `siteground-wordpress-setup`, four new languages per article, eight complete documents and 24 localized assets.
- [ ] Author pair B: `fastcomet-wordpress-setup` and `hostgator-wordpress-setup`, four new languages per article, eight complete documents and 24 localized assets.
- [ ] Exchange independent prose and image reviews between authors, preserve superseded candidates and require exact final review pins before integration.
- [ ] Assemble an outside-repository candidate, independently verify all 52 eventual content paths, 20 models, 16 reviewed translations and 12 original assets, then apply only the approved candidate.
- [ ] Run the applicable local checks and preserve immutable command logs, selected receipts and final before/after source pins.
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

Authoring, independent review, integration, local checks and PR acceptance are pending when this body is prepared. Actual claim/PR/test/release-task references must be added only after those events occur.
