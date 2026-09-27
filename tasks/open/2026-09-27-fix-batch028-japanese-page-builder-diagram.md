---
id: 2026-09-27-fix-batch028-japanese-page-builder-diagram
title: Fix Batch028 Japanese page builder diagram card padding
status: in-progress
priority: P1
area: web
owner: codex-batch028-jp-diagram-fit
claimed_at: 2026-09-27T17:26:13Z
created_at: 2026-09-27T17:26:02Z
completed_at:
branch: codex/batch028-jp-diagram-fit
depends_on: []
scope:
  - apps/web/public/guides/wordpress-page-builder-choice/diagram-1-ja.svg
---

# Fix Batch028 Japanese page builder diagram card padding

## Why

After Batch028 published its five-language WordPress design guides, independent post-deploy visual QA measured `wordpress-page-builder-choice/diagram-1-ja.svg`. The third card's line `テンプレートの影響範囲` has only 8.80px of right padding at the native 1600×900 size, below the acceptance audit's 12px minimum. The text remains inside the border but looks crowded. The English repair and the 16 published article documents are separate work.

## Definition of done

- [x] The Japanese line keeps its exact wording and the diagram remains 1600×900.
- [x] Every card has at least 12px inner right margin with no text overlap, clipping or missing glyphs at native size and in desktop/mobile article renderings.
- [ ] The diff changes only this SVG and this task record; no production write is made by this task.

## Steps

- [x] Claim the exact SVG scope in an isolated worktree based on deployed commit `853a3434dcc2eefe7f2b28f08e725f479b304090`.
- [x] Render local candidate and inspect all four cards and title/footer at native size.
- [ ] Independently review the final rendered SVG, run the focused checks, and prepare a reviewable PR.

## How to verify

Run a local Chromium SVG `getBBox()` audit against all card text and verify the minimum right margin is at least 12px. Render the full 1600×900 SVG and desktop/mobile article diagrams and inspect the original pixels. Parse SVG XML, compare its visible Japanese text inventory with the deployed version, and run `npm run check:tasks`. Do not treat the previously captured production FAIL as a local PASS.

## Notes

Read-only production card audit at 17:22 UTC: full 20-diagram receipt SHA `6121211a718e12e1203dc56df9cee7c698c806591ad484c1c540c9ecbc4c733f`; Japanese target text bbox right 1142.203px, card right 1151px, margin 8.797px. The 27px original has 52px vertical baseline separation to adjacent rows. Wrapping it into two 27px lines would overlap the next 32px line unless multiple rows are shifted. A 1px font reduction retains the original four-row alignment and wording; local geometry and visual review will determine whether it is sufficient.

Local candidate changes only that one font-size attribute, `27` to `26`. SHA256 `017b9865991f441d0d48986378bcc4ca613b3bdbf121bcb65afb0f84f3cb7091`. External evidence `C:\Users\x8120\.codex\article-localization-release\batch028-wordpress-design\diagram-fit-ja-review\validation.json` SHA256 `3fab14b437601b594b0893c8993ae5f2cbcf7cf5b40949da088655bbf6e882c6`: 4 cards, exact text, minimum right margin 19.765625px, no bbox overlap, native render and desktop/mobile page injection PASS. I viewed native 1600×900 and mobile third-card PNG; all text remains legible. `git diff --check` and `npm run check:tasks` pass (task checker reports pre-existing stale-claim warnings). Independent review is pending; this local simulation is not a production PASS.
