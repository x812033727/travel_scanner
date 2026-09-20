---
id: 2026-09-20-tutorial-hub-query-ads
title: Preserve tutorial hub filters when ads are enabled
status: in-progress
priority: P1
area: web
owner: gpt-6
claimed_at: 2026-09-20T05:59:14Z
created_at: 2026-09-20T05:59:13Z
completed_at:
branch: codex/tutorial-hub-query-ads
depends_on: []
scope:
  - apps/web/app/(ads-public)/[locale]/layout.tsx
  - apps/web/app/(ads-public)/[locale]/layout.test.tsx
---

# Preserve tutorial hub filters when ads are enabled

## Why

With AdSense enabled, the public article root redirects every URL with a query string to
the clean path so vendor code cannot read private search terms. The Codex and Claude Code
tutorial directories intentionally store their search and filters in the URL. A reload of
`/zh-TW/life/codex-learning-hub?q=AGENTS.md&unit=D` therefore loses both filters in
production, even though the client-side controls and local tests pass.

## Definition of done

- [x] Codex and Claude Code directory query URLs survive a direct request and reload.
- [x] The two interactive directories never load the ad configuration into their document.
- [x] Other advertised article URLs still remove query strings before rendering.

## Steps

- [x] Exempt only the two URL-filtered tutorial directory routes from the advertised layout.
- [x] Add regression coverage for both hubs and retain the generic article privacy test.
- [ ] Verify the exact production URL after merge and deployment.

## How to verify

Run the ads-public layout test, affected web lint/type checks, and the Codex public browser
acceptance. Confirm the production query URL returns 200 without redirect and retains
`q=AGENTS.md&unit=D` after reload.

## Notes

The production failure was found after the Codex packs were published: `curl -I` returned
307 with `location: /zh-TW/life/codex-learning-hub`. Keeping ads on the initial clean hub
would not protect later client-side URL changes, so the complete interactive document must
use the ordinary ad-free locale layout.

Local verification: the focused ads-public layout suite passed 6/6; web lint, web typecheck,
and the task registry check passed. Production verification remains gated on PR CI, exact
merge, and deployment.
