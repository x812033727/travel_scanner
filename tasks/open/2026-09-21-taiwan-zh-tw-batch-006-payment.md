---
id: 2026-09-21-taiwan-zh-tw-batch-006-payment
title: Taiwan zh-TW batch 006: payment and food
status: in-progress
priority: P2
area: docs
owner: codex-taiwan-zh-tw-batch006
claimed_at: 2026-09-21T17:03:05Z
created_at: 2026-09-21T17:02:57Z
completed_at:
branch: codex/taiwan-zh-tw-batch-006
depends_on: []
scope:
  - apps/api/app/guides/content/taiwan-payment-easycard-cash-cards.json
  - apps/api/app/guides/content/taiwan-food-guide-must-eat.json
  - apps/web/public/guides/taiwan-payment-easycard-cash-cards/diagram-1-zh-tw.svg
  - apps/web/public/guides/taiwan-food-guide-must-eat/diagram-1-zh-tw.svg
---

# Taiwan zh-TW batch 006: payment and food

## Why

The next two published Taiwan guides in the original launch order that still
lack Traditional Chinese are the payment/EasyCard guide and the food/ordering
guide. Add complete `zh-TW` documents and localized diagrams while preserving
the four existing locales, top-level metadata, visibility, provenance, and
photo licensing.

## Definition of done

- [x] Both published guides have complete native-quality `zh-TW`
  `GuideDocument`s with the same field and block structure as the live source.
- [x] Both text-bearing diagrams have dedicated Traditional Chinese SVGs whose
  wording and numbers match the corresponding documents.
- [x] Current prices, limits, payment acceptance, lottery rules, dietary labels,
  and tourist-facing procedures are supported by reader-visible official sources.
- [x] An independent reviewer reports no unresolved blocker or major finding,
  and all focused checks and desktop/mobile renders pass.

## Steps

- [x] Confirm the two guides are published in `en`, `ja`, `ko`, and `zh-CN`
  while the public API reports `zh-TW` as unpublished.
- [x] Recheck official sources and write the two complete Traditional Chinese
  documents without changing existing locales or pack metadata.
- [x] Create and inspect the localized SVGs at 1600x900 and 390x219.
- [x] Resolve independent-review findings and complete the focused validation.
- [ ] Keep the branch ready without opening a PR until batch005 PR #626 merges;
  then rebase onto the new `origin/main` and prove content hashes are unchanged.

## How to verify

```text
cd apps/api
uv run pytest tests/test_guides_pack_ingest.py tests/test_guide_rich_blocks.py tests/test_guides_content_pack.py
cd ../..
npm run test:tools
npm run check:tasks
git diff --check
```

Run scoped `pack_cli lint`, target-only schema/field/number/source checks, verify
existing-locale and top-level hashes against the pinned base, and inspect both
SVGs at desktop and 390px widths.

## Notes

- Fresh worktree and branch started from
  `f33005805c031ba2dad6d7c2268760f6f67dbc97`.
- Original launch order places `taiwan-hsr-tra-ticket-guide` immediately after
  batch005, but that guide already has `zh-TW`. The next two missing locales are
  `taiwan-payment-easycard-cash-cards` and `taiwan-food-guide-must-eat`.
- Read-only public API checks on 2026-09-22 returned `published` documents for
  `en`, `ja`, `ko`, and `zh-CN`, and `unpublished` with no document for `zh-TW`
  on both slugs.
- Both new documents validate against `GuideDocument`; their block type
  sequences and block field sets match the live `zh-CN` source documents.
  Top-level and all four existing-locale canonical hashes match the pinned
  base. Scoped pack lint has no errors.
- Chrome renders at 1600x900 and 390x219 were visually inspected with no
  clipping, overlap, or missing glyphs. Both SVG descriptions exactly match the
  corresponding image blocks and every drawn number occurs in the article.
- Focused API tests passed (51 passed, 7 skipped), `npm run test:tools` passed
  (75 passed, 1 skipped), `npm run check:tasks` passed with unrelated stale
  queue warnings, and `git diff --check` passed.
- Independent fact/content review initially found mismatched hero alt text,
  unsupported food-price ranges, an ambiguous stamp-tax sentence, two SVG
  wording issues, and missing lottery-range parity. All were corrected. The
  final re-review reports 0 blocker, 0 major, and 0 minor.
