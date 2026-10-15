---
id: 2026-10-15-include-cached-retakes-in-dub-dry
title: Include cached retakes in dub dry-run and monthly budget preflight
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-15T12:07:50Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Include cached retakes in dub dry-run and monthly budget preflight

## Why

dub --redo or --force can synthesize current cached lines while dryRun and the pre-call monthly needed estimate report zero. Both preflight paths use only cache validity; actual dubLocale also considers redo and force. This understates a requested retake budget even though the server still reserves characters per request.

## Definition of done

- [ ] Dry-run and monthly preflight count exactly the same pending requests and billable characters as actual synthesis for --redo, --force, stale clips and partial-scene retakes.
- [ ] A fully current cache with one selected --redo line reports the selected line cost, and a monthly allowance below that cost fails before synthesis.
- [ ] Unchanged cache reuse remains zero, and focused regression tests cover multi-line partial retakes.

## Steps

- [ ] Extract or share the pending-request and partial-line planning logic currently in dubLocale.
- [ ] Exercise the shared plan from dryRun and monthly budget preflight; add regression coverage.

## How to verify

Run node --test tools/video/dubs/dubs.test.mjs, npm run test:tools and npm run check:tasks. Use mocked service calls to verify the budget failure sends no synthesis request.

## Notes

Observed during H09 on 2026-10-15. All 100 EN clips were current; a two-line redo (h0pu8prr, h1e4dxa5) manually planned via dubRequests/lineBody/billableForRequest as 2 requests / 136 billable characters, but the real CLI dry-run printed 0 requests / 0 characters. Read-only independent audit confirmed the mismatch at tools/video/dubs/cli.mjs:215-230,419-434,493. apps/api/app/video_speech/admin_api.py still reserves each request. Do not describe this as bypassing all server budget enforcement. Existing active task 2026-10-14-enforce-usd-25-all-in-cap overlaps cli.mjs; this ticket remains unclaimed and no shared tool implementation was changed by the production task.
