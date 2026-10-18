---
id: 2026-10-07-detect-card-padding-collisions-in-localized
title: Detect card padding collisions in localized SVG previews
status: done
priority: P2
area: tools
owner: claude-opus-5-5-pr-tidy
claimed_at: 2026-10-16T18:05:02Z
created_at: 2026-10-07T16:58:05Z
completed_at: 2026-10-16T18:05:04Z
branch: claude/youthful-brahmagupta-1giys7
depends_on: []
scope:
  - tools/article-localization/render-layout.mjs
  - tools/article-localization/render-layout.test.mjs
  - tools/article-localization/render.mjs
---

# Detect card padding collisions in localized SVG previews

## Why

The official English Japan entry diagram render returned automated layout passed,
but two independent readers saw the final phone and landing-sticker text touch or
cross card borders, with three other labels touching borders or transition arrows.
Human native review correctly withheld approval. Improve automatic diagnostics to
catch this class without replacing the independent native review gate.

## Definition of done

- [x] Reproduce actual card-edge collisions from a small deterministic SVG fixture.
- [x] Distinguish usable inner card bounds/padding from outer shapes or canvas bounds.
- [x] Flag border/arrow collisions while preserving valid existing diagram text.
- [x] Keep meaningful renderer/layout tests passing and document remaining limits.

## Steps

- [x] Inspect the frozen actual failed native image and original measurements.
- [x] Diagnose the bound/padding selection, add a focused regression and fix it.

## How to verify

Run the render-layout tests and reproduce the actual compact fixture before/after.
Render a native preview and genuinely inspect clipping and arrow/card spacing; an
automated exit-zero receipt alone does not establish editorial acceptance.

## Notes

- Actual frozen English native preview SHA:
  `1fb3e937` is only a short locator; use the full hash in the preserved finding below.
- Actual exact-five-label finding receipt SHA:
  `eb12a15bb88f2b6bb9f9d8d79f491b52505d65d1ef9eb764b2a747c2555e7d89`.
- Native visible indices 9, 17, 23, 25 and 32 correspond to staged field indices
  11, 19, 25, 27 and 34. Two readers separately confirmed indices 17 and 32.
- This follow-up is not implemented by the current article localization PR. The
  current release candidate uses faithful compact labels plus fresh human review.

### 2026-10-16 fix (claude-opus-5-5-pr-tidy)

Claimed with `--force`: its scope is the same three files as the other ticket, claimed for the same change.

Fixed together with `2026-10-07-travel-diagram-font-and-legend-review` in one change, since both checks live in the same files.

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
