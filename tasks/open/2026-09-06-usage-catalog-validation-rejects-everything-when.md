---
id: 2026-09-06-usage-catalog-validation-rejects-everything-when
title: usage catalog validation rejects everything when web ships ahead of api
status: in-progress
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T04:27:51Z
created_at: 2026-09-06T00:55:44Z
completed_at:
branch: claude/api-p2-data
depends_on: []
scope:
  - apps/web/lib/usage-catalog.ts
  - apps/web/lib/usage-catalog.server.ts
  - apps/web/lib/usage-catalog.test.ts
  - apps/web/lib/usage-catalog.server.test.ts
  - apps/web/lib/usage-catalog-e2e-fixture.test.ts
  - README.md
---

# usage catalog validation rejects everything when web ships ahead of api

## Why

`isUsageCatalog()` requires **every** operation in `usageOperations` to carry a cost, and
returns false for the whole catalog if one is missing. A false catalog means
`status: "unavailable"`, and every metered surface renders its unavailable branch.

That is fail-closed by design, and defensible. But the failure is total and silent: adding
one operation to the list disables pricing copy on the search page, the alerts page, the
fare lab, back-to-back comparison and the planner previews — none of which have anything to
do with the new operation.

This already happened once. Adding `ai_itinerary_refine` broke sixteen browser tests on
unrelated pages because `tools/e2e-runtime-api.mjs` hardcodes its own copy of the operation
list. The fixture is fixed and guarded by `apps/web/lib/usage-catalog-e2e-fixture.test.ts`,
so the test-side drift cannot recur.

The production shape of the same hazard is untouched: if a web bundle is deployed ahead of
an API that does not yet serve the new operation, every metered surface in the product goes
dark at once, for a reason no error message explains.

## Definition of done

- [x] A catalog missing one operation degrades that operation, not the entire catalog.
- [x] Whatever the product decides here is deliberate and written down, rather than an
      emergent property of a validator.

## Steps

- [x] Decide the policy. Options, roughly:
      (a) keep fail-closed but log/surface which key was missing, so the cause is findable;
      (b) accept a catalog missing keys and fall back to the default cost for those, so an
          unknown operation is priced conservatively rather than blanking the product;
      (c) version the catalog payload so the client knows the API is older and can say so.
- [x] Implement the chosen policy and cover the missing-key path with a test.
- [x] Note the deploy-ordering assumption somewhere a deployer will read it. Today the web
      and API images are built and deployed together by
      `docker compose -f docker-compose.prod.yml --profile hotspots up --build -d`, so the
      window is small — but nothing enforces that they stay in step.

## How to verify

```bash
npm run test:web
```

Plus: serve a catalog with one operation removed and confirm the rest of the product still
prices correctly.

## Notes

Found while debugging a CI failure that looked like flakiness — sixteen browser tests
failing on pages unrelated to the change, in a cascade that started a third of the way
through the run. Diagnosed twice as an environment problem before a clean-main worktree
proved otherwise. Recorded here because the diagnostic difficulty is part of the cost: the
symptom points nowhere near the cause.

2026-09-06 claude-fable-5-1: policy (b), written down in `normalizeUsageCatalog`'s
doc comment and in the README's production deployment section.

- `isUsageCatalog` validates structure only: `trial_uses`, `packages`, and that every
  cost that *is* present is an integer in 0..100. A missing operation is version skew
  and passes; a present-but-invalid cost is corruption and still refuses the payload.
- `normalizeUsageCatalog` fills the missing operations from `defaultUsageCatalog`
  (one use, the conservative guess) and returns which keys were missing;
  `loadUsageCatalog` logs them with `console.warn` so the cause is findable in the
  web container's log instead of showing up as sixteen unrelated failures.
- (a) alone would have kept the product dark for a deploy-ordering slip; (c) needs
  an API change for a problem the web can absorb on its own. Neither is ruled out
  later.
- The e2e fixture guard (`usage-catalog-e2e-fixture.test.ts`) is kept: the browser
  suite would now pass with a stale fixture, which is exactly why the drift test has
  to stay. README says the API ships first or together with the web, never behind.
