---
id: 2026-10-04-investigate-braces-advisory-in-the-next
title: Investigate braces advisory in the Next ESLint toolchain
status: done
priority: P2
area: web
owner: claude-opus-5-5-board-closures
claimed_at: 2026-10-06T00:45:44Z
created_at: 2026-10-04T06:02:00Z
completed_at: 2026-10-06T01:39:33Z
branch: claude/board-closures
depends_on: []
scope:
  - tasks/open/2026-10-04-investigate-braces-advisory-in-the-next.md
---

# Investigate braces advisory in the Next ESLint toolchain

## Why

During frontend validation, npm audit reported five high-severity entries caused
by one development-tool advisory propagated through the Next ESLint dependency
chain. npm's suggested major downgrade would conflict with the current Next 16
tooling; investigate a compatible upstream correction or mitigation instead.

## Definition of done

- [x] Record the affected lockfile chain and assess whether trusted repository patterns can reach the vulnerable parser.
- [x] Apply a compatible upstream fix or documented mitigation when available, without blindly downgrading Next/ESLint.
- [x] npm ci, audit and lint:web remain usable and explain any unresolved advisory.

## Steps

- [x] Check npm audit and existing tasks before filing a duplicate.
- [x] Monitor the primary advisory and investigate a compatible dependency path.
- [x] Validate the chosen fix or mitigation with reproducible evidence.

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

- 2026-10-06 (claude-opus-5-5-board-closures), checked against origin/main cff4a6ac6:
  - **Chain today.** #1252 moved the pair to 16.3.8, so the lockfile reads
    eslint-config-next 16.3.8 (dev) -> @next/eslint-plugin-next 16.3.8 -> fast-glob 3.3.1
    -> micromatch 4.0.8 -> braces 3.0.3. Each of the last four has exactly one dependent in
    `package-lock.json`, the package before it, and no workspace depends on any of them
    directly.
  - **Reachability.** In the published @next/eslint-plugin-next 16.3.8 tarball the only
    file that loads fast-glob is `dist/utils/get-root-dirs.js` (the installed 16.3.7 copy
    is byte-identical). It calls `globSync` only on `context.settings.next.rootDir`;
    without that setting it returns `[context.cwd]` and globs nothing. Neither
    `apps/web/eslint.config.mjs` nor eslint-config-next 16.3.8's own `settings` (react,
    import/parsers, import/resolver) sets `next.rootDir`, so braces never receives a
    pattern from this repository, trusted or not.
  - **Upstream.** The GitHub advisory API (updated 2026-10-02T22:36Z) still gives range
    `<= 3.0.3` and `first_patched_version: null`. The npm registry's latest versions are
    braces 3.0.3, micromatch 4.0.8 and fast-glob 3.3.3. @next/eslint-plugin-next 16.3.8
    (latest) and 16.4.0-canary.61 both pin `fast-glob: 3.3.1`. An `overrides` entry would
    not help: fast-glob 3.3.3 still asks for `micromatch ^4.0.8`, which is braces 3.0.3.
    The 14.2.35 downgrade npm offers stays rejected.
  - **Mitigation.** #1209 (20cea81f0) is the documented mitigation:
    `tools/npm-audit-allow.json` exempts GHSA-vfj7-8cjw-p6xm for braces only, with a
    reason naming this ticket and `review_by: 2026-11-04`, and `tools/npm-audit-gate.mjs`
    stops honouring it after that date. That date is the monitoring: on 2026-11-05 the
    daily npm audit turns red unless someone has re-checked the advisory for a patched
    release and renewed or removed the entry. The ticket id in that reason still
    resolves, under `tasks/done/`.
  - **Evidence, Node 24.13.0 / npm 11.6.2.** `npm audit --json`: 5 high, all
    GHSA-vfj7-8cjw-p6xm (@next/eslint-plugin-next, braces, eslint-config-next, fast-glob,
    micromatch). Piped into `node tools/npm-audit-gate.mjs`: "exempted until 2026-11-04:
    braces high GHSA-vfj7-8cjw-p6xm …" then "npm audit gate: ok", exit 0.
    `npm audit --omit=dev --json`: total 0. `node --test tools/npm-audit-gate.test.mjs`:
    5/5 pass. `npm run lint:web`: exit 0, run against node_modules linked from another
    checkout whose lock still has 16.3.7 (the chain and the plugin file are the same). The
    clean-install half comes from CI. On main cff4a6ac6 the `web-checks` job (npm ci,
    advisory audit, `npm run lint:web` on Node 24) passed. The scheduled `npm audit`
    workflow (npm ci, `--omit=dev --audit-level=high`, then the gate) passed on
    2026-10-05 at 88459c4ef. `npm ci` was not repeated locally because this machine is
    short of disk.
  - **Scope.** The scope was `apps/web/package.json` and `package-lock.json`. This
    ticket changes neither, so it is narrowed to the ticket file. That also keeps it off
    Dependabot PR #1313, which bumps lucide-react and next-intl in those files and does
    not touch this chain.
