---
id: 2026-10-11-curio-series-own-intro-thumbnail-shorts
title: 奇聞檔案局 gets its own intro, thumbnail series and Shorts theme instead of the channel's
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:02:28Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/render/plan.mjs
  - tools/video/shorts/episode.mjs
  - tools/video/qa/thumbnail.mjs
  - docs/videos/BRANDING.md
---

# 奇聞檔案局 gets its own intro, thumbnail series and Shorts theme instead of the channel's

## Why

The owner's decision 1 of 2026-10-10 (docs/videos/explainer-route/DECISIONS.md): for now a
`cute-mystery` video takes the channel-default bookends and the channel `thumb` thumbnail (tag =
the pillar's name, headline of at most 6 characters), as the three approved local pilots did,
and a series-own identity is a follow-up. In code `explainerSeries(doc)` answers `null` for
`cute-mystery` ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 2), so `branding.mjs`, `render/plan.mjs` `thumbnailSeries` and
`shorts/episode.mjs` treat it as no series: its Shorts are saved as series `illustrated`, whose
theme reads 你以為 · 其實 (design 5.8), and its thumbnail tags 奇異現象 and 預言 have no pilot
thumbnail yet.

## Definition of done

- [ ] The owner has approved an intro (and outro) for 奇聞檔案局, as was done for So That's Why
      on 2026-10-02 (docs/videos/branding-release/).
- [ ] `EXPLAINER_IDENTITY["cute-mystery"]` names the series; a `THUMB_SERIES` entry with its
      pillar ids, a branding registry entry and a Shorts theme exist for it.
- [ ] `cute-cartoon` and `flat-explainer` keep the `sothatswhy` identity unchanged; existing
      `cute-mystery` videos keep the thumbnails they were approved with.
- [ ] The cute-mystery prompt texts brief the series thumbnail instead of the channel's (a
      prompt change: deploy with no cute-mystery run unfinished).

## Steps

- [ ] Wait for the owner's go: this starts with artwork, not code.
- [ ] Widen the scope to the prompt registry and its test when the prompt part starts.

## How to verify

`node --test tools/video/core/branding.test.mjs tools/video/core/explainer-family.test.mjs`; a
`cute-mystery` episode's build picks the series bookends and its Shorts carry the series theme.

## Notes

- 2026-10-11 filed from the design's section 7, item 3.
