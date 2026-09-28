---
id: 2026-09-28-localize-seo-keyword-and-title-guides
title: Localize SEO keyword and title guides
status: in-progress
priority: P2
area: docs
owner: codex-batch041-pair-a
claimed_at: 2026-09-28T14:07:19Z
created_at: 2026-09-28T14:06:26Z
completed_at:
branch: codex/article-localization-041-seo-a
depends_on: []
scope:
  - apps/api/app/guides/content/seo-keyword-research.json
  - apps/api/app/guides/content/seo-title-writing.json
  - apps/web/public/guides/seo-keyword-research
  - apps/web/public/guides/seo-title-writing
  - docs/article-localization/batch041-pair-a-evidence.md
---

# Localize SEO keyword and title guides

## Why

`seo-keyword-research` and `seo-title-writing` are published life guides with
only zh-TW content. Readers in zh-CN, English, Japanese and Korean lack the
full article and the text-bearing artwork. Complete these two guides from the
current published zh-TW version while keeping publication as a separate gate.

## Definition of done

- [x] Both packs include complete zh-TW, zh-CN, en, ja and ko documents with
      the same block structure, numbers, cautions, sources and relevant links.
- [x] Original zh-TW documents and pack metadata remain unchanged.
- [ ] Both text-bearing hero and diagram SVGs plus raster covers have four
      localized versions, with rendered desktop/mobile visual QA.
- [ ] Pack, content-link, asset, API/web, i18n and task checks pass; a reviewed
      PR is merged after green CI.
- [ ] Guarded import/publication and browser verification have separate receipts.

## Steps

- [x] Four-lock read-only production and repository inventory captured.
- [x] Claimed exact two-pack, two-asset-directory and evidence scope.
- [x] Translate all eight missing locale documents and independently compare
      root metadata and zh-TW against pinned sources; peer review is in progress.
- [x] Localized both text-bearing hero/diagram sets into four languages;
      Edge rendered all 16 SVGs with zero layout issues and exported eight JPGs.
- [ ] Validate, peer-review and open a focused PR.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug` for each pack,
guide content-link/API tests, relevant Web article tests, `npm run check:i18n`,
`npm run check:tasks`, and `git diff --check`. Compare parsed zh-TW and root
metadata to their pinned source, inspect each SVG/browser render, then review
the exact PR diff and CI. Import/publication checks remain separate.

## Notes

Read-only production receipt:
`C:\Users\x8120\.codex\article-localization-release\batch041-seo-readonly-inventory-20260928\receipt-20260928T134834Z.json`
SHA-256 `01da33a9f151c5472997a449408593b2b8f4e789dcef06b7f0f9084f1760bb99`.
It shows both life articles active/published v2, zh-TW draft/published v4
matching the repository, all four target locales absent, and no writes.
Candidate source/asset inventory SHA-256:
`a1d44c2eb60092af75ce09fe1f85f52805c4e6f635ff79d475dda23b3a4bc7b1`.

At main `fa28079a`, pack SHA-256 values are
`1384792649add24306aea80f76e274f2a837c9351661e846dba6f55c01e8f89d`
(keyword, 32 blocks/5 sources) and
`88f444c85c32953cfe54e99166e234029f6400a537d12f009166136e0624ab4f`
(title, 32 blocks/4 sources). Each has a text-bearing hero.svg and diagram-1.svg
plus a 1600×900 hero.jpg. Google Ads/Trends/Search Console interfaces and
metrics must be checked against the linked official sources before finalizing
translations. Internal article targets require locale publication checks.

Artwork render receipt SHA-256:
`cd7fe39256484f6ae95d0e6676d53a85b41e8bdab111490bfb4825422794f363`.
The independent 4×2 contact sheets were visually reviewed; desktop/mobile
article-page previews remain pending until the translated documents exist.

The combined keyword candidate outside the repository has SHA-256
`1dd67c76d9b9f8de1960a1628c01317846d250abfba9d1b7a9a38a32131ece74`,
audit receipt SHA-256
`fb708e39c978bafe216dca5090b22631c136b678a5728b3521cb6b93a2b68d58`.
The title candidate has SHA-256
`0696ef4e8c13f93e8b391dc6fb8b5f6a86470dfd7ee4f04ebe6375ba9dcb2450`;
its external audit and GuideDocument schema check passed. Both were installed
only after confirming exact source SHA, unchanged root metadata and unchanged
zh-TW. The resulting diffs add locale documents only. New-locale related
reading labels are translated plain text until the exact target locales are
public; they do not create premature public links.
