---
id: 2026-09-23-release-localized-digital-organization-guides-batch019
title: Release localized digital organization guides batch019
status: done
priority: P1
area: ops
owner: codex-batch019-release
claimed_at: 2026-09-23T09:28:46Z
created_at: 2026-09-23T09:06:20Z
completed_at: 2026-09-23T10:30:26Z
branch: codex/article-localization-019-release-record
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

- [x] Exact content PR head passes required CI and is reviewed and merged; obtain
      applicable PostgreSQL release-safety evidence for the exact dependencies.
- [x] Fresh live source/visibility/version inventory permits exactly the missing
      language operations below; preserve any later editing or visibility changes.
- [x] Assemble and independently review the canonical bundle with exact source,
      tool, document, image and final Git hashes; freeze the portable artifact.
- [x] Verify a fresh database backup and hold/locking ownership, deploy the reviewed
      necessary files through the existing hostinger2 workflow, and check health.
- [x] Dry-run and idempotent import/publication change only the sixteen explicitly
      listed missing-language targets, retaining all original zh-TW rows/metadata.
- [x] All twenty five-language pages pass full-body/image/canonical/hreflang/link
      checks and desktop/mobile visual review; the explicit release scope excludes
      every unrelated draft publication (no site-wide privacy audit is claimed).
- [x] Record per-article content/import/publication/browser results, final journals
      and actual database acceptance; clear only the owned hold after acceptance.

## Steps

- [x] Review final content Git export, PR and exact-head CI evidence.
- [x] Refresh source inventory and freeze the approved canonical bundle.
- [x] Run backup/deploy/dry-run/import/publication through the explicit-list tools.
- [x] Complete database and browser acceptance and record the release evidence.

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

At the initial claim, no batch019 production action had completed. The dated
closing record below supersedes that initial preparation checkpoint.

Content PR: [#680](https://github.com/x812033727/travel_scanner/pull/680).
Required CI and merge are pending; recheck the exact final PR head before release.

### 2026-09-23 fresh release preparation

Root claimed this release separately from the completed content-authoring task.
At 09:28 UTC a fresh read-only production export confirmed all four complete
article and source-locale rows are identical to the independently reviewed
08:08 snapshot. No target locales have been created. New snapshot:
`batch019-digital-organization/live-source-full-20260923T092820Z.json`, SHA256
`123b135609fd189752ba5c228b7d91bbd156a5ce78f578d68eebb69e5de7c1c1`.

The exact content PR head remains 2d0beedc53254ae34e22762cdc1ed10e93c6badd.
Seven of eight CI checks have passed; API is still running at this note. No
merge, production write or final release acceptance is claimed yet.

At 09:39 UTC all eight checks passed at exact PR head 2d0beedc, and PR #680
merged as e21d8d29833eacd830da25b00307f017b4f76fa6. The tested head and
merged commit have identical complete Git trees. The clean content worktree
remains at 2d0beedc for offline canonical bundle assembly; this release worktree
retains the task claim separately. Canonical assembly and independent freeze
review are in progress; no batch019 production mutation has run.

Exact CI receipt: batch019-digital-organization/pr680-green-exact-2d0beedc.json,
SHA256 ce5ee165c12d9077275a4179b13d5e24caf2c52daa15dc4bb9f65f816aec2dab.
Merge receipt: batch019-digital-organization/pr680-merge.json,
SHA256 84552eb747198b94fdab2d796be5e04786e153c0ec60491a474f1122cf5d482d.


2026-09-23 10:15 UTC release checkpoint: exact reviewed target
 e21d8d29833eacd830da25b00307f017b4f76fa6 was deployed after a fresh
pg_dump custom-format backup passed pg_restore --list. The successful dry run
selected exactly sixteen missing-language starts and sixteen article publications,
with zero hub publications. Draft creation, article publication, empty hub phase
and one final host verification completed. Do not rerun host verification after
accepting journal 431d2b67ad24211d68d68a5b3640da5c23fe65cd7fc6749b316a4a9b49182639.

Actual database and sealed-journal acceptance passed independently: all twenty
normalized models match, all sixteen new locales are published at v2, and all
four source zh-TW v6 rows and parent article v1 metadata remain unchanged.
Twenty-four public image hashes match (sixteen new SVGs, eight preserved originals).
Public desktop/mobile body/SEO/link/sitemap checks and actual screenshot reviews
are in progress. Owned release hold remains active until full public acceptance.

Private evidence archive: mokaair-localization-019-e21d8d29833e/.
- database-acceptance.json: 69dbe228f458d1931e96c93cf520483981fd6760ce3cdc7c449ce2d313d97ac5
- independent-database-journal-acceptance.json: d8e136f135b27f93d50fbf0b615e1f8c79da2392ec7a779a5a12a5fe20883968
- host-capture/capture.json: 8982c0f98acd9c342d7e49d334f827c543b1751e74222628eb3eef642ca5aead
- public-assets-all24.json: 465eaf59c758be95761658da07471a7da8802e7d66733f53fb8ed8ca2fcc2a3f


## Completed release acceptance — 2026-09-23 10:28 UTC

The reviewed content PR680 was merged at e21d8d29833eacd830da25b00307f017b4f76fa6.
All four articles now provide five public languages. Actual acceptance covers
20 complete normalized models,16 new published-v2 locales,4 unchanged zh-TW-v6
full rows,4 unchanged article-v1 metadata rows,32 sealed commits,0 hubs,24 public
asset-byte matches,40 public page cases,20 expanded-description/source cases and
80 individually viewed original screenshots. The complete sitemap has1000+944
unique API entries, all1944 covered by XML. No publisher verification was rerun
after the accepted final journal was pinned.

Applicable PostgreSQL release-safety evidence was bound by byte identity of766
runtime/tool/workflow dependency files in the canonical wrapper; historical119
SQLite/PostgreSQL cases and66 subtests are distinct from the new wrapper's115
passed/59 PostgreSQL-skipped/25-subtest local run. No local PostgreSQL execution
is claimed. The explicit publisher phases preserve all unrelated articles/drafts;
this does not claim a full-site privacy audit.

Final evidence: mokaair-localization-019-e21d8d29833e/final-evidence.json,
SHA4718d740337ea5018734712904600ac3244ca7f252d39b3471fe6d5502663643.
Acceptance:39bf8f1051cec4e946e23ab70a28bcdb876035040adead5ebf7f9403107dc829.
The owned hold was successfully cleared at10:28 UTC after staging acceptance;
post-clear snapshot9146e91aded80e85e09963079adee9a2e062da1c4cef8ca6ec6868e5dbb0ffa3
confirms clean deployed e21d8d29, no hold and three healthy endpoints.

Repository delivery: docs/article-localization/releases/batch019/README.md and
evidence.json separate per-article content/import/publication/browser states and
all20 public URLs. They deliberately omit private actor/database identities.
Only existing desktop search placeholder/icon overlap remains recorded in its
separate task. Desktop/mobile means browser viewports; mobile diagram screenshots
cover the center pan, with full SVG labels also reviewed in desktop/local renders.
