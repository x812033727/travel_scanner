---
id: 2026-09-20-localize-hong-kong-ferry-tram-zh
title: Localize Hong Kong ferry/tram zh-TW diagram labels
status: in-progress
priority: P2
area: web
owner: codex-batch005-author
claimed_at: 2026-09-20T12:41:20Z
created_at: 2026-09-20T12:34:47Z
completed_at:
branch: codex/hong-kong-zh-svg-localization
depends_on: []
scope:
  - apps/web/public/guides/hong-kong-ferry-tram-day/diagram-1.svg
---

# Localize Hong Kong ferry/tram zh-TW diagram labels

## Why

The published Traditional Chinese Hong Kong ferry/tram guide's original step
diagram still shows six English helper labels, including its footer, even
though the article and the diagram's other visible text are in Traditional
Chinese. Readers should see one consistent language in the source artwork.

## Definition of done

- [x] All six authored English helper labels in the zh-TW SVG are natural
      Traditional Chinese; only the Mokaair brand name remains in Latin script.
- [x] SVG dimensions, shapes, colors, step numbers and attribution remain intact.
- [x] 1600×900 and 390px previews have no missing glyphs, collisions or clipping.
- [ ] A narrow SVG-only PR is open for independent review.

## Steps

- [x] Inventory all visible `title`, `desc`, `text` and `tspan` content.
- [x] Change the six English helper labels, including the footer.
- [x] Compare XML structure, protected numbers and provenance with base.
- [x] Render and visually inspect desktop/mobile previews.
- [ ] Run task checks and open the focused PR.

## How to verify

Run `npm run check:tasks` and `git diff --check`. Parse the SVG as XML,
compare all element tags and attributes with `HEAD`, and confirm only six
visible text nodes changed. Render the SVG at 1600×900 and 390px; inspect
both previews for Chinese glyphs and layout.

## Notes

Batch004's completed scope initially blocked the claim. Its owner authorized
closeout; `tasks/done/2026-09-20-five-language-article-batch-004.md` records
the published work and this remaining source-art issue. Windows left an open
copy after `tasks -- done`; the exact stale copy was removed with `git rm`,
then this narrower task was claimed without `--force`.

Original authored English: “A practical sequence”, “Choose the pier”,
“Connect on foot”, “Read destination”, “Plan the return” and the footer
“Editorial diagram”. The footer retains the Mokaair brand while the
attribution becomes `Mokaair · 編輯自製示意圖`. No English appears in `title` or
`desc`; there are no `tspan` nodes. The six replacements preserve the
1600×900/viewBox geometry and all 01–04 labels. XML comparison found 28
elements, 19 visible text nodes, identical tags/attributes and exactly six
changed text nodes. Original SVG SHA-256:
`c132a9da02316522e6158a4abe5c52f2988b8195e82b6a525b01b3c6911cb958`;
new SVG SHA-256:
`c1dcc5a83a98d2fd12cd825ba5e4c172774ccfa16a176e7504fd24b7853ea645`.
Both rendered previews were visually inspected with no missing glyphs,
overlap or clipping. The author QA receipt and previews are external at
`C:\Users\x8120\.codex\article-localization-batch-005\hong-kong-zh-svg-review`;
the receipt SHA-256 is
`5c906a161b85655483996584de74c18a28e413e610a56fb24aeb9da7e79b618b`.
