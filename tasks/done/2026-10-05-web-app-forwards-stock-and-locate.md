---
id: 2026-10-05-web-app-forwards-stock-and-locate
title: Web app forwards stock and locate media routes
status: done
priority: P1
area: web
owner: claude-fable-5-1-forward
claimed_at: 2026-10-05T18:18:03Z
created_at: 2026-10-05T18:08:15Z
completed_at: 2026-10-05T18:31:46Z
branch: claude/web-forward-stock-locate
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

- [x] `POST /api/video/media/locate`, `POST /api/video/media/stock/search` and
      `POST /api/video/media/stock/fetch` with a video tool token reach the API (JSON routes;
      `stock/fetch` runs a vendor download inside the API, so give it the job timeout, not the short one).
- [x] Any other `stock/*` or `locate/*` path still answers 404 `video_media_route_unknown`.
- [x] `route.test.ts` covers the three routes and a refused sibling.

## Steps

- [x] `mediaRoute`: `locate` (POST, judge timeout), `stock` with `search` or `fetch` as the one
      remaining segment (POST; search short or submit timeout, fetch the job timeout).
- [x] Tests beside the existing ones in `route.test.ts`.

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
- 2026-10-05 (claude-fable-5-1-forward): claimed with `--force` over the open dependency
  `2026-10-05-stock-photo-source-endpoint`, whose PR #1304 is still open (as is #1294 for
  `locate`): `mediaRoute()` is a path whitelist, so the web change compiles and its tests pass
  without the API routes. Until those PRs land, the live API answers these paths with its own 404
  instead of the forwarder's `video_media_route_unknown`. The ticket file itself came from the
  branch of #1306, which filed it.
- Deadlines: `locate` takes the judge deadline (180 s) because the API books and runs it like a
  judge call with another Gemini question. `stock/search` takes the submit deadline (90 s), not
  the short one: `stock.search` asks each configured vendor in turn with a 20 s client, so two
  vendors can need more than 30 s. `stock/fetch` takes the job deadline (240 s): the API streams
  the photo from the vendor under `video_media_fetch_timeout_seconds` (default 240 s), the same
  wait a poll that runs a vendor download has, and nginx allows 300 s.
- Verified on the branch: `npm run lint:web`, `npm run typecheck:web`,
  `npx vitest run app/api/video/media` (8 tests) and `npm run check:tasks` green; reverse check:
  with `forward.ts` reverted to main the new test fails on the three routes.
- Not done here: the post-deploy `stock search` line in How to verify needs #1294 and #1304
  deployed and a video tool token on the machine.
