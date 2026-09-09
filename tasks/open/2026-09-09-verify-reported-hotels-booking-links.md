---
id: 2026-09-09-verify-reported-hotels-booking-links
title: Verify the two reported hotels exact Booking links
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-09T13:04:46Z
completed_at:
branch:
depends_on: []
scope:
  - docs/reported-hotels-booking-review.md
---

# Verify the two reported hotels exact Booking links

## Why

Booking through Stay22 is enabled by an explicitly authorized, audited settings
change (config version 7, AID mokaair, Booking only). The two reported hotel cards
still have only approved official-site options; their missing OTA links are a
separate catalog-review task, not fixed by enabling Stay22.

## Definition of done

- [ ] Independently verify both exact Booking properties against official names and addresses.
- [ ] If authorized and all existing gates pass, use normal admin catalog review to publish the exact Booking options; record any unresolved checks instead of guessing.
- [ ] Distinguish link readiness from real Stay22 landing/Hub attribution; no test orders.

## Steps

- [x] Record researched candidates and primary-source limitations.
- [ ] Complete review and document outcomes in the scoped report before any publication.

## How to verify

Read the official hotel and exact Booking property pages using normal browser
access. Compare hotel identity/address, retain evidence and existing review gates.
After an authorized publication, inspect the public card's Booking option/channel.
Do not bulk approve, bypass browser/robot barriers or fabricate property IDs.

## Notes

- Ginza Premier product `b510c418-5e7e-4cd0-88c1-cf397caad925`:
  candidate https://www.booking.com/hotel/jp/mitsui-garden-ginza-premier-chuo.en-gb.html .
  Booking's first-party search index and https://www.gardenhotels.co.jp/ginza-premier/eng/access/
  agree on 8-13-1 Ginza, Chuo-ku. Direct Booking access required JS/robot verification;
  the read-only researcher stopped without bypass, so full review remains incomplete.
- Otemachi product `ce410c0c-dea0-432b-94d3-4d842f979dac`:
  candidate https://www.booking.com/hotel/jp/mitsui-garden-otemachi.en-gb.html .
  Booking's first-party index gives Chiyoda-ku Uchikanda 2-1-2. The independent
  https://www.gardenhotels.co.jp/otemachi/eng/access/ address fetch timed out.
  Direct Booking also required JS/robot verification. No completed review claimed.
- No catalog records were added, changed or approved during this investigation.
