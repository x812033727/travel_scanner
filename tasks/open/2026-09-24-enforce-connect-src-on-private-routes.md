---
id: 2026-09-24-enforce-connect-src-on-private-routes
title: Enforce connect-src on private routes
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-24T02:30:51Z
completed_at:
branch:
depends_on:
  - 2026-09-23-third-party-scripts-on-privileged-routes
scope:
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
  - apps/web/proxy.ts
---

# Enforce connect-src on private routes

## Why

The follow-up step of `2026-09-23-third-party-scripts-on-privileged-routes`, filed on its
own so it is not lost when that ticket closes.

That ticket keeps Travelpayouts Drive and GA4's `gtag.js` out of every document that shows
a private page (`apps/web/lib/private-routes.ts`). It does not close the whole exposure.
A vendor script running on a *public* page, in the browser of a signed-in owner, can still
call `/api/travel/admin/...` same-origin with the owner's cookies. Cookies follow the request
URL, not the page. It can then send the answer anywhere, because `connect-src` is only
Report-Only (`apps/web/lib/csp.ts`, `buildStrictContentSecurityPolicy`). An enforced
`connect-src` stops that last step, the exfiltration.

The private routes are the right place to start. After the 2026-09-23 change no
third-party script runs in their documents, so their legitimate connections are the site
itself plus the few first-party integrations those pages use. `csp.ts` explains why
enforcing `connect-src` site-wide is not safe yet: it names no Google Maps host, and no
local run can prove the map works.

## Definition of done

- [ ] Documents for the sections in `PRIVATE_SECTIONS` (`lib/private-routes.ts`) get an
      enforced `connect-src` that lists only what those pages actually connect to.
- [ ] Nothing on those pages breaks in production: trips (maps, routes), account, admin,
      LINE linking, share.
- [ ] `csp.test.ts` pins the enforced directive for a private route and proves public
      routes are unchanged.

## Steps

- [ ] List every `connect-src` origin the private sections hit. **Nothing collects the
      Report-Only violations today**: there is no `report-uri`, `report-to` or
      `Reporting-Endpoints` anywhere in `csp.ts`, `proxy.ts` or `next.config.ts` (checked
      2026-09-24), so they only reach each visitor's own console. Either add a small
      first-party report endpoint first and collect for a week, or walk every private page
      in production with DevTools open, including a trip with a real map key.
- [ ] Build the enforced directive from that list. `proxy.ts` already knows the path
      (`adsenseRequestGate` is the precedent for a per-route policy).
- [ ] Watch the planner's map and route calls closely; Google Maps hosts are the known gap.

## How to verify

```bash
cd apps/web && npx vitest run lib/csp.test.ts && npx playwright test e2e/csp.spec.ts --project=desktop-chromium
```

In production, open a trip with the map and the admin console with DevTools open: no CSP
violation in the console.

## Notes

- Filed 2026-09-24 while closing `2026-09-23-third-party-scripts-on-privileged-routes`
  (security review 2026-09-23, finding M2).
