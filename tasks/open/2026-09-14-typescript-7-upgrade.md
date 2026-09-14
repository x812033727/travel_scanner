---
id: 2026-09-14-typescript-7-upgrade
title: Upgrade TypeScript to 7 once typescript-eslint supports it
status: blocked
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-14T11:01:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/package.json
  - package-lock.json
  - apps/web/tsconfig.json
---

# Upgrade TypeScript to 7 once typescript-eslint supports it

## Why

Dependabot opened [#484](https://github.com/x812033727/travel_scanner/pull/484) on
2026-09-14 to move `typescript` from 6.0.3 to 7.0.2, the native (Go) compiler. CI was green
apart from one `containers` run, and that failure was Docker Hub timing out on
`nginx:1.28-alpine` (exit code 125); the other run of the same job passed.

It was still not merged, because of what the lock file did. `typescript-eslint` 8.68.0, which
`eslint-config-next` brings in, declares `typescript >=4.8.4 <6.1.0` as a peer. To satisfy
it npm kept `node_modules/typescript` at 6.0.3 and nested 7.0.2 under
`apps/web/node_modules/typescript`. So `npm run typecheck:web` and `next build` checked types
with 7.0.2 while ESLint parsed the same files with 6.0.3. Two compilers in one project is a
setup to choose on purpose, not one to inherit from a version bump. Next 16.3.4's release
notes fix a build error "when aliasing typescript to `@typescript/typescript6`", which is
the side-by-side arrangement the ecosystem is using for tools that still need the 6.x API.

The pull request was closed with `@dependabot ignore this major version`, so Dependabot will
not propose TypeScript 7.x again by itself.

What the upgrade buys, measured on #484's `web` job against `main` at the same base: the
TypeScript step of `next build` went from 18.8 s to 4.0 s, and `npm run typecheck:web` from
about 18 s to about 3 s.

## Definition of done

- [ ] `npm run typecheck:web` and `next build` run TypeScript 7.
- [ ] ESLint runs on a TypeScript that `typescript-eslint` supports, and the lock file layout is
      intentional: one TypeScript, or a documented alias such as `@typescript/typescript6`.
- [ ] A deliberate type error makes `npm run typecheck:web` fail, so a much faster check is
      proven to still be a check.

## Steps

- [ ] Check upstream: `npm view typescript-eslint@latest peerDependencies`. Either it accepts
      TypeScript 7, or choose the alias arrangement Next 16.3.4 supports.
- [ ] Upgrade and read `apps/web/tsconfig.json` for options TypeScript 6 deprecated and 7
      removes.
- [ ] Nothing in `tools/` or `apps/web` imports the `typescript` JS API directly (checked
      2026-09-14 with `git grep`), so only the `tsc` binary, Next and ESLint consume it; check
      again before upgrading.

## How to verify

```bash
npm ci
npm ls typescript
npm run typecheck:web
npm run lint:web
npm run build:web
```

## Notes

- Filed from the 2026-09-14 review of the first Dependabot batch (#475–#484).
