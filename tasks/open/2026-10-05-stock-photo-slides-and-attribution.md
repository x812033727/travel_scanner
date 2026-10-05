---
id: 2026-10-05-stock-photo-slides-and-attribution
title: Stock photos on slides and the assets list credited in the description
status: in-progress
priority: P2
area: tools
owner: claude-fable-5-1-stockslides
claimed_at: 2026-10-05T17:47:49Z
created_at: 2026-10-05T16:08:26Z
completed_at:
branch: claude/stock-photo-slides
depends_on:
  - 2026-10-05-stock-photo-source-endpoint
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
  - tools/video/media/stock.mjs
  - tools/video/media/cli.mjs
  - tools/video/media/client.mjs
  - tools/video/media/media.test.mjs
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/package/metadata.mjs
  - .agents/skills/youtube-video/references/visuals.md
  - docs/videos/ILLUSTRATED.md
---

# Stock photos on slides and the assets list credited in the description

## Why

`video.json` validates an `assets[{path, source, license}]` list that nothing reads, and
templates can only load pictures from repository paths. With the stock endpoint
(`2026-10-05-stock-photo-source-endpoint`) a slide can show a real photo; the credit must
reach the description (never burnt in, the owner's rule) and the picture's bytes must be in
the frame key so a swapped photo re-renders.

## Definition of done

- [x] `stock fetch` (through `media/cli.mjs`) stores the photo under `<workdir>/stock/<sha256>.<ext>`
      and appends `{path, source, license, author, url}` to `video.json.assets`.
- [x] The `screenshot` template accepts a `stock/<sha256>.<ext>` path resolved under the work
      directory (the fake origin already serves `/work/…`) and an optional `credit`; `sceneAssets`
      hashes the bytes into the frame key.
- [x] `composeDescription` appends a 「圖片來源」 block from `assets[]`; `package/metadata.mjs`
      passes them; the description stays under the 5,000-byte limit (a ≤ 300-byte slack noted).

## Steps

- [x] `media/stock.mjs` (`search`, `fetch`), `client.mjs`, tests with a fake site.
- [x] `templates.mjs` path rule + credit, `render/plan.mjs sceneAssets`, `render/cli.mjs`; tests.
- [x] `core/metadata.mjs`, `package/metadata.mjs`; `visuals.md`, `ILLUSTRATED.md`.

## How to verify

```bash
node --test tools/video/templates/templates.test.mjs tools/video/render/render.test.mjs tools/video/media/media.test.mjs tools/video/core/metadata.test.mjs
node tools/video/cli.mjs render --slug <video> && node tools/video/cli.mjs package --slug <video>   # description carries the credits
```

## Notes

- No bound file: no new template name (`TEMPLATES` lives in the bound `core/schema.mjs`), the
  `screenshot` template is extended instead; `lint.mjs` (bound) is not touched.

### Done (2026-10-05, branch `claude/stock-photo-slides`, on top of `claude/stock-photo-source` / #1304)

- `media/client.mjs`: `stockSearch` → `POST stock/search`, `stockFetch` → `POST stock/fetch`, the
  token and User-Agent as every call; `video_media_stock_unavailable` is the owner's (exit 3),
  `video_media_stock_not_found` the tool's (a wrong id, exit 2, not retried),
  `video_media_stock_failed` retried like `video_media_locate_failed`, 429 with its Retry-After.
- `media/stock.mjs` (new): `stock search` prints provider, id, size and shape, the vendor's credit
  line, the photo page and alt, the totals, `problems`, the notices each vendor's API terms ask for
  ("Photos provided by Pexels", "Images from Pixabay"), the Pixabay 24 h note and the next command;
  `stock fetch` calls the server, downloads with `downloadFile` to `<workdir>/stock/<sha256>.<ext>`
  (extension from `content_type`; a present copy with the right hash is not downloaded again, a
  torn one is), and writes `{path, source: credit.text, license, author, url}` into `video.json`
  `assets[]` (replacing an entry with the same path; a document without `assets` gets it before
  `scenes`; the file is rewritten with 2-space JSON like the automation does). Free: no ledger entry.
- `media/cli.mjs`: `stock` in `STAGES` (so an older checkout names this ticket), a `HELP`, and a
  `main` + direct-run block so `node tools/video/media/cli.mjs stock …` works: `tools/video/cli.mjs`
  (`AREAS`) is outside this scope, so the main CLI does not know `stock` yet (follow-up ticket
  filed). No top-level await, for the same reason cli.mjs has none.
- `templates.mjs`: `STOCK_PATH`/`isStockPath` (`stock/<64 hex>.png|jpg|webp`, lowercase only),
  `workUrl` (`/work/…`, the renderer's fake origin), the `screenshot` spec takes either path and an
  optional one-line `credit` (≤ 60 characters, `CREDIT_MAX_CHARS`); the credit is a dark pill in the
  picture's corner, drawn after the highlight box so it sits above the scrim; its CSS rides in the
  page only when a credit is set (`TEMPLATE_CSS.screenshot` is a function of the data), so pages
  without one and `theme.css` are byte for byte what they were: no existing frame key moves.
- `render/plan.mjs`: `assetFile(asset, {root, workdir})`; `renderProblems(doc, root, {workdir})`
  demands a stock image be listed in `assets[]` (else the description has no credit) and, with a
  workdir, fetched; `renderPlan(..., {workdir})` hashes the photo's bytes into the scene's keys.
  `render/cli.mjs` resolves the workdir before the data check and passes it; `run` honours
  `ctx.openRenderer` like `thumbnailsOnly`, which is what the end-to-end render test uses.
- `core/metadata.mjs`: `LABELS[*].pictures` + `parens`, `ASSET_FIELDS`, `creditedAssets` (only
  entries with `author` or `url`: the own diagrams that eight existing videos list stay out, so their
  descriptions and the publish approvals bound to `upload/metadata.json` do not move), `creditLine`,
  `pictureCredits` (after sources, before hashtags), `creditBytes`; `composeDescription({assets})`.
  `package/metadata.mjs` passes `doc.assets` for every locale and, when the limit is passed, says
  how many bytes the credits added (lint composes without them).
- Byte budget measured in the tests: two credit lines cost 200–300 bytes with the block's header;
  about 110–130 bytes a line. Written into ILLUSTRATED.md and visuals.md as "leave ≈130 bytes a
  photo under lint's count; 300 for two".
- Tests: fake site + a 1×1 PNG constant (no network, no ffmpeg); `render` end to end with a fake
  renderer (draws from `/work/stock/…`, reuses, redraws on new bytes, refuses a missing file or
  entry). No real browser in this container, so the credit pill was not looked at in Chromium.
- Not measured live: no Pexels/Pixabay key here, and the web app cannot forward the calls yet
  (below), so the first real `stock search` should check the printed credits against the photo pages.

### Noticed, not fixed (tickets filed)

- `apps/web/app/api/video/media/[...path]/forward.ts` `mediaRoute` whitelists status/images/clips/
  music/judge/jobs/files only: `POST stock/search`, `POST stock/fetch` (and `POST locate` from
  `2026-10-05-media-locate-subject-boxes`) answer 404 `video_media_route_unknown` on the live
  site. `stock.mjs` turns that into an owner message. Ticket `2026-10-05-web-app-forwards-stock-and-locate`.
- `tools/video/cli.mjs` `AREAS` lacks `stock` (one line + HELP); `tools/video/cli.test.mjs` is
  receipt-bound. Ticket `2026-10-05-stock-joins-the-video-cli-area`.
- `docs/videos/README.md` §說明欄 (bound) lists four description parts; the fifth, 圖片來源, is
  documented in ILLUSTRATED.md instead.
- `video_media_store_full` (507) is retried five times with backoff before exit 4; it is really the
  owner's. Left as it was (the DoD asked for locate's classification).
- `render/repeat.mjs` plans without a workdir, so a stock scene's key there lacks the bytes; it
  compares its own runs with each other, so it still works.
