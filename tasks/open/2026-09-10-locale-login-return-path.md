---
id: 2026-09-10-locale-login-return-path
title: Normalize locale-prefixed login return paths
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-10T06:02:16Z
completed_at:
branch:
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

- [ ] Locale-prefixed and unprefixed internal next paths return to one valid route.
- [ ] Unsafe external, protocol-relative and encoded redirect targets remain rejected.

## Steps

- [ ] Inspect safe-next normalization and localized router behavior.
- [ ] Cover all supported locales, query parameters and redirect safety cases.

## How to verify

Use auth-form unit tests and an isolated browser login; assert the resulting
URL has exactly one locale prefix. Do not use a production account.

## Notes

Reproduced 2026-09-10 against the local Korea route branch. Recorded separately
to keep the user's transport-settings fix narrowly scoped.
