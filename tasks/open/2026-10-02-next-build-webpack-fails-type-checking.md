---
id: 2026-10-02-next-build-webpack-fails-type-checking
title: next build --webpack fails type checking on two video route handlers
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-02T18:51:07Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/api/video/reviews/[...path]/route.ts
---

# next build --webpack fails type checking on two video route handlers

## Why

Two agents on 2026-10-02 (the offline day view, PR #1147, and the airline comparison timeout
investigation) built the web app locally with `next build --webpack` (Turbopack refuses the
node_modules junctions agents use) and both hit the same type-check failure: the route handlers
`apps/web/app/api/video/media/[...path]/route.ts` and `apps/web/app/api/video/reviews/[...path]/route.ts`
export names other than the HTTP methods and route config Next.js allows in a route file. Both
agents worked around it with a local-only `ignoreBuildErrors` and reverted it. CI and the Docker
image build use the default bundler and pass, so production is not affected today, but any
webpack build (local e2e against a production build, a future bundler switch) fails.

## Definition of done

- [ ] The extra exports move to a sibling module (for example `./forward.ts` or a shared lib file)
      that both the route and its tests import, so each `route.ts` exports only Next.js route names.
- [ ] `cd apps/web && npx next build --webpack` type-checks cleanly (no `ignoreBuildErrors`).
- [ ] The route tests still pass and import the helpers from their new place.

## Steps

- [ ] Find the extra exports (`grep -n "^export" apps/web/app/api/video/*/\[...path\]/route.ts`).
- [ ] Move them, update imports in the routes and tests.
- [ ] Run the webpack build once, then `npm run typecheck:web`, `npm run lint:web` and the route tests.

## How to verify

`cd apps/web && npx next build --webpack` finishes without type errors.

## Notes

- Filed 2026-10-03 by claude-opus-5-5 (coordinator) from the two agents' reports; nobody has changed code yet.
