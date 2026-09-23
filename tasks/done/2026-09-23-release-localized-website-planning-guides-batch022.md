---
id: 2026-09-23-release-localized-website-planning-guides-batch022
title: Release localized website planning guides batch022
status: done
priority: P1
area: ops
owner: codex-batch022-release
claimed_at: 2026-09-23T14:03:17Z
created_at: 2026-09-23T13:47:27Z
completed_at: 2026-09-23T15:16:16Z
branch: codex/article-localization-022-release-record
depends_on:
  - 2026-09-23-localize-four-website-planning-guides-batch022
scope:
  - docs/article-localization/releases/batch022
---

# Release localized website planning guides batch022

## Why

The four reviewed website-planning ArticlePacks add16complete missing-language documents and48localized assets. Repository content completion does not import or publish those languages. Finish the guarded release against fresh exact source versions and preserve each article's actual visibility and existing editorial state.

## Definition of done

- [x] Actual content PR checks all pass at the reviewed head; record the merge target, exact tree, dependency applicability and actual PostgreSQL release-safety evidence.
- [x] Fresh read-only source and host snapshots match the reviewed scope, then a canonical bundle is independently reviewed and frozen with every input/document/render/hash pinned.
- [x] A verified fresh database backup and guarded deployment complete under the existing hostinger2 release protocol, with healthy services and no competing writes.
- [x] Exactly16missing-language drafts are imported and16article languages published, followed by the explicit0hub phase; all source models/metadata/visibility and12original assets remain protected.
- [x] Actual database/journal verification and five-language public/browser acceptance pass; release evidence is recorded and the owned hold is cleared only through final acceptance.

## Steps

- [x] Claim this release task in a separate release-record worktree and reconcile the actual content PR/CI/main/host versions.
- [x] Capture fresh full source rows for cloudways-wordpress-setup, website-budget-worksheet, wordpress-com-org-choice and wordpress-first-site. Prior baseline article2/zh-TW4 must not be assumed current; halt and reconcile any source, draft, visibility or version difference.
- [x] Assemble20full locale models from the16reviewed target documents and4unchanged source documents. Bind all48new assets and12original assets, independent content/render reviews, actual local logs and actual CI/dependency proof. Freeze only after complete independent review.
- [x] Prepare an explicit4article/16locale allowlist: en,ja,ko,zh-CN for each article; no hubs and no source-locale rewrite. Pin target/config/manifest/backup/driver and preserve durable journal/phase receipts.
- [x] Verify fresh pg_dump custom-format backup using pg_restore --list, acquire the existing competition locks/owned hold, deploy through hostinger2 and check target revision/service health.
- [x] Run the exact import dry-run; confirm changes are limited to missing locales and required image references. Import16drafts, publish16article locales, then execute0hubs. Preserve withdrawn/hidden/expired states and stop on concurrent edits.
- [x] Verify20full database models, preserved source versions and metadata, exact16draft+16publish journal operations, authorized actor, seals, no pending operations and idempotent scope.
- [x] Check20public language URLs and all40desktop/mobile cases, capturing80top/diagram PNGs. Verify full body, image geometry/readability, canonical, reciprocal hreflang, same-language links and all sitemap pages/XML completeness.
- [x] Hash and validate all60asset files (48new+12original); inspect allused hero/diagram assets and source/credit/expanded descriptions. Each target image.description is the recorded canonical SVG-desc backfill, not an invented paragraph.
- [x] Independently review actual final evidence, stage acceptance, clear only this release's owned hold, and record the release receipt and remaining follow-ups under docs/article-localization/releases/batch022.

## How to verify

Use ArticlePack/GuideDocument and the existing canonical assembler, publisher, durable phase driver and hostinger2 protocol. Preserve real before/after snapshots, phase receipts, sealed publication journal, CI job/log/dependency identities and actual desktop/mobile browser captures. Local skipped PostgreSQL checks are not a CI pass; HTTP200 alone is not publication or content proof. Check each structured related target against actual same-language publication; unavailable targets remain unclickable. Do not infer global draft safety beyond the explicit checked scope.

## Notes

