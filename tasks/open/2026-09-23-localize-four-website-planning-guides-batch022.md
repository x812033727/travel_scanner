---
id: 2026-09-23-localize-four-website-planning-guides-batch022
title: Localize four website planning guides batch022
status: in-progress
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

- [ ] Sixteen complete language documents independently reviewed against the full current published source.
- [ ] Forty-eight localized assets (16 hero SVG originals, 16 rendered hero JPGs and 16 diagram SVGs) rendered and visually inspected for glyphs, overlap, overflow and mobile legibility.
- [ ] All four original Traditional Chinese documents, metadata and original assets remain unchanged.
- [ ] Scoped content/tool/frontend checks pass and a batch PR is opened; publication remains a separate release task.

## Steps

- [x] Reconcile repository, task/worktree scopes, open PRs and full published database rows.
- [x] Claim the exact four-article scope in an isolated worktree.
- [ ] Author missing languages and SVG text; render each language cover from the existing SVG.
- [ ] Independently review complete text, numbers, audience, links and all new renders.
- [ ] Integrate exact reviewed bytes, run relevant checks and open the content PR.
- [ ] Record a separate guarded release task for actual CI/merge/deployment/import/publication/browser acceptance.

## How to verify

Use the existing ArticlePack/GuideDocument and article-localization pipeline. Verify every source and translated block, source title, description, image alt text and credit; preserve dates, URLs and product names. Run scoped pack lint, pipeline/assembly/publication tests, related frontend tests, lint, i18n, typecheck, build and task checks. Inspect new SVGs and rendered JPGs on desktop and mobile sizes. CI, merge, deployment, publication and browser acceptance are separate recorded states.

## Notes

- Base: `a588cca1f0573380ace2e1c4d85a3e29b9d822cf`. Candidates: `cloudways-wordpress-setup` (26 blocks/5 sources), `website-budget-worksheet` (26/3), `wordpress-com-org-choice` (26/4), `wordpress-first-site` (27/4).
- Outside inventory archive: `C:/Users/x8120/.codex/article-localization-release/batch022-candidate-inventory/`. Repository candidate manifest SHA256 `14c874b586a0ff79e5553b0d9a6d79f8d59aa7f529b27a64e69fcec4e0ecca63`. Scope scan covered 146 worktrees and 12,542 task files; no active conflicts or other translations found. Related broad summary and lint tasks are unclaimed and are different work; this task changes only the explicit article paths above.
- Fresh read-only snapshot `live-source-full-20260923T122114Z.json`, SHA256 `0de6c3f4884f6b50c5010ccbb7183aac2ab08e1da988014eb6c9f390ea0c264b`; approval `live-approval-20260923T122114Z.json`, SHA256 `35bfd652e30a935c6d8dd73672aa54a0cbb0c81e0cb5fdecdac5a0f290d841dd`.
- All four source article versions are 2 and Traditional Chinese locale/published versions are 4. Full draft/published/latest models and metadata match the repository; each is active/published with only zh-TW, and no conflicting open PR exists.
- All four existing 1600x900 hero JPGs contain Traditional Chinese text and have editable hero.svg originals. They require localized SVG and JPG versions; they must not be classified as textless reusable photos. Original files, attribution and licensing remain intact.
- No production operation belongs to this content task. Translation review must preserve original reader applicability and must not infer nationality from language.
