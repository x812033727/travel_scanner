---
id: 2026-09-20-constrain-related-guide-cards-to-mobile
title: Constrain related guide cards to mobile grid width
status: done
priority: P2
area: web
owner: codex-related-grid
claimed_at: 2026-09-20T16:12:22Z
created_at: 2026-09-20T16:12:13Z
completed_at: 2026-09-21T12:19:27Z
branch: codex/batch006-hawker-card-width
depends_on: []
scope:
  - apps/web/components/guides/related-grid.tsx
---

# Constrain related guide cards to mobile grid width

## Why

At 390px, the English Singapore hawker guide is 391px wide. Its "More on this topic" grid has one implicit `auto` column on mobile; the long unbroken route text in the fourth related-card description gives that track a 370.766px minimum inside a 350px list. All four cards then reach x=390.766px and create horizontal scrolling.

## Definition of done

- [x] Related cards stay within the article column at 320px and 390px without clipping text.
- [x] The other four article locales and the two-column tablet layout retain their widths.
- [x] Relevant frontend checks pass and a narrow PR is open.

## Steps

- [x] Reproduce the live DOM width and identify the intrinsic grid-track cause.
- [x] Set an explicit minmax(0,1fr) mobile grid column through `grid-cols-1`.
- [x] Verify rendered mobile/tablet geometry and run frontend checks.

## How to verify

Run the related-grid component test, web lint and typecheck. In a 390px and 320px browser, compare `document.documentElement.scrollWidth` with `innerWidth`, each related `li` right edge with its 350px/280px grid width, and each card's `scrollWidth` with its `clientWidth`. Repeat for five locales; check 768px remains two columns. Inspect a card screenshot for wrapping rather than hidden content.

## Notes

Live DOM before change: English Hawker `/en/guides/howto/singapore-hawker-first-visit` at 390px had list x=20 width=350, computed implicit track=370.766px, card right=390.766px and document.scrollWidth=391. The fourth related card's min-content width is 370.766px because of its long route string. A read-only inline `grid-template-columns:minmax(0,1fr)` probe returned document.scrollWidth to the viewport at 320/360/390px, kept card contents within their client widths, and left 430/768px geometry unchanged. Baseline visual evidence: `C:\Users\x8120\.codex\article-localization-release\batch006-three-live-2c2cf990\independent-visual-review.json` SHA 20e51c6d7c1a879ecec6f4b174f9763371d47034826e16221aa6fe2dd0562a38.

Validation on 2026-09-20 UTC: equivalent grid CSS on the signed-out live page gave document widths 320/320 and 390/390 for English, 390/390 in the other four locales, and 768/768 with 356px × 2 columns. Every related card had `scrollWidth == clientWidth`; full English card screenshots at 320 and 390 showed the long text wrapping. `npm run test:web -- related-grid.test.tsx` passed 3/3, `npm run typecheck:web` passed, `npx eslint components/guides/related-grid.tsx --max-warnings=0` passed, and `npm run check:tasks` passed with unrelated queue warnings. CI will perform full lint/build after PR.

PR #607: https://github.com/x812033727/travel_scanner/pull/607. Full `npm run lint:web` passed sequentially after an earlier parallel Windows process exited without diagnostics. Task remains in review until the PR is merged.

PR #607 merged as `de4ea69861c8181fd67af4d0b9b52a9ddc65544c` and is included in deployed main `42b1754e6e51ddbdd3694ae5666e62a04fd98648`. Signed-out final browser QA passed Hawker/en at both 390px and 320px with document width equal to the viewport, card contents contained, and no horizontal overflow; the other four locales and the complete Batch006 desktop/mobile matrix also passed. Raw final evidence SHA-256 is `70a746075f3f8f3defe1069f69c0def6defcde5795a70e8abbf3f72ad9d67222`.
