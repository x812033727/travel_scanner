---
id: 2026-09-27-news-images-under-guides-news-assets
title: News images under /guides/news-assets answer 500 in production
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-27T06:41:12Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/guides/news-assets
---

# News images under /guides/news-assets answer 500 in production

## Why

Every request to `/guides/news-assets/<file>` on mokaair.com answers 500, so the hero
and diagram images that the hourly AI news pipeline generates cannot be shown.
`apps/web/app/guides/news-assets/[filename]/route.ts` builds its upstream as
`new URL("/api/travel/news-assets/<file>", request.url)` and fetches it. That sends the
request back out through the site's own origin instead of calling the API. Behind nginx,
TLS ends at nginx and the Next server speaks plain HTTP, but `request.url` resolves to an
`https://` URL whose port answers plain HTTP. `fetch` then fails with
`ERR_SSL_WRONG_VERSION_NUMBER`, nothing catches the error, and Next answers 500. The
exact origin `request.url` carries in production was not captured; the TLS error only
shows that the other end does not speak TLS. Locally the dev server is plain `http://`,
so the self-fetch works there. No test sits next to the route, so nothing caught this.

Found on 2026-09-27 during the post-deploy log check of `243b0f2f`. The route has not
changed since #694 (2026-09-23), so that deploy did not cause it:

- web container, 06:34:14Z and 06:34:15Z: `TypeError: fetch failed` with cause
  `ERR_SSL_WRONG_VERSION_NUMBER`; the stack is in the server chunk built from this route.
- `GET https://mokaair.com/guides/news-assets/0123456789abcdef0123456789abcdef-hero.webp`
  → 500.
- `GET https://mokaair.com/api/travel/news-assets/0123456789abcdef0123456789abcdef-hero.webp`
  → 404 `application/json`, so the BFF proxy and the API side work.

No reader is affected yet. Production holds 182 `news_assets` rows, but the 8 published
news articles predate the image step and do not reference `/guides/news-assets/`; the
newest, `tech-news-nvidia-ai-agent-security-20260921`, contains no occurrence. Guide
images render through a plain `<img>` (`components/guides/guide-image.tsx`), so the
browser requests this route directly. The first published article that carries generated
images will show broken images.

Every other server-side caller in `apps/web` reads
`process.env.API_INTERNAL_URL || "http://localhost:8000"` and calls `${base}/api/v1/...`
directly, for example `app/[locale]/out/guides/[guideId]/route.ts` and
`app/api/travel/[...path]/route.ts`. The API serves these files at
`/api/v1/news-assets/<file>` (`app/news_automation/router.py`, mounted with the `/api/v1`
prefix in `app/main.py`). This route is the only one in `apps/web` that derives an
upstream from `request.url`.

## Definition of done

- [ ] On production, `/guides/news-assets/<well-formed name that does not exist>.webp`
      answers 404 instead of 500, and an existing asset answers 200 with `image/webp` or
      `image/svg+xml`.
- [ ] After the deploy, the web container logs no `ERR_SSL_WRONG_VERSION_NUMBER`.
- [ ] A route test pins the upstream to `API_INTERNAL_URL`. It also covers a 404 passed
      through, a wrong content type (502), an upstream network error (502, not an
      unhandled throw) and a HEAD request without a body.

## Steps

- [ ] Fetch `${API_INTERNAL_URL || "http://localhost:8000"}/api/v1/news-assets/<file>`
      directly and stop deriving the upstream from `request.url`.
- [ ] Catch an upstream fetch failure and answer 502, as the BFF proxy does.
- [ ] Keep the filename pattern and the content-type allowlist. Consider also applying the
      5 MiB cap that `app/api/travel/[...path]/route.ts` sets for news assets
      (`MAX_NEWS_ASSET_BYTES`).
- [ ] Add `route.test.ts` next to the route, modelled on the news-asset case in
      `app/api/travel/[...path]/route.test.ts`.
- [ ] After merge, deploy through skill `deploy` and run the checks below.

## How to verify

```bash
cd apps/web && npx vitest run app/guides/news-assets
# after the deploy: expect 404 (it was 500 on 2026-09-27)
curl -s -o /dev/null -w '%{http_code}\n' https://mokaair.com/guides/news-assets/0123456789abcdef0123456789abcdef-hero.webp
```

On the host, with the owner's OK and following skill `deploy`'s SSH rules, this should
print 0:
`docker compose -f docker-compose.prod.yml logs --since 30m web | grep -c ERR_SSL_WRONG_VERSION_NUMBER`.
For the 200 check, take a real file name from a news preview in `/admin/news`, or read
one from `news_assets` with the owner's OK.

## Notes

- `app/api/travel/[...path]/route.ts` already proxies `news-assets/<file>` with its own
  checks. Routing through it would keep a single code path, but calling the API directly
  is what every other server route in `apps/web` does.
- Not in scope: the article renderer and the API. If the fix needs a shared helper in
  `apps/web/lib`, widen the scope in this file and say why.
