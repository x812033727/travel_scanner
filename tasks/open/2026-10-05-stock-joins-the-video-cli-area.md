---
id: 2026-10-05-stock-joins-the-video-cli-area
title: stock joins the video CLI area table
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T18:08:16Z
completed_at:
branch:
depends_on:
  - 2026-10-05-stock-photo-slides-and-attribution
scope:
  - tools/video/cli.mjs
  - tools/video/cli.test.mjs
---

# stock joins the video CLI area table

## Why

`tools/video/cli.mjs` dispatches every stage through its `AREAS` table (command → directory,
ticket). `2026-10-05-stock-photo-slides-and-attribution` built `stock search` and `stock fetch`
in `tools/video/media/stock.mjs`, reached through `tools/video/media/cli.mjs`, but that ticket's
scope did not include the main CLI, so `node tools/video/cli.mjs stock …` answers
`unknown command "stock"` and the media CLI had to grow a direct-run `main` of its own
(`node tools/video/media/cli.mjs stock …`). One line in `AREAS` and one in `HELP` make the main
CLI the one entry point again, as it is for `look`, `keyframes`, `clips` and `music`.

## Definition of done

- [ ] `node tools/video/cli.mjs stock search --query "Seoul skyline"` and
      `node tools/video/cli.mjs stock fetch --slug S --provider P --id N` run `media/stock.mjs` with
      the main CLI's exit codes; `--help` lists them beside the media stages.
- [ ] `docs/videos/ILLUSTRATED.md` §圖庫照片 工具端 and
      `.agents/skills/youtube-video/references/visuals.md` name the main CLI form (add them to the
      scope when claiming; neither is bound).

## Steps

- [ ] `AREAS.stock = ["media", "2026-10-05-stock-photo-slides-and-attribution"]`; `HELP` line.
- [ ] `tools/video/cli.test.mjs` is receipt-bound (`tools/video/long-form/review.mjs`
      `REVIEW_FILES`): a test there needs the independent reviewer to re-bind
      `docs/videos/long-form/review.*`; otherwise cover it in `tools/video/media/media.test.mjs`.

## How to verify

```bash
node --test tools/video/cli.test.mjs tools/video/media/media.test.mjs
node tools/video/cli.mjs stock   # exit 2 with the subcommand usage, not "unknown command"
node tools/video/long-form/cli.mjs check
```

## Notes

- The direct-run `main` in `tools/video/media/cli.mjs` can stay: the media tests use it, and it
  costs nothing.
