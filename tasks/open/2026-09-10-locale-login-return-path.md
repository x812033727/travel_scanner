---
id: 2026-09-10-locale-login-return-path
title: Normalize locale-prefixed login return paths
status: review
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:33:04Z
created_at: 2026-09-10T06:02:16Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/web/components/auth-form.tsx
  - apps/web/components/auth-form.test.tsx
---

# Normalize locale-prefixed login return paths

## Why

In local Chrome, opening /zh-TW/login with a manually supplied
next=/zh-TW/trips/seoul-transport-fixture and logging in produced
/zh-TW/zh-TW/trips/seoul-transport-fixture (404). A locale-prefixed internal next
path should not receive the locale twice. This was a diagnostic link, not a
claim that every existing product entry currently produces the wrong next value.

## Definition of done

- [x] Locale-prefixed and unprefixed internal next paths return to one valid route.
- [x] Unsafe external, protocol-relative and encoded redirect targets remain rejected.

## Steps

- [x] Inspect safe-next normalization and localized router behavior.
- [x] Cover all supported locales, query parameters and redirect safety cases.

## How to verify

Use auth-form unit tests and an isolated browser login; assert the resulting
URL has exactly one locale prefix. Do not use a production account.

## Notes

Reproduced 2026-09-10 against the local Korea route branch. Recorded separately
to keep the user's transport-settings fix narrowly scoped.

### 2026-09-19 done in repo (claude-fable-5-1)

- Cause: `AuthForm` handed `safeNextPath(next)` straight to next-intl's localized
  `router.push(path, { locale })`. With `localePrefix: "always"` that router prepends
  `/<locale>` itself and never strips one, so `next=/zh-TW/trips/x` became
  `/zh-TW/zh-TW/trips/x`. Prefixed `next` values come from real entries, not only the
  diagnostic link: `app/[locale]/admin/layout.tsx` builds `next` from the raw
  `x-travel-pathname` header and `components/price-alert-button.tsx` from
  `window.location.pathname`; both carry the locale.
- Fix (`components/auth-form.tsx`): a module-private `splitLocalePrefix` takes one leading
  locale segment off the safe path (whole segment only, so `/japan` is not `/ja`;
  case-insensitive, because the middleware serves `/zh-tw/` too; query string kept) and
  the form pushes the remainder with `{ locale: prefixLocale ?? preferredLocale }`. The
  remainder passes `safeNextPath` again, so `/zh-TW//evil.example` ends at `/` instead
  of relying on the router's prefix to keep it same-origin.
- Decision: a locale named in `next` wins over the account's `preferred_locale` and is
  kept as is (`/ja/trips/x` for a zh-TW account returns to `/ja/trips/x`). It is a
  specific, valid route the visitor was on or was linked to; the preference applies only to
  a bare path, as before. The OAuth callback already behaves this way
  (`app/api/auth/oauth/_shared.ts` `localizedPath` keeps an existing prefix verbatim), so
  both sign-in routes now agree. Only one prefix is stripped, as the middleware does; a
  doubled prefix from an old broken link still 404s, and nothing produces one any more.
- Not changed: `lib/navigation.ts` `safeNextPath` (outside scope) rejects the same shapes
  as before: `//host`, `https://…`, backslashes, control characters, and anything not
  starting with `/` (`%2F%2Fevil.example`, `%2e%2e/…`, `javascript:`). Encoded
  remainders are never decoded and stay paths on this origin.
- Tests (`auth-form.test.tsx`): bare path with a query, prefix in the current locale, prefix
  in each other locale (en/ja/ko/zh-CN, plus lower-case `zh-tw`), locale-only paths with and
  without a query, the `/japan` non-match, prefix-wins-over-preference and
  bare-path-follows-preference, nine rejected shapes, and an encoded remainder. The API mock
  is now routed by path: `SocialLoginButtons` probes `/auth/oauth/providers` on mount, and
  it was that probe, not the sign-in call, that consumed the one-shot rejection in the
  existing 503 test (its alert came from a TypeError on an undefined response). That test now
  asserts the 503 message.
- Validation: `npx vitest run components/auth-form.test.tsx` 24 passed; `npm run lint:web`,
  `npm run typecheck:web` and `npm run check:i18n` clean. The browser login from "How to
  verify" was not run in this session (no isolated browser or account here); the exact
  arguments reaching the router are pinned instead.
