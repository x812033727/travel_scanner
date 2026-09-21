---
id: 2026-09-21-taiwan-zh-tw-batch-007-tax
title: Taiwan zh-TW batch 007: tax refund and etiquette
status: in-progress
priority: P2
area: docs
owner: codex-taiwan-zh-tw-batch007
claimed_at: 2026-09-21T17:38:07Z
created_at: 2026-09-21T17:38:00Z
completed_at:
branch: codex/taiwan-zh-tw-batch-007
depends_on: []
scope:
  - apps/api/app/guides/content/taiwan-tax-refund-shopping-2026.json
  - apps/api/app/guides/content/taiwan-etiquette-safety-tips.json
  - apps/web/public/guides/taiwan-tax-refund-shopping-2026/diagram-1-zh-tw.svg
  - apps/web/public/guides/taiwan-etiquette-safety-tips/diagram-1-zh-tw.svg
---

# Taiwan zh-TW batch 007: tax refund and etiquette

## Why

The next two published Taiwan guides in the original launch order that still
lack Traditional Chinese are the shopping tax-refund guide and the etiquette
and safety guide. Add complete `zh-TW` documents and localized diagrams while
preserving all existing locales, top-level metadata, visibility, provenance,
and photo licensing.

## Definition of done

- [ ] Both guides have complete native-quality `zh-TW` documents with the
  live source field/block structure.
- [ ] Both text-bearing diagrams have dedicated Traditional Chinese SVGs whose
  wording and numbers match the documents.
- [ ] Tax eligibility, thresholds, fees, export timing, fines, emergency
  procedures, and reader scope are current and backed by reader-visible
  official sources.
- [ ] Independent review reports no unresolved blocker or major finding, and
  focused checks plus desktop/mobile renders pass.

## Steps

- [x] Confirm production publishes `en`, `ja`, `ko`, and `zh-CN` but
  reports `zh-TW` as unpublished for both exact slugs.
- [ ] Recheck official sources and write both complete Traditional Chinese
  documents without changing the existing locales or pack metadata.
- [ ] Create and inspect the localized SVGs at 1600x900 and 390x219.
- [ ] Resolve independent-review findings and complete focused validation.
- [ ] Keep the branch clean without opening a PR until batch006 PR #627
  merges; then rebase onto the new exact `origin/main`, prove content hashes
  unchanged, complete this task, and open a non-draft PR.

## How to verify

```text
cd apps/api
uv run pytest tests/test_guides_pack_ingest.py tests/test_guide_rich_blocks.py tests/test_guides_content_pack.py
cd ../..
npm run test:tools
npm run check:tasks
git diff --check
```

Run scoped `pack_cli lint`, target-only schema/field/number/source checks,
verify existing-locale and top-level hashes against the pinned base, and
inspect both SVGs at desktop and 390px widths.

## Notes

- Fresh sparse worktree and branch started from
  `d390cc5da44185e546668c8fd8bce412c34d5b79`. Sparse checkout avoids the
  repository's large historical browser-evidence directory after a full
  checkout exhausted the remaining disk space.
- Original launch order places `taiwan-convenience-store-guide` immediately
  after batch006, but that guide already has a public `zh-TW` document. The
  next two missing locales are `taiwan-tax-refund-shopping-2026` and
  `taiwan-etiquette-safety-tips`.
- Read-only public API checks on 2026-09-22 returned published documents for
  `en`, `ja`, `ko`, and `zh-CN`, and unpublished with no document for
  `zh-TW` on both slugs.
- Draft validation: both target `pack_cli lint` commands completed with no errors (only the pre-existing no-summary warning shared by every locale); the target-only schema, live block-type parity, top-level/existing-locale semantic hashes, image credit, SVG description, number, date, and link checks pass.
- Focused API result: 49 passed, 7 skipped, 2 global asset tests deselected. Running those two in this sparse checkout reports only unrelated missing asset directories; both target packs and all six referenced target assets are present and validated.
- `npm run test:tools` passed in the complete batch005 worktree (75 passed, 1 skipped); `npm run check:tasks` and `git diff --check` pass here. Both diagrams were inspected at 1600x900 and responsive 390x219.
- Current official-source review corrected two stale source-locale claims: some heated-tobacco products have been approved since 2025, while e-cigarette use and unapproved heated tobacco remain prohibited; natural-disaster closure notices use the current 19:00-22:00 / 04:30 / 10:30 windows.
- Independent review remains pending because every subagent slot is occupied. PR #627 is still open; no batch007 PR will be created before it merges.
