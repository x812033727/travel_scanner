---
id: 2026-09-23-release-localized-digital-organization-guides-batch019
title: Release localized digital organization guides batch019
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-23T09:06:20Z
completed_at:
branch:
depends_on:
  - 2026-09-23-localize-four-digital-organization-guides-batch019
scope:
  - docs/article-localization/releases/batch019
---

# Release localized digital organization guides batch019

## Why

Four already-public digital-organization articles have sixteen reviewed missing
language documents and sixteen localized diagrams ready for review. Content in
Git does not publish those languages. Track the remaining CI, merge, guarded
deployment/import/publication and real public acceptance separately.

## Definition of done

- [ ] Exact content PR head passes required CI and is reviewed and merged; obtain
      applicable PostgreSQL release-safety evidence for the exact dependencies.
- [ ] Fresh live source/visibility/version inventory permits exactly the missing
      language operations below; preserve any later editing or visibility changes.
- [ ] Assemble and independently review the canonical bundle with exact source,
      tool, document, image and final Git hashes; freeze the portable artifact.
- [ ] Verify a fresh database backup and hold/locking ownership, deploy the reviewed
      necessary files through the existing hostinger2 workflow, and check health.
- [ ] Dry-run and idempotent import/publication change only the sixteen explicitly
      listed missing-language targets, retaining all original zh-TW rows/metadata.
- [ ] All twenty five-language pages pass full-body/image/canonical/hreflang/link
      checks and desktop/mobile visual review; unrelated drafts remain private.
- [ ] Record per-article content/import/publication/browser results, final journals
      and actual database acceptance; clear only the owned hold after acceptance.

## Steps

- [ ] Review final content Git export, PR and exact-head CI evidence.
- [ ] Refresh source inventory and freeze the approved canonical bundle.
- [ ] Run backup/deploy/dry-run/import/publication through the explicit-list tools.
- [ ] Complete database and browser acceptance and record the release evidence.

## How to verify

Use the existing `docs/article-localization/assemble_bundle.py` and
`docs/article-localization/publish_bundle.py` contracts. Follow the deployment
skill and content-pipeline runbook; bind source rows, versions, content hashes,
deployed image bytes, journals and screenshots. Abort each conflicting item and
recheck it rather than overwriting concurrent edits. Verify rerun idempotency and
draft/state protection. Keep content completion, import, publication and browser
acceptance separate in the final receipt.

## Notes

Exact four-article scope and target locales:

| Article slug | Missing target locales |
| --- | --- |
| browser-bookmark-project-folders | en, ja, ko, zh-CN |
| digital-receipt-archive | en, ja, ko, zh-CN |
| file-naming-system-for-home | en, ja, ko, zh-CN |
| phone-photo-declutter-workflow | en, ja, ko, zh-CN |

That is sixteen complete new documents and sixteen new diagrams, one
`diagram-1-{en,ja,ko,zh-cn}.svg` per slug/language under
`apps/web/public/guides/<slug>/`. The four original textless hero JPGs and four
original SVGs (eight assets total), existing zh-TW documents and all article
metadata are preserved. These four articles have no series hub publication step.

Read-only source capture on 2026-09-23T08:08:30Z found each article active and
published at article v1 / zh-TW locale v6, with matching normalized draft,
published and latest source documents. Recheck these facts before release; this
task does not assert they remain current. Source snapshot:
`C:/Users/x8120/.codex/article-localization-release/batch019-candidate-inventory/live-source-full-20260923T080827Z.json`,
SHA256 `ecce8f28e22246ed54bfa4ee67f07cd3aea007ce57829a93447651e3ffe31032`.

The dependent content task records two independent body/image reviews and exact
twenty-file integration/test hashes. Persistent outside-Git evidence is under
`C:/Users/x8120/.codex/article-localization-release/batch019-digital-organization/`.
All sixteen documents and diagrams passed independent review with zero numeric
exceptions. Local validation passed while retaining 32 editorial advisories,
five PostgreSQL skips and one Windows/Bash tool-test skip. Those skips require
honest CI/release accounting and do not prove PostgreSQL execution.

No batch019 deployment, import/publication or public browser verification has
been completed or claimed by this task. This release task remains open/unclaimed.

Content PR: [#680](https://github.com/x812033727/travel_scanner/pull/680).
Required CI and merge are pending; recheck the exact final PR head before release.
