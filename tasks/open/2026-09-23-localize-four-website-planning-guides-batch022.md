---
id: 2026-09-23-localize-four-website-planning-guides-batch022
title: Localize four website planning guides batch022
status: review
priority: P1
area: api
owner: codex-batch022
claimed_at: 2026-09-23T12:25:55Z
created_at: 2026-09-23T12:25:52Z
completed_at:
branch: codex/article-localization-batch022-website-basics
depends_on: []
scope:
  - apps/api/app/guides/content/cloudways-wordpress-setup.json
  - apps/api/app/guides/content/website-budget-worksheet.json
  - apps/api/app/guides/content/wordpress-com-org-choice.json
  - apps/api/app/guides/content/wordpress-first-site.json
  - apps/web/public/guides/cloudways-wordpress-setup
  - apps/web/public/guides/website-budget-worksheet
  - apps/web/public/guides/wordpress-com-org-choice
  - apps/web/public/guides/wordpress-first-site
---

# Localize four website planning guides batch022

## Why

Four currently public website-planning articles from the original 626-article localization inventory have only Traditional Chinese documents. Add complete English, Japanese, Korean and Simplified Chinese documents and language-specific text-bearing covers and diagrams, preserving the published source and metadata.

## Definition of done

- [x] Sixteen complete language documents independently reviewed against the full current published source.
- [x] Forty-eight localized assets (16 hero SVG originals, 16 rendered hero JPGs and 16 diagram SVGs) rendered and visually inspected for glyphs, overlap, overflow and mobile legibility.
- [x] All four original Traditional Chinese documents, metadata and original assets remain unchanged.
- [ ] Scoped content/tool/frontend checks pass and a batch PR is opened; publication remains a separate release task.

## Steps

- [x] Reconcile repository, task/worktree scopes, open PRs and full published database rows.
- [x] Claim the exact four-article scope in an isolated worktree.
- [x] Author missing languages and SVG text; render each language cover from the existing SVG.
- [x] Independently review complete text, numbers, audience, links and all new renders.
- [ ] Integrate exact reviewed bytes, run relevant checks and open the content PR.
- [x] Record a separate guarded release task for actual CI/merge/deployment/import/publication/browser acceptance.

## How to verify

Use the existing ArticlePack/GuideDocument and article-localization pipeline. Verify every source and translated block, source title, description, image alt text and credit; preserve dates, URLs and product names. Run scoped pack lint, pipeline/assembly/publication tests, related frontend tests, lint, i18n, typecheck, build and task checks. Inspect new SVGs and rendered JPGs on desktop and mobile sizes. CI, merge, deployment, publication and browser acceptance are separate recorded states.

## Notes

- Base: `a588cca1f0573380ace2e1c4d85a3e29b9d822cf`. Candidates: `cloudways-wordpress-setup` (26 blocks/5 sources), `website-budget-worksheet` (26/3), `wordpress-com-org-choice` (26/4), `wordpress-first-site` (27/4).
- Outside inventory archive: `C:/Users/x8120/.codex/article-localization-release/batch022-candidate-inventory/`. Repository candidate manifest SHA256 `14c874b586a0ff79e5553b0d9a6d79f8d59aa7f529b27a64e69fcec4e0ecca63`. Scope scan covered 146 worktrees and 12,542 task files; no active conflicts or other translations found. Related broad summary and lint tasks are unclaimed and are different work; this task changes only the explicit article paths above.
- Fresh read-only snapshot `live-source-full-20260923T122114Z.json`, SHA256 `0de6c3f4884f6b50c5010ccbb7183aac2ab08e1da988014eb6c9f390ea0c264b`; approval `live-approval-20260923T122114Z.json`, SHA256 `35bfd652e30a935c6d8dd73672aa54a0cbb0c81e0cb5fdecdac5a0f290d841dd`.
- All four source article versions are 2 and Traditional Chinese locale/published versions are 4. Full draft/published/latest models and metadata match the repository; each is active/published with only zh-TW, and no conflicting open PR exists.
- All four existing 1600x900 hero JPGs contain Traditional Chinese text and have editable hero.svg originals. They require localized SVG and JPG versions; they must not be classified as textless reusable photos. Original files, attribution and licensing remain intact.
- No production operation belongs to this content task. Translation review must preserve original reader applicability and must not infer nationality from language.

