---
id: 2026-09-11-guides-sitemap-and-entry-points
title: Wire /guides into the sitemap, footer and destination pages
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T15:47:19Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
  - apps/web/components/destination-guide.tsx
  - apps/web/components/destination-guide.test.tsx
  - apps/web/lib/discovery-copy.ts
---

# Wire /guides into the sitemap, footer and destination pages

## Why

`/guides` shipped in PR #398 (`2026-09-11-travel-guides-api` and `2026-09-11-travel-guides-web`),
but four pieces were left out because their files were held by `review` tasks whose pull
requests had already merged:

- `apps/web/app/sitemap.ts` lists neither `/guides` nor any article. The API already serves
  `GET /guides/sitemap`, the publication-aware list, for exactly this.
- `components/site-footer.tsx` has no link to the section.
- Destination pages do not link to their guides.
- `kinds.article` in `lib/discovery-copy.ts` still gives discovery's external articles the
  name the new first-party section now uses (攻略, and "Guides" in English).

All of those locks were released on 2026-09-11: PR #399 closed
`2026-09-10-seo-home-ssr-and-internal-links`, which held `site-footer.tsx`, and the change
that filed this task closed the rest.

## Definition of done

- [ ] The sitemap lists the guide hubs and every published article, each only in the locales
      where it is published, and an expired notice drops out of it.
- [ ] The footer and each destination page link to the guides.
- [ ] Discovery's label for external articles no longer shares the new section's name.

## Steps

- [ ] Sitemap entries from `GET /guides/sitemap`, with cases in `app/sitemap.test.ts`.
- [ ] Footer link and destination-page cross-link.
- [ ] Relabel `kinds.article` in every locale of `lib/discovery-copy.ts`.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run build:web && npm --workspace @travel-scanner/web run start
curl -s localhost:3000/sitemap.xml | grep -c /guides
```

## Notes

- `sitemap.ts` is `force-dynamic` on purpose (`2026-09-10-seo-robots-sitemap`): at build time
  the site URL can be missing and no API is reachable. The guides list is therefore fetched per
  request; when that fetch fails, drop the guide entries, never the whole sitemap.
- An article advertises hreflang only for the locales it is published in
  (`2026-09-11-travel-guides-web`), so its sitemap alternates must match.
- If the footer or destination link needs new copy, add the `messages/*` files it lives in to
  `scope` before editing them.