- Content dependency:2026-09-23-localize-four-website-planning-guides-batch022. This release was completed separately from the content PR; the actual accepted evidence and post-clear state are recorded below.
- Exact articles:cloudways-wordpress-setup;website-budget-worksheet;wordpress-com-org-choice;wordpress-first-site. Source baseline:article2/zh-TW4; target count16,full models20,new assets48,original assets12,total assets60,public URLs20,desktop/mobile cases40,expected PNGs80,hubs0.
- Outside evidence:C:/Users/x8120/.codex/article-localization-release/batch022-website-basics/. Integration manifest SHA256 bf547264c73f6568f185c42fb84f37a966f836db0e151acc6de3cbb20a6c77f1; independent integration review90235c260448f38c518ff3ea0119a1b3175b410a5b8a7c18d775fb6eb96fe010; apply receipt0c8dda7e17db8593e82a27b0417fd74a3f2f93d2f80e51e511fd795ae31fef06; local summaryd4c6a3a05558e7ad867cd098958f79cbd2ed0b43a2a9f5d7086d4fc6802170bf.
- Existing local limits:64PostgreSQL skips total,1WindowsBash skip,24nonfatal pack advisories; first Vitest worker timeout retained and complete333-test retry passed. CI and release evidence must state their own actual results.
- The original2026-09-14source check dates and Mokaair/©Mokaair licensing remain unchanged. Preserve original audience and all source metadata. Original plaintext/source models are never silently retranslated.

## Completed release evidence

- Content PR #692 was already merged when this executor resumed. Nine checks passed for content head 25da625679a5b1f10a46cce69e07b918c2d2befe; its full Git tree equals deployed revision 32f032b161534328f95366010fda1722397ae10c. This executor did not merge the content PR.
- Canonical freeze: batch022-offline-release-25da6256.zip SHA256 265b5c952598ff420085e9a69a567582b6b8b0c30d6705bab2f1d15dcc167ad9, 504 files. The independently reviewed actual PostgreSQL CI evidence, frozen documents, assets and dependency identities remain in the outside evidence archive.
- Fresh custom-format backup and pg_restore --list, guarded deployment, explicit dry run, 16 draft imports, 16 article publications and 0 hub publications completed. All 20 full database models passed; original article version 2, zh-TW version 4, complete source rows, metadata and 12 original images remain unchanged.
- Final sealed publisher journal SHA256 6d1c11a347e497df82d83409504d4fda2e414d2066a4a6ef2d60ff29da85e81e contains exactly 32 committed operations, no pending operation and no duplicate publication. This sealed journal must not be modified by another verify invocation.
- Public acceptance checked 20 language URLs, 40 desktop/mobile viewport cases, 80 independently viewed PNGs, 20 expanded-description/source cases, full body and heading text, all 60 exact image bytes, canonical, reciprocal hreflang and conditional same-language article links. Sitemap API pages [1000, 984] contain 1,984 unique rows, all covered by XML. Viewport evidence is not physical-device or site-wide draft-visibility acceptance.
- Final evidence SHA256 7cf5104ef7cd7eabb7dcb350b911c6cc5872da36be4d35662b13a5c8944bd2f9; final acceptance ccaa68fb0c68353dc5b24c83bbc7ed18e9cefe215071cbebd96940dbaafc7665. Successful owned hold clear local receipt 23869f2b5e53d67e5d5f40b1caa0f752a71161be299a5726dd77bbb4a2bdca71. Post-clear snapshot 899eea0709327de318e1903fda60bd5af281c1c581790e6eaf2bd0259f0762db confirms exact clean host revision, no hold, no foreign pending releases and healthy services.
- The repository record is docs/article-localization/releases/batch022/{README.md,evidence.json}. Its generated Windows-local JSON SHA256 is a6ad90d4a6dcb9cf144db9b303b444489c7f3555164f9ee870a9a6775ab68d64; Git normalizes line endings and its separate blob hash is recorded in the outside root review.
- The existing desktop global-search placeholder/icon finding is tracked by its existing task. Other article source corrections and later translation batches are outside this completed release.
- One record-writer invocation supplied a malformed acceptance hash and correctly stopped before any repository write; the corrected invocation validated the immutable actual acceptance and produced these records. No host action or evidence file changed in that rejected invocation.
