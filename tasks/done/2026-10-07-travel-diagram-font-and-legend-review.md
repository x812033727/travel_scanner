---
id: 2026-10-07-travel-diagram-font-and-legend-review
title: Detect undersized travel diagram labels and cross-legend overlaps
status: done
priority: P2
area: tools
owner: claude-opus-5-5-pr-tidy
claimed_at: 2026-10-16T18:05:01Z
created_at: 2026-10-07T08:24:17Z
completed_at: 2026-10-16T18:05:03Z
branch: claude/youthful-brahmagupta-1giys7
depends_on: []
scope:
  - tools/article-localization/render.mjs
  - tools/article-localization/render-layout.mjs
  - tools/article-localization/render-layout.test.mjs
  - .github/workflows/article-localization.yml
---

# Detect undersized travel diagram labels and cross-legend overlaps

## Why

Taiwan 2027 holiday-planning jobs reached official rendered/PASS state, but the
independent native-image review found an English Lunar New Year legend drawn over
the adjacent Japan colour swatch. It also found four actual14px labels although
the travel diagram review policy requires at least15px. Automated containment
checks alone did not establish typography or cross-legend readability.

## Definition of done

- [x] The travel diagram check reports/refuses actual computed font sizes below
      the applicable15px policy without changing original drawings or shrinking type.
- [x] Adjacent legend text/swatch collisions are detected from measured geometry.
- [x] Meaningful regression fixtures fail for these observed cases and pass for
      sufficiently short semantic labels, including CJK and English legend text.
- [x] Existing non-travel layout behavior is preserved or explicitly documented;
      automated checks remain separate from genuine full-image/glyph review.

## Steps

- [x] Reproduce from the preserved pre-correction Taiwan artifacts and native image.
- [x] Add narrowly scoped measurement/refusal rules and regression coverage.
- [x] Validate actual SVG, raster and browser measurements with bundled Node.

## How to verify

Run the applicable render-layout tests and genuine renders of the preserved
failing fixture and a final corrected fixture. Assert real computed font sizes
and text/swatch bounding-box intersections; do not mock the implementation.

## Notes

This is an unclaimed follow-up, not part of the14-article content cohort or its
route-guard implementation. Root is separately applying reviewer-proposed short
labels to Taiwan jobs. Those content fixes must be independently re-reviewed;
they do not complete this tooling task. No font, geometry, source or original
artwork should be changed to make a fixture pass.

The initial immutable Taiwan input plan SHA is
`bc4b0cbdbbc4ffd9ce7958e69b2988860c5381b95077357881a85913c7a604fb`.
The independent review's actual pre-correction frozen input SHA is
`1b51b6e63b52a7337398f73c12aa716128359f0aeab548827378cae4765c3394`.
Observed visible text indices: EN26 and50, JA50 and KO26 are14px; EN59 is the
Lunar New Year legend that overlaps the Japan swatch. A proposed correction or
an automated render PASS is not a final editorial PASS.

### 2026-10-16 fix (claude-opus-5-5-pr-tidy)

Fixed together with `2026-10-07-detect-card-padding-collisions-in-localized` in one change, since both checks live in the same files.

`tools/article-localization/render-layout.mjs`:
- `layoutIssues({ original, localized, size })` now holds every layout check. It was inline in
  `render.mjs`, so none of it could be tested without a browser.
- The four earlier checks are unchanged: visible text count, outside the canvas, outside the
  original containing shape, and a new text overlap.
- New checks, each reported only when the localization introduced it (the source did not already
  do the same):
  - `font size below 15px` (`MIN_FONT_PX`), when the source label was 15px or more. A source drawn
    smaller is the drawing's choice and is not refused.
  - `touches the edge of its containing shape`, when the label sits closer than `EDGE_PADDING`
    (4px) to an edge of the shape that holds it and the source label did not.
  - `new overlap with a neighbouring shape`, for a rect, circle or ellipse that does not hold the
    label, such as a legend's next swatch or a neighbouring card.
  - `new overlap with a line or arrow`. `render.mjs` now measures `line,polyline,polygon,path`
    boxes as `strokes`, widened by 3px because a line's box has no thickness. A polygon that holds
    the label counts as its shape, not an obstacle.

`render.mjs`:
- It shrinks a label no further than `MIN_FONT_PX`. The floor was 14, which produced the four
  14px labels.
- A label that still does not fit at 15px is reported (outside its shape), not shrunk below the
  policy.
- Original drawings are not changed, and only font size is ever adjusted.

`render-layout.test.mjs` was not run anywhere in CI. It now runs in the Article localization
tooling workflow, next to `artifact-integrity.test.mjs`.

Ran:
- `node --test tools/article-localization/render-layout.test.mjs`: 9/9, 6 of them new. They cover
  a clean CJK and English localization, a 14px shrink against a 12px source, the English legend
  over the Japan swatch, a card-border touch, text onto the arrow, a source that already sat 2px
  from the edge, a label inside a polygon, and the earlier checks.
- The same geometry rendered as a real SVG in Chromium (Playwright, measured as `render.mjs`
  does): clean gave no issue, the legend over the next swatch gave the shape overlap, and card
  text to the border gave the edge touch.
- `artifact-integrity.test.mjs` with it: 23/23. `tools/*.test.mjs`: 301/301.

Limits: these checks use boxes, not glyph outlines. A stroke's box covers a whole curved
connector, and touching is measured against the shape's box, not a rounded corner. They do not
replace the independent native full-image and glyph review, which stays required
(`visualReviewRequired`, `glyphReviewRequired`).
