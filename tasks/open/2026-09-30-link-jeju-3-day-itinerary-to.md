---
id: 2026-09-30-link-jeju-3-day-itinerary-to
title: Link jeju-3-day-itinerary to the Hallasan booking and Marado guides once they exist
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-30T02:45:05Z
completed_at:
branch:
depends_on:
  - 2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924
scope:
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
---

# Link jeju-3-day-itinerary to the Hallasan booking and Marado guides once they exist


## Why

Split out of `2026-09-20-jeju-itinerary-gwaneumsa-reopens-0924`, which fixed the
Gwaneumsa reopening, the 漢拏山 spelling and the "upper sections only" booking rule
but could not add links to two batch 8 guides that do not exist yet:
`hallasan-hiking-reservation-guide` and `marado-gapado-ferry-day-trip`.

## Definition of done

- [ ] Both guides are published (check the live page title, not only HTTP 200).
- [ ] `jeju-3-day-itinerary` blocks[19] becomes a `rich_paragraph` in place with an
      `article` inline to `hallasan-hiking-reservation-guide`; its text otherwise unchanged.
- [ ] The pack's `related` lists both slugs.
- [ ] Lint 0 errors; after deploy, dry-run shows one `update`, then `--publish`.

## How to verify

`uv run python -m app.guides.pack_cli lint --slug jeju-3-day-itinerary` and
`guides-links-check --locale zh-TW` after publishing.
