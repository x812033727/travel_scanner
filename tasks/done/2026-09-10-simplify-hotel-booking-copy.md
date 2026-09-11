---
id: 2026-09-10-simplify-hotel-booking-copy
title: Simplify hotel booking platform and source copy
status: done
priority: P2
area: web
owner: codex-hotel-copy
claimed_at: 2026-09-10T00:47:25Z
created_at: 2026-09-10T00:46:05Z
completed_at: 2026-09-11T02:50:18Z
branch: codex/hotel-booking-copy
depends_on: []
scope:
  - apps/web/components/travel-services/booking-panel.tsx
  - apps/web/messages/zh-TW/travelServices.json
  - apps/web/messages/zh-CN/travelServices.json
  - apps/web/messages/en/travelServices.json
  - apps/web/messages/ja/travelServices.json
  - apps/web/messages/ko/travelServices.json
  - apps/web/lib/stay22-allez-messages
---

# Simplify hotel booking platform and source copy

## Why

The user wants a cleaner hotel booking panel: remove the Stay22-specific
partner-link badge, shorten the source heading to "資料來源", and stop displaying
the long Mokaair processing note. This is a frontend presentation change, not a
request to disable affiliate routing, delete source records, or change settings.

## Definition of done

- [x] Platform buttons no longer show the Stay22 partner-link badge in any locale.
- [x] The source heading says "資料來源" with equivalent concise labels in five locales.
- [x] Source processing notes are not rendered; source/publisher/license links and stored data remain intact.
- [x] General commission disclosure and original first-party clickout behavior remain unchanged.
- [x] Focused unit/browser tests, lint, i18n, TypeScript, and production build pass.

## Steps

- [x] Locate shared BookingPanel/SourceCredits rendering and all five-language labels.
- [x] Remove only the requested display text and unused Stay22 badge translations.
- [x] Validate desktop/mobile booking behavior with synthetic fixtures and no real affiliate traffic.
- [x] Deliver the reviewed change without merging or deploying without new authorization.

## How to verify

`npm run lint:web`, `npm run check:i18n`, `npm run typecheck:web`,
focused BookingPanel/catalog/Stay22 Vitest tests, `npm run build:web`, and
`PLAYWRIGHT_SERVE_BUILD=true` with `stay22-allez.spec.ts` on desktop Chromium and
Pixel 7. Source notes must be absent from the DOM, not merely folded closed.

## Notes

2026-09-11 housekeeping: GitHub freshly confirmed PR #384 merged at
2026-09-10T01:14:40Z (merge daa71684167aafcaea9d1f44505132a0b3ace749).
Archive the completed claim before the new hotel-operation task; this is not a new deployment.

Built from origin/main 30a8e06a in an isolated worktree; the old canonical checkout
and other working changes are untouched. `SourceCredit.changes` remains part of
the API data model but is no longer rendered. Source and license links stay
visible when the source section is expanded. The general commission notice stays
in the panel footer; only the per-platform Stay22 badge is removed.

Task-board cleanup before claiming: PR #383 was freshly verified merged, so its
completed referrer-policy task was archived. The merchant-style task's claim was
over 42 hours old and its referenced batch PR #361 was verified merged; its broad
claim was released back to open, not marked done. All outstanding merchant maps,
review, and publication work remain pending and unchanged. No forced overlapping
claim or production data mutation was used.

Validation: full Web ESLint, five locales/25 namespaces, standalone TypeScript,
Next.js production build (272 routes), 41 focused Vitest tests, 27 tools tests,
and task-board validation passed. Desktop Chromium + Pixel 7 ran all 22 existing
Allez browser scenarios with strengthened copy/source assertions: 22 passed in
47.8 seconds. All booking targets were local fixtures; source links were inspected
but not followed. Parent inspected both synthetic panel screenshots; there is no
horizontal overflow or per-platform Stay22 badge. First-click, retry, POST/date
payloads and general commission notice remain verified.

The first local build rejected cross-worktree dependency junctions. Those links
were preserved in a task-specific temporary directory; npm ci installed isolated
dependencies, after which the ordinary Turbopack build passed. No config workaround,
dependency lockfile change, or broad filesystem cleanup was committed. Generated
next-env.d.ts changes were returned to their original content after verification.
