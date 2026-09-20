---
id: 2026-09-20-localize-four-tokyo-first-trip-guides
title: Localize four Tokyo first-trip guides and diagrams
status: in-progress
priority: P1
area: docs
owner: codex-batch007-source-pr
claimed_at: 2026-09-20T14:39:09Z
created_at: 2026-09-20T12:47:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/narita-haneda-to-tokyo.json
  - apps/api/app/guides/content/tokyo-transit-passes.json
  - apps/api/app/guides/content/tokyo-disney-guide.json
  - apps/api/app/guides/content/tokyo-where-to-stay.json
  - apps/web/public/guides/narita-haneda-to-tokyo
  - apps/web/public/guides/tokyo-transit-passes
  - apps/web/public/guides/tokyo-disney-guide
  - apps/web/public/guides/tokyo-where-to-stay
---

# Localize four Tokyo first-trip guides and diagrams

## Why

The four public Tokyo planning guides have only `zh-TW` published. Their main-tree
packs also contain only `zh-TW`, and each article embeds an editable text SVG. Complete
`en`, `ja`, `ko` and `zh-CN` bodies and diagrams from the current published source,
then hand off for independent review before any import or publication.

## Definition of done

- [ ] Four full documents in each of the four missing languages, including title,
  description, every body block, tables, links, captions, alt text and source titles.
- [ ] Four-language SVG variants for each diagram, rendered and checked for overflow.
- [ ] Source versions and hashes pinned; no existing `zh-TW` prose or artwork replaced.
- [ ] Independent editorial review completed before a separate release task uses the packs.

## Steps

- [x] Check active task scopes and claim exact article/asset paths.
- [x] Capture live published source in a read-only repeatable-read transaction.
- [x] Reconcile published documents against main packs and translate all content in provisional drafts.
- [x] Localize SVG text; render and inspect the four language versions provisionally.
- [x] Produce provisional handoff for an independent reviewer.

## How to verify

Run source-hash comparison, pack lint and SVG rendering checks on the external draft.
After independent review, run the guarded import dry-run and normal API/web checks
in the release branch. No import, PR or publication is authorized by this task alone.

## Notes

- Main tree: `5648b84043a09e9db7f773d7a080260d39f9d453`.
- Live source snapshot: `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-live-source.json`,
  captured 2026-09-20T12:44:58Z; SHA-256
  `cadd602ab7da7865dc60295fe8af9cab0861741fec35734b13d3de575fd5ab69`.
- All four articles were `published`, active, `article_version=2`, `zh-TW`
  `published_version=6`, with no expiry and no other published locale.
- Published source differs from the main packs in description and image metadata.
  Use the live published document as translation source; preserve current attribution.
- Source rechecked by another production read-only transaction before revision:
  all four article/source versions and published document hashes were unchanged.
  Recheck capture: `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-live-source-refresh.json`.
- Updated provisional 16-document handoff:
  `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-provisional\review-handoff.json`,
  SHA-256 `787c615ea9e6ccec5b61d1ea8518bd1ad25f676e4ddeeb6d5523b7037c1f2661`.
  It includes 60 translated summary items, 16 separately translated image descriptions,
  complete source/version bindings, corrected document/SVG hashes, and 1600×900 plus
  390px previews for every language.
- The original model attempts, second-pass numeric repairs, two narrow manual
  corrections and SVG pre-layout originals are preserved outside the repo.
  Corrected drafts now have zero strict field, numeric/URL/code token, schema,
  SVG canvas and text-text overlap errors. The original 219 field and 23 canvas
  errors remain visible in provenance rather than being erased.
- This handoff is **not ready for import**: the shared pipeline has not formally
  materialized `summary.items` or `image.description`, and independent editorial
  and visual review remains. At 390px the whole 1600px diagram is scaled down;
  small lettering needs explicit mobile-readability review.
- Formal materialization awaits shared-pipeline support for `summary.items` and
  `image.description`, followed by independent text/image review.
- No active task scope overlapped the eight explicit pack and asset paths when claimed.

## Published-source correction checkpoint (2026-09-20)

- The independent review at
  `C:\Users\x8120\.codex\article-localization-release\batch007-tokyo-provisional\independent-review-HOLD.md`
  identified seven zh-TW source issues; its SHA-256 is
  `912f4038b3d0bc98ac0aeb6257813d0d730fe79ceadc4b953bbbe26d26aae48f`.
- A narrow source-correction PR changes only the existing Narita, Disney and transit
  zh-TW packs and the transit zh-TW decision-tree SVG. Tokyo stay is unchanged.
  The new facts are sourced to Tokyo Metro, JR Group, JR East and Tokyo Disney
  official pages checked on 2026-09-20; existing source links and check dates
  remain intact. The Narita pack already has the schema maximum of 20 source
  entries; the JR East eligibility page is cited in the PR review description
  rather than replacing or deleting an existing source.
- The 16 provisional translation documents and language SVGs remain outside the
  repository and **on hold**. Re-read the published source after any eventual
  source release, rebind versions/hashes, fix their locale text and images,
  rerender at desktop and mobile widths, then obtain an independent re-review
  before importing or publishing them.
- A 1600×900 render of the existing zh-TW transit decision tree also shows
  pre-existing IC-card banner text extending beyond its rounded box. The price
  card corrected in this PR fits; the broader diagram layout needs separate
  visual cleanup during Batch007 image review.
