---
id: 2026-09-30-correct-the-zh-cn-arrival-card
title: Correct the zh-CN arrival-card guide's outdated 47-city mainland tourism claim
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-30T01:29:06Z
completed_at:
branch:
depends_on:
  - 2026-09-21-91-ci
scope:
  - apps/api/app/guides/content/taiwan-entry-2026-arrival-card.json
---

# Correct the zh-CN arrival-card guide's outdated 47-city mainland tourism claim

## Why

`taiwan-entry-2026-arrival-card` zh-CN block 2 still says mainland individual
tourism is limited to residents of 47 designated cities with 15-day stays. The
zh-TW source says the current eligibility depends on residence, status and the
open category, and explicitly warns not to use the old "47 cities" description.
Found while fixing the content checker in `2026-09-21-91-ci`, which only added
the other nationalities' visa-free days to this block.

## Definition of done

- [ ] zh-CN block 2 and the block 3 table match the zh-TW wording on mainland
      and Hong Kong/Macau entry, checked against the NIA page on the day of the edit.
- [ ] Independent review; lint 0 errors; after deploy, import and publish zh-CN only.

## How to verify

Read zh-TW block 2 next to zh-CN blocks 2-3; no "47" city claim remains.
