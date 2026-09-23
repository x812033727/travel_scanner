---
id: 2026-09-23-release-localized-household-purchasing-guides-batch021
title: Release localized household purchasing guides batch021
status: done
priority: P1
area: ops
owner: codex-batch021-release
claimed_at: 2026-09-23T11:56:24Z
created_at: 2026-09-23T11:50:02Z
completed_at: 2026-09-23T14:06:10Z
branch: codex/article-localization-021-release-record
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

- [x] Bind the final content commit, all required successful checks, independent review and actual merge tree. Obtain actual PostgreSQL release-safety evidence, or prove all dependencies are identical to an explicitly approved existing run.
- [x] Refresh both full live article/locale rows, preserving concurrent edits, drafts, visibility, ordering and expiry. Only the four still-missing locales per article are eligible.
- [x] Independently review and freeze exact canonical jobs, source/model/version, tool, Git, SVG and render hashes.
- [x] Use the existing hostinger2 workflow: verified fresh database backup, owned hold, four deployment locks, durable background deployment and health/revision checks.
- [x] Dry-run and execute exactly eight translation starts, eight article publications and zero hubs with sealed idempotent journals. Preserve both full original zh-TW locale rows and all article metadata.
- [x] Verify ten public language URLs, twenty desktop/mobile cases, forty actual screenshots, expanded descriptions, sources, canonical/hreflang and same-language links. Check all twelve asset bytes and complete API/XML sitemap coverage.
- [x] Record each article's separate content/import/publication/browser states and clear only the owned hold after actual acceptance. Do not claim a global draft audit from these two articles.

## Steps

- [x] Claim this release task in a dedicated worktree after the content PR is ready.
- [x] Bind actual CI, merge and dependency applicability; refresh source and host state.
- [x] Assemble, independently review and freeze the exact release artifacts.
- [x] Back up, deploy, preview import, create drafts and publish the explicit list.
- [x] Complete actual database/journal, image and public browser acceptance.
- [x] Write the release record and clear the owned hold after acceptance.

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
It fully equals the selected 10:35 source rows. This historical snapshot was
superseded by the fresh 13:25 pre-release comparison recorded below.

Completed 2026-09-23: content PR687 was already merged before the release executor
continued. All nine actual checks passed for head
`27e8ec56e5e88cdad94bb83d2950c13d544d3001`; its full tree matches deployed merge
`e4476b843d43eaa603737b2adef270dfa0368e1c`. Actual PostgreSQL release-safety CI,
fresh source/host reconciliation and independently reviewed canonical artifacts
were accepted before the guarded deployment.

The fresh custom-format backup passed `pg_restore --list`; backup, durable
deployment, dry run, eight drafts, eight publications, zero hubs and verification
all completed. The sealed final journal is
`cb7d7e0d673079acf428fe1ed95aefd8a39ab247eebb18d0de46cc5739ed0b04`.
Never re-run publisher verification merely to regenerate this accepted journal.

Full database documents, source rows and metadata passed; ten public language
URLs, twenty desktop/mobile cases, ten expanded description/source cases, forty
independently viewed original screenshots and all twelve public image hashes
passed. Sitemap pages `[1000, 968]` cover 1,968 unique API language URLs, all also
present in XML. The original source article versions remain 1 and 2, and both
complete zh-TW version 6 rows remain unchanged.

Final evidence SHA256:
`160fe5bdd2a6ee9919333ad1449c577950f206a3f4798a8327949398870e25df`.
Final acceptance SHA256:
`11769cc4c4532156f5fc3ba5252b5ca6ca9be1041de66cb7c666e29f82a2eea2`.
Owned hold clear at 13:54 UTC succeeded with three health checks; clear receipt
SHA256 `2de83ac11e68034990361ce0be1c5dd2361c541a9b2829befc9b172adf91cefd`.
The 13:55 read-only snapshot confirms clean deployed e4476b84, three healthy
endpoints and no hold or pending release; SHA256
`a71de8045a9ada9b77ff42445bbddfdb6fc3f01f68eae40176672342ce8b567d`.

Per-article completion states, public URLs, document/version hashes and evidence
references are in `docs/article-localization/releases/batch021/evidence.json`
(SHA256 `8e6d38820883a5acccb96b69505f3cc99165307e882134461bce56343173254e`).
Desktop/mobile acceptance means browser viewports, not physical devices; mobile
diagram captures show a center pan. The existing desktop search placeholder/icon
overlap remains a separate nonblocking task. This batch makes no whole-site draft
visibility claim. A separate open task records three unrelated source glossary
links found while selecting future batches; their content was not changed here.
