---
id: 2026-09-08-travel-discovery-web
title: Travel discovery homepage search collections and media experience
status: in-progress
priority: P1
area: web
owner: codex-discovery-web
claimed_at: 2026-09-08T23:36:49Z
created_at: 2026-09-08T23:24:10Z
completed_at:
branch: codex/travel-discovery-community
depends_on: []
scope:
  - apps/web/components/discovery
  - apps/web/lib/discovery.ts
  - apps/web/lib/discovery-copy.ts
  - apps/web/lib/discovery-messages
  - apps/web/app/[locale]/explore
  - apps/web/app/[locale]/page.tsx
  - apps/web/components/community
  - apps/web/lib/community/types.ts
  - apps/web/components/travel-card-actions.tsx
  - apps/web/components/travel-card-actions.test.tsx
---

# Travel discovery homepage search collections and media experience

## Why

Unify sourced travel discovery, clear recommendations, private collections and safe media without replacing the existing search experience when the rollout is disabled.

## Definition of done

- [x] Flag-off homepage remains unchanged; flag-on homepage and explore support URL filters and honest source disclosure.
- [x] Explicit preferences, dismiss/undo, private collection and trip handoff work with authentication return paths.
- [x] Creator invites and reference-only video editing preserve existing publication review and draft behavior.
- [ ] Five-language UI, focused tests and static checks pass; parent validates desktop/Pixel 7 end-to-end.

## Steps

- [x] Read repository task protocol and installed Next use-client/page documentation.
- [x] Coordinate discovery/community API contracts and isolated localization ownership.
- [x] Implement discovery and community UI with focused regression coverage.
- [ ] Complete final static checks, route metadata catalogs and parent browser/release verification.

## How to verify

`npm exec --workspace @travel-scanner/web -- vitest run components/discovery components/community/discovery-social.test.tsx components/travel-card-actions.test.tsx --pool=threads --maxWorkers=1`

`npm run typecheck:web` and focused ESLint across all scoped TypeScript/TSX files.

Parent owns real desktop/Pixel 7 Playwright, production build and full-stack verification; no production writes are performed by this task.

## Notes

Root approved a bounded scope extension for opt-in TravelCardActions login-resume and modal accessibility. Existing legacy callers retain default behavior. No global CSS, shared translations, planner or provider configuration edits.

- Public status is fail-closed and deduplicated; account data is abortable and bound to the active login identity. Discovery OFF retains both the existing home form and legacy TravelExplore hub.
- Keyword/feed filters persist in the URL. Search uses the server's selected mode; destination/topic options come from suggestions taxonomy, not the active filter echo. No AI or fabricated-image claims.
- Guide/hotel collection actions use discovery wrappers over existing collection storage, including ordinary accounts without a social profile. Existing community collections understand the new authorized references too.
- Exact server-derived place selection paths reuse the trip/day picker. Login return intents only reopen confirmation; resumed saves use idempotent setSaved(true), never toggle an existing favourite off.
- Source details show actual language, source type, author/date and update time. YouTube refs are canonical IDs only; verified players use click-to-load exact youtube-nocookie embeds, no autoplay, minimum 200px in each dimension.
- Explicit preference 409 conflict/discard/reload and expired-page restart paths added after independent review. No preference or browser-history inference is stored by the UI.
- First final focused run: 5 files / 34 tests passed; extra pagination/conflict/available-option regressions added afterward. Focused ESLint and whole-web TypeScript passed before final additions and are being rerun.
- New page metadata requires discoveryCollectionsTitle/Description in five existing metadata catalogs. Their broader messages scope is held by another task; parent is coordinating that handoff. Do not weaken metadata tests.
