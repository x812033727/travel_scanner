---
id: 2026-09-11-hotel-operation-rakuten-clickout
title: Hotel operating date guards Rakuten Japan and resilient clickouts
status: done
priority: P1
area: api
owner: codex-hotel-guard
claimed_at: 2026-09-11T02:50:20Z
created_at: 2026-09-11T02:50:19Z
completed_at: 2026-09-11T15:54:24Z
branch: codex/hotel-operation-rakuten-clickout
depends_on: []
scope:
  - apps/api/app/travel_services
  - apps/api/tests/test_hotel_operating_rules.py
  - apps/api/tests/test_rakuten_japan.py
  - apps/api/tests/test_stay22_script.py
  - apps/api/tests/test_hotel_operating_integration.py
  - apps/web/components/travel-services/booking-panel.tsx
  - apps/web/app/[locale]/hotels/[productId]/page.tsx
  - apps/web/components/travel-services/hotel-booking-page.tsx
  - apps/web/components/travel-services/hotel-booking-page.test.tsx
  - apps/web/components/travel-services/booking-panel.test.tsx
  - apps/web/components/travel-services/stay22-public-hotels.tsx
  - apps/web/components/travel-services/stay22-public-hotels.test.tsx
  - apps/web/components/travel-services/catalog.tsx
  - apps/web/components/travel-services/hotel-operation-fields.tsx
  - apps/web/components/travel-services/hotel-operation-fields.test.tsx
  - apps/web/components/travel-services/admin.tsx
  - apps/web/lib/hotel-operation-rules.ts
  - apps/web/lib/hotel-operation-rules.test.ts
  - apps/web/lib/stay22-allez-messages
  - apps/web/lib/hotel-clickout-error.ts
  - apps/web/lib/hotel-clickout-error.test.ts
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/travel/[...path]/hotel-clickout.test.ts
  - apps/web/messages/en/travelServices.json
  - apps/web/messages/ja/travelServices.json
  - apps/web/messages/ko/travelServices.json
  - apps/web/messages/zh-CN/travelServices.json
  - apps/web/messages/zh-TW/travelServices.json
  - apps/web/e2e/hotel-operating.spec.ts
  - apps/web/e2e/stay22-allez.spec.ts
  - apps/web/e2e/stay22-script.spec.ts
  - docs/hotel-operation-rakuten-clickout.md
---

# Hotel operating date guards Rakuten Japan and resilient clickouts

## Why

Four hotel reviews are held because operating notices cannot yet constrain stay
dates. Rakuten Japan's exact property pages cannot use the Global-only ordinary
link validator. Native booking POSTs open correctly in Chrome but the same
production button did not produce an observable new tab in the in-app browser.

## Definition of done

- [x] Source-backed unavailable nights / final checkout protect recommendations, selection, quotes and all booking boundaries.
- [x] Admin edits retain a single versioned JSON draft; saving is not approval.
- [x] Precise Rakuten Japan links preserve their own IDs and remain direct-only.
- [x] A booking attempt exposes a deliberate same-tab POST fallback, never an automatic retry or guessed external URL.
- [ ] Focused and full validations complete; PR opened without merge, deployment or production approvals.

## Steps

- [x] Start from freshly fetched main d0ec33ee in an isolated worktree and release verified merged task claims.
- [x] Implement backend guards and Japanese-market identity checks in separate scopes.
- [x] Add five-language admin/public controls, native fallback and typed error recovery.
- [x] Verify browser privacy boundaries, run suites and document any unavailable local integration services.
- [x] Push tested implementation and create PR, leaving merge/deploy for explicit authorization.

## How to verify

See docs/hotel-operation-rakuten-clickout.md. Run API pytest/ruff/mypy,
Web lint/typecheck/i18n/Vitest (one worker), production build and
stay22-allez.spec.ts plus stay22-script.spec.ts on desktop/mobile. CI supplies
PostgreSQL, containers and full-stack smoke. No real booking or provider quote
calls in synthetic tests; production Chrome diagnosis is a read-only clickout.

## Notes

2026-09-11: Production Chrome clicked the amba Taipei Zhongshan Trip.com form and
opened a new tab at /hotels/taipei-hotel-detail-1917532/amba-taipei-zhongshan/.
This disproves a universal backend clickout failure; in-app new-tab support is a
distinct observation. Preserve original POST and no-referrer redirect contracts.
Trip.com subsequently required sign-in, retaining the exact hotel as backurl;
external hotel content/booking completion was not verified in this Chrome tab.

Date intervals represent occupied nights [start,end), not hourly opening times.
Past-cutoff hotels disappear in destination local time. Existing trip records
are not removed; modifying a trip date does not reconfirm hotel availability.
Restricted hotels cannot export original booking anchors into Stay22's public
script document. They must navigate to the first-party /hotels/<id> booking page
before entering dates, including when Discovery is disabled. Rakuten Japan also
stays outside script conversion.

Local Docker command is unavailable. Never report skipped PostgreSQL/container
checks as passed; obtain those results from PR CI. No production data modified.

PR: https://github.com/x812033727/travel_scanner/pull/389 (draft until final-head
CI passes). Local browser tests: 60 passed, desktop and mobile. Full API: 2,955
passed / 161 skipped; final focused boundary tests: 273 passed / 2 skipped.
First full Web run had three test timeouts and one worker-start timeout; all
three affected files subsequently passed separately (48 tests). Full Web CI,
PostgreSQL integration, containers and full-stack smoke remain release gates.

## Closed after merge (site owner's instruction, not the holder)

PR #389 merged on 2026-09-11 as squash `5e3168e`, whose tree is identical to the PR head
`8303d93`, so everything on the branch reached main; the branch has since been deleted.
Every check on that head passed: `api`, `web`, `containers`, `full-stack-smoke`,
`discovery-browser` and `planner-browser`. The task stayed in `review` and kept holding its
scope, which blocked later claims, so claude-opus-5 moved it to done on 2026-09-11.

The unticked item was full validation while the PR was still unmerged. The PostgreSQL,
container and full-stack gates its notes left to CI are the `api`, `containers` and
`full-stack-smoke` checks above.

If the holder still has follow-up work that never reached the branch, file a new task rather
than reopening this one.