## Content and local-validation handoff — 2026-09-23

- All 16 complete English/Japanese/Korean/Simplified Chinese documents are authored and independently reviewed. All 48 localized assets are present: 16 editable hero SVGs, 16 rendered 1600x900 hero JPGs and 16 diagram SVGs. Accessible SVG titles identify the complete localized article; author and license remain Mokaair / © Mokaair.
- All four Traditional Chinese documents and article metadata retain the published source at article version2 / zh-TW locale and published version4. All 12 original asset files remain byte-identical. Preserve the Taiwan-specific applicability, product names, code/commands, official source URLs and original checked_on2026-09-14.
- The existing canonical pipeline mechanically fills 16 new-locale image.description fields from the translated SVG desc; the source descriptions remain unchanged. The exact backfill ledger is in the integration manifest. No numeric exception or article-route derivative was introduced. Structured related links retain their identities and must resolve against actual target-language publication during release.
- Author pair A output-map-v2 SHA256 `41986022ad83164a7dd49d33963b897c9439622815adffa1a924a5b95d6fefcb`; author pair B output-map-v3 `09c51a913ddfe3340c075206eadb9b9b95af40417c79933e72de9562e1390719`. Independent pair A review `bae754a8764c543981ecbd5268c8561a4740f55b08b58fa3aa2fe01a94531115`; pair B review `c3ae5c4805453ce1807fc89be0ac70a5795c00590426fb632547389cf83f634a`.
- Pair B's final correction ledger preserves prior versions and closes full SVG-title metadata, one English diagram label, four Korean label font sizes and one Korean no-index phrase. Final author receipt SHA256 `d9a45505e0884a4d1d188dc0ace191bf4736c41f762a206a12d8f01fb00c436e`; correction proof `4656a9c4bec8d5820f8f716f57a34b8060da3cb1be2cace64d3eee9ebe660be8`. Pair A final author receipt `f0a3a4678670999ed9fa3d33404b1223bd02f51c0e99a86ccf3cd443575970f1`.
- Outside evidence root: `C:/Users/x8120/.codex/article-localization-release/batch022-website-basics/`. Integration manifest `integration-candidate-v1/integration-manifest.json` SHA256 `bf547264c73f6568f185c42fb84f37a966f836db0e151acc6de3cbb20a6c77f1`; independent integration review `90235c260448f38c518ff3ea0119a1b3175b410a5b8a7c18d775fb6eb96fe010` verifies52files/20models/12originals,1,240strictfields and1,865checks. Actual root apply receipt `integration-applied.json` SHA256 `0c8dda7e17db8593e82a27b0417fd74a3f2f93d2f80e51e511fd795ae31fef06`.
- Local `test-evidence/summary-pass.json` SHA256 `d4c6a3a05558e7ad867cd098958f79cbd2ed0b43a2a9f5d7086d4fc6802170bf`:16checksPASS; API64passed/5PostgreSQL-skipped; assembly/publication83passed/59PostgreSQL-skipped; web9files/333passed; pipeline32passed; render17passed; tools81passed/1WindowsBash-skipped. Pack lint, i18n, web lint, build, typecheck, task validation and diff check passed. PostgreSQL execution requires separately pinned actual CI evidence.
- The first web attempt retained234completed tests/8files and a worker-startup timeout for the ninth file. It was not accepted as a complete pass. Only the web group was rerun with the same nine files and maxWorkers2; the complete333-test attempt passed. Both attempts and exact logs are preserved.
- All24pack-lint advisories remain explicit:20missing-summary-block advisories inherited from source structure and4English body-length advisories (6092–6255characters against a6000guideline). These are nonfatal lint results; complete translated bodies were not shortened to silence them.
- This task's completion boundary is reviewed content, local checks and an opened content PR. Actual CI, merge, frozen canonical bundle, backup/deployment,16draft imports/16publications,0hubs and public/browser acceptance are unfinished work in `2026-09-23-release-localized-website-planning-guides-batch022`; this content task makes none of those claims. PR creation remains unchecked until a real URL is recorded below.
