---
id: 2026-09-23-third-party-scripts-on-privileged-routes
title: Affiliate and analytics scripts load on admin and account pages
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-24T02:24:54Z
created_at: 2026-09-23T15:57:48Z
completed_at:
branch: claude/third-party-scripts-private-routes
depends_on: []
scope:
  - apps/web/app/[locale]/layout.tsx
  - apps/web/components/travelpayouts-drive.tsx
  - apps/web/components/travelpayouts-drive.test.tsx
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/analytics-provider.test.tsx
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
  - apps/web/lib/private-routes.ts
  - apps/web/lib/private-routes.test.ts
  - apps/web/components/private-route-isolation.tsx
  - apps/web/components/private-route-isolation.test.tsx
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

- [x] Neither the affiliate drive script nor the GTM script is requested on `/admin/*`,
      `/account`, `/my`, `/trips/*` (or any signed-in-only route) in any locale.
- [x] Public content routes keep both scripts and their existing behaviour (DNT/GPC opt-out,
      click counting).
- [x] A test proves the exclusion for at least `/zh-TW/admin/users` and `/zh-TW/trips`.

## Steps

- [x] Decide the mechanism: a pathname gate inside both components (`usePathname`, the same
      regex as `sanitizedPath`), or a second root layout for the privileged routes. The
      pathname gate is the smaller change and keeps one layout tree.
- [x] Apply it to `travelpayouts-drive.tsx` and to the `<Script>` in
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

### 2026-09-24 what was built (with `2026-09-24-travelpayouts-drive-loads-on-share-token`, one PR)

- **Which routes.** `apps/web/lib/private-routes.ts` lists the sections: `account`, `admin`,
  `alerts`, `forgot-password`, `line`, `login`, `my`, `register`, `share`, `share-target` and `trips`.
  That is wider than this ticket's four. The sign-in pages take a password, the LINE link
  carries a one-time token, and a share URL is itself the secret; each is worse for a
  third-party script to see than an admin table.
- **The pathname gate alone was not enough, so the owner chose full isolation (2026-09-24).**
  `TravelpayoutsDrive` and `AnalyticsProvider` return no `<Script>` on a private route, and GA4's
  `initializeGa4` waits for a public page. That only protects a document that *starts* on a
  private page. The app router swaps pages inside one document, and a script that already ran
  cannot be unloaded, so `components/private-route-isolation.tsx` does the rest:
  - A same-origin link into a private section, clicked in a document that has run either
    script, becomes a full load. The capture listener runs before `Link`, which skips a
    prevented click.
  - A navigation with no link (`router.push`) reloads once on arrival. A `sessionStorage`
    guard stops a loop and clears itself on the next clean private page.
  - The cost: on production, going from a public page to trips, my, account and the other
    private sections takes one full page load.
- **First-party analytics still runs on private pages.** It is the site's own code; `sanitizedPath`
  already keeps admin paths out and folds tokens.
- **Not fixed here:** a vendor script on a public page, in a signed-in owner's browser, can
  still call the admin API same-origin, because cookies follow the request, not the page.
  Stopping it from sending the answer anywhere is the enforced `connect-src`, filed as
  `2026-09-24-enforce-connect-src-on-private-routes`. The last Step above moved there.
- **e2e are unaffected.** Drive only loads when `NEXT_PUBLIC_SITE_URL` is production, and CI
  builds e2e with localhost. The e2e runtime API answers `ga4_enabled: false`. `stay22-script`
  runs in the CI `web` job. `csp.spec.ts` is **not** in CI and did **not** run locally on
  2026-09-24: this machine has no browser for the worktree's Playwright (build 1243), and
  downloading one needs the owner's go-ahead. This PR does not touch `csp.ts` or `proxy.ts`.
  To run it: `npx playwright install chromium`, then
  `PLAYWRIGHT_PORT=3217 npx playwright test e2e/csp.spec.ts --project=desktop-chromium`.
