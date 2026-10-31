---
id: 2026-10-30-daily-brief-thumbnails-carry-the-lead
title: Daily brief thumbnails carry the lead story's official image
status: done
priority: P2
area: tools
owner: claude-opus-5-5-lead-picture
claimed_at: 2026-10-31T13:21:56Z
created_at: 2026-10-30T00:14:24Z
completed_at: 2026-10-31T13:49:36Z
branch: claude/dazzling-wright-pqolfx
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/lead-picture.mjs
  - tools/video/automation/automation.test.mjs
  - .agents/skills/youtube-video/references/daily-brief.md
  - tools/video/render/browser.mjs
  - tools/video/templates/theme.css
  - tools/video/qa/thumbnail.mjs
  - tools/video/qa/thumbnail.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Daily brief thumbnails carry the lead story's official image

## Why

The daily brief's thumbnail template (`thumb`) has a picture box on the right. The first
episode, `daily-ai-20261028`, went out with that box empty: a flat purple square in zh-TW and in
all eight locale thumbnails. On 2026-10-30 the owner asked for Gemini 4 Carbon's official image
there. It was added by hand after the owner had approved the upload package: nine JPEGs were
handed over to upload in YouTube Studio, and the repo and the package were left unchanged.

The host worker makes a brief every day, and nobody checks the thumbnail by hand, so the picture
has to come with the brief.

## Definition of done

- [x] A brief the worker makes has `thumbnail.data.asset` set to the lead story's official image,
      credited in `assets[]` (source URL and license line), before `render` runs.
- [x] The picture fills the box without cutting off the product's name or wordmark.
- [x] When no usable image is found, the brief still renders: the box stays as it is today and the
      notes say why.

## Steps

- [x] When planning (`draftDaily` in `tools/video/automation/flow.mjs`), read the `og:image` of
      the lead story's official source page (`video.json` `sources`, the one the first chapter
      cites).
- [x] Download the image into `docs/videos/<slug>/`. A 16:9 image gets padded to the box's aspect
      over a blurred copy of itself, so the wordmark stays whole. The episode 1 filter, for a
      1300×731 source:
      `[0]format=rgb24,split[a][b];[a]scale=1300:1171,boxblur=40:4[bg];[bg][b]overlay=0:(H-h)/2`
- [x] Write `thumbnail.data.asset` and the `assets[]` entry as the writer stage's output, never
      after `render` or `assemble`: changing `video.json` after the final cut makes
      `package` refuse with "final.mp4 is older than the script", and the final has to be
      approved again.
- [x] Note it in `.agents/skills/youtube-video/references/daily-brief.md`.

## How to verify

- `node tools/video/cli.mjs render --slug <a brief>` draws `thumbnail.jpg` and
  `thumbnails/<locale>.jpg` with the picture, and its output has no "does not fit" note.
- Look at the contact sheet: the wordmark is whole and no text sits under the bottom bar.

## Notes

- SKILL.md rule 6 bars other people's photos from thumbnails. It allows a product's official page
  or logo as the subject when the video comments on that product (owner 2026-10-08), with the
  source credited. The license line used on episode 1: "Google's official announcement image,
  quoted as the subject of a news commentary thumbnail with the source credited".
- Episode 1's image:
  `https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini_carbon_102726_social_share.width-1300.png`,
  the `og:image` of Google's "Introducing Gemini 4 Carbon" post.
- Locale thumbnail words must also fit. On episode 1, en, ko, es, id and vi first came out too
  long and had no thumbnail of their own (#1924). The headline holds about 10 Latin characters a
  line in bold.
- Done 2026-10-31 (`tools/video/automation/lead-picture.mjs`, `flow.mjs` `leadPicture`). It runs
  in `advance()` for a daily brief whose next stage is `frames rendered`, not when planning: the
  official sources are in the script, not in the site's articles the planner reads. Tried once
  per brief (`auto.json` `lead_picture`); a page without an og:image, or a picture lint refuses,
  leaves the box as it was. The first source that is not mokaair.com is the lead. Layout `a`
  (the card) is set when the brief has none: layout `b` spreads the picture under the headline's
  scrim, where Carbon's wordmark sat.
- The padding filter is general (`PAD_FILTER`): any aspect is fitted whole into a 1536×1440 box
  over a cover-scaled blurred copy.
- Same pull request, from the owner's look at the 10-29 locale thumbnails: id "keliru" and pt
  "errada" lost the foot of their last line, because #1937 kept the thumbnail's 0.4 em overflow
  allowance; the thumbnail now uses the slides' measure (glyph spill plus 0.04 em), and
  `qa/thumbnail.mjs` `HEADLINE.tolerance` follows (0.215). A Japanese headline broke anywhere and
  left 「た」 alone on a line; `.thumb h1:lang(ja)` and `.sub` now use `word-break: auto-phrase`.
- Reproduced on episode 1's script with the 10-29 locale words: before, both feet cut; after,
  whole, with blog.google's Carbon image in the card.
