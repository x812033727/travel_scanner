---
id: 2026-10-05-stock-joins-the-video-cli-area
title: stock joins the video CLI area table
status: done
priority: P2
area: tools
owner: claude-opus-5-5-stock-cli
claimed_at: 2026-10-07T05:58:07Z
created_at: 2026-10-05T18:08:16Z
completed_at: 2026-10-07T05:59:36Z
branch:
depends_on:
  - 2026-10-05-stock-photo-slides-and-attribution
scope:
  - tools/video/cli.mjs
  - tools/video/cli.test.mjs
  - tools/video/media/cli.mjs
  - docs/videos/ILLUSTRATED.md
  - .agents/skills/youtube-video/references/visuals.md
  - tools/video/media/stock.mjs
  - tools/video/media/media.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/render/render.test.mjs
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

- [x] `node tools/video/cli.mjs stock search --query "Seoul skyline"` and
      `node tools/video/cli.mjs stock fetch --slug S --provider P --id N` run `media/stock.mjs` with
      the main CLI's exit codes; `--help` lists them beside the media stages.
- [x] `docs/videos/ILLUSTRATED.md` §圖庫照片 工具端 and
      `.agents/skills/youtube-video/references/visuals.md` name the main CLI form (add them to the
      scope when claiming; neither is bound).

## Steps

- [x] `AREAS.stock = ["media", "2026-10-05-stock-photo-slides-and-attribution"]`; `HELP` line.
- [x] `tools/video/cli.test.mjs` is receipt-bound (`tools/video/long-form/review.mjs`
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
- Done 2026-10-07 by claude-opus-5-5-stock-cli. `AREAS.stock` sends `stock` to `media/cli.mjs`
  `run`, which hands it to `stock.mjs`, so `node tools/video/cli.mjs stock search|fetch …` answers
  with the main CLI's exit codes (a usage mistake 2 through the main CLI's own catch, no token 3);
  `--help` lists both subcommands under the media stages. Scope widened to `media/cli.mjs` for
  its two comments that said the main CLI had no `stock` yet. `ILLUSTRATED.md` (§圖庫照片 table
  and "沒做、留給後面") and the youtube-video skill's `references/visuals.md` (no `.claude`
  copy exists of that file) now give the main CLI form.
- The test is in `tools/video/media/media.test.mjs` ("stock is a command of the main video CLI"),
  which imports the main CLI's `main`; it fails against the CLI before this change. It was first
  put in `tools/video/cli.test.mjs`, but that file is bound by the duration receipt and the ticket
  allows either, so it moved and no re-bind is needed.
- An independent review also found a third stale sentence under the §圖庫照片 table in
  `ILLUSTRATED.md` ("還沒做：…`AREAS` 沒列 `stock`"), removed, and two runtime hints that still
  named `media/cli.mjs`: the `next:` line after `stock search` (`media/stock.mjs`) and render's
  "not in the work directory" problem (`render/plan.mjs`). Both now name
  `node tools/video/cli.mjs`; scope widened to them and their tests (none is receipt-bound).
