---
id: 2026-09-12-trip-partner-cta
title: Day-level and post-AI partner call-to-actions in the trip planner
status: in-progress
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-12T13:27:22Z
created_at: 2026-09-12T13:27:20Z
completed_at:
branch: claude/trip-partner-offers
depends_on:
  - 2026-09-12-trip-partner-offer-availability
scope:
  - apps/web/lib/trip-types.ts
  - apps/web/lib/trip-partner-offers.ts
  - apps/web/lib/trip-partner-offers.test.ts
  - apps/web/components/trip-day-partner-offers.tsx
  - apps/web/components/trip-day-partner-offers.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/travel-services/catalog.tsx
  - apps/web/components/travel-services/catalog.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/zh-CN/trips.json
---

# Day-level and post-AI partner call-to-actions in the trip planner

## Why

The only partner buttons on the trip page were three taps deep in the tools overlay. The
moments a traveller actually needs a ride, a way online, or tickets — the arrival day, the
day being planned, the second after an AI plan lands — had nothing.

## Definition of done

- [x] Each planner day ends with a closed disclosure that mounts the destination-offer panel
      only when opened: arrival day → transport + connectivity (+ hotel until one is set),
      departure day → transport, other days → activities.
- [x] The block exists only when `trip.partner_offers.modules` has something for that day; the
      first paint still makes no `/affiliates/*` request.
- [x] Applying an AI plan shows a dismissible "what you can book next" card that mounts at once.
- [x] The tools-overlay catalog labels its destination offers `trip` when a trip is in context.
- [x] Five-locale copy under `trips.editor.partnerDay.*`.

## Steps

- [x] `lib/trip-partner-offers.ts` (kind + module helpers), `components/trip-day-partner-offers.tsx`.
- [x] Mounts in `trip-editor.tsx`; `catalog.tsx` placement; message keys; tests.

## How to verify

```
cd apps/web && npx vitest run lib/trip-partner-offers.test.ts components/trip-day-partner-offers.test.tsx components/trip-editor.test.tsx components/travel-services/catalog.test.tsx
npx playwright test e2e/planner-premium.spec.ts
```

## Notes

A plain `<details>` does not lazy-mount in React (`DayHealthStrip` fetches while collapsed),
so the block tracks `open` via `onToggle` and renders the panel only then. `2026-09-09-site-
experience-settings` (blocked) lists `trip-editor.tsx` and `apps/web/messages`; rebase when it
unblocks. Anonymous clickouts record `placement=trip` but no `trip_id`.
