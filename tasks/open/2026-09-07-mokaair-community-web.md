---
id: 2026-09-07-mokaair-community-web
title: Mokaair community responsive web and five-language experience
status: in-progress
priority: P1
area: web
owner: codex-community
claimed_at: 2026-09-07T10:14:21Z
created_at: 2026-09-07T10:14:21Z
completed_at:
branch: codex/mokaair-community
depends_on: []
scope:
  - apps/web/lib/api.ts
  - apps/web/lib/api.test.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/components/community
  - apps/web/app/[locale]/community
  - apps/web/app/[locale]/pet-friendly
  - apps/web/app/[locale]/my
  - apps/web/app/[locale]/explore
  - apps/web/app/[locale]/account/confirm
  - apps/web/app/[locale]/forgot-password
  - apps/web/app/[locale]/admin/community
  - apps/web/app/[locale]/admin/pet-friendly
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/layout.tsx
  - apps/web/app/[locale]/account/page.tsx
  - apps/web/app/api/travel
  - apps/web/lib/community
  - apps/web/messages
  - apps/web/i18n/request.ts
  - apps/web/components/site-navigation.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/app-bottom-nav.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/header-session.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/e2e/community.spec.ts
  - apps/web/public/sw.js
  - README.md
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
  - apps/web/lib/ui-text.ts
  - apps/web/lib/ui-text.test.ts
  - apps/web/vitest.setup.tsx
  - apps/web/components/admin-nav.test.tsx
---

# Mokaair community responsive web and five-language experience

## Why

Deliver the approved international travel community and reviewed pet-friendly
experience within the existing five-locale Web/PWA, without exposing private trips.

## Definition of done

- [ ] Responsive discovery, publishing, profiles, collections, messaging and moderation work.
- [ ] Pet filters and trip companion requirements expose uncertainty instead of guessing.
- [ ] New copy exists in all five catalogs; closed/unavailable states fail safely.
- [ ] Web tests, i18n, TypeScript, lint, production build and desktop/Pixel 7 flows pass.

## Steps

- [ ] Shared state, accessible UI and conservative server-side feature gates.
- [ ] Wire all content, social, pet and administration flows to the real BFF.
- [ ] Verify permissions, responsive layout, keyboard controls and service failures.

## How to verify

Run npm run test:web, check:i18n, typecheck:web, lint:web and build:web. Run the
community Playwright suite on desktop and Pixel 7 against isolated services.

## Notes

Checkpoint: rebased onto main 54009ba. CI 34130887751 passed Web components,
TypeScript, lint, five-locale checks, the default production build and isolated
desktop/Pixel 7 UI tests. Existing real-stack travel journeys also pass after
fixing a community Provider remount which reset core forms during auth hydration.
New regressions preserve core state and prevent cross-account community caches.
The real SMTP/MinIO community journey reached blocking on both devices; update
assertions to distinguish an unfollowed read-only thread from a hidden blocked
thread, and verify rejected writes never enter delivered history.
Pet/account lifecycle browser acceptance remains open. Local Webpack build passes;
default Turbopack cannot use this workspace's shared node_modules junction.
Draft PR #340 must not enable production or claim complete plan acceptance.

Built on isolated main 516713d. The existing forgot-password task owns the login
entry; this task owns the new confirmation/recovery UI and public community pages.
