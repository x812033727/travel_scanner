---
id: 2026-09-23-third-party-scripts-on-privileged-routes
title: Affiliate and analytics scripts load on admin and account pages
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-23T15:57:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/[locale]/layout.tsx
  - apps/web/components/travelpayouts-drive.tsx
  - apps/web/components/travelpayouts-drive.test.tsx
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/analytics-provider.test.tsx
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
---

# Affiliate and analytics scripts load on admin and account pages

## Why

`app/[locale]/layout.tsx` mounts `<TravelpayoutsDrive>` (the affiliate script served from
`emrldtp.cc`) and `<AnalyticsProvider>` (the GTM `gtag.js` script) for every locale route, and
`/admin/*`, `/account`, `/my` and `/trips/*` all live under that layout. The only gate is
DNT/GPC; `analytics-provider.tsx` hides admin paths from the reported URL (`sanitizedPath`)
but still loads the script there.

The enforced CSP covers `script-src` only. `connect-src` is still Report-Only, and
`'strict-dynamic'` trusts whatever those scripts load next. A compromised or rogue vendor
script therefore runs inside the owner's admin document, can call `/api/travel/admin/...`
same-origin (the Origin check passes and `travel_access` plus `admin_step_up` ride along),
and can send the result anywhere. The `(ads-public)` root already treats AdSense as a
document-lifetime risk and isolates it; affiliate and analytics scripts never got the same
treatment on privileged routes. No vendor compromise is known. This is the blast radius if
one happens.

## Definition of done

- [ ] Neither the affiliate drive script nor the GTM script is requested on `/admin/*`,
      `/account`, `/my`, `/trips/*` (or any signed-in-only route) in any locale.
- [ ] Public content routes keep both scripts and their existing behaviour (DNT/GPC opt-out,
      click counting).
- [ ] A test proves the exclusion for at least `/zh-TW/admin/users` and `/zh-TW/trips`.

## Steps

- [ ] Decide the mechanism: a pathname gate inside both components (`usePathname`, the same
      regex as `sanitizedPath`), or a second root layout for the privileged routes. The
      pathname gate is the smaller change and keeps one layout tree.
- [ ] Apply it to `travelpayouts-drive.tsx` and to the `<Script>` in
      `analytics-provider.tsx` (page-view events for admin are already suppressed; keep that).
- [ ] Extend the component tests; run the `csp` and `stay22-script` Playwright specs to
      confirm public pages are unchanged.
- [ ] Follow-up, separate PR: with the scripts off privileged routes, promote `connect-src`
      from Report-Only to enforced for those routes first.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && cd apps/web && npx vitest run components/travelpayouts-drive.test.tsx components/analytics-provider.test.tsx
```

In a browser signed in as admin, open `/zh-TW/admin/users` and check the Network panel: no
request to `emrldtp.cc` or `googletagmanager.com`.

## Notes

- Found in the 2026-09-23 security review (finding M2).
- SRI is not an option: the drive script URL serves changing content.
