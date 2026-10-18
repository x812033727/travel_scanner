---
id: 2026-10-18-upgrade-sharp-and-source-map-js
title: Upgrade sharp and source-map-js for the 2026-10-18 npm audit advisories
status: in-progress
priority: P2
area: ops
owner: claude-opus-5.5-npm-audit
claimed_at: 2026-10-18T08:28:18Z
created_at: 2026-10-18T08:28:08Z
completed_at:
branch: claude/npm-audit-2026-10-18
depends_on: []
scope:
  - package-lock.json
  - tasks/open/2026-10-18-upgrade-sharp-and-source-map-js.md
---

# Upgrade sharp and source-map-js for the 2026-10-18 npm audit advisories

## Why

From 2026-10-16 the daily `npm audit` workflow (`.github/workflows/npm-audit.yml`) has been red.
Its first step, `npm audit --omit=dev --audit-level=high`, takes no exemption, and on
2026-10-18 it reported two high advisories in production dependencies:

- `sharp` <0.35.5, GHSA-wq5f-xc86-pv6w (librsvg, CVE-2026-96889). Reached through
  `next` (`sharp ^0.35.4`, optional), which uses it for image optimisation, so it ships
  in the production image.
- `source-map-js` 1.0.0–1.2.1, GHSA-68fv-2mgg-jv7q (event-loop DoS through indexed
  source-map section offsets). Reached through `postcss` (production) and through
  `@tailwindcss/node`, `css-tree` (jsdom) and vite's postcss (dev).

Both have patched releases inside the ranges their dependents already ask for.

## Definition of done

- [x] `npm audit --omit=dev --audit-level=high` reports 0 vulnerabilities.
- [x] `node tools/npm-audit-gate.mjs` on the full `npm audit --json` says ok; only the
      already exempted braces advisory (review by 2026-11-04) remains.
- [ ] lint, typecheck and the web tests pass with the new lockfile.

## Steps

- [x] `npm update sharp source-map-js --package-lock-only`.
- [x] Keep only the version changes: npm 11.6.2 locally also rewrote `peer`/`libc` metadata
      on about seventy unrelated entries, so the lockfile was rebuilt from main's copy with
      just the 28 changed entries (sharp 0.35.5, its `@img/sharp-*` 0.35.5 and
      `@img/sharp-libvips-*` 1.3.4 binaries, source-map-js 1.2.2).
- [ ] Run lint, typecheck, web tests and load sharp on this machine.

## How to verify

```bash
npm ci
npm audit --omit=dev --audit-level=high
npm audit --json > /tmp/a.json; node tools/npm-audit-gate.mjs < /tmp/a.json
npm run lint:web && npm run typecheck:web && npm run test:web
```

## Notes

- The PR-time audit step in `ci.yml` (`web-checks`) is `continue-on-error: true`, so these
  advisories never failed a pull request by themselves. On 2026-10-18 #1565's red
  `web-checks` came from `npm run test:tools` (the duration review test), not from audit.
- The remaining full-tree finding, braces GHSA-vfj7-8cjw-p6xm through
  eslint-config-next, has no patched release and is already exempted in
  `tools/npm-audit-allow.json` until 2026-11-04; nothing new needs an owner decision.
