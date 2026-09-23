---
id: 2026-09-23-localize-two-household-purchasing-guides-batch021
title: Localize two household purchasing guides batch021
status: in-progress
priority: P1
area: api
owner: codex-batch021
claimed_at: 2026-09-23T10:51:19Z
created_at: 2026-09-23T10:51:06Z
completed_at:
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

- [ ] Eight complete translated documents and eight localized SVGs independently reviewed against the published source.
- [ ] Both original Traditional Chinese documents, article metadata and four original assets remain unchanged.
- [ ] Content, image renders, scoped tests and final Git exports pass; open a batch PR with content and publication states reported separately.

## Steps

- [x] Inventory the full published rows, source versions, existing translations, task conflicts and original assets.
- [x] Claim the exact two-article scope in an isolated worktree.
- [ ] Author and independently review the complete four missing locales per article and SVG labels.
- [ ] Integrate exact reviewed outputs, run checks, and open the content PR.
- [ ] Create a separate release task for guarded import/publication and public acceptance.

## How to verify

Use the existing article-localization pipeline and ArticlePack/GuideDocument validation. Run scoped pack lint, localization pipeline/assembly/publication tests, related frontend checks, lint, i18n, typecheck, build and task checks. Preserve actual logs and numeric/link evidence; inspect every new SVG desktop and mobile render. Full CI, merge, production backup/deploy/import/publication and browser verification remain distinct later gates.

## Notes

- Inventory: outside archive `batch021-candidate-inventory/inventory-final.json`, SHA256 `fd288e7533132529f1495df3f6343fc5e49929b7bfb9714e1c485fe262375979`; full published source snapshot captured 2026-09-23 10:35 UTC, SHA256 `9794e7d03a9ba11ced25f245d54f1be0f4c5d43b5304f02cea976831303ac590`.
- The inventory covered three candidates; this batch selects only `gadget-purchase-needs-checklist` and `household-inventory-spreadsheet`. Their article versions are respectively 1 and 2, and both zh-TW locale versions are 6. Each has 15 blocks, one source and four missing locales.
- `desk-cable-charging-organization` is excluded because its physical-label text links to an unrelated AI glossary article. The separate open source-correction task records that issue; it does not block these two independent articles.
- Both selected articles link to `digital-receipt-archive`, whose five locales were published and accepted in batch019. Preserve structured article links and resolve using actual publication state.
- Textless AI hero JPGs are reused with translated reader-facing provenance; original SVGs and attribution remain unchanged. Eight new language-suffixed SVGs are required.
- Initial worktree base: `8ab9f182bc432886420a5c96bada4d1c2c2f76c5`. No production operation belongs to this content task.
