---
id: 2026-09-14-eslint-10-upgrade
title: Upgrade ESLint to 10 once eslint-config-next supports it
status: blocked
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-14T11:01:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/package.json
  - package-lock.json
  - apps/web/eslint.config.mjs
---

# Upgrade ESLint to 10 once eslint-config-next supports it

## Why

Dependabot opened [#481](https://github.com/x812033727/travel_scanner/pull/481) on
2026-09-14 to move `eslint` from 9.39.5 to 10.10.0. Its `web` job failed at
`npm run lint:web` before a single file was linted
([job log](https://github.com/x812033727/travel_scanner/actions/runs/34809364054/job/103867419573)):

```text
TypeError: Error while loading rule 'react/display-name': contextOrFilename.getFilename is not a function
    at resolveBasedir (node_modules/eslint-plugin-react/lib/util/version.js:31:100)
```

ESLint 10 removed `context.getFilename()`, which ESLint 9 had deprecated, and
`eslint-plugin-react` 7.37.5 still calls it. The plugin is not ours to fix: it arrives through
`eslint-config-next` 16.3.x, and its own peer range (`eslint ^3 || … || ^9.7`) stops before 10.
Short of dropping Next's lint configuration there is nothing to change on this side, so the
upgrade waits for upstream.

It should not wait forever: the same CI run printed
`npm warn deprecated eslint@9.39.5: This version is no longer supported`.

The pull request was closed with `@dependabot ignore this major version`, so Dependabot will
not propose ESLint 10.x again by itself. This file is what remembers the upgrade.

## Definition of done

- [ ] `apps/web/package.json` asks for ESLint 10, and `npm ls eslint` shows a single ESLint —
      not a nested `apps/web/node_modules/eslint` 10.x beside a root 9.x, which is the layout
      #481's lock file had.
- [ ] `npm run lint:web` passes without new rule disables.

## Steps

- [ ] Check upstream first: `npm view eslint-plugin-react@latest peerDependencies` must include
      ESLint 10, and `npm view eslint-config-next@latest dependencies` must pull that plugin
      version (or no longer need it).
- [ ] Upgrade `eslint` together with `eslint-config-next`, regenerate the lock file, and fix
      whatever ESLint 10's configuration reports.
- [ ] Decide whether Dependabot should track ESLint majors again. The ignore lives in
      Dependabot's state, not in `.github/dependabot.yml`; `@dependabot show eslint ignore
      conditions` on any Dependabot pull request lists it. A manual upgrade does not need it
      lifted.

## How to verify

```bash
npm ci
npm ls eslint
npm run lint:web
```

## Notes

- Filed from the 2026-09-14 review of the first Dependabot batch (#475–#484). The same batch's
  minor/patch group and the other green majors were merged.
