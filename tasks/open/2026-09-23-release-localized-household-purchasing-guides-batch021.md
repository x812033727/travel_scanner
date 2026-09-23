---
id: 2026-09-23-release-localized-household-purchasing-guides-batch021
title: Release localized household purchasing guides batch021
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-23T11:50:02Z
completed_at:
branch:
depends_on:
  - 2026-09-23-localize-two-household-purchasing-guides-batch021
scope:
  - docs/article-localization/releases/batch021
---

# Release localized household purchasing guides batch021

## Why

The two already-public household purchasing guides have eight missing-language
documents and eight localized SVG diagrams ready for a content PR. Track exact CI,
merge, canonical release, guarded deployment/import/publication and actual public
acceptance separately from authoring. No source correction belongs to this batch.

## Definition of done

- [ ] Bind the final content commit, all required successful checks, independent review and actual merge tree. Obtain actual PostgreSQL release-safety evidence, or prove all dependencies are identical to an explicitly approved existing run.
- [ ] Refresh both full live article/locale rows, preserving concurrent edits, drafts, visibility, ordering and expiry. Only the four still-missing locales per article are eligible.
- [ ] Independently review and freeze exact canonical jobs, source/model/version, tool, Git, SVG and render hashes.
- [ ] Use the existing hostinger2 workflow: verified fresh database backup, owned hold, four deployment locks, durable background deployment and health/revision checks.
- [ ] Dry-run and execute exactly eight translation starts, eight article publications and zero hubs with sealed idempotent journals. Preserve both full original zh-TW locale rows and all article metadata.
- [ ] Verify ten public language URLs, twenty desktop/mobile cases, forty actual screenshots, expanded descriptions, sources, canonical/hreflang and same-language links. Check all twelve asset bytes and complete API/XML sitemap coverage.
- [ ] Record each article's separate content/import/publication/browser states and clear only the owned hold after actual acceptance. Do not claim a global draft audit from these two articles.

## Steps

- [ ] Claim this release task in a dedicated worktree after the content PR is ready.
- [ ] Bind actual CI, merge and dependency applicability; refresh source and host state.
- [ ] Assemble, independently review and freeze the exact release artifacts.
- [ ] Back up, deploy, preview import, create drafts and publish the explicit list.
- [ ] Complete actual database/journal, image and public browser acceptance.
- [ ] Write the release record and clear the owned hold after acceptance.

## How to verify

Use the existing ArticlePack/GuideDocument, canonical assembler and publisher
services. Run existing tests for rerun idempotency, conflicts and private-draft
protection. Compare actual full source rows, metadata, document and image hashes;
inspect the sealed journal and independent visual evidence. Preserve failed or
partial evidence. Local PostgreSQL skips require separate actual CI evidence.

## Notes

Exact scope, target locales `en`, `ja`, `ko`, `zh-CN` for each:

| Slug | Original article version | Original zh-TW version | Planned operations |
| --- | --- | --- | --- |
| gadget-purchase-needs-checklist | 1 | 6 | 4 drafts + 4 publications |
| household-inventory-spreadsheet | 2 | 6 | 4 drafts + 4 publications |

Both source articles have fifteen blocks and one source. Preserve two original
textless hero JPGs and two original SVGs; add eight language-suffixed SVGs. The
structured `digital-receipt-archive` links are backed by accepted batch019
five-language publication. Do not include the separately tracked cable-label
source correction or infer article version 1 for the household-inventory article.

Content evidence is recorded by the dependent content task and archived under
`C:/Users/x8120/.codex/article-localization-release/batch021-household-purchasing/`.
Fresh two-row snapshot at 2026-09-23 11:47 UTC: SHA256
`4d49279676fcb389212b5f4519add66199fec17ccc78166de007ea6b9be4e57b`.
It fully equals the selected 10:35 source rows; this historical snapshot still
requires a fresh pre-release check. All fourteen scoped local checks passed;
required CI, merge, deployment, publication and public acceptance are not yet
claimed by this open release task.
