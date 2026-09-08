---
id: 2026-09-08-travelpayouts-full-partner-links
title: Travelpayouts full partner links for production verification
status: done
priority: P1
area: api
owner: codex
claimed_at: 2026-09-08T06:37:26Z
created_at: 2026-09-08T06:37:26Z
completed_at: 2026-09-08T06:41:00Z
branch: codex/travelpayouts-full-partner-links
depends_on: []
scope:
  - apps/api/app/affiliates/service.py
  - apps/api/app/travel_services/registry.py
  - apps/api/tests/test_affiliates.py
  - apps/api/tests/test_travel_services.py
  - docs/travel-services.md
---

# Travelpayouts full partner links for production verification

## Why

PR #358 production verification found that Partner Links `shorten=true` returns
branded `tpx.gr` hosts absent from existing approved redirect domains. Request full
links instead, invalidate old short-link caches, and respect the official API's
Kiwi.com exclusion. The shared production checkout remains untouched.

## Definition of done

- [x] Dynamic Partner Links use full URLs and cannot reuse old shortener caches.
- [x] Kiwi.com remains available only through reviewed static affiliate links.
- [x] Focused API tests (74), ruff and mypy pass; complete CI gates deployment.

## Steps

- [x] Reproduce with the configured production account without disclosing credentials.
- [x] Confirm `shorten=false` and Kiwi.com exclusion in official documentation.
- [x] Preserve rejection of unverified redirects and HTTP 403 landing pages.

## How to verify

`uv run pytest tests/test_affiliates.py tests/test_travel_services.py -q`
and `uv run ruff check .`, `uv run mypy app`. Production: generate full links through
the existing shared limiter, confirm approved first-hop domains, and keep failed
landing checks unpublished. Exact main CI is required before activation.

## Notes

2026-09-08: Project 570089 was configured. Existing catalog brands Klook/KKday were
approved; Booking/Trip.com pending. There were no product-level affiliate offers.
Full URLs generated successfully for Aviasales/Klook/KKday. Aviasales reached HTTP
200. Klook reached its exact path with HTTP 403; KKday traversed `invl.me` and reached
HTTP 403. No candidate was published based only on conversion success. The desktop
helper stopped because it could not reliably identify the current browser URL;
live project approval reconciliation remains outstanding.

Official contract: https://support.travelpayouts.com/hc/en-us/articles/25289759198226-API-for-Travelpayouts-partner-links
