---
id: 2026-10-04-keep-subsection-anchors-unique-across-article
title: Keep subsection anchors unique across article slices
status: done
priority: P2
area: web
owner: claude-opus-5-5-subsection-anchors
claimed_at: 2026-10-04T14:45:17Z
created_at: 2026-10-04T08:25:39Z
completed_at: 2026-10-04T15:12:32Z
branch: claude/subsection-anchors-unique
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

- [x] H3 IDs remain unique and sequential within their authored H2 across ad and partner slices.
- [x] Existing H2 TOC targets and H3 IDs before the first slice retain their behavior.
- [x] Default/admin ContentBlocks rendering and ads-off articles retain their behavior.
- [x] Regression coverage proves the later H3 has a distinct target with ads enabled and with an authored partner boundary.

## Steps

- [x] Reproduce duplicate H3 IDs with a valid thick article, then claim the narrow component/test scope after the active FAQ task has landed.
- [x] Carry the subsection numbering state across slices without changing authored content, ad placement, or partner resolution.
- [x] Run focused component/article tests and scoped lint; leave broader CI to the integration owner.

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

2026-10-04, claude-opus-5-5-subsection-anchors:

- The FAQ task this waited on landed on origin/main as #1206 (06b89c835, "keep
  FAQ in order"); `2026-10-04-keep-article-faq-headings-and-answers` and
  `2026-10-04-verify-article-faq-table-of-contents` are in `tasks/done/`, and
  `who-is-on-it.mjs --scope apps/web/components/content-blocks.tsx` showed no
  active task or open PR on the scope. Claimed without `--force`.
- Reproduced first: the three new GuideArticle cases and the new ContentBlocks
  case failed on origin/main with `['section-1-1', 'section-1-1']` (ads on with a
  hero: the first unit lands between the paragraph and the FAQ; partner link
  between the H3s: failed with ads off and with ads on).
- Fix: `ContentBlocks` takes an optional `subsectionStart` (default 0) that seeds
  the H3 count, the same way `headingStart` seeds the H2 count. `GuideArticle`
  walks its pieces in render order and passes each the H3s already drawn in the
  section it opens inside; any H2 resets the count, as it does inside one call.
  `lib/adsense.ts` and `lib/guides.ts` are untouched, so ad placement, segment
  cuts, partner resolution and the TOC ids are as before.
- Unchanged callers: the admin preview (`admin-guides-panel.tsx`) and every other
  `ContentBlocks` caller pass no `subsectionStart`, so they number exactly as
  before. That includes the admin preview's own partner-sliced segments, which
  can still repeat an H3 id inside the preview; the ticket asked to keep
  admin rendering unchanged, and nothing links into the preview.
- An ads-off article without a partner or offer block is one piece starting at
  0, so its ids are unchanged; one with a partner/offer boundary between two H3s
  in the same section now gets distinct ids (that is the defect).
- The first draft carried the count in a `.map` closure; the React compiler
  lint (`react-hooks/immutability`, "Cannot reassign variable after render
  completes") rejects that, so it is a plain loop in the render body.
- Checks (apps/web): `npx vitest run components/content-blocks.test.tsx
  components/guides/article.test.tsx --maxWorkers=2` 122 passed (4 red before
  the fix); `npx eslint` on the four scoped files clean; `npm run typecheck:web`
  from the root clean.
