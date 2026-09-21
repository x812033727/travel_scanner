---
id: 2026-09-21-diagram-text-is-unreadable-at-mobile
title: Diagram text is unreadable at mobile width
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-21T01:04:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/guides/guide-image.tsx
  - apps/web/components/guides/guide-image.test.tsx
---

# Diagram text is unreadable at mobile width

## Why

Editorial diagrams are authored on a 1600x900 canvas and rendered inside the article
column. At a 375px viewport that column is 335px wide, so the whole SVG is scaled to
21% and every label shrinks with it. Measured on the live English
`singapore-gardens-indoor-outdoor` guide on 2026-09-21, all 19 text elements land
between 4.8 and 8.8 CSS pixels, against 16px body text in the same article:

| Authored size | Rendered at 375px | Count | Example label |
|---|---|---|---|
| 42 | 8.8 px | 1 | Step order · A practical sequence |
| 34 | 7.1 px | 4 | 01 |
| 33 | 6.9 px | 3 | Choose your focus |
| 29 | 6.1 px | 1 | Check maintenance |
| 26 | 5.4 px | 5 | Indoor vs. outdoor |
| 25 | 5.2 px | 1 | Choose what suits you… |
| 23 | 4.8 px | 4 | Pick one priority |

The diagram is decorative on a phone: the reader can see the shape of the four steps
but cannot read them.

This is not one article's problem. The same 1600x900 convention is used across the
localized guide batches, and two independent reviews already recorded it per article:
batch-006 asked for KL English SVG legibility, and
`2026-09-20-localize-four-tokyo-first-trip-guides` notes that "at 390px the whole
1600px diagram is scaled down; small lettering needs explicit mobile-readability
review". Both notes sit inside article-scoped localization tasks owned by other
sessions, so nothing tracks the shared rendering problem that causes them.

It is not an accessibility failure today. Every diagram carries alt text, the figure
has a "Read the full description" disclosure that repeats the content as prose, and
the page allows pinch zoom (`width=device-width, initial-scale=1`, with no
`user-scalable=no` and no `maximum-scale`). The gap is that a phone reader cannot use
the diagram as a diagram without leaving the reading flow.

## Definition of done

- [ ] At a 375px viewport a reader can read every label in an article diagram.
- [ ] Desktop rendering is unchanged.
- [ ] The document still has `scrollWidth == innerWidth` at 375px; no horizontal page scroll.
- [ ] Alt text and the full-description disclosure are untouched; this does not replace them.

## Steps

- [ ] Choose an approach. Tapping the figure to open the SVG at full size, or giving it
  the `overflow-x-auto` treatment the article tables already use with a minimum width,
  both fit the declared scope. Emitting a separate mobile SVG variant with larger type
  does not: that lives in the localization render pipeline and needs the scope widened
  to `tools/article-localization` and the asset directories, which other localization
  tasks currently hold.
- [ ] Implement it in `guide-image.tsx` and cover it in `guide-image.test.tsx`.
- [ ] Check one diagram in each of the five locales; label lengths differ per language,
  so a fix that fits English can still overflow Japanese or Korean.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
```

Then on a deployed build, at a 375x812 viewport, on
`/en/guides/howto/singapore-gardens-indoor-outdoor`:

- `document.documentElement.scrollWidth` equals `window.innerWidth` (375).
- No element inside `main` has a bounding rect extending past the viewport.
- Every `<text>` in the diagram resolves to at least 11 CSS pixels, or is reachable at
  that size through whatever affordance the fix adds.

## Notes

- Measured live on 2026-09-21 with the in-app browser at 375x812. The article page
  itself was clean: no viewport widening, zero overflowing elements, hero and diagram
  both at 335px, largest font 30px on the H1. The only defect was diagram type size.
- A first screenshot showed the diagram area blank. That was `loading="lazy"` not yet
  painted, not a missing asset. All five locale SVGs return 200 with valid markup, and
  the English one reports `naturalWidth` 1600 once loaded. Scroll it into view and wait
  before judging a diagram screenshot.
- The SVG carries its own opaque background (`<rect width="1600" height="900"
  fill="#f4f0e5">`) and fixed hex fills, with no `prefers-color-scheme`, `currentColor`
  or CSS variables. It therefore renders as a light card on the dark theme, which is
  legible but means a future dark-mode diagram treatment has no hook to work with.
- Separate small inconsistency found while measuring, not covered by this task: the
  English SVG's internal `<title>` still reads `Singapore’s` with a typographic
  apostrophe, which PR #605 replaced everywhere else in that article. It is not
  rendered, because the SVG is loaded through `<img>`, but it is inconsistent and tools
  that parse the SVG will read the old character.
