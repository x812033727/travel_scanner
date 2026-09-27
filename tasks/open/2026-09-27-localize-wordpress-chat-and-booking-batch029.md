---
id: 2026-09-27-localize-wordpress-chat-and-booking-batch029
title: Localize WordPress chat contact buttons and booking system for Batch029
status: in-progress
priority: P2
area: api
owner: codex-batch029-pair-b
claimed_at: 2026-09-27T09:37:39Z
created_at: 2026-09-27T09:37:33Z
completed_at:
branch: codex/article-localization-batch029-contact-pair-b
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-chat-contact-buttons.json
  - apps/api/app/guides/content/wordpress-booking-system.json
  - apps/web/public/guides/wordpress-chat-contact-buttons
  - apps/web/public/guides/wordpress-booking-system
---

# Localize WordPress chat contact buttons and booking system for Batch029

## Why

Two published Traditional Chinese WordPress guides lack en, ja, ko, and zh-CN content and localized text-bearing art. Live source snapshot 2026-09-27T09:29:13Z is pinned in external Batch029 inventory; article v2 and zh-TW v4 match main bd98f467.

## Definition of done

- [x] Both guides have complete en, ja, ko, and zh-CN locales with equivalent blocks, sources, links, credits, and localized cover/diagram text.

## Steps

- [x] Translate both guides from the pinned published zh-TW source and preserve conditions, numbers, citations, and target links.
- [x] Render and inspect 24 localized SVG/JPG assets, lint both packs, and obtain independent peer review.

## How to verify

Run `python -m app.guides.pack_cli lint --slug wordpress-chat-contact-buttons` and `--slug wordpress-booking-system` from apps/api, validate structure/source hashes and image layout, and run `npm run check:tasks`.

## Notes

Inventory: `C:\Users\x8120\.codex\article-localization-release\batch029-contact-inventory\fresh-live\live-source-full-20260927T092913Z.json` SHA256 2557112824db91c3eff0365927d48230d42aee65c7c3a09f13c5d8a0ac6b731d. `candidate-inventory.json` SHA256 3331a9013922e6549c7c399075d27d760135c9f30590d4634eda2b887d0ef850. Host original assets comparison PASS. No production writes in this task.

Both packs preserve the published zh-TW document unchanged at the parsed-document level, all root metadata, 31/32 block types and counts, source URLs/check dates, article-link targets, credits, and 1600×900 geometry. The new eight locales and 24 assets are in this task's exact scope. `pack_cli lint --slug` passed for both; advisories are inherited `no_summary` and complete English body lengths (6,160 and 6,785 characters). The structural and asset audit receipt is `C:\Users\x8120\.codex\article-localization-release\batch029-contact-pair-b\audit-receipt.json` SHA256 a8a4b404cfcd622fbdd1793dd0ec6cecb5a6bd2be71032245dfcad364543449e. Chromium render data is in `render-receipt.json` SHA256 88920acd29fb0ba64ba6049e94c1101309a21dd5a7fe7c174c92d923c93db5b6; all 16 localized SVGs fit the canvas and panel boundaries, and contact sheets were visually reviewed for glyphs and overlap. Numeric differences are only number words converted to digits: 2024, six participants, one hour, and one-person appointment.

Independent Pair B review PASSED: all English body paragraphs checked against the source, with key terms, conditions, numbers, and images sampled in Japanese, Korean, and Simplified Chinese. Reviewer receipt: `C:\Users\x8120\.codex\article-localization-release\batch029-contact\pair-a\pair-b-review.json` SHA256 4081a3bc726ce2d0f3421d826dff21ff61b88b283dee3ae44c0ffbd38fdf8524. Commit content manifest: `C:\Users\x8120\.codex\article-localization-release\batch029-contact-pair-b\commit-manifest.json` SHA256 e88e0e94ba8c8420e9b1a26b636de79f9a84338f019c78b66b567572f5d65210. Awaiting integration PR, deployment, and publication in the Batch029 release task.
