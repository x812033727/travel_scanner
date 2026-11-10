---
id: 2026-11-10-life-hub-reader-discovery
title: Make news and useful knowledge easier to discover on the life hub
status: done
priority: P1
area: web
owner: codex-layout-review-discovery
claimed_at: 2026-11-10T13:37:32Z
created_at: 2026-11-10T13:37:30Z
completed_at: 2026-11-10T13:57:23Z
branch: codex/mokaair-news-discovery-20261110
depends_on: []
scope:
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/components/guides/life-discovery.tsx
  - apps/web/components/guides/life-discovery.test.tsx
  - apps/web/components/guides/news-list.tsx
  - apps/web/components/guides/news-list.test.tsx
  - apps/web/lib/life-discovery.ts
  - apps/web/lib/life-discovery.test.ts
  - apps/web/lib/life-discovery-messages
---

# Make news and useful knowledge easier to discover on the life hub

## Why

The unfiltered life hub puts twenty news stories ahead of its topics and practical reading. Readers looking for useful knowledge must pass a long, often specialized news list before discovering the rest of the existing collection.

## Definition of done

- [x] The first page shows six latest stories and a native disclosure for the remaining stories, preserving the existing twenty-story chronology.
- [x] Readers can jump to news or up to three existing non-news knowledge articles, without duplicate cards in the remaining listing.
- [x] Five-language copy, filtered/cursor behavior, Gemini visibility, empty/failure semantics and pagination remain correct in focused unit checks.
- [x] Focused checks and independent review/browser verification pass before handoff.

## Steps

- [x] Audit task scopes, local/remote branches, worktrees, open PRs and main path history; claim the narrow scope.
- [x] Implement first-page discovery using existing fetched article fields and independent locale catalogs.
- [x] Run focused unit tests and lint; hand off for root's independent review and browser validation.

## How to verify

Run the life page, life-discovery helper/component and NewsList Vitest files; run scoped ESLint and TypeScript. Verify native details opens with JavaScript disabled, the remaining ordered list starts at seven, keyboard jump targets exist, first-page cards are not repeated, and filtered/cursor views keep their former shape.

## Notes

- Started on codex/mokaair-news-discovery-20261110 atop e0f251680. Root explicitly created this branch so PR #2061 remains fixed while this approved continuation is prepared.
- Exact path audit found only the unowned, blocked 2026-09-14-codex-learning-series ticket on life page/tests; it is not an active claim and its existing behavior is preserved. The earlier layout task is done. Open-PR scope matches only the parent-owned #2061; new discovery paths have no match. Remote heads confirm the earlier news layout/editorial branches; no competing discovery branch was found.
- Shared NewsList changes are limited to an optional native ordered-list start, defaulting to one, with existing callers unchanged. Root approved this narrow addition to avoid brittle direct component invocation.
- Use existing kind/topics/news_date/curated order; do not invent event clusters, popularity, testing status or editorial rankings. No extra API reads, schema changes, content edits, commit, push, merge or deployment in this task.
- Route/API caching is unchanged: existing guides reads use `cache: no-store`; React `cache` deduplicates only within one render. No cross-request cache or client fetch was introduced. The original three news reads still request twenty rows each; the curated listing, topics and Gemini registry reads retain their arguments.
- First-page knowledge requires an available curated response, excludes both news-dated entries and every NEWS_TOPICS tag, and requires `valid_until: null`, then takes at most three unique life articles in existing order. Expired and future-deadline entries remain in the ordinary listing rather than being promoted into this rail. No expiry date is not evidence that facts remain current. Those exact identities are removed from the lower listing; no cursor is discarded, even if all current-page cards moved into the rail. Filtered/cursor pages retain the old listing and intro.
- Existing event/category work remains separate: [30-day duplicate recall](../open/2026-10-13-improve-30-day-cross-category-news.md), [held-category correction](../open/2026-10-10-add-audited-held-news-category-correction.md), and the published near-duplicate/category concern are not solved by this presentation change. No title-similarity merging or content reclassification was added.
- Validation: final 4 focused Vitest files / 45 tests passed (exit 0); scoped ESLint on 8 TS/TSX files and TypeScript passed (exit 0); `git diff --check` passed. Task validation passed for 2,396 files, with only pre-existing unrelated claim warnings. Root also completed the production build and i18n checks. A separate agent independently reviewed the final logic and all five catalogs, recomputing all 13 freeze hashes, with no required changes or unsupported quality/testing claims. The initial type check caught only a test-case union inference error, corrected by an explicit `it.each<Record<string, string>>` type; the final check passed.
- Browser verification: root's final `discovery-visual-04` capture passed 12 states with zero page errors, covering five languages, desktop/mobile/320px, dark mode, JavaScript disabled, knowledge-only, empty and cursor views. Assertions cover native keyboard expansion/collapse, six plus fourteen stories, ordered start seven, unique knowledge links and no outer overflow. The implementation author separately viewed all 30 final PNGs and found no blocking layout issue; independent source/locale review was by another agent. Final Korean receipts supplied 23 curated rows and 13/7/0 rows for AI/technology/crypto news, all HTTP 200. No live publication or traffic outcome is implied.
- Capture history is preserved: 01 passed all 12 states; 02 stopped at Korean after seven states with an empty listing and unknown cause; 03/04 added image-readiness and request receipts without changing runtime code or its 3,000 ms API budget. Some end screenshots retain unpainted thumbnail slots despite positive image completion/naturalWidth checks, so this is not an all-image visual certification. Loaded thumbnails are visible in final desktop/390px/Japanese/simplified-Chinese end captures. Detailed freeze, independent logic, browser results and exact 30-image visual receipts remain under `<home>/.codex/tmp/mokaair-news-upgrade-20261110/`.
