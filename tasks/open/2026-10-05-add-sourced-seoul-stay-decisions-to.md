---
id: 2026-10-05-add-sourced-seoul-stay-decisions-to
title: Add sourced Seoul stay decisions to the city page
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-10-05T02:05:34Z
completed_at:
branch: claude/project-thread-8bpz38
depends_on: []
scope:
  - apps/web/lib/destination-decisions.ts
  - apps/web/lib/destination-decisions.json
  - apps/web/components/destination-guide.test.tsx
  - apps/web/app/[locale]/destinations/[destinationId]/page.test.tsx
  - docs/adsense-seoul-sources.md
---

# Add sourced Seoul stay decisions to the city page

## Why

The 2026-10-04 AdSense sample in docs/adsense-review-readiness.md found the Seoul city page
still lists Myeongdong, Hongdae, Dongdaemun and Gangnam by name only, with no transport
trade-offs or official sources. Tokyo got sourced stay decision cards in #1206; Seoul should
meet the same standard so the city-guide example is not a single page.

## Definition of done

- [x] Seoul renders four sourced stay decision cards (Myeongdong, Hongdae, Dongdaemun, Gangnam) in all five locales, before partner options.
- [x] Tokyo's cards and every other city's catalog area list are unchanged.
- [x] Each card's claims trace to an official page recorded in docs/adsense-seoul-sources.md.
- [ ] Deployed and checked on the live Seoul page in each locale (after merge; not part of this PR).

## Steps

- [x] Read official Visit Seoul area pages and the Incheon Airport railroad route.
- [x] Make the decision data per destination so a city is added by data alone, and add Seoul in five locales.
- [x] Cover every decision destination in the component test and Seoul in the route test.

## How to verify

From apps/web: `npx vitest run components/destination-guide.test.tsx 'app/[locale]/destinations/[destinationId]/page.test.tsx'`.
From the root: `npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`.
After deploy, open /zh-TW/destinations/seoul (and the other four locales) and confirm four cards with official links above the partner options.

## Notes

- `destination-decisions.json` is now keyed by destination (`destinations.<id>` with `checkedOn`, `areaIds`, `sources`, `locales`); Tokyo's copy and sources moved over unchanged. The component needed no change.
- arex.or.kr answered with a firewall page from the cloud environment, so AREX stops were checked against the Incheon Airport route page instead.
- Fares, headways and journey minutes are deliberately left out of the cards, as for Tokyo.
- The readiness doc's Seoul row should be updated only after the page is live (its scope belongs to the AdSense coordination task).

## 2026-10-07 看板總整理（由站主授權，非原持有者）

釋出過期認領（認領超過 24 小時，主要工作已落地）。程式已隨 #1348 合併；剩部署後五個語系的線上檢查。
