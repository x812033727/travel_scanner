---
id: 2026-09-06-fx-currency-api
title: 匯率改由 Currency-api 供應，Frankfurter 退為備援；行程報價與記帳顯示換算
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T06:28:55Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/crawlers/fx.py
  - apps/api/app/fx
  - apps/api/app/main.py
  - apps/api/app/config.py
  - apps/api/app/trips/pricing.py
  - apps/api/app/trips/router.py
  - apps/api/tests/test_back_to_back_fares.py
  - apps/api/tests/test_trip_pricing.py
  - apps/api/tests/test_fx_rates.py
  - apps/web/lib/currency.ts
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - .env.example
---

# 匯率改由 Currency-api 供應，Frankfurter 退為備援；行程報價與記帳顯示換算

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
