---
id: 2026-09-08-travel-discovery-web
title: Travel discovery homepage search collections and media experience
status: done
priority: P1
area: web
owner: codex-discovery-web
claimed_at: 2026-09-09T00:43:12Z
created_at: 2026-09-08T23:24:10Z
completed_at: 2026-09-09T01:18:24Z
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
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/e2e/planner-premium.spec.ts
  - apps/web/components/header-session-identity.test.tsx
---

# Travel discovery homepage search collections and media experience

## Why

Unify sourced travel discovery, clear recommendations, private collections and safe media without replacing the existing search experience when the rollout is disabled.

## Definition of done

- [x] Flag-off homepage remains unchanged; flag-on homepage and explore support URL filters and honest source disclosure.
- [x] Explicit preferences, dismiss/undo, private collection and trip handoff work with authentication return paths.
- [x] Creator invites and reference-only video editing preserve existing publication review and draft behavior.
- [x] Five-language UI, focused tests, route metadata and static checks pass.
- [x] Parent completes discovery desktop/Pixel 7 and full-stack acceptance.
- [x] PR review, merge and parent-owned release validation complete.

## Steps

- [x] Read repository task protocol and installed Next use-client/page documentation.
- [x] Coordinate discovery/community API contracts and isolated localization ownership.
- [x] Implement discovery and community UI with focused regression coverage.
- [x] Complete final static checks and route metadata catalogs.
- [x] Complete browser acceptance and prepare PR review evidence.
- [x] Parent completes final PR/release verification.

## How to verify

`npm exec --workspace @travel-scanner/web -- vitest run 'app/[locale]/metadata.test.ts' components/discovery components/community/discovery-social.test.tsx components/travel-card-actions.test.tsx components/community/community.test.tsx --pool=threads --maxWorkers=1`

`npm run typecheck:web` and focused ESLint across all scoped TypeScript/TSX files.

Parent owns real desktop/Pixel 7 Playwright, production build and full-stack verification; no production writes are performed by this task.

## Notes

Root approved bounded scope extensions for opt-in TravelCardActions login-resume/modal accessibility and the exact five metadata catalogs after their previous owner released them. Existing legacy callers retain default behavior. No global CSS, other shared translations, planner or provider configuration edits.

- Public status is fail-closed and deduplicated; account data is abortable and bound to the active login identity. Discovery OFF retains both the existing home form and legacy TravelExplore hub.
- Keyword/feed filters persist in the URL. Search uses the server's selected mode; destination/topic options come from suggestions taxonomy, not the active filter echo. No AI or fabricated-image claims.
- Guide/hotel collection actions use discovery wrappers over existing collection storage, including ordinary accounts without a social profile. Existing community collections understand the new authorized references too.
- Exact server-derived place selection paths reuse the trip/day picker. Login return intents only reopen confirmation; resumed saves use idempotent setSaved(true), never toggle an existing favourite off.
- Source details show actual language, source type, author/date and update time. YouTube refs are canonical IDs only; verified players use click-to-load exact youtube-nocookie embeds, no autoplay, minimum 200px in each dimension.
- Explicit preference 409 conflict/discard/reload and expired-page restart paths added after independent review. No preference or browser-history inference is stored by the UI.
- Final source verification before metadata: 6 focused files / 59 tests passed, including original thumbnail/full image authorization, session-identity reset, mobile filter collapse, public video/itinerary snapshots, pagination/conflict and available-option regressions. Scoped ESLint and whole-web TypeScript passed after final source changes.
- After rebase and exact metadata scope handoff: metadata plus scoped suite passed, 7 files / 99 tests. check:i18n passed (5 locales / 25 namespaces); check:tasks passed (195 task files). The metadata test was not weakened.
- Only exploreTitle/Description and discoveryCollectionsTitle/Description changed in each metadata catalog. Explore wording remains accurate with discovery OFF; the new private collection page has distinct titles/descriptions in all five languages.
- Parent reported desktop/Pixel 7 focused search, dialog focus restoration and legacy-hub checks passed (6 cases). Parent retains final full-stack/build/release ownership; no generated next-env or production changes were made by this task.
- Review handoff: [PR #372](https://github.com/x812033727/travel_scanner/pull/372), draft head fa280c3a at the time of the CI fixture follow-up. Parent reports discovery full-stack acceptance and all 18 local discovery Playwright cases passed.
- CI compatibility follow-up: claimed only apps/web/e2e/planner-premium.spec.ts after the prior planner task was archived. Added GET /api/travel/discovery/status to the existing read-only enabled:false shell fixture; mutationPaths and unexpectedRequests assertions remain unchanged. Existing production build, port 3143: desktop Chromium plus Pixel 7 passed all 8 planner-premium cases (46.9s). No paid-provider or production data access; no commits or pushes performed by this task.
- PR #372 head 582054e2 CI repair (web job 102291601001): claimed only header-session-identity.test.tsx after the prior settings task was archived. Its SessionProbe reports through a passive useEffect; findByText can observe the DOM commit before that probe receives the same render. Initial identity captures and all probe-dependent transitions now synchronize with waitFor, retaining stable identity on profile/currency changes, fresh identity after logout/re-login or principal changes, and rejection of late pre-logout responses. header-session.tsx and authentication behavior remain unchanged.
- CI repair validation: 10 separate Vitest invocations of header-session-identity.test.tsx all passed (5 tests each, 50 successful executions). Related site-navigation, mobile-nav, app-bottom-nav and discovery-navigation tests passed (4 files / 19 tests). Focused ESLint and git diff --check passed. Parent owns the subsequent commit/push and CI verification.

## Completion evidence

- Coordinating root verified PR #372 merged as 6eacb821, with every main CI check green.
- Coordinating root deployed that revision to hostinger2: all 8 services running, schema 0066, and three consecutive readiness checks passed. Existing environment configuration and volumes were preserved; the verified pre-deployment backup is 13,672,114 bytes with mode 0600.
- Discovery and community remain OFF in production. This completes deployed implementation and verification, not a rollout enablement claim. No production operations were performed by this subtask.
- The planner-calm owner (thread 01a057cf) requested apps/web/e2e/planner-premium.spec.ts back after merge. Completing this task releases its exact scope, with no pending source edits or further claim on that test. Root handles the task-only archive commit and handoff.
