---
id: 2026-09-23-bff-admin-shell-hardening
title: BFF and admin shell hardening: backslash redirects, dotted-path CSP gap, locale cookie flag, admin soft navigation
status: in-progress
priority: P3
area: web
owner: claude-opus-5-5-bff-hardening
claimed_at: 2026-10-02T14:27:38Z
created_at: 2026-09-23T15:57:49Z
completed_at:
branch: claude/bff-admin-shell-hardening
depends_on: []
scope:
  - apps/web/app/api/travel/[...path]/proxy-security.ts
  - apps/web/app/api/travel/[...path]/proxy-security.test.ts
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/travel/[...path]/route.test.ts
  - apps/web/proxy.ts
  - apps/web/proxy.test.ts
  - apps/web/e2e/csp.spec.ts
  - apps/web/lib/csp.ts
  - apps/web/app/ads.txt/route.ts
  - apps/web/app/llms.txt/route.ts
  - apps/web/i18n/routing.ts
  - apps/web/i18n/routing.test.ts
  - apps/web/app/api/auth/oauth/_shared.ts
  - apps/web/components/auth-form.tsx
  - apps/web/components/header-session.tsx
  - apps/web/app/[locale]/admin/template.tsx
  - apps/web/app/[locale]/admin/template.test.tsx
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

- [x] `safeRedirectLocation` rejects any relative location containing `\` or a control
      character; test cases for `/\host`, `/\\host`, `/\/host`.
- [x] The middleware matcher excludes only static file extensions, and a 404 document carries
      the nonce and the enforced `script-src`.
- [x] `travel_locale` is set with the same `secure` rule everywhere.
- [x] Soft navigation to an admin page outside the role's capabilities renders the forbidden
      state, via `admin/template.tsx` or a per-page check.

## Steps

- [x] One PR, four commits, so a reviewer can drop any one of them.
- [x] Run `e2e/csp.spec.ts` after the matcher change: it fails on any Report-Only violation
      and is the proof that the 404 document is now covered.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && cd apps/web && npx vitest run "app/api/travel/[...path]" && npx playwright test e2e/csp.spec.ts --project=desktop-chromium
```

## Notes

- Found in the 2026-09-23 security review (findings L3, L4, L5, L13).
- 2026-10-02, claude-opus-5-5-bff-hardening: done as four commits, one per finding, each with
  a test written first and seen failing.
  1. Redirects. Relative locations now get `lib/navigation.ts` `safeNextPath`'s test (no
     `//`, no `\`, no control character) instead of a copy of it. The test also covers tab and
     newline (`/\t/evil.example` resolves off-site because browsers drop them before parsing),
     keeps `/%5C...` and ordinary paths forwarding unchanged, and a `route.test.ts` case shows
     the BFF answering 502 `unsafe_upstream_redirect` instead of a 302 to `/\evil.example/x`.
  2. Matcher. Skips `api`, `_next`, `_vercel`, `.well-known/` and paths that end in one of
     avif css csv gif html ico jpe?g js json map mjs mp3 mp4 otf pdf png svg ttf txt wasm webm
     webmanifest webp woff2? xml zip. `.well-known/` stays out because nginx proxies it to Next
     and Apple reads an extensionless association file there. `proxy.test.ts` runs the real
     config through Next's `unstable_doesMiddlewareMatch` and samples one file per extension
     found in `public/` (case-sensitive, like the matcher), plus the metadata files and dotted
     route handlers. Left as they are, on purpose: a 404 for a path that itself ends in one of
     those extensions (`/zh-TW/x.png`) still has no nonce, and a junk path with no locale
     (`/foo.bar`) now takes one 307 to `/zh-TW/foo.bar` before its 404. Comments in
     `lib/csp.ts`, `app/ads.txt/route.ts` and `app/llms.txt/route.ts` that said "any path with
     a dot" are corrected. `e2e/csp.spec.ts` gains the 404 document in its no-violation loop and
     a header check; that spec is not in any CI workflow list, so it only runs by hand.
  3. Locale cookie. There were six writers, not two: next-intl's middleware and client
     navigation, the login proxy, the OAuth callback, and `document.cookie` in
     `components/auth-form.tsx` and `components/header-session.tsx`. Only the OAuth callback
     set `Secure`, and fixing `route.ts` alone would have changed nothing a browser keeps,
     because `auth-form.tsx` overwrites the cookie from the page right after a password sign-in.
     `i18n/routing.ts` now owns the attributes (`localeCookieAttributes`,
     `localeCookieString`) and every writer uses them. `Secure` is production only, the session
     cookie's rule, so a development server over plain HTTP keeps its cookies; the OAuth
     callback's locale cookie moves from "production or https" to that rule, which differs only
     on a development server run over HTTPS. `Secure` is omitted rather than `false`: next-intl's
     browser writer (`syncLocaleCookie`) prints a boolean attribute's name whatever its value.
  4. Admin. A client `admin/template.tsx` reads the path with next-intl's `usePathname`, runs
     the same `canAccessAdminPath` on the same bootstrap and renders `AdminAccessState`
     (inside the shell) instead of the page. `layout.tsx` is unchanged: its full-load check
     still answers without the shell and without rendering the page on the server. A template
     does not change remounting: Next keys the template slot per child segment whether or not a
     custom template exists.
- Scope additions, all needed by the findings above: `proxy.test.ts`, `e2e/csp.spec.ts`, the
  three comment fixes, `i18n/routing.ts` and its test, `app/api/auth/oauth/_shared.ts`, the two
  components and `admin/template.test.tsx`. `components/auth-form.tsx` is also in the scope of
  `2026-09-10-locale-login-return-path` (review, claude-fable-5-1); that ticket's branch
  `claude/travel-scanner-pr-552-rpq36m` only has merged PRs (#553-#565) and no open one, so
  the claim is stale and `check:tasks` prints the expected overlap warning. The change there
  is one line.
- Verified: `npx vitest run` on proxy.test.ts, i18n/routing.test.ts, `app/api/travel/[...path]`,
  `app/[locale]/admin/template.test.tsx`, lib/admin-operations.test.ts, admin-shell,
  header-session-locale, auth-form, the OAuth `_shared` test and the ads.txt/llms.txt route
  tests (14 files, 136 tests); `npm run typecheck:web`; `npm run lint:web`. `e2e/csp.spec.ts`
  on desktop-chromium against a production build: 4 passed, including the 404 document in the
  no-violation loop and its `'nonce-` header (the first, cold run timed the loop out at
  `/zh-TW/my` under the default 30 s on a loaded machine; rerun with `--timeout=240000`, 36 s).
  Against that build, robots.txt, ads.txt, llms.txt, sitemap.xml, manifest.webmanifest,
  favicon.ico, icon.svg, apple-icon.png, sw.js, og.png and a /brand svg answered 200 with no
  redirect and no nonce; `/no-such.page` answered 307 to `/zh-TW/no-such.page`.
- Building locally with `node_modules` junctions: Turbopack refuses them ("points out of the
  filesystem root"), and `next build --webpack` stops at a type check of `.next/types` for
  `app/api/video/{media,reviews}/[...path]/route.ts` (they export helpers besides handlers;
  webpack's typegen only, CI builds with Turbopack). `--experimental-build-mode=compile` then
  `generate` produced a servable build; the generate step ends on an ENOENT renaming
  `proxy.js`, which the compile step had already done.
