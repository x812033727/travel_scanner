---
id: 2026-09-23-localize-two-household-purchasing-guides-batch021
title: Localize two household purchasing guides batch021
status: done
priority: P1
area: api
owner: codex-batch021
claimed_at: 2026-09-23T10:51:19Z
created_at: 2026-09-23T10:51:06Z
completed_at: 2026-09-23T11:52:51Z
branch: codex/article-localization-batch021-household-purchasing
depends_on: []
scope:
  - apps/api/app/guides/content/gadget-purchase-needs-checklist.json
  - apps/api/app/guides/content/household-inventory-spreadsheet.json
  - apps/web/public/guides/gadget-purchase-needs-checklist
  - apps/web/public/guides/household-inventory-spreadsheet
---

# Localize two household purchasing guides batch021

## Why

The currently public gadget purchasing and household inventory articles have only a Traditional Chinese document. Add complete English, Japanese, Korean and Simplified Chinese documents and localized SVG text, preserving the current source, metadata and original artwork.

## Definition of done

- [x] Eight complete translated documents and eight localized SVGs independently reviewed against the published source.
- [x] Both original Traditional Chinese documents, article metadata and four original assets remain unchanged.
- [x] Content, image renders, scoped tests and final Git exports pass; open a batch PR with content and publication states reported separately.

## Steps

- [x] Inventory the full published rows, source versions, existing translations, task conflicts and original assets.
- [x] Claim the exact two-article scope in an isolated worktree.
- [x] Author and independently review the complete four missing locales per article and SVG labels.
- [x] Integrate exact reviewed outputs, run checks, and open the content PR.
- [x] Create a separate release task for guarded import/publication and public acceptance.

## How to verify

Use the existing article-localization pipeline and ArticlePack/GuideDocument validation. Run scoped pack lint, localization pipeline/assembly/publication tests, related frontend checks, lint, i18n, typecheck, build and task checks. Preserve actual logs and numeric/link evidence; inspect every new SVG desktop and mobile render. Full CI, merge, production backup/deploy/import/publication and browser verification remain distinct later gates.

## Notes

- Inventory: outside archive `batch021-candidate-inventory/inventory-final.json`, SHA256 `fd288e7533132529f1495df3f6343fc5e49929b7bfb9714e1c485fe262375979`; full published source snapshot captured 2026-09-23 10:35 UTC, SHA256 `9794e7d03a9ba11ced25f245d54f1be0f4c5d43b5304f02cea976831303ac590`.
- The inventory covered three candidates; this batch selects only `gadget-purchase-needs-checklist` and `household-inventory-spreadsheet`. Their article versions are respectively 1 and 2, and both zh-TW locale versions are 6. Each has 15 blocks, one source and four missing locales.
- `desk-cable-charging-organization` is excluded because its physical-label text links to an unrelated AI glossary article. The separate open source-correction task records that issue; it does not block these two independent articles.
- Both selected articles link to `digital-receipt-archive`, whose five locales were published and accepted in batch019. Preserve structured article links and resolve using actual publication state.
- Textless AI hero JPGs are reused with translated reader-facing provenance; original SVGs and attribution remain unchanged. Eight new language-suffixed SVGs are required.
- Initial worktree base: `8ab9f182bc432886420a5c96bada4d1c2c2f76c5`. No production operation belongs to this content task.

Completed local content evidence (outside Git under `C:/Users/x8120/.codex/article-localization-release/batch021-household-purchasing/`):

- Gadget editorial/visual independent approval: `independent-review-gadget/independent-review-pass.json`, SHA256 `1da7b28719e0f3b4585748412339a2176c10789ef8cd5b5cbad7f01ded9b98cf`.
- Inventory editorial/visual independent approval: `independent-review-inventory/receipt-pass.json`, SHA256 `e26bc6cf8eba022c5d9ea30abd4f44a6dc1ca0086590633dd2f360607c37bd2d`.
- Exact two-pack/eight-SVG integration manifest: `integration-candidate-v2/integration-manifest.json`, SHA256 `9d306a551c8c0223210e3f3ba1c8997bb917d59b39c2206a35c7aaf967716441`.
- Independent integration approval: `independent-integration-review-v1/receipt-pass.json`, SHA256 `eec5f2ebe65cbec08922687636bf5e7f200ed68657ca818e53a7445cd6b3371d`; 390 checks and 524 strict text fields, no numeric exceptions or URL derivatives.
- Applied exact ten files: `integration-applied.json`, SHA256 `70aeadb1c48ace7d2c4ca5360447788854c121a68d30051aee42e4ff478de48f`.
- Fourteen local checks passed: `test-evidence/attempt-v1/summary-pass.json`, SHA256 `b026786245b941d52e6868553ca79e9d3d26abda98f4fb18e611fb19c4f22b68`. API 64 passed/5 PostgreSQL skips; assembly/publication 83 passed/59 PostgreSQL skips; related web 9 files/333 tests; render/integrity 17; tools 81 passed/1 Windows Bash skip; pipeline, i18n, lint, build, typecheck, tasks and diff checks passed. PostgreSQL release-safety evidence is a separate CI/applicability gate. Scoped pack lint has zero errors and 12 existing no-summary/length advisories.
- Every new SVG was visually reviewed at desktop and mobile sizes; the two textless hero images were also inspected. The original raw pack can be recovered byte-for-byte by removing only the inserted locale members.
- Historical review validator references to `94ed2d55` are preserved with an immutable Git export and an exact applicability proof. Current strict checks use `c6b2af0a`; its only change is the previously approved `/guides` route allowlist. All validator function ASTs are equal.
- The fresh 2026-09-23 11:47 UTC source refresh contains exactly the selected two articles and matches their full 10:35 rows: source SHA256 `4d49279676fcb389212b5f4519add66199fec17ccc78166de007ea6b9be4e57b`; comparison SHA256 `3af6beb7627520b094417147b356ecb68c6cd0908c4cb3270385f0838d826afa`.

Release work is tracked separately in `2026-09-23-release-localized-household-purchasing-guides-batch021`. Local content completion does not claim CI, merge, deployment, import, publication or public browser acceptance.

Content PR: https://github.com/x812033727/travel_scanner/pull/687. The content task is complete at authoring/review/local-validation scope. Required CI, actual merge, release artifacts and all production acceptance remain in the separate release task.
