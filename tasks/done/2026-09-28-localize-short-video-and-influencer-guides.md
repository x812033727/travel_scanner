---
id: 2026-09-28-localize-short-video-and-influencer-guides
title: Localize short video and influencer guides in five languages (Batch037 Pair B)
status: done
priority: P1
area: docs
owner: codex-batch037-pair-b
claimed_at: 2026-09-28T10:58:13Z
created_at: 2026-09-28T10:58:04Z
completed_at: 2026-09-28T13:24:34Z
branch: codex/article-localization-037-social-b
depends_on: []
scope:
  - apps/api/app/guides/content/short-video-marketing.json
  - apps/api/app/guides/content/influencer-collaboration.json
  - apps/web/public/guides/short-video-marketing
  - apps/web/public/guides/influencer-collaboration
  - docs/article-localization/batch037-pair-b-evidence.md
  - tasks/open/2026-09-28-localize-short-video-and-influencer-guides.md
  - tasks/done/2026-09-28-localize-short-video-and-influencer-guides.md
---

# Localize short video and influencer guides in five languages (Batch037 Pair B)

## Why

These two public zh-TW life guides have no zh-CN, en, ja, or ko documents. Their
hero and diagram artwork also contains Chinese text. Batch037 Pair B supplies
complete, reviewable translations without changing the published originals.

## Definition of done

- [x] Both packs have complete, validated zh-CN, en, ja, and ko documents.
- [x] Both text-bearing images have localized SVGs and rendered hero covers for every target locale.
- [x] Source facts, publication-aware article links, responsive previews, and asset hashes are reviewed.
- [x] A scoped evidence record and draft PR are ready for editorial review; publication remains a separate gate.

## Steps

- [x] Recheck remote main, pinned repository hashes, task scopes, and live source under a guarded read-only transaction.
- [x] Translate and review all document fields and image text in four target locales.
- [x] Render and inspect all target artwork and article previews.
- [x] Run focused lint, tests, and task checks; seal content/asset hashes.
- [x] Open a draft PR after validation; attach the evidence record in the PR.

## How to verify

`uv run --project apps/api python -m app.guides.pack_cli lint --slug short-video-marketing --slug influencer-collaboration`, focused API tests, web checks, `npm run check:tasks`, and the scoped hash/layout audit recorded in `docs/article-localization/batch037-pair-b-evidence.md`.

## Notes

- Branch base and remote main were `5329ad8920300fec4fda06ded8bd006607a72d4f` on 2026-09-28; both pack and six source asset hashes match pinned inventory SHA-256 `3bea364352f11e97fe1af688426c7f9c7c8e6c64b94a7dd6b8e55c1c60cac01c`.
- Final review branch was rebased onto `origin/main` `5b35df86` after unrelated Batch035 translations landed; the two source packs and original images still match the pinned inventory.
- Fresh four-lock, repeatable-read, read-only production capture for all four Batch037 slugs passed at `2026-09-28T11:00:27Z`. External receipt: `<home>/.codex/article-localization-release/batch037-social-content-preflight-20260928/receipt-20260928T110024Z.json`, SHA-256 `575c4ec04629900421c106f6c58f81e3e6ce2ccd0a28f97b76515c59ad1ad669`; all source published hashes match, and no target locale rows exist.
- Eight localized documents retain the 33-block structures, four source URLs/check dates, and article target slugs. Twenty-four new locale assets are sealed in `docs/article-localization/batch037-pair-b-evidence.md` with browser layout reports: 16 art cases and 16 article desktop/mobile cases, zero issues.
- API content/link/ingest tests: 67 passed, 5 skipped. Targeted web renderer suites: 57 tests passed across an initial two-suite run and an isolated article-suite rerun; Windows worker-start timeouts prevented a clean combined invocation. Scoped pack lint, web typecheck, task check, and content/asset hash audit pass.
- PR [#914](https://github.com/x812033727/travel_scanner/pull/914) merged at `2026-09-28T12:09:44Z` as `c54594e488f48e3655566cc8a86d45e9dc2e004e`, with all nine GitHub checks successful, including API and Web CI. Its scoped implementation and evidence are in main.
- This task completed the repository translation and review work. It did not import, deploy, or publish the translations to production; any later release still needs a fresh live preflight and separate authorization.
