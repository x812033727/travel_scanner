---
id: 2026-09-07-signed-out-account-fires-401s
title: A signed-out visit to /account still fires seven requests that can only 401
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T06:52:37Z
created_at: 2026-09-07T02:06:17Z
completed_at: 2026-09-07T07:02:02Z
branch:
depends_on: []
scope:
  - apps/web/components/account-saved-items.tsx
  - apps/web/app/[locale]/account
---

# A signed-out visit still fires requests that can only 401

## Why

Measured on production before the fix, a signed-out `/zh-TW/account` sent four requests
to the API and two came back 401:

```
401 /api/travel/auth/me
200 /api/travel/analytics/config
401 /api/travel/saved-items?limit=100
200 /api/travel/auth/oauth/providers
```

Both 401s answer the same question — is anyone signed in — and both providers asked it
by sending a request, because the request *was* the answer. `SavedItemsProvider` is
mounted in the locale layout, so that second one went out on every page a signed-out
reader opened, not only `/account`.

The audit counted seven; `2026-09-07-account-signed-out-states` had already removed five
by the time this was measured.

## Definition of done

- [x] A signed-out reader's first page view sends neither `/auth/me` nor `/saved-items`.
- [x] A cookie that is present is still verified, because it may have expired.
- [x] Signing in or out does not leave the previous session's answers in client state.

## How to verify

`npx playwright test e2e/signed-out.spec.ts` — one case counts the requests with no
cookie, the other sets an invalid `travel_access` and expects both calls to go out.

## Notes

- `travel_access` is the only session cookie and it is HttpOnly, so the browser cannot
  read it — but the locale layout is a server component and `cookies().has()` can. An
  absent cookie is proof of signed-out; a present one proves nothing about validity, so
  it is still verified the old way.
- Both providers take `hasSession` with a default of `true`, so every existing test that
  renders them directly keeps its current behaviour.
- The providers are keyed on the flag in the layout. Without that, a soft navigation
  after signing out would leave `status: "authenticated"` in client state while the
  cookie was gone.
- `networkidle` cannot be used in this spec: the dev server holds an HMR socket open and
  never reaches it. Each route gets a fixed settle window instead.
