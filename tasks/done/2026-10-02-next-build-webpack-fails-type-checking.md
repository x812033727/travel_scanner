---
id: 2026-10-02-next-build-webpack-fails-type-checking
title: next build --webpack fails type checking on two video route handlers
status: done
priority: P2
area: web
owner: codex-webpack-routes-20261003
claimed_at: 2026-10-03T09:21:34Z
created_at: 2026-10-02T18:51:07Z
completed_at: 2026-10-03T09:33:52Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - apps/web/app/api/video/reviews/[...path]/route.ts
  - apps/web/app/api/video/reviews/[...path]/route.test.ts
  - apps/web/app/api/video/reviews/[...path]/forward.ts
  - apps/web/app/api/video/media/[...path]/route.ts
  - apps/web/app/api/video/media/[...path]/route.test.ts
  - apps/web/app/api/video/media/[...path]/forward.ts
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

- [x] The extra exports move to a sibling module (for example `./forward.ts` or a shared lib file)
      that both the route and its tests import, so each `route.ts` exports only Next.js route names.
- [x] `cd apps/web && npx next build --webpack` type-checks cleanly (no `ignoreBuildErrors`).
- [x] The route tests still pass and import the helpers from their new place.

## Steps

- [x] Find the extra exports (`grep -n "^export" apps/web/app/api/video/*/\[...path\]/route.ts`).
- [x] Move them, update imports in the routes and tests.
- [x] Run the webpack build once, then `npm run typecheck:web`, `npm run lint:web` and the route tests.

## How to verify

`cd apps/web && npx next build --webpack` finishes without type errors.

## Notes

- Filed 2026-10-03 by claude-opus-5-5 (coordinator) from the two agents' reports; nobody has changed code yet.
- 2026-10-03 implementation on main `5af4ffebfcea96fd23b387288901e513ed63d4f7`:
  moved each route's existing policy/constants and forwarding code to its own
  `forward.ts`; each route now exports only GET, POST and PUT. Handler tests still
  import the actual route, while helper/constant imports use the sibling module.
  No request, token, body limit, timeout, header or streaming behavior was changed.
- Node 24.19.0 focused Vitest run: both existing route test files passed, 11 tests,
  exit 0. An independent mechanical comparison confirmed the forwarding code is
  byte-equivalent apart from exporting the moved Context/forward declarations,
  all handler bodies are unchanged, and test edits only alter the imports.
  A TypeScript AST check against the installed Next webpack validator's allowed
  runtime exports identified the old PART_MAX_BYTES/mediaRoute/reviewRoute exports
  and confirms they are absent from the new route modules. This static proof is
  not a substitute for the real webpack build; the coordinating agent completed
  that acceptance and the full web lint/typecheck as recorded below.
- 2026-10-03: Corrected the scope to include both route files described above,
  their existing tests and the planned sibling helper modules before claiming.
  Fresh main `5af4ffebf`, two open PRs, remote/local branches and 38 visible
  worktrees showed no active changes or ownership overlap in these six paths.
- Final local acceptance: real Next.js 16.3.7 `next build --webpack` exited 0,
  including its route-export type validation and 348 static pages. No build
  errors were ignored and no build configuration was changed. Standalone
  `tsc --noEmit`, complete `eslint .`, staged i18n (5 locales / 25 namespaces)
  and Git diff checks passed on Node 24.19.0.
- Staged diff checking found one extra blank EOF line in each newly moved helper.
  Those two lines were removed; strict comparison proved this was the only
  post-build/typecheck source difference, with helper/handler content unchanged.
  The 11 route tests, build and typecheck were not rerun for that whitespace-only
  cleanup; complete lint and final diff checks cover the cleaned files.
- Independent review found no import cycles or forwarding-contract changes.
  The fresh pre-PR main remained `5af4ffebf`, and current open PR/remote changes
  did not overlap these six source paths or this task. No production access,
  provider calls, uploads or deployment were performed.
