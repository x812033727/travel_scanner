---
id: 2026-10-07-travel-diagram-font-and-legend-review
title: Detect undersized travel diagram labels and cross-legend overlaps
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T08:24:17Z
completed_at:
branch:
depends_on: []
scope:
  - tools/article-localization/render.mjs
  - tools/article-localization/render-layout.mjs
  - tools/article-localization/render-layout.test.mjs
---

# Detect undersized travel diagram labels and cross-legend overlaps

## Why

Taiwan 2027 holiday-planning jobs reached official rendered/PASS state, but the
independent native-image review found an English Lunar New Year legend drawn over
the adjacent Japan colour swatch. It also found four actual14px labels although
the travel diagram review policy requires at least15px. Automated containment
checks alone did not establish typography or cross-legend readability.

## Definition of done

- [ ] The travel diagram check reports/refuses actual computed font sizes below
      the applicable15px policy without changing original drawings or shrinking type.
- [ ] Adjacent legend text/swatch collisions are detected from measured geometry.
- [ ] Meaningful regression fixtures fail for these observed cases and pass for
      sufficiently short semantic labels, including CJK and English legend text.
- [ ] Existing non-travel layout behavior is preserved or explicitly documented;
      automated checks remain separate from genuine full-image/glyph review.

## Steps

- [ ] Reproduce from the preserved pre-correction Taiwan artifacts and native image.
- [ ] Add narrowly scoped measurement/refusal rules and regression coverage.
- [ ] Validate actual SVG, raster and browser measurements with bundled Node.

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
