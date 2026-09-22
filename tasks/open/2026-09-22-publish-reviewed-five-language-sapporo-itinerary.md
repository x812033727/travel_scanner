---
id: 2026-09-22-publish-reviewed-five-language-sapporo-itinerary
title: Prepare reviewed five-language Sapporo itinerary PR
status: in-progress
priority: P1
area: docs
owner: codex-batch012-draft
claimed_at: 2026-09-22T01:55:51Z
created_at: 2026-09-22T01:55:46Z
completed_at:
branch: codex/article-localization-batch012-sapporo-pr
depends_on: []
scope:
  - apps/api/app/guides/content/sapporo-3-day-itinerary.json
  - apps/web/public/guides/sapporo-3-day-itinerary
---

# Prepare reviewed five-language Sapporo itinerary PR

## Why

The public Sapporo three-day guide only has a zh-TW document. The reviewed candidate adds full en, ja, ko, and zh-CN documents plus text-bearing route diagrams, and corrects the zh-TW source's premature promise of specific 2027 Tsudome attractions. The existing article slug, photos, credits, source URLs, and visibility remain unchanged. This task prepares a reviewable PR only; production source revision and locale publication require later approval and live version checks.

## Definition of done

- [ ] A narrow PR contains only this guide pack, four localized SVGs, and this task record, with full independent editorial approval tied to exact hashes.
- [ ] Scoped tests and required CI pass; the PR description distinguishes repository content from live publication.

## Steps

- [x] Start from freshly fetched main `d52af4d95a40f5e353c567d366ee1b2b69dc5696` and claim the two-path scope.
- [x] Verify the independent receipt and copy only the reviewed Sapporo pack and four SVGs byte for byte.
- [x] Run scoped lint/tests, task check, and review diff.
- [ ] Open PR, verify all CI, and mark task `review`.

## How to verify

Run `python -m app.guides.pack_cli lint --slug sapporo-3-day-itinerary` from `apps/api`, the focused guide content/link tests, `npm run check:tasks`, `git diff --check`, and GitHub CI. Compare pack and all four SVG file SHA-256 values to `C:\Users\x8120\.codex\article-localization-release\batch012-selection\sapporo-final-full-review\receipt.json`. Verify the only normalized zh-TW source delta from the published v4 snapshot is `/blocks/22/text` and the new four locales have 30 blocks and 13 sources each.

## Notes

- Independent full review receipt SHA-256 `58de5ef025f5696d28bfd4bfe3f529e78f79221ecb9046f84d563b74d47de5d1` has disposition PASS for exact pack SHA-256 `050d862073cf13a3c8b3523bdd759a5da24e975136bd0e0c549e99b07d3491e1`. The four reviewed SVG hashes are recorded in the receipt.
- Independent source-only approval receipt SHA-256 `dbfc14b23d5d0768ada22757cc6663a66472d11b902eda28a84889515c6c665e` approves the one-pointer Tsudome correction. The previously published zh-TW normalized document is `9e332a1838281c3c50bc32fdf5d6ad81674ae163b47764355bdfc9843168b2a3` at article v2, locale/published v4. The reviewed local zh-TW candidate is `2777a791e06871e0fe191c46fe7ceb5620c223c4e31ef4dbf96ed491c34c5806`; a production write must recheck version/hash and create a guarded revision.
- The Sapporo-only clean worktree was created from current main after PR #635 merged. Otaru is excluded because its separate candidate still has review blockers.
- Verified the final full-review receipt file hash and exact candidate pack, all five normalized GuideDocument hashes, and four SVG hashes. The only normalized zh-TW delta from main/published v4 is `/blocks/22/text`.
- Scoped pack lint exited 0. It reports inherited `no_summary` warnings and the full English body over the howto length guideline, with no errors. Focused guide content/link tests: 12 passed, 5 skipped. `npm run check:tasks` passed (668 files); `git diff --check` passed.
