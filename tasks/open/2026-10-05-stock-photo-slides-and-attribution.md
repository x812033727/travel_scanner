---
id: 2026-10-05-stock-photo-slides-and-attribution
title: Stock photos on slides and the assets list credited in the description
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:26Z
completed_at:
branch:
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

- [ ] `stock fetch` (through `media/cli.mjs`) stores the photo under `<workdir>/stock/<sha256>.<ext>`
      and appends `{path, source, license, author, url}` to `video.json.assets`.
- [ ] The `screenshot` template accepts a `stock/<sha256>.<ext>` path resolved under the work
      directory (the fake origin already serves `/work/…`) and an optional `credit`; `sceneAssets`
      hashes the bytes into the frame key.
- [ ] `composeDescription` appends a 「圖片來源」 block from `assets[]`; `package/metadata.mjs`
      passes them; the description stays under the 5,000-byte limit (a ≤ 300-byte slack noted).

## Steps

- [ ] `media/stock.mjs` (`search`, `fetch`), `client.mjs`, tests with a fake site.
- [ ] `templates.mjs` path rule + credit, `render/plan.mjs sceneAssets`, `render/cli.mjs`; tests.
- [ ] `core/metadata.mjs`, `package/metadata.mjs`; `visuals.md`, `ILLUSTRATED.md`.

## How to verify

```bash
node --test tools/video/templates/templates.test.mjs tools/video/render/render.test.mjs tools/video/media/media.test.mjs tools/video/core/metadata.test.mjs
node tools/video/cli.mjs render --slug <video> && node tools/video/cli.mjs package --slug <video>   # description carries the credits
```

## Notes

- No bound file: no new template name (`TEMPLATES` lives in the bound `core/schema.mjs`), the
  `screenshot` template is extended instead; `lint.mjs` (bound) is not touched.
