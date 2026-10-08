---
id: 2026-10-07-release-localized-design-web-life-wave5
title: Release localized design workflow life articles wave5
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-root-release
claimed_at: 2026-10-08T02:18:51Z
created_at: 2026-10-07T23:53:23Z
completed_at:
branch: codex/article-locales-wave5-release-20261008
depends_on:
  - 2026-10-07-localize-twelve-design-workflow-and-performance
scope:
  - docs/article-localization/releases/wave5-design-web-life-20261008
---

# Release localized design workflow life articles wave5

## Why

Twelve published life articles now include 48 new locale documents and four
approved source corrections. Normal merge/deployment, all nine durable release
phases and all 60 five-language desktop/mobile public pages are verified.
The owner explicitly approved merging PR #1378, normal deployment and publication
of this twelve-article cohort with its four source corrections on 2026-10-08.
The separate frozen PR #1374 and any future cohort are outside that choice.

## Definition of done

- [x] The approved content commit is merged with CI green at the exact current head.
- [x] Live code contains that commit; normal deployment and hold checks are verified.
- [x] Fresh production source/version guards, rehearsal and dry-run match this cohort.
- [x] Owner release choice and a readable, verified database backup precede writes.
- [x] All 48 new locales and four approved source updates complete durable phases.
- [x] Replay is unchanged and all 60 five-language pages pass desktop/mobile acceptance.
- [ ] Sanitized release evidence and final source/version hashes are committed.

## Steps

- [x] Check the exact content PR head, current CI and approved merge scope.
- [x] Check live HEAD, holds, release locks and publish_holds; use normal deployment.
- [x] Capture a fresh snapshot and rebind the reviewed bundle without changing content.
- [x] Rehearse with the deployed API image; dry-run and compare all expected operations.
- [x] Obtain the cohort choice, create pg_dump and verify its restore table of contents.
- [x] Run durable drafts, article publication and hub phases; preserve failures/holds.
- [x] Rebuild links, inspect selected locale findings and verify unchanged replay.
- [x] Verify document/media hashes, links, hreflang, sitemaps and desktop/mobile pages.
- [ ] Record results, clear only this release's owned hold and finish this task in its PR.

## How to verify

Follow article-localization, content-pipeline and deploy skills, and
`ops/release/README.md`. Use only these twelve slugs and en, ja, ko, zh-CN plus
the four explicitly approved source corrections. Record actual CLI exit codes,
durable phase outcomes and fresh five-language public responses; healthy services
or green CI alone do not establish publication. Do not use force/ignore-hold or
retry an uncertain provider/write request.

## Notes

Prepared manifest:
`58fe016c0fe00a1b3256fdf67a0718d2d6451ee9b90cc5feba1324d3eec28c01`.
All 48 genuine review pins:
`2c3d09dac1c51faa18698b400c3e35700129ddb467035c414db583701244a9a5`.
Actual local install/replay receipt:
`feb551e70b55ef01c407dfb24f5a5c040b2e5d8ac345f81fc34f32963674db16`.
Both official installer executions exited 0 with 164 operations and identical
full pack/asset/journal/backups/article-receipt captures. This does not publish.

The sanitized preparation record and exact cohort are in
`docs/article-localization/releases/wave5-design-web-life-20261008/README.md`.
Private baselines, DB guards, genuine reviews and full native inspection evidence
remain in the owner's persistent storage outside Git. Preserve original attempts,
the authoring CLI exit 1, the assembly wrapper topic-order failure and the
read-only finalization receipt. Eight unchanged sources retain their canonical
hashes; four source changes are exactly five approved inline objects with the
same visible words. All 36 original media files and original dates are unchanged.

This release is claimed by the Root operator. The separate frozen PR #1374 and
completed first 32 articles are not part of it.

Content draft PR #1378 passed 21 checks at its content commit
`7416a9ccbc83e5342319d47f0cf2e87bb9b4d160`, exact-head receipt SHA256
`dd4b1accd5189d63c27c77c0e280244d402da6a800482d4c02385acbb965bf4d`.
Recheck the current final head after its closing authoring-task commit; do not
use the content commit's CI receipt as proof for a different head. Local-only
installation and green CI remain separate from the owner's production choice.

The owner's concrete release choice bound the approved content head
`2150d414168a681b3598bf56eb985d74dda2201a`. An ordinary main integration merge
produced `f01faf630664e8bf1a6fac55511a3ef8ab8701e4`; all 162 approved changed
files remained byte-identical. Actual synchronization receipt SHA256:
`256d99930a567a6ffcf28766bddae8603dde3854aead7c1b867471d1760742b7`.
All 21 checks succeeded at that exact synchronized head; fresh CI receipt SHA256:
`c2d484fb5530a567a80965aa423d996c38924496c4f958fe3e4fc270e1e80c7d`.

PR #1378 was ordinarily squash-merged with that head pinned. Actual merged commit:
`bcba139a05e1ac6c3ce8a4e768086bf0d3b4a86f`; actual merge receipt SHA256:
`9fb7977b9ee9b39630503cd2a2db2171b27e78d25354e23be81354342cd274a3`.
The original gh ready invocation hit a TLS handshake timeout and its wrapper
exited 1. A fresh read proved the PR was still a draft. The same account's official
GitHub API then completed ready and normal SHA-bound squash operations, all curl
exits 0, with certificate verification and branch protection intact. Original
failure evidence remains; the first gh child exit was not separately persisted.

