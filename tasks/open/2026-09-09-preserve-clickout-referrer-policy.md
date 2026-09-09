---
id: 2026-09-09-preserve-clickout-referrer-policy
title: Preserve no-referrer on external clickout responses
status: review
priority: P1
area: web
owner: codex-clickout-headers
claimed_at: 2026-09-09T13:14:19Z
created_at: 2026-09-09T13:11:39Z
completed_at:
branch: codex/stay22-modular-toggle
depends_on: []
scope:
  - apps/web/next.config.ts
  - apps/web/e2e/stay22-allez.spec.ts
---

# Preserve no-referrer on external clickout responses

## Why

The production Next BFF returned strict-origin-when-cross-origin on successful
external clickout redirects even though the handler returned no-referrer. The
global next.config header was written first, and Next 16.3.3 does not overwrite an
existing Referrer-Policy while sending a Route Handler response. Direct handler
unit tests did not include this final HTTP assembly.

## Definition of done

- [x] Successful BFF clickouts expose no-referrer on the actual production HTTP response.
- [x] Recoverable clickout errors expose same-origin and native retries retain their Origin.
- [x] Other pages/API routes keep the existing global policy and security headers.

## Steps

- [x] Exclude only BFF clickout paths from the static Referrer-Policy rule.
- [x] Verify effective headers with an isolated production Next server and synthetic upstream.
- [x] Run focused lint, TypeScript, BFF/browser regression and production build checks.

## How to verify

npm run build:web; PLAYWRIGHT_SERVE_BUILD=true with npm run test:e2e --workspace
@travel-scanner/web -- stay22-allez.spec.ts --workers=1. The wire test starts its own
loopback upstream/Next server and never follows the reserved .test redirect.

## Notes

The header conflict predates PR #382; this does not change CSRF, native form rel,
redirect allowlists or affiliate behavior. Do not set a blanket no-referrer policy
on error documents because same-origin is required by their native retry form.
Only the two scoped source files and this task record belong to this subtask.

Validated locally: focused ESLint and TypeScript passed, 48 BFF/error Vitest tests
passed, production Next build passed (267 routes), all 22 Playwright tests passed
across Desktop Chromium and Pixel 7. The isolated wire test covers five successful
clickout path families, HTML failure, and the default header elsewhere; browser
retries verify the effective same-origin header and Origin. Redirects are disabled
for the local synthetic 303 and no affiliate destination is contacted. The existing
CI web job already runs this spec after next build. No commit, PR, production
deployment or settings change is part of this subtask.
