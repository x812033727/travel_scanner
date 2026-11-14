# Admin topic pools

`GET /api/v1/admin/video-pools` and its `/{series}/themes`, `/{series}/themes/{id}` and
`/{series}/expansions` children require `content.read` and read the immutable
`data/pools.json` inside the API image. The video admin opens them through
`/zh-TW/admin/videos?tab=pools`. Viewing changes nothing: themes are editorial candidates
(`EDITORIAL_THEMES_NOT_SCRIPTS`), not approved scripts or production requests.

The bundle is generated from the two topic pools under `docs/videos/history-curiosity/pool`
and `docs/videos/so-thats-why/pool` (themes with independent audience scores and their
improvement rounds, manifest counts, expansion batches and checkpoints):

```sh
node tools/video/pool-admin/bundle.mjs build
node tools/video/pool-admin/bundle.mjs check
node --test tools/video/pool-admin/bundle.test.mjs
```

Either pool's `cli.mjs build` rewrites the bundle as well, so it never lags a rebuilt pool;
`npm run test:tools` fails when the committed bundle differs from the pools. Deployment ships
it through the API Dockerfile `COPY . .`; no migration or import step is needed. A missing
or invalid bundle returns `503 video_pools_unavailable` without a partial or stale answer.

`status` filters themes: `producible` (long and passed the material review and the 6.5
audience bar), `reserve` (long but held back), `short`, or `all`. `category`, `min_score`
and `q` (id, title or core question) narrow it further; `sort` is `rank` (audience rank,
unscored last) or `id`; `page_size` is at most 100.
