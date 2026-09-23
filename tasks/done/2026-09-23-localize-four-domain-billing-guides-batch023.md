---
id: 2026-09-23-localize-four-domain-billing-guides-batch023
title: Localize four domain billing guides batch023
status: done
priority: P2
area: api
owner: codex-batch023
claimed_at: 2026-09-23T14:05:15Z
created_at: 2026-09-23T14:05:12Z
completed_at: 2026-09-23T15:14:09Z
branch: codex/article-localization-batch023-domain-billing
depends_on: []
scope:
  - apps/api/app/guides/content/domain-hosting-renewal.json
  - apps/web/public/guides/domain-hosting-renewal
  - apps/api/app/guides/content/bluehost-domain-billing.json
  - apps/web/public/guides/bluehost-domain-billing
  - apps/api/app/guides/content/gandi-domain-management.json
  - apps/web/public/guides/gandi-domain-management
  - apps/api/app/guides/content/namecheap-domain-setup.json
  - apps/web/public/guides/namecheap-domain-setup
---

# Localize four domain billing guides batch023

## Why

The four domain and billing guides previously had only Traditional Chinese documents. Add complete English, Japanese, Korean and Simplified Chinese content and localized illustrations while preserving source documents, metadata and original assets.

## Definition of done

- [x] All four scoped packs contain five complete language documents; original zh-TW models and metadata are preserved.
- [x] Sixteen new documents and 48 localized assets received independent prose and visual review, with explicit image-description backfills and zero numeric guard exceptions.
- [x] Scoped local validation passed and a separate release task records actual CI, merge, canonical freeze, deployment, import, publication and public acceptance as unfinished work.
- [x] A reviewable content PR is opened and its URL is recorded here.

## Steps

- [x] Recheck full source baselines and 16 original file pins; inspect shared task, worktree and open-PR scope conflicts, then claim this exact scope.
- [x] Author 16 complete translations and 48 localized assets outside the repository, retaining source URLs, checked dates, audience and currency.
- [x] Independently review documents and renders before integrating exact approved artifacts.
- [x] Run scoped pack, localization, API, publication, frontend, tool, task, lint, type and build checks.
- [x] Create the separate unclaimed release task `2026-09-23-release-localized-domain-billing-guides-batch023`.
- [x] Open the content PR and record its actual URL; CI and production acceptance remain in the release task.

## How to verify

Use the exact integration, independent review and local-test receipts below. Validate final Git bytes against all 52 approved files and 12 original assets after syncing main. Actual CI/PostgreSQL, merge, frozen bundle and publication are separate release gates. Browser screenshots are not real-device acceptance.

## Content and local-validation evidence — 2026-09-23

