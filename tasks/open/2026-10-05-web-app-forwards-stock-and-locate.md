---
id: 2026-10-05-web-app-forwards-stock-and-locate
title: Web app forwards stock and locate media routes
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-10-05T18:08:15Z
completed_at:
branch:
depends_on:
  - 2026-10-05-stock-photo-source-endpoint
scope:
  - apps/web/app/api/video/media/[...path]/forward.ts
  - apps/web/app/api/video/media/[...path]/route.test.ts
---

# Web app forwards stock and locate media routes

## Why

nginx exposes only the web app, so every media call of the video tool goes through
`apps/web/app/api/video/media/[...path]/forward.ts`, whose `mediaRoute()` whitelists the routes it
forwards: `status`, `images`, `clips`, `music`, `judge`, `jobs/<uuid>` and `files/<slug>/<sha256>`.
The API has since gained `POST /video/media/locate` (`2026-10-05-media-locate-subject-boxes`) and
`POST /video/media/stock/search` + `POST /video/media/stock/fetch`
(`2026-10-05-stock-photo-source-endpoint`), and the tool calls them (`tools/video/media/client.mjs`
`locate`, `stockSearch`, `stockFetch`), but on the live site each answers 404
`video_media_route_unknown` from the forwarder before the API is reached. `stock search` reports
it as "the site does not serve the stock photo routes yet"; `locate` reports it as the tool's own
mistake.

## Definition of done

- [ ] `POST /api/video/media/locate`, `POST /api/video/media/stock/search` and
      `POST /api/video/media/stock/fetch` with a video tool token reach the API (JSON routes;
      `stock/fetch` runs a vendor download inside the API, so give it the job timeout, not the short one).
- [ ] Any other `stock/*` or `locate/*` path still answers 404 `video_media_route_unknown`.
- [ ] `route.test.ts` covers the three routes and a refused sibling.

## Steps

- [ ] `mediaRoute`: `locate` (POST, judge timeout), `stock` with `search` or `fetch` as the one
      remaining segment (POST; search short or submit timeout, fetch the job timeout).
- [ ] Tests beside the existing ones in `route.test.ts`.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web -- apps/web/app/api/video/media
# after a deploy, with a video tool token on the machine:
node tools/video/media/cli.mjs stock search --query "Seoul skyline"
```

## Notes

- Found while building `2026-10-05-stock-photo-slides-and-attribution`; the API side and the tool
  side are done, this is the only piece between them on the live site.
- Bodies are small JSON (`JSON_MAX_BYTES`); nothing streams, so the `json` kind fits all three.
