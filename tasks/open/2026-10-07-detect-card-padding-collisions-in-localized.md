---
id: 2026-10-07-detect-card-padding-collisions-in-localized
title: Detect card padding collisions in localized SVG previews
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T16:58:05Z
completed_at:
branch:
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

- [ ] Reproduce actual card-edge collisions from a small deterministic SVG fixture.
- [ ] Distinguish usable inner card bounds/padding from outer shapes or canvas bounds.
- [ ] Flag border/arrow collisions while preserving valid existing diagram text.
- [ ] Keep meaningful renderer/layout tests passing and document remaining limits.

## Steps

- [ ] Inspect the frozen actual failed native image and original measurements.
- [ ] Diagnose the bound/padding selection, add a focused regression and fix it.

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