- The four packs contain 20 full models: four unchanged source documents and 16 complete target documents, each with 27 blocks. Source counts by article are 4 / 4 / 4 / 3. Source baseline is article version 2 and zh-TW locale/published version 4.
- All 48 new assets are reviewed: 16 editable hero SVGs, 16 rendered 1600×900 hero JPGs and 16 diagram SVGs. All 12 original assets remain byte-identical. Text-bearing source heroes are preserved; credits remain Mokaair / © Mokaair.
- The existing canonical pipeline mechanically backfills 16 new-locale image descriptions from localized SVG desc text. The source descriptions remain unchanged. The exact ledger is preserved; zero numeric exceptions and zero route derivatives were introduced. Structured article-link identities remain unchanged and require actual same-language publication at release.
- `author-domain-bluehost/output-map.json` SHA256 `1469207608bfd221728e46e1be3c037db046460d16fcb3ee9dfccaa6744fa60c`.
- `author-gandi-namecheap/output-map.json` SHA256 `4430689fa8f61a9e410b2bc0d7bfb455439391b54d471e736d9eb793be4388ab`.
- `independent-domain-bluehost-review-v1/receipt-pass.json` SHA256 `77bc541e79d01d4a8171053203fbc699df224e7f33612c8e6df7023221a7ad37`.
- `independent-pair-b-review-v1/receipt-pass.json` SHA256 `fac773be4d9d589d6aa23042824e375b5d1d31237655222ef4746cc7f68f92f2`.
- Evidence root: `C:/Users/x8120/.codex/article-localization-release/batch023-domain-billing/`. Integration manifest `integration-candidate-v1/integration-manifest.json` SHA256 `76664a531730e6d1a8e5fa945fd680398cc0bae78aa98f4c2420d500766292c3`; independent integration receipt `500703376539c837d8117d90993951124c64d2fb5e7f0a12493465c78f4fbff5` binds all 52 files, 20 models, 12 originals and 1,220 strict reader fields. Actual apply receipt `b209f6fe97e6899c9e4c861ac18945b172e29f8e51a130b49cb83a7fed37a1b5`.
- Local `test-evidence/summary-pass.json` SHA256 `5be528a18e260c714703e8bf047bd988d1bae4accbd679b8dd2df1d64bbff8c6`: all 16 commands across seven groups passed in attempt v1. API 64 passed / 5 PostgreSQL skips; publication and assembly 83 passed / 59 PostgreSQL skips; web 333 passed across nine files; pipeline 32 passed; render 17 passed; tools 81 passed / one Windows Bash skip. Pack lint, i18n, web lint, build, typecheck, task and diff checks passed. No Batch023 failed or incomplete test attempts are omitted. Local skips require separately captured actual CI PostgreSQL results.
- All 24 nonfatal pack advisories are retained: 20 missing summary-block advisories preserve source structure; four English body-length advisories cover 6,495–6,866 characters against the 6,000-character guideline. Complete translations were not shortened to silence advisories.
- Completion here means reviewed content, local checks and an opened PR. Actual CI, merge, canonical freeze, backup/deployment, 16 draft imports, 16 publications, zero hubs, 20 public URLs and five-language desktop/mobile acceptance remain open in `2026-09-23-release-localized-domain-billing-guides-batch023`. No Batch022 production evidence is reused as Batch023 acceptance.

## Original source and ownership notes


Approved source snapshot: `batch023-candidate-inventory/replacement-v1/live-source-full-20260923T134051Z.json`, SHA256 `1a03bf97d598c023cadc4aa4a1e6192cec5c0b22d7bfbe4e0301e77fc78437d3`. All four source article versions are 2, zh-TW versions are 4, and each source is active/published with no draft divergence. Exact source bytes remain identical at main `0d0e872f3c86c521c50e9694d6abec6455f45a11`.

Approved claim manifest SHA256 `7e500a035d7ebc5c17d9308c584b9f56cffd875a5672d4d90fed27cdaacb6d4c`; source supplement `69b8f4d0296f486d00f1a5055f5b85e664e17b5df98e9cbefef222e2c00ed765`. Durable working evidence is outside Git under `C:/Users/x8120/.codex/article-localization-release/batch023-domain-billing/`.

Shared scope scan covered 189 registered worktrees and 12,710 open task records, with no active scoped claims, translated candidates or open-PR path conflicts. Initial strict HOLD is preserved: four historical P: checkout anomalies were read-only triaged as missing-index/incomplete or task-only sparse checkouts, with no selected candidate files. Supplemental proof SHA256 `3cecf8a61aeebf328e373469abd6a93adb697775dff5f1f5fc59e4c44d8cd7f8`; no ownership override, index repair or cleanup occurred.

Preserve original source facts and checked dates. Bluehost refund policy retrieval previously timed out, so no fresh verification is claimed. Related-article publication availability remains a release-time guard. Existing source corrections and other batches are outside this task.

## Actual PR handoff

- Content PR: https://github.com/x812033727/travel_scanner/pull/695, opened against main `ffa42476205f60e1e52c06f6600b51c9b26e572a` from reviewed content head `e76b08abb279b217303774b3bbe81a3dad91f557`. The exact 52 approved content bytes, 12 original assets, 20 models and 14 local-test dependency bytes were rechecked after merging known main. Task and diff checks passed.
- All nine actual CI checks started on the initial head; no CI success, merge, import, publication or public acceptance is claimed by this completion. Those gates remain unchecked in the separate release task.
- Final Git proof is recorded outside Git under `batch023-domain-billing/pr-handoff/`; the PR task-archive commit only records this completed content handoff.
