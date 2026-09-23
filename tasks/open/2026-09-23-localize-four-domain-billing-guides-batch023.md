---
id: 2026-09-23-localize-four-domain-billing-guides-batch023
title: Localize four domain billing guides batch023
status: in-progress
priority: P2
area: api
owner: codex-batch023
claimed_at: 2026-09-23T14:05:15Z
created_at: 2026-09-23T14:05:12Z
completed_at:
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

The four published domain and billing guides currently provide only Traditional Chinese. Add complete English, Japanese, Korean and Simplified Chinese documents and language-specific text-bearing illustrations while preserving the published source, metadata and original assets.

## Definition of done

- [ ] All four scoped packs contain five complete language documents; the original zh-TW model and metadata are preserved.
- [ ] Sixteen new documents and 48 localized assets receive independent prose and visual review, with explicit image-description backfill evidence and zero numeric guard exceptions.
- [ ] Scoped local checks and PR CI pass before merge; deployment, import, publication and actual public browser acceptance are recorded separately.
- [ ] Only the approved missing locales are imported/published, with current source versions and visibility rechecked before release.

## Steps

- [x] Recheck four live-source baselines and 16 original file pins against known main; inspect shared task, worktree and open-PR scope conflicts.
- [x] Create an isolated worktree and claim this exact four-pack/four-asset-directory scope.
- [ ] Author 16 complete translations and 48 localized assets outside the repository, retaining source URLs, checked dates, audience and currency.
- [ ] Obtain independent document and image review before integrating exact approved artifacts.
- [ ] Run scoped pack, localization, API, frontend, task, lint, type and build checks and open a batch PR.
- [ ] Complete guarded deployment, import preview, publication and five-language desktop/mobile public acceptance.

## How to verify

Use `tools/article-localization` baseline/strict-field/materialization/render checks, scoped `pack_cli lint`, relevant API/publication/frontend tests, `npm run test:tools`, `npm run check:tasks`, i18n, lint, typecheck and build. Release acceptance must separately bind source/article versions, exact target/CI/backup, import preview and publication results, all target-language bodies/assets/links, canonical/hreflang and complete sitemap pages. Headless screenshots do not establish real-device acceptance.

## Notes

Approved source snapshot: `batch023-candidate-inventory/replacement-v1/live-source-full-20260923T134051Z.json`, SHA256 `1a03bf97d598c023cadc4aa4a1e6192cec5c0b22d7bfbe4e0301e77fc78437d3`. All four source article versions are 2, zh-TW versions are 4, and each source is active/published with no draft divergence. Exact source bytes remain identical at main `0d0e872f3c86c521c50e9694d6abec6455f45a11`.

Approved claim manifest SHA256 `7e500a035d7ebc5c17d9308c584b9f56cffd875a5672d4d90fed27cdaacb6d4c`; source supplement `69b8f4d0296f486d00f1a5055f5b85e664e17b5df98e9cbefef222e2c00ed765`. Durable working evidence is outside Git under `C:/Users/x8120/.codex/article-localization-release/batch023-domain-billing/`.

Shared scope scan covered 189 registered worktrees and 12,710 open task records, with no active scoped claims, translated candidates or open-PR path conflicts. Initial strict HOLD is preserved: four historical P: checkout anomalies were read-only triaged as missing-index/incomplete or task-only sparse checkouts, with no selected candidate files. Supplemental proof SHA256 `3cecf8a61aeebf328e373469abd6a93adb697775dff5f1f5fc59e4c44d8cd7f8`; no ownership override, index repair or cleanup occurred.

Preserve original source facts and checked dates. Bluehost refund policy retrieval previously timed out, so no fresh verification is claimed. Related-article publication availability remains a release-time guard. Existing source corrections and other batches are outside this task.
