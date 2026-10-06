---
id: 2026-10-04-investigate-braces-advisory-in-the-next
title: Investigate braces advisory in the Next ESLint toolchain
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5-board-closures
claimed_at: 2026-10-06T00:45:44Z
created_at: 2026-10-04T06:02:00Z
completed_at:
branch: claude/board-closures
depends_on: []
scope:
  - apps/web/package.json
  - package-lock.json
---

# Investigate braces advisory in the Next ESLint toolchain

## Why

During frontend validation, npm audit reported five high-severity entries caused
by one development-tool advisory propagated through the Next ESLint dependency
chain. npm's suggested major downgrade would conflict with the current Next 16
tooling; investigate a compatible upstream correction or mitigation instead.

## Definition of done

- [ ] Record the affected lockfile chain and assess whether trusted repository patterns can reach the vulnerable parser.
- [ ] Apply a compatible upstream fix or documented mitigation when available, without blindly downgrading Next/ESLint.
- [ ] npm ci, audit and lint:web remain usable and explain any unresolved advisory.

## Steps

- [x] Check npm audit and existing tasks before filing a duplicate.
- [ ] Monitor the primary advisory and investigate a compatible dependency path.
- [ ] Validate the chosen fix or mitigation with reproducible evidence.

## How to verify

Run npm ci, npm audit --json, npm audit --omit=dev --json and npm run lint:web
with a Node version satisfying package engines. Compare the actual lockfile chain.

## Notes

- 2026-10-04: eslint-config-next@16.3.7 -> @next/eslint-plugin-next@16.3.7 ->
  fast-glob@3.3.1 -> micromatch@4.0.8 -> braces@3.0.3. All five reported entries
  trace to GHSA-vfj7-8cjw-p6xm (CVE-2026-93687), a stack-exhaustion DoS on deeply
  nested brace patterns. npm audit --omit=dev reported zero vulnerabilities.
- Primary advisory: https://github.com/advisories/GHSA-vfj7-8cjw-p6xm . It lists
  affected <=3.0.3 and no patched version at this check; do not invent an upgrade.
- npm audit fixAvailable proposed eslint-config-next@14.2.35 as a major change.
  No package or lockfile change was made in the monetization work.
