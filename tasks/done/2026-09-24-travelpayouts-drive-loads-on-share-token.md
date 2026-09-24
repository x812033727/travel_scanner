---
id: 2026-09-24-travelpayouts-drive-loads-on-share-token
title: Travelpayouts Drive loads on share token pages
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-24T02:25:06Z
created_at: 2026-09-24T00:30:03Z
completed_at: 2026-09-24T02:47:50Z
branch: claude/third-party-scripts-private-routes
depends_on: []
scope:
  - apps/web/components/travelpayouts-drive.tsx
  - apps/web/components/travelpayouts-drive.test.tsx
---

# Travelpayouts Drive loads on share token pages

## Why

The URL of a shared trip, `/{locale}/share/{token}`, is the secret: anyone holding it can
read the trip. The site's own rule is that no third-party script shares a document with
that URL (`docs/adsense-feasibility.md` 4.6; `apps/web/lib/adsense.ts` keeps AdSense off
`/share/`). That rule is enforced for AdSense only.

`<TravelpayoutsDrive>` is mounted in `apps/web/app/[locale]/layout.tsx:129` for every locale
route. Its only gates are the production origin and DNT/GPC
(`components/travelpayouts-drive.tsx`), so on mokaair.com the affiliate script from
`emrldtp.cc` runs on `/share/{token}` and can read `location.href`, token included. No
misuse is known; this is the exposure if the vendor script logs page URLs, which link
converters commonly do.

The open ticket `2026-09-23-third-party-scripts-on-privileged-routes` covers the same
component for `/admin`, `/account`, `/my` and `/trips`, but not `/share`. Found on
2026-09-24 while planning revenue channels.

## Definition of done

- [x] No request to the Drive script's host is made on `/{locale}/share/{token}` in any locale.
- [x] Public content pages (articles, destinations) keep the script and its DNT/GPC opt-out.
- [x] A component test covers a share path.

## Steps

- [x] Use the same mechanism as `2026-09-23-third-party-scripts-on-privileged-routes`
      (a pathname gate inside the component is the smaller change). If one agent takes
      both, do them in one PR; the scopes overlap on `travelpayouts-drive.tsx`.
- [x] Add `/share/` to the excluded paths and a test for it.

## How to verify

```bash
cd apps/web && npx vitest run components/travelpayouts-drive.test.tsx
```

On production after a deploy, open any share link with the Network panel open: no request
to `emrldtp.cc`.

## Notes

- Share pages already carry only first-party form-POST offers (`components/shared-trip-view.tsx`),
  so removing Drive there loses no tracked affiliate link that the site itself renders.
- 2026-09-24: done together with `2026-09-23-third-party-scripts-on-privileged-routes` in
  one PR, as the Steps suggested. Claimed with `--force` because that ticket, held by the same
  owner on the same branch, already covered `travelpayouts-drive.tsx`. `share` is one of the
  sections in `apps/web/lib/private-routes.ts`. A share link opened from outside the site
  loads a document with no Drive script. Reaching a share page by an in-site link, after a
  public page already ran Drive, becomes a full load (`components/private-route-isolation.tsx`).
  The design notes are in the other ticket.
