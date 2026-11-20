---
id: 2026-11-20-add-layout-visibility-toggles-to-hide
title: Add layout visibility toggles to hide flight search, videos, and member chrome by default
status: done
priority: P0
area: web
owner: antigravity
claimed_at: 2026-11-20T17:15:12Z
created_at: 2026-11-20T17:15:02Z
completed_at: 2026-11-20T17:38:04Z
branch: agy/info-only-visibility-toggles
depends_on: []
scope:
  - .github/workflows/ci.yml
  - apps/api/app/config.py
  - apps/api/app/admin/schemas.py
  - apps/api/app/admin/service.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_site_visibility.py
  - apps/web/app/[locale]/destinations/[destinationId]/page.tsx
  - apps/web/app/[locale]/page.seo.test.tsx
  - apps/web/app/[locale]/page.test.tsx
  - apps/web/app/[locale]/page.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/app-bottom-nav.test.tsx
  - apps/web/components/app-bottom-nav.tsx
  - apps/web/components/destination-guide.tsx
  - apps/web/components/discovery-navigation.test.tsx
  - apps/web/components/discovery/card.tsx
  - apps/web/components/discovery/explorer.tsx
  - apps/web/components/header-auth.test.tsx
  - apps/web/components/header-auth.tsx
  - apps/web/components/home-guides.test.tsx
  - apps/web/components/home-guides.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/nav-menu.tsx
  - apps/web/components/public-feature-gate.tsx
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-navigation.tsx
  - apps/web/components/travel-card-actions.tsx
  - apps/web/lib/admin-settings-ownership.test.ts
  - apps/web/lib/frontend-navigation.ts
  - apps/web/lib/nav-links.ts
  - apps/web/lib/site-features.ts
  - apps/web/lib/site-visibility.server.test.ts
  - apps/web/lib/site-visibility.server.ts
  - apps/web/messages
  - tools/e2e-runtime-api.mjs
---

# Add layout visibility toggles to hide flight search, videos, and member chrome by default

## Why

The owner wants the public frontend to run as a clean, single-row **editorial information portal** (AI/tech news, guides, destinations, hotspots, foods) and temporarily hide incomplete or member-oriented surfaces: **搜尋機票與住宿** (flights & stays search), **影音專區 / 影片** (videos), **我的 / 我的旅程 / 收藏** (member collections/trips/account chrome), and the public **登入** button — while keeping direct URL access to `/[locale]/login` working for admin sign-in and allowing each surface to be re-enabled anytime from `/admin/layout-settings`.

## Definition of done

- [x] `flight_search_enabled`, `videos_enabled`, and `member_features_enabled` added to `Settings`, `SiteVisibility`, `SITE_VISIBILITY_FIELDS`, `/admin/layout-settings`, and 5-locale `admin.json` / `availability.json`, all defaulting to `False`.
- [x] Desktop header hides `收藏`, `我的旅程`, `我的`, `影片`, and signed-out `登入` when switches are off (so header fits on one clean row), while preserving `後台` (`/admin`) and `登出` once signed in via direct `/[locale]/login`.
- [x] Homepage (`HomeGuides` + `DiscoveryExplorer` + non-discovery body) hides `搜尋機票與住宿`, `影音專區`, signed-out preferences login prompt, and card-level `收藏` / `加入旅程` actions.
- [x] Footer hides `影片`; mobile header hides signed-out `登入` and `我的`; mobile bottom bar switches cleanly to four pure information tabs (`探索`, `AI`, `旅遊指南`, `生活`).
- [x] Rolling-deploy safe (`parseSiteVisibility` defaults omitted new flags to `false`); existing CI isolated & full-stack e2e suites remain green via explicit `true` fixture/env configuration.

## Steps

- [x] Add `flight_search_enabled`, `videos_enabled`, `member_features_enabled` (default `False`) to API config, schema, and `SITE_VISIBILITY_FIELDS`.
- [x] Extend `apps/web/lib/site-features.ts`, `site-visibility.server.ts`, `public-feature-gate.tsx`, `admin-settings-panel.tsx`, and 5-locale i18n catalogs.
- [x] Gate header, mobile nav, bottom nav, footer, homepage, discovery explorer/cards, travel card actions, and destination guide links.
- [x] Add/update API and web unit tests covering both full-feature and information-only modes; keep e2e fixtures green.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_site_visibility.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
npm run test --workspace @travel-scanner/web -- lib/site-visibility.server.test.ts components/app-bottom-nav.test.tsx components/discovery-navigation.test.tsx components/header-auth.test.tsx components/home-guides.test.tsx components/site-navigation.test.tsx components/site-footer.test.tsx components/mobile-nav.test.tsx lib/admin-settings-ownership.test.ts "app/[locale]/page.seo.test.tsx" "app/[locale]/page.test.tsx"
npm run check:tasks
```

## Notes

- Zero database migration required: `layout` settings are stored as JSON in `provider_configs`, and missing keys fall back to `Settings` defaults (`False` for the three new switches).
- Direct navigation to `https://mokaair.com/zh-TW/login` remains open; once an admin signs in, `HeaderAuth` and `MobileNav` immediately display `/admin`, email/account, and sign-out controls even while `member_features_enabled` is `false`.
