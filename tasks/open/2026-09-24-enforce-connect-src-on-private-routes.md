---
id: 2026-09-24-enforce-connect-src-on-private-routes
title: Administrators never load third-party scripts (was: enforce connect-src on private routes)
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-24T05:09:19Z
created_at: 2026-09-24T02:30:51Z
completed_at:
branch: claude/admins-skip-third-party-scripts
depends_on:
  - 2026-09-23-third-party-scripts-on-privileged-routes
scope:
  - apps/web/lib/third-party-audience.ts
  - apps/web/components/third-party-audience.tsx
  - apps/web/components/third-party-audience.test.tsx
  - apps/web/components/travelpayouts-drive.tsx
  - apps/web/components/travelpayouts-drive.test.tsx
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/analytics-provider.test.tsx
  - apps/web/app/[locale]/layout.tsx
---

# Administrators never load third-party scripts (was: enforce connect-src on private routes)

## Why

The residual risk after `2026-09-23-third-party-scripts-on-privileged-routes` (security review
2026-09-23, finding M2) is a vendor script on a *public* page running in a signed-in
administrator's browser. Cookies follow the request, not the page. So that script can call
`/api/travel/admin/...` same-origin with the owner's session and read the answer. No vendor
compromise is known; this is the blast radius if one happens.

**This ticket was first filed as "enforce `connect-src` on private routes", and that premise
was wrong.** Found 2026-09-24 when starting the work:

- After PR #711 no third-party script runs in a private document at all. `script-src` is
  already enforced (nonce + `'strict-dynamic'`), so an injected script does not run either.
  A `connect-src` on private routes would guard against a risk that is essentially gone.
- The remaining risk plays out in a public document. Enforcing `connect-src` there would
  still have to allow GA and Travelpayouts' own hosts, and a compromised vendor script can
  send the data to those.
- Inventory for the record: of the private pages, only a trip's map (Google Maps JS,
  `components/route-map.tsx`; Naver Maps) connects to another origin. Everything else is
  same-origin. The site has no CSP report endpoint (`report-uri`, `report-to`), so
  Report-Only violations reach nobody.

What closes the risk is the owner's decision of 2026-09-24: an administrator's browser never
loads Travelpayouts Drive or GA4's `gtag.js`, on any page. Ordinary readers are unaffected.

## Definition of done

- [x] With an administrator signed in, no page (public or private) requests `emrldtp.cc` or
      `googletagmanager.com`.
- [x] Signed-out readers load both scripts on public pages as before. Signed-in readers who
      are not administrators do too, once `/auth/me` has answered.
- [x] Tests prove the admin, unknown-role and late-clearance cases.

## Steps

- [x] `lib/third-party-audience.ts`: a document-level state (`pending`, `allowed`, `blocked`)
      that both script components read. It is a module store because both sit above the
      session provider in the layout. `blocked` is final for the document: the session
      provider remounts on sign-out, so component state would forget it.
- [x] `components/third-party-audience.tsx` inside `HeaderSessionProvider` sets it from
      `/auth/me`. On an ads document, which never asks `/auth/me`, a session cookie means
      `blocked`.
- [x] `TravelpayoutsDrive` and `AnalyticsProvider` load only when `allowed`. GA4 starting late
      sends the page view first-party analytics already counted, once.
- [x] Tests; full web checks.

## How to verify

```bash
cd apps/web && npx vitest run components/third-party-audience.test.tsx components/travelpayouts-drive.test.tsx components/analytics-provider.test.tsx
```

On production after a deploy:

1. Signed out: an article page loads `emrldtp.cc` and `gtag.js`.
2. Signed in as the administrator (the owner signs in inside the browser): the same article
   and the home page load neither.

## Notes

- Considered and not chosen, 2026-09-24:
  - Enforcing `connect-src` on private routes (above).
  - Dropping the scripts for every signed-in reader. That would also shield members' trips
    from a compromised vendor, but costs Drive link conversion and GA for all members. The
    owner chose administrators only; revisit if members' data becomes the concern.
- 2026-09-24: done on `claude/admins-skip-third-party-scripts`. Full web checks pass (300 files,
  3,274 tests; lint, typecheck, i18n). The admin, unknown-role and late-clearance tests fail on the
  pre-change components. The production check as an administrator needs the owner to sign in inside
  a browser; it is listed under How to verify and reported in the session, not assumed here.
