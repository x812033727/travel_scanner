---
id: 2026-09-27-record-batch030-five-language-wordpress-migration
title: Record Batch030 five-language WordPress migration release
status: review
priority: P2
area: docs
owner: codex-batch030-release-record
claimed_at: 2026-09-27T23:26:15Z
created_at: 2026-09-27T23:26:06Z
completed_at:
branch: codex/article-localization-030-release-record-docs
depends_on: []
scope:
  - docs/article-localization/releases/batch030
  - tasks/open/2026-09-27-record-batch030-five-language-wordpress-migration.md
  - tasks/done/2026-09-27-record-batch030-five-language-wordpress-migration.md
---

# Record Batch030 five-language WordPress migration release

## Why

Batch030 merged four WordPress migration guides and their five-language packs.
Two source-language inline links then required a narrowly scoped correction
before the 16 missing target locales could be published. The source correction,
target import, publication, and independent public QA need one durable record
that distinguishes each step from a merged content PR.

## Definition of done

- [x] Record the four-article, five-language content, draft, publication, and
      desktop/mobile browser results with pinned release evidence.
- [x] Record the source correction and both independently cleared production
      holds without conflating their receipts.
- [ ] Pass repository task checks and merge the release-record PR after CI.

## Steps

- [x] Claim an isolated release-record-only scope.
- [x] Recheck the preceding Batch029 release-record format.
- [x] Recheck the sealed source-correction and target-publication receipts.
- [x] Confirm final independent target QA and target hold-clear readback.
- [x] Write and review the release record; run checks.
- [x] Open the release-record PR.
- [ ] Merge after successful CI and release coordination.

## How to verify

`npm run check:tasks` and `git diff --check`; inspect the pinned publisher,
independent public/visual QA, and both hold-clear receipts. Confirm PR CI and
merge state separately.

## Notes

Source correction independently passed four-article/20-API/20-HTML checks,
with exactly two zh-TW inline links converted to plain text and no target
locales published at that step. The later 16-target publication has its own
verified backup, publisher journal, independent QA, and owned hold. Do not
reuse source-correction QA as target-publication proof.

Independent target visual QA initially found text overflow in all four
English `diagram-1` SVGs (`CHANGES_REQUIRED`, SHA-256 `e443a66161516aee76777196218a089a712ecec163bc2dd0eb9861497f07467d`).
PR #874 fixed the four assets, passed CI, merged and deployed. Fresh backup
transport SHA-256 `02bff69a0dab3607f2524ab729e5d499c237dce6253eb6d3140bd606d1f51db2`;
postdeploy independent QA PASS SHA-256 `df9ccb74b6c63c598127426c4916f82dee5104ffcde3cf9c00a63efb6d6763bc`.
Four-lock target hold-clear SHA-256 `2bbe87e598f1ba999318ca6f23b3f02df991db2c973e90c0b150678b12f7fa7c`;
independent post-clear readback SHA-256 `d83e40084ea20f54229f00694f784f8cafb5825f7f6641aedfbc64115998174c`.
The one-off target driver never produced a final verify success receipt: it
rejected only the three runtime-only public API metadata fields. The release
record preserves this limitation and its pinned refusal evidence.

Release-record PR #877 is open for review. Its merge remains a separate step;
the production publication and browser acceptance occurred before this
documentation PR.
