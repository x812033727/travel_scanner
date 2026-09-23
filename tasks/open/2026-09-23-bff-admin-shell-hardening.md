---
id: 2026-09-23-bff-admin-shell-hardening
title: BFF and admin shell hardening: backslash redirects, dotted-path CSP gap, locale cookie flag, admin soft navigation
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-23T15:57:49Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/api/travel/[...path]/proxy-security.ts
  - apps/web/app/api/travel/[...path]/proxy-security.test.ts
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/travel/[...path]/route.test.ts
  - apps/web/proxy.ts
  - apps/web/app/[locale]/admin/template.tsx
  - apps/web/app/[locale]/admin/layout.tsx
---

# BFF and admin shell hardening: backslash redirects, dotted-path CSP gap, locale cookie flag, admin soft navigation

## Why

Four small gaps in the web layer. None is exploitable today; each is one line from being so.

1. `proxy-security.ts::safeRedirectLocation` accepts any `Location` that starts with `/`
   and not `//`. `/\evil.example/x` passes and browsers resolve it to
   `https://evil.example/x` (WHATWG treats `\` as `/` for special schemes; verified with
   Node). Every API redirect emitter today returns an absolute HTTPS URL (flight clickout
   checks scheme and host, affiliate clickout uses `allowed_hosts`, the Places photo 302
   validates the Google URI), so nothing reaches this line, but this helper is the one place
   that vets upstream redirects, and `safeNextPath` already rejects `\`.
2. The `proxy.ts` matcher `/((?!api|_next|_vercel|.*\..*).*)` skips any path containing a
   dot. No dynamic segment allows a dot today, so only the `[...rest]` 404 document renders
   without the nonce and the enforced `script-src`; that document still mounts the full
   provider tree and the third-party scripts.
3. `route.ts` sets `travel_locale` on login without `secure` (the OAuth callback in
   `_shared.ts` sets it). Preference cookie only; HSTS covers it.
4. `app/[locale]/admin/layout.tsx` runs `canAccessAdminPath` on full loads. Next.js does not
   re-render a layout on soft navigation, so a role-limited admin who follows a `<Link>` into
   a page outside their capabilities gets the shell. Every admin endpoint enforces
   `require_capability`, so data is safe.

## Definition of done

- [ ] `safeRedirectLocation` rejects any relative location containing `\` or a control
      character; test cases for `/\host`, `/\\host`, `/\/host`.
- [ ] The middleware matcher excludes only static file extensions, and a 404 document carries
      the nonce and the enforced `script-src`.
- [ ] `travel_locale` is set with the same `secure` rule everywhere.
- [ ] Soft navigation to an admin page outside the role's capabilities renders the forbidden
      state, via `admin/template.tsx` or a per-page check.

## Steps

- [ ] One PR, four commits, so a reviewer can drop any one of them.
- [ ] Run `e2e/csp.spec.ts` after the matcher change: it fails on any Report-Only violation
      and is the proof that the 404 document is now covered.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && cd apps/web && npx vitest run "app/api/travel/[...path]" && npx playwright test e2e/csp.spec.ts --project=desktop-chromium
```

## Notes

- Found in the 2026-09-23 security review (findings L3, L4, L5, L13).
