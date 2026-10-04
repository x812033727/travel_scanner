---
id: 2026-10-04-keep-subsection-anchors-unique-across-article
title: Keep subsection anchors unique across article slices
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-04T08:25:39Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
---

# Keep subsection anchors unique across article slices

## Why

Article bodies are rendered in slices around AdSense units and authored partner
buttons. Each ContentBlocks call receives the previous H2 count, but resets its
H3 subsection count to zero. Two H3 headings under the same H2, separated by an
ad or partner slice, can therefore share `section-1-1`. An existing fragment
link to the later subsection reaches the earlier one instead.

## Definition of done

- [ ] H3 IDs remain unique and sequential within their authored H2 across ad and partner slices.
- [ ] Existing H2 TOC targets and H3 IDs before the first slice retain their behavior.
- [ ] Default/admin ContentBlocks rendering and ads-off articles retain their behavior.
- [ ] Regression coverage proves the later H3 has a distinct target with ads enabled and with an authored partner boundary.

## Steps

- [ ] Reproduce duplicate H3 IDs with a valid thick article, then claim the narrow component/test scope after the active FAQ task has landed.
- [ ] Carry the subsection numbering state across slices without changing authored content, ad placement, or partner resolution.
- [ ] Run focused component/article tests and scoped lint; leave broader CI to the integration owner.

## How to verify

With an article ordered H2 Prices, H3 Before booking, paragraph, FAQ with two
items, H3 After booking, then 20 paragraphs, enable advertising and a hero.
Assert the two H3 IDs are `section-1-1` and `section-1-2`, rather than both
`section-1-1`. Add a separate valid partner-link/offer boundary between the two
H3 headings and make the same assertion. Repeat with advertising disabled and
verify default ContentBlocks callers remain unchanged.

From apps/web, use the verified Node runtime to run
`vitest run components/content-blocks.test.tsx components/guides/article.test.tsx --maxWorkers=1`
and ESLint on the four scoped files. A browser fragment check is useful at
integration time, but a DOM assertion on unique IDs must catch the defect first.

## Notes

2026-10-04, read-only independent review by codex-gpt6-home:

- This defect predates the FAQ-in-authored-order fix. Running the actual
  `adsensePlacements` with the source sequence above and simulating the existing
  ContentBlocks heading pass produced duplicate `section-1-1` both when the FAQ
  was hoisted out and when it remained inline. This is not a regression blocker
  for the FAQ task.
- Relevant source: ContentBlocks initializes `subsection = 0` for every call;
  GuideArticle passes each piece's H2 `headingStart` but no H3 continuation.
  Partner slices have the same limitation. Existing FAQ tests prove continuity
  only within one ContentBlocks call.
- No implementation, claim, full suite, server, production write, or deployment
  was performed. The task is intentionally open while the overlapping active
  FAQ task finishes; task scopes are not locks.