At 2026-10-08T03:06Z, the unchanged host preflight exited 0 with no deployment
hold, no staged activation and a free deployment lock. It found one running paid
video stage, created at 03:05Z, alongside three prior uncertain stages. The local
deployment guard stopped before starting any deployment (wrapper exit 1).
That observation preceded deployment. The running stage settled without
interruption before the fresh normal-deploy preflight; all later outcomes are
recorded below. No uncertain provider request or unrelated hold was retried.

Actual normal deployment and postdeploy verification both exited 0; deployed
commit is `bcba139a05e1ac6c3ce8a4e768086bf0d3b4a86f`. All 11 checks passed.
The local postdeploy formatter failure was preserved; only read-only verification
resumed, and deployment was not repeated. Deployment receipt SHA256:
`f31e8ee7c7ec26dd912af7e25b2f4f8b84385e12f8cbd2ff598880fabf0afced`.

A fresh complete production snapshot preserved all original rows. Only 350
unselected database-only news rows were projected out of the repository-backed
baseline; none lacked a published target locale. All 12 raw source/version guards
matched. The reviewed payload was rebound without changing reviews, attempts,
content or assets. Fresh manifest SHA256:
`7195c55422170f3eb76ce9856eeb3cad6d7082914a18190e821ba89ab94c80a0`.

All nine actual phase and capture SSH exits were 0. The consistent backup and
restored fixture covered 161 tables; source guards, all counts and four-phase
replay passed. Actual drafts/publications were 52/52/0 hubs, with no pending
operation. Production replay preserved selected data and write journals.

Actual public acceptance covered 60 pages, 120 original desktop/mobile views
personally reviewed by three reviewers, 180 exact media GET hashes and complete
sitemap coverage. Original PNGs, per-view identity/time/notes and failed local
checks remain preserved externally. No new editorial PASS or live scroll/click
interaction is asserted. Final QA SHA256:
`f81f0860ed79ab6e8ce5d068aa4066b0c6ea96df69328d700722779fb8ca807a`.
Acceptance SHA256 (actually transferred and independently rehashed on host):
`ce17b65521b2af129ff578cbcea7c718962b11bb81faf21d9d1a47883b1eb345`.
Actual completed driver state SHA256:
`15bf44e7e61de2e27735749676370280229e191c28c65b04063eb24e4de698ed`.
Its hold-clear result is `cleared`; only this release's owned hold was removed.

Link rebuilding materialized 3,768 links with zero dropped/unavailable and one
unresolved out-of-scope Gemini target already covered by the shared task queue.
All five global checks exited 1. This cohort had zero zh-TW findings; each added
locale retained 23 `unpublished` related-target findings and no other problems.
These existing target-language gaps remain in the overall localization work.

Independent preservation audit SHA256:
`ebaa1aa20f672fe0e0a4ca77164131434fd4b80c3af330348509cbcf7bdcce16`.
It verified all 60 new cohort documents, original 32/160 exact data and the frozen
13/52 still-unpublished cohort. Actual census SHA256:
`2c30ef4f1012cb46d6537ce85bef7e0ff38366a2589b69076383af2afdc2d217`:
1,409 scoped public articles, 818 incomplete and 3,272 missing locale documents.
The completion ledger CAS preserved all original rows/waves/choices/prepared
cohorts and archived the previous coverage observation; it records total 44
published articles and 176 newly published locale targets. No global completion.

Final actual published zh-TW source guards (all added locale guards and raw receipt
hashes are in the sanitized release evidence):

| Source slug | Published version | Normalized public SHA256 |
| --- | --- | --- |
| amp-website-decision | 6 | `7369c58003df56cc169d35efb05523c392cace876dddc1247daa5dfe250bbd40` |
| core-web-vitals-diagnosis | 4 | `79ea28908b8fc68573f202b0fdb0ade13029263a27073b88c9f672e01f925372` |
| figma-design-basics | 4 | `00bacd3467a6441febabc6372f10b96ce8a610784af66623d01684a467aee851` |
| lazy-loading-images | 6 | `2dda1061b6dd39fdfd06fe12b257d82ac92bfea46ded62ac0bddba6bb68bbde4` |
| lottie-web-animation | 4 | `56418ca1b26624eff12ed8efc540cf922391bba7d62e9b3ace31d959e3c85328` |
| open-graph-sharing | 6 | `8df97903caaae96f1792f04a3947d4a043991347ad5768051db0a110c5bc936f` |
| pagespeed-performance-review | 4 | `531a885101bc55e7c004988f19b64e818f219fbc9f2c2d7e1d843218b7666011` |
| rgb-cmyk-export | 4 | `f061761570269a8db0bf37b55c5eca0e809b4420f259032b72c359f5d8681ee4` |
| saas-paas-iaas-responsibility | 4 | `09bf76eb30950895f5c383381387442b5616522dee4d380d06cdb1f1ce35aaf2` |
| sass-scss-workflow | 4 | `37205fd94a9316f066553fb8b475a9577417a4372372d283fb1234edd4ff631f` |
| ui-ux-learning | 6 | `b01fb3630f90549698f89d9eac791dcc011b91e6b0e38069f0c9d8c1a6469411` |
| wireframe-prototype-testing | 4 | `74caa606d5c8265ef1d3494e690781b9db11ee3d442fc904c6ebc70c3d976b75` |
