---
id: 2026-10-30-daily-brief-thumbnails-carry-the-lead
title: Daily brief thumbnails carry the lead story's official image
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-30T00:14:24Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation
  - .agents/skills/youtube-video/references/daily-brief.md
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

- [ ] A brief the worker makes has `thumbnail.data.asset` set to the lead story's official image,
      credited in `assets[]` (source URL and license line), before `render` runs.
- [ ] The picture fills the box without cutting off the product's name or wordmark.
- [ ] When no usable image is found, the brief still renders: the box stays as it is today and the
      notes say why.

## Steps

- [ ] When planning (`draftDaily` in `tools/video/automation/flow.mjs`), read the `og:image` of
      the lead story's official source page (`video.json` `sources`, the one the first chapter
      cites).
- [ ] Download the image into `docs/videos/<slug>/`. A 16:9 image gets padded to the box's aspect
      over a blurred copy of itself, so the wordmark stays whole. The episode 1 filter, for a
      1300×731 source:
      `[0]format=rgb24,split[a][b];[a]scale=1300:1171,boxblur=40:4[bg];[bg][b]overlay=0:(H-h)/2`
- [ ] Write `thumbnail.data.asset` and the `assets[]` entry as the writer stage's output, never
      after `render` or `assemble`: changing `video.json` after the final cut makes
      `package` refuse with "final.mp4 is older than the script", and the final has to be
      approved again.
- [ ] Note it in `.agents/skills/youtube-video/references/daily-brief.md`.

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
