---
id: 2026-10-24-story-series-thumbnails-take-the-bold
title: Story-series thumbnails take the bold look of the high-view channels (bright ground, two-line outlined headline, the thing itself)
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-24T16:49:13Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates/theme.css
  - tools/video/templates/templates.mjs
  - tools/video/qa/thumbnail.mjs
  - docs/videos/BRANDING.md
---

# Story-series thumbnails take the bold look of the high-view channels (bright ground, two-line outlined headline, the thing itself)

## Why

2026-10-25 the owner asked why 奇聞檔案局 and 品牌故事 get 0–7 views while the channels they were
modelled on get hundreds of thousands (report: `docs/videos/channel-review-20261025-story-series/README.md`).
Side by side, the thumbnails are the most visible gap. The reference channels (黑猫研究院 Seiko,
A4, Dolby; 馬臉姐; cheap) share one look: a bright, saturated ground; two lines of yellow or white
text with a black outline, a 6–8 character headline and an 8–12 character second line; the thing
itself as the subject (the watch, the Michelin man, an A4 sheet, the Dolby mark) or a face with an
exaggerated expression. Ours (`thumb` template, `tools/video/templates/theme.css` `.thumb`) are a
dark teal ground, a 136 px six-character headline, a label pill, a muted MiniMax illustration with
no expression close-up and a small MOKAAIR mark. At list size they read as one dark rectangle.

## Definition of done

- [ ] The owner has seen two or three sample thumbnails of delivered episodes (H01 v2, S01, C01)
      in the bold look and chosen one; this starts with artwork, not code.
- [ ] A `thumb` layout for `curio-` and `story-` videos: full-bleed keyframe or a bright tone
      ground, headline plus second line in outlined type readable at 320 px wide, no label pill,
      the series name small; `thumbnail.data.shot` prefers a face or the object itself.
- [ ] `qa/thumbnail.mjs` keeps the 6-character and word-boundary checks and adds the second line's
      limit; the other series' thumbnails are byte-identical to before.
- [ ] `docs/videos/BRANDING.md` records the look and the owner's choice.

## Steps

- [ ] Render the three samples with the existing `thumbnail.variants` machinery and send them to
      the owner (brand stories: the company name stays as the owner decided on 2026-10-18).
- [ ] Add the layout under `THUMB_LAYOUTS`/`thumbnailHtml` keyed by the two slug prefixes.
- [ ] Extend the QA checks and the template tests.

## How to verify

`node --test tools/video/templates/templates.test.mjs tools/video/qa/thumbnail.test.mjs`; render a
curio episode's thumbnail (`node tools/video/cli.mjs render --slug curio-h01-v2`) and view it at
320 px wide next to a reference thumbnail.

## Notes

- 2026-10-25 filed from the story-series channel review. The open task
  `2026-10-11-curio-series-own-intro-thumbnail-shorts` is about a series identity (intro, Shorts
  theme); this one is only the thumbnail look and should land first.
- The reference thumbnails viewed on 2026-10-25 (ids a7NlBfRCgqI, cP_Y9n23cmQ, ni-loGxhkgs,
  cbTaGjK-YQE, hbTsNpCg5N4) are not reused: the look is copied, never the pictures.
